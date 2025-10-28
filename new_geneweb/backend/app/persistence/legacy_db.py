"""
Legacy GeneWeb database connector.

Provides access to genealogical data stored in .gwb files via GEDCOM export/import.
This module encapsulates all legacy GeneWeb interactions, allowing DBConnector
to remain clean and focused on PostgreSQL metadata management.

Implementation of DatabaseProvider interface for legacy .gwb file system.

Phase 1 Strategy:
- .gwb files are the source of truth for genealogical data
- GEDCOM is used as an intermediate format (gwb2ged → parse → in-memory cache)
- All write operations go through GEDCOM → ged2gwb → .gwb
- In-memory cache with TTL to minimize expensive GEDCOM conversions

Future Phase 2/3:
- PostgreSQL becomes primary store
- This module becomes a migration/sync utility
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from gedcom.parser import Parser as GedcomParser  # type: ignore[import-untyped]

from app.persistence.database_provider import CacheStats, DatabaseProvider

log = logging.getLogger(__name__)


class LegacyDB(DatabaseProvider):
    """
    Legacy GeneWeb database provider using .gwb files.

    Implements DatabaseProvider interface for backward compatibility.
    Manages access to .gwb files via GEDCOM conversion, caching, and CRUD operations.
    Designed to be easily replaceable when migrating to PostgreSQL-only architecture.
    """

    def __init__(
        self,
        gwb_path: Path | str | None = None,
        gwb2ged_bin: Path | str | None = None,
        ged2gwb_bin: Path | str | None = None,
        gwc_bin: Path | str | None = None,
        cache_ttl_seconds: int = 300,  # 5 minutes
    ) -> None:
        """
        Initialize legacy GeneWeb connector.

        Args:
            gwb_path: Path to .gwb database file
            gwb2ged_bin: Path to gwb2ged executable
            ged2gwb_bin: Path to ged2gwb executable
            gwc_bin: Path to gwc (GeneWeb Compiler) executable
            cache_ttl_seconds: Cache lifetime in seconds
        """
        self.gwb_path = Path(gwb_path) if gwb_path else None
        self.gwb2ged_bin = Path(gwb2ged_bin) if gwb2ged_bin else None
        self.ged2gwb_bin = Path(ged2gwb_bin) if ged2gwb_bin else None
        self.gwc_bin = Path(gwc_bin) if gwc_bin else None
        self.cache_ttl_seconds = cache_ttl_seconds

        # Validations
        if self.gwb_path:
            if not self.gwb_path.exists():
                raise FileNotFoundError(f"GeneWeb database not found: {gwb_path}")

            if self.gwb2ged_bin and not self.gwb2ged_bin.exists():
                raise FileNotFoundError(f"gwb2ged binary not found: {gwb2ged_bin}")

            if self.ged2gwb_bin and not self.ged2gwb_bin.exists():
                raise FileNotFoundError(f"ged2gwb binary not found: {ged2gwb_bin}")

            if self.gwc_bin and not self.gwc_bin.exists():
                raise FileNotFoundError(f"gwc binary not found: {gwc_bin}")

        # In-memory cache
        self._cache: dict[str, Any] = {}
        self._cache_lock = asyncio.Lock()
        self._stats = CacheStats()
        self._last_cache_refresh: datetime | None = None
        self._background_refresh_task: asyncio.Task[None] | None = None

        log.info(f"LegacyDB initialized: gwb={bool(gwb_path)}")

    # =========================================================================
    # Database Management
    # =========================================================================

    async def is_connected(self) -> bool:
        """
        Test if LegacyDB connection is working.

        Checks:
        - .gwb file exists
        - gwb2ged binary exists and is executable
        - ged2gwb binary exists and is executable

        Returns:
            bool: True if all resources are accessible, False otherwise
        """
        try:
            # Check .gwb file
            if not self.gwb_path or not self.gwb_path.exists():
                log.warning(f"GeneWeb database not found: {self.gwb_path}")
                return False

            # Check gwb2ged binary
            if self.gwb2ged_bin:
                if not self.gwb2ged_bin.exists():
                    log.warning(f"gwb2ged binary not found: {self.gwb2ged_bin}")
                    return False
                if not self.gwb2ged_bin.is_file():
                    log.warning(f"gwb2ged is not a file: {self.gwb2ged_bin}")
                    return False

            # Check ged2gwb binary
            if self.ged2gwb_bin:
                if not self.ged2gwb_bin.exists():
                    log.warning(f"ged2gwb binary not found: {self.ged2gwb_bin}")
                    return False
                if not self.ged2gwb_bin.is_file():
                    log.warning(f"ged2gwb is not a file: {self.ged2gwb_bin}")
                    return False

            return True

        except Exception as e:
            log.error(f"Error checking LegacyDB connection: {e}")
            return False

    def list_geneweb_databases(self) -> list[str]:
        """
        List all available GeneWeb databases in the base directory.

        Scans the GeneWeb distribution bases folder for .gwb files.

        Returns:
            List of database names (without .gwb extension)

        Example:
            dbs = connector.list_geneweb_databases()
            print(f"Available databases: {dbs}")  # ["royal", "smith"]
        """
        if not self.gwb_path:
            return []

        base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent
        if not base_dir.exists():
            log.warning(f"Base directory not found: {base_dir}")
            return []

        databases = []
        for item in base_dir.iterdir():
            if item.is_dir() and item.suffix == ".gwb":
                # GeneWeb database: directory ending in .gwb containing a 'base' file
                base_file = item / "base"
                if base_file.exists() and base_file.is_file():
                    databases.append(item.stem)  # stem removes .gwb extension

        return sorted(databases)

    def get_database_info(self, db_name: str) -> dict[str, Any] | None:
        """
        Get detailed information about a specific GeneWeb database (instance method).

        Args:
            db_name: Name of the database (without .gwb extension)

        Returns:
            Dictionary with database information or None if not found

        Note:
            This instance method uses self.gwb_path as base directory
            if it's a dir, otherwise its parent.
        """
        if not self.gwb_path:
            return None
        base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent
        return self.get_database_info_static(base_dir, db_name)

    @staticmethod
    def get_database_info_static(
        base_dir: Path | str, db_name: str
    ) -> dict[str, Any] | None:
        """
        Get detailed information about a specific GeneWeb database.

        Args:
            base_dir: Base directory containing GeneWeb databases
            db_name: Name of the database (without .gwb extension)

        Returns:
            Dictionary with database information or None if not found

        Example:
            info = LegacyDB.get_database_info("/data/bases", "royal")
            if info:
                print(f"Database: {info['name']}, Persons: {info['nb_persons']}")
        """
        base_dir = Path(base_dir)
        db_path = base_dir / f"{db_name}.gwb"

        if not db_path.exists():
            return None

        # Read base file for metadata
        base_file = db_path / "base"
        if not base_file.exists():
            # Try alternative structure (old format with base.gwb)
            gwb_files = list(db_path.glob("*.gwb"))
            if not gwb_files:
                return None
            base_file = gwb_files[0]

        # Parse base file for basic info (simplified)
        try:
            with base_file.open("rb") as f:
                # Read header (first 100 bytes typically contain metadata)
                _ = f.read(100)  # Placeholder for future header parsing

                # Extract basic info
                info: dict[str, Any] = {
                    "name": db_name,
                    "path": str(db_path),
                    "size": base_file.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        base_file.stat().st_mtime
                    ).isoformat(),
                    "nb_persons": 0,  # Would require full parse
                }

                return info
        except Exception as e:
            log.error(f"Error reading database info for {db_name}: {e}")
            return None

    def list_databases_with_info(
        self, base_dir: Path | str | None = None
    ) -> list[dict[str, Any]]:
        """
        List all databases with their detailed information.

        Args:
            base_dir: Optional base directory (uses gwb_path parent if not provided)

        Returns:
            List of database info dictionaries

        Example:
            dbs = connector.list_databases_with_info()
            for db in dbs:
                print(f"{db['name']}: {db['nb_persons']} persons")
        """
        if base_dir is None:
            if not self.gwb_path:
                return []
            base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent

        base_dir = Path(base_dir)
        db_names = self.list_geneweb_databases()

        databases = []
        for name in db_names:
            info = self.get_database_info_static(base_dir, name)
            if info:
                databases.append(info)

        return databases

    def _get_geneweb_uid_gid(self, base_dir: Path) -> tuple[int | None, int | None]:
        """
        Get UID/GID to use for database files.

        Tries to find UID/GID from:
        1. An existing non-root database
        2. The gwc binary

        Args:
            base_dir: Base directory containing databases

        Returns:
            Tuple of (uid, gid) or (None, None) if not found
        """
        geneweb_uid = None
        geneweb_gid = None

        # Try to find an existing database to copy ownership from
        log.info(f"Searching for existing databases in {base_dir}")
        for item in base_dir.iterdir():
            if item.is_dir() and item.name.endswith(".gwb"):
                try:
                    stat_info = item.stat()
                    # Skip if owned by root (0)
                    if stat_info.st_uid != 0:
                        geneweb_uid = stat_info.st_uid
                        geneweb_gid = stat_info.st_gid
                        log.info(
                            f"Found existing database {item.name} with "
                            f"UID:GID {geneweb_uid}:{geneweb_gid}"
                        )
                        break
                except Exception as e:
                    log.debug(f"Could not stat {item}: {e}")
                    continue

        # If no existing database, try gwc binary
        if geneweb_uid is None and self.gwc_bin:
            try:
                stat_info = Path(self.gwc_bin).stat()
                geneweb_uid = stat_info.st_uid
                geneweb_gid = stat_info.st_gid
                log.info(f"Using gwc binary ownership: {geneweb_uid}:{geneweb_gid}")
            except Exception as e:
                log.warning(f"Could not stat gwc binary: {e}")

        return geneweb_uid, geneweb_gid

    def _chown_database_files(
        self, db_path: Path, db_name: str, base_dir: Path, uid: int, gid: int
    ) -> None:
        """
        Change ownership of database files to specified UID/GID.

        Args:
            db_path: Path to .gwb directory
            db_name: Database name
            base_dir: Base directory containing databases
            uid: Target UID
            gid: Target GID
        """
        if sys.platform != "win32":
            # Change ownership of .gwb directory and all its contents
            for root, dirs, files in os.walk(db_path):
                os.chown(root, uid, gid)  # type: ignore[attr-defined,unused-ignore]
                for d in dirs:
                    os.chown(os.path.join(root, d), uid, gid)  # type: ignore[attr-defined,unused-ignore]
                for f in files:
                    os.chown(os.path.join(root, f), uid, gid)  # type: ignore[attr-defined,unused-ignore]

            # Change ownership of .gwf and .lck files
            gwf_file = base_dir / f"{db_name}.gwf"
            lck_file = base_dir / f"{db_name}.lck"
            if gwf_file.exists():
                os.chown(gwf_file, uid, gid)  # type: ignore[attr-defined,unused-ignore]
            if lck_file.exists():
                os.chown(lck_file, uid, gid)  # type: ignore[attr-defined,unused-ignore]

        log.info(f"✅ Changed ownership to {uid}:{gid}")

    def _create_additional_database_files(self, db_path: Path) -> None:
        """
        Create additional files/directories required by legacy GeneWeb.

        Args:
            db_path: Path to .gwb directory
        """
        # Create caches directory (empty but required)
        caches_dir = db_path / "caches"
        caches_dir.mkdir(exist_ok=True)
        log.info(f"✅ Created caches directory: {caches_dir}")

        # Create nb_persons file (21 bytes, matching legacy format)
        nb_persons_file = db_path / "nb_persons"
        with nb_persons_file.open("wb") as f:
            f.write(b"\x84\x95\xa6\xbe\x00\x00\x00\x01" + b"\x00" * 12 + b"\x40")
        log.info(f"✅ Created nb_persons file: {nb_persons_file}")

    def _write_comm_log(self, base_dir: Path, stdout: str, stderr: str | None) -> None:
        """
        Write gwc output to comm.log file (legacy behavior).

        Args:
            base_dir: Base directory containing databases
            stdout: Standard output from gwc
            stderr: Standard error from gwc (if any)
        """
        comm_log = base_dir / "comm.log"
        with comm_log.open("a", encoding="utf-8") as f:
            f.write(stdout)
            if stderr:
                f.write(stderr)

    async def create_geneweb_database(
        self, db_name: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Create a new GeneWeb database using gwc (GeneWeb Compiler).

        Mimics the legacy command: ../gw/gwc -f -o base_name > comm.log

        Args:
            db_name: Name of the database (without .gwb extension)
            metadata: Optional metadata (ignored for legacy, no place to store)

        Returns:
            Dictionary with database info

        Raises:
            ValueError: If database already exists
            RuntimeError: If gwc fails

        Example:
            db_info = await legacy_db.create_geneweb_database("new_family")
            # Creates: /bases/new_family.gwb
        """
        if not self.gwb_path:
            raise RuntimeError("No gwb_path configured, cannot create database")

        if not self.gwc_bin:
            raise RuntimeError("No gwc_bin configured, cannot create database")

        # gwb_path is the base directory containing all databases
        base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent
        new_db_path = base_dir / f"{db_name}.gwb"

        # Check if already exists
        if new_db_path.exists():
            raise ValueError(f"Database '{db_name}' already exists at {new_db_path}")

        log.info(f"Creating new GeneWeb database: {db_name}")

        try:
            # Run gwc command: ../gw/gwc -f -o base_name
            # -f: force creation
            # -o: output database name
            result = subprocess.run(  # noqa: S603
                [str(self.gwc_bin), "-f", "-o", db_name],
                cwd=base_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Write output to comm.log (like legacy does)
            self._write_comm_log(base_dir, result.stdout, result.stderr)

            if result.returncode != 0:
                log.error(f"gwc failed: {result.stderr}")
                raise RuntimeError(f"Failed to create database: {result.stderr}")

            log.info(f"✅ Created database: {new_db_path}")

            # Create additional files/directories that legacy creates
            self._create_additional_database_files(new_db_path)

            # Change ownership to match legacy databases
            # Required for the legacy front-end to manage (delete, modify)
            try:
                geneweb_uid, geneweb_gid = self._get_geneweb_uid_gid(base_dir)

                if geneweb_uid is None or geneweb_gid is None:
                    log.warning("⚠️ Could not determine geneweb UID/GID, skipping chown")
                else:
                    self._chown_database_files(
                        new_db_path, db_name, base_dir, geneweb_uid, geneweb_gid
                    )
            except Exception as e:
                log.warning(f"⚠️ Failed to change ownership: {e}")

            # Return database info
            return {
                "name": db_name,
                "path": str(new_db_path),
                "nb_persons": 0,
                "nb_families": 0,
                "created": datetime.now().isoformat(),
            }

        except subprocess.TimeoutExpired as e:
            log.error(f"gwc command timed out: {e}")
            raise RuntimeError(f"Database creation timed out: {e}") from e
        except subprocess.CalledProcessError as e:
            log.error(f"gwc failed: {e.stderr}")
            raise RuntimeError(f"Failed to create database: {e.stderr}") from e
        except Exception as e:
            log.error(f"Database creation failed: {e}")
            raise

    async def delete_geneweb_database(self, db_name: str) -> None:
        """
        Delete a GeneWeb database (.gwb directory).

        Args:
            db_name: Name of the database to delete (without .gwb extension)

        Raises:
            ValueError: If database does not exist
            RuntimeError: If deletion fails

        Example:
            await legacy_db.delete_geneweb_database("old_family")
            # Deletes: /bases/old_family.gwb/
        """
        if not self.gwb_path:
            raise RuntimeError("No gwb_path configured, cannot delete database")

        base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent
        db_path = base_dir / f"{db_name}.gwb"

        # Check if exists
        if not db_path.exists():
            raise ValueError(f"Database '{db_name}' does not exist at {db_path}")

        log.info(f"Deleting GeneWeb database: {db_name}")

        try:
            # Delete the .gwb directory
            shutil.rmtree(db_path)
            log.info(f"✅ Deleted database directory: {db_path}")

            # Delete associated files (.gwf and .lck)
            gwf_file = base_dir / f"{db_name}.gwf"
            lck_file = base_dir / f"{db_name}.lck"

            if gwf_file.exists():
                gwf_file.unlink()
                log.info(f"✅ Deleted .gwf file: {gwf_file}")

            if lck_file.exists():
                lck_file.unlink()
                log.info(f"✅ Deleted .lck file: {lck_file}")

        except Exception as e:
            log.error(f"Database deletion failed: {e}")
            raise RuntimeError(f"Failed to delete database: {e}") from e

    # =========================================================================
    # Cache Management
    # =========================================================================

    async def initialize(self) -> None:
        """
        Initialize LegacyDB provider (load cache from .gwb file).

        This is the public interface for initialization.
        Called by DBConnector during startup.
        """
        await self._load_cache()

    async def _load_cache(self) -> None:
        """Load genealogical data from .gwb into in-memory cache via GEDCOM."""
        log.info("Loading cache from .gwb...")

        if not self.gwb_path:
            log.warning("No gwb_path configured, skipping cache load")
            return

        async with self._cache_lock:
            try:
                # Export .gwb to GEDCOM
                gedcom_path = await self._export_gwb_to_gedcom()

                # Parse GEDCOM into cache
                persons, families = await self._parse_gedcom(gedcom_path)

                # Update cache
                self._cache = {"persons": persons, "families": families}
                self._stats.persons_count = len(persons)
                self._stats.families_count = len(families)
                self._stats.last_refresh = datetime.now()
                self._last_cache_refresh = datetime.now()

                log.info(
                    f"✅ Cache loaded: {len(persons)} persons, {len(families)} families"
                )

            except Exception as e:
                log.error(f"Failed to load cache: {e}")
                raise

    async def invalidate_cache(self) -> None:
        """Force cache reload on next access."""
        async with self._cache_lock:
            self._cache.clear()
            self._last_cache_refresh = None
        log.info("Cache invalidated")

    def get_cache_stats(self) -> CacheStats:
        """Get current cache statistics."""
        return self._stats

    async def start_background_refresh(self) -> None:
        """Start background task to refresh cache periodically."""
        if self._background_refresh_task:
            log.warning("Background refresh already running")
            return

        async def refresh_loop() -> None:
            while True:
                await asyncio.sleep(self.cache_ttl_seconds)
                try:
                    await self._load_cache()
                    log.info("Background cache refresh completed")
                except Exception as e:
                    log.error(f"Background refresh failed: {e}")

        self._background_refresh_task = asyncio.create_task(refresh_loop())
        log.info("Background cache refresh started")

    async def stop_background_refresh(self) -> None:
        """Stop background cache refresh task."""
        if self._background_refresh_task:
            self._background_refresh_task.cancel()
            try:
                await self._background_refresh_task
            except asyncio.CancelledError:
                pass
            self._background_refresh_task = None
            log.info("Background cache refresh stopped")

    # =========================================================================
    # Person Operations (Read)
    # =========================================================================

    async def get_all_persons(self) -> list[dict[str, Any]]:
        """
        Get all persons from the genealogical database.

        Returns:
            List of person dictionaries with fields: id, name, birth, death, etc.
        """
        if "persons" not in self._cache:
            await self._load_cache()

        self._stats.hit_count += 1
        return list(self._cache.get("persons", {}).values())

    async def get_person(self, person_id: str) -> dict[str, Any] | None:
        """
        Get a single person by their ID.

        Args:
            person_id: GEDCOM individual ID (e.g., "I123")

        Returns:
            Person dictionary or None if not found
        """
        if "persons" not in self._cache:
            await self._load_cache()

        persons = self._cache.get("persons", {})
        person: dict[str, Any] | None = persons.get(person_id)

        if person:
            self._stats.hit_count += 1
        else:
            self._stats.miss_count += 1

        return person

    async def search_persons(
        self,
        firstname: str | None = None,
        surname: str | None = None,
        birth_year: int | None = None,
        death_year: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search persons by various criteria.

        Args:
            firstname: First name to search for (case-insensitive)
            surname: Surname to search for (case-insensitive)
            birth_year: Birth year filter
            death_year: Death year filter

        Returns:
            List of matching persons
        """
        if "persons" not in self._cache:
            await self._load_cache()

        persons = self._cache.get("persons", {}).values()
        results = []

        for person in persons:
            # Filter by firstname
            if firstname and not self._matches_firstname(person, firstname):
                continue

            # Filter by surname
            if surname and not self._matches_surname(person, surname):
                continue

            # Filter by birth year
            if birth_year:
                birth = person.get("birth")
                if not birth or self._get_year_from_event(birth) != birth_year:
                    continue

            # Filter by death year
            if death_year:
                death = person.get("death")
                if not death or self._get_year_from_event(death) != death_year:
                    continue

            results.append(person)

        self._stats.hit_count += 1
        return results

    def _extract_surname(self, name: str) -> str:
        """Extract surname from GEDCOM name format (First /SURNAME/)."""
        if "/" in name:
            parts = name.split("/")
            if len(parts) >= 2:
                return parts[1].strip().lower()
        return name.strip().lower()

    def _matches_surname(self, person: dict[str, Any], search_surname: str) -> bool:
        """Check if person's surname matches search term (case-insensitive)."""
        name = person.get("name", "")
        surname = self._extract_surname(name)
        return search_surname.lower() in surname

    async def search_by_surname(
        self, surname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Search persons by surname.

        Args:
            surname: Surname to search for
            limit: Maximum results to return

        Returns:
            List of matching persons (up to limit)
        """
        return (await self.search_persons(surname=surname))[:limit]

    def _extract_firstname(self, name: str) -> str:
        """Extract first name from GEDCOM name format (First /SURNAME/)."""
        if "/" in name:
            return name.split("/")[0].strip().lower()
        return name.strip().lower()

    def _matches_firstname(self, person: dict[str, Any], search_firstname: str) -> bool:
        """Check if person's first name matches search term (case-insensitive)."""
        name = person.get("name", "")
        firstname = self._extract_firstname(name)
        return search_firstname.lower() in firstname

    async def search_by_firstname(
        self, firstname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Search persons by first name.

        Args:
            firstname: First name to search for
            limit: Maximum results to return

        Returns:
            List of matching persons (up to limit)
        """
        return (await self.search_persons(firstname=firstname))[:limit]

    def _parse_person_key(self, key: str) -> tuple[str, str] | None:
        """
        Parse person key in format 'firstname.occ surname'.

        Args:
            key: Person key (e.g., "john.1 smith")

        Returns:
            Tuple of (firstname_with_occ, surname) or None if invalid
        """
        parts = key.strip().split()
        if len(parts) < 2:
            return None

        firstname_occ = parts[0].lower()
        surname = " ".join(parts[1:]).lower()

        return firstname_occ, surname

    def _person_matches_key(
        self, person: dict[str, Any], firstname_occ: str, surname: str
    ) -> bool:
        """Check if person matches the parsed key components."""
        name = person.get("name", "")
        person_firstname = self._extract_firstname(name)
        person_surname = self._extract_surname(name)

        # Extract occurrence number if present
        if "." in firstname_occ:
            base_firstname, occ = firstname_occ.split(".", 1)
            # For now, ignore occurrence number (would need additional data)
            return (
                person_firstname == base_firstname.lower()
                and person_surname == surname.lower()
            )

        return (
            person_firstname == firstname_occ.lower()
            and person_surname == surname.lower()
        )

    async def search_by_key(self, key: str, limit: int = 100) -> list[dict[str, Any]]:
        """
        Search persons by GeneWeb person key format.

        Args:
            key: Person key in format "firstname.occ surname" (e.g., "john.1 smith")
            limit: Maximum results to return

        Returns:
            List of matching persons
        """
        parsed = self._parse_person_key(key)
        if not parsed:
            return []

        firstname_occ, surname = parsed

        if "persons" not in self._cache:
            await self._load_cache()

        persons = self._cache.get("persons", {}).values()
        results = [
            p for p in persons if self._person_matches_key(p, firstname_occ, surname)
        ]

        self._stats.hit_count += 1
        return results[:limit]

    # =========================================================================
    # Statistics & Analysis
    # =========================================================================

    def _get_year_from_event(self, event: dict[str, Any] | None) -> int | None:
        """Extract year from event dictionary."""
        if not event:
            return None

        date_str = event.get("date", "")
        if not date_str:
            return None

        # Try to extract year (basic parsing)
        parts = date_str.split()
        for part in parts:
            if part.isdigit() and len(part) == 4:
                return int(part)

        return None

    def _is_person_dead(self, person: dict[str, Any]) -> bool:
        """Check if person is deceased (has death event)."""
        return person.get("death") is not None

    def _count_sex_statistics(self, persons: list[dict[str, Any]]) -> dict[str, int]:
        """Count persons by sex."""
        stats = {"male": 0, "female": 0, "unknown": 0}

        for person in persons:
            sex = person.get("sex", "").lower()
            if sex == "m":
                stats["male"] += 1
            elif sex == "f":
                stats["female"] += 1
            else:
                stats["unknown"] += 1

        return stats

    def _update_longevity_records(
        self,
        person: dict[str, Any],
        oldest_male: dict[str, Any] | None,
        oldest_female: dict[str, Any] | None,
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """Update oldest person records by sex."""
        birth_year = self._get_year_from_event(person.get("birth"))
        death_year = self._get_year_from_event(person.get("death"))

        if birth_year and death_year:
            age = death_year - birth_year
            sex = person.get("sex", "").lower()

            if sex == "m":
                if not oldest_male or age > oldest_male.get("age", 0):
                    oldest_male = {"person": person, "age": age}
            elif sex == "f":
                if not oldest_female or age > oldest_female.get("age", 0):
                    oldest_female = {"person": person, "age": age}

        return oldest_male, oldest_female

    def _update_parenting_age_record(
        self,
        parent: dict[str, Any],
        child_birth_year: int,
        current_record: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Update oldest parent at birth record."""
        parent_birth_year = self._get_year_from_event(parent.get("birth"))
        if parent_birth_year:
            age_at_birth = child_birth_year - parent_birth_year
            if not current_record or age_at_birth > current_record.get("age", 0):
                return {"parent": parent, "age": age_at_birth}
        return current_record

    def _analyze_family_parenting_ages(
        self,
        family: dict[str, Any],
        persons: dict[str, Any],
        oldest_father: dict[str, Any] | None,
        oldest_mother: dict[str, Any] | None,
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """Analyze parenting ages for a family."""
        for child_id in family.get("children", []):
            child = persons.get(child_id)
            if not child:
                continue

            child_birth_year = self._get_year_from_event(child.get("birth"))
            if not child_birth_year:
                continue

            # Check father
            father_id = family.get("husband_id")
            if father_id:
                father = persons.get(father_id)
                if father:
                    oldest_father = self._update_parenting_age_record(
                        father, child_birth_year, oldest_father
                    )

            # Check mother
            mother_id = family.get("wife_id")
            if mother_id:
                mother = persons.get(mother_id)
                if mother:
                    oldest_mother = self._update_parenting_age_record(
                        mother, child_birth_year, oldest_mother
                    )

        return oldest_father, oldest_mother

    def _clean_statistics(self, stats: dict[str, Any]) -> None:
        """Remove None values from statistics dictionary."""
        keys_to_remove = [k for k, v in stats.items() if v is None]
        for key in keys_to_remove:
            del stats[key]

    async def get_database_statistics(self) -> dict[str, Any]:
        """
        Calculate comprehensive database statistics.

        Returns:
            Dictionary with statistics including person counts, age records, etc.
        """
        if "persons" not in self._cache:
            await self._load_cache()

        persons_dict = self._cache.get("persons", {})
        families_dict = self._cache.get("families", {})
        persons = list(persons_dict.values())

        # Basic counts
        total_persons = len(persons)
        total_families = len(families_dict)
        living = sum(1 for p in persons if not self._is_person_dead(p))
        deceased = total_persons - living

        # Sex distribution
        sex_stats = self._count_sex_statistics(persons)

        # Longevity records
        oldest_male: dict[str, Any] | None = None
        oldest_female: dict[str, Any] | None = None

        for person in persons:
            if self._is_person_dead(person):
                oldest_male, oldest_female = self._update_longevity_records(
                    person, oldest_male, oldest_female
                )

        # Parenting age records
        oldest_father: dict[str, Any] | None = None
        oldest_mother: dict[str, Any] | None = None

        for family in families_dict.values():
            oldest_father, oldest_mother = self._analyze_family_parenting_ages(
                family, persons_dict, oldest_father, oldest_mother
            )

        # Build statistics
        stats = {
            "total_persons": total_persons,
            "total_families": total_families,
            "living_persons": living,
            "deceased_persons": deceased,
            "male_count": sex_stats["male"],
            "female_count": sex_stats["female"],
            "unknown_sex_count": sex_stats["unknown"],
            "oldest_male": oldest_male,
            "oldest_female": oldest_female,
            "oldest_father_at_birth": oldest_father,
            "oldest_mother_at_birth": oldest_mother,
        }

        # Clean None values
        self._clean_statistics(stats)

        return stats

    # =========================================================================
    # Person Operations (Write)
    # =========================================================================

    async def create_person(self, person_data: dict[str, Any]) -> str:
        """
        Create a new person in the database.

        Args:
            person_data: Dictionary with person fields (name, birth, death, etc.)

        Returns:
            New person's ID

        Note:
            This operation modifies the .gwb file through GEDCOM conversion.
        """
        if "persons" not in self._cache:
            await self._load_cache()

        # Generate new ID
        persons = self._cache.get("persons", {})
        max_id = 0
        for person_id in persons:
            if person_id.startswith("I"):
                try:
                    num = int(person_id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    pass

        new_id = f"I{max_id + 1}"
        person_data["id"] = new_id

        # Build GEDCOM with new person
        gedcom_path = await self._build_gedcom_with_person(person_data)

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Created person {new_id}")
        return new_id

    async def update_person(self, person_id: str, person_data: dict[str, Any]) -> None:
        """
        Update an existing person.

        Args:
            person_id: ID of person to update
            person_data: Updated person fields

        Raises:
            ValueError: If person not found
        """
        if "persons" not in self._cache:
            await self._load_cache()

        persons = self._cache.get("persons", {})
        if person_id not in persons:
            raise ValueError(f"Person {person_id} not found")

        # Update cache
        person_data["id"] = person_id
        persons[person_id] = person_data

        # Rebuild GEDCOM with all persons
        all_persons = list(persons.values())
        gedcom_path = await self._build_gedcom_with_persons(all_persons)

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Updated person {person_id}")

    async def delete_person(self, person_id: str) -> None:
        """
        Delete a person from the database.

        Args:
            person_id: ID of person to delete

        Raises:
            ValueError: If person not found
        """
        if "persons" not in self._cache:
            await self._load_cache()

        persons = self._cache.get("persons", {})
        if person_id not in persons:
            raise ValueError(f"Person {person_id} not found")

        # Remove from cache
        del persons[person_id]

        # Remove from families (as spouse or child)
        families = self._cache.get("families", {})
        for family in families.values():
            if family.get("husband_id") == person_id:
                family["husband_id"] = None
            if family.get("wife_id") == person_id:
                family["wife_id"] = None
            if person_id in family.get("children", []):
                family["children"].remove(person_id)

        # Rebuild GEDCOM
        all_persons = list(persons.values())
        all_families = list(families.values())
        gedcom_path = await self._build_gedcom_with_persons_and_families(
            all_persons, all_families
        )

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Deleted person {person_id}")

    # =========================================================================
    # Family Operations
    # =========================================================================

    async def get_family(self, family_id: str) -> dict[str, Any] | None:
        """Get a family by ID."""
        if "families" not in self._cache:
            await self._load_cache()

        families = self._cache.get("families", {})
        family: dict[str, Any] | None = families.get(family_id)

        if family:
            self._stats.hit_count += 1
        else:
            self._stats.miss_count += 1

        return family

    async def get_all_families(self) -> list[dict[str, Any]]:
        """Get all families."""
        if "families" not in self._cache:
            await self._load_cache()

        self._stats.hit_count += 1
        return list(self._cache.get("families", {}).values())

    async def get_family_members(
        self, family_id: str
    ) -> dict[str, dict[str, Any] | list[dict[str, Any]] | None]:
        """
        Get all members of a family (parents and children).

        Args:
            family_id: Family ID

        Returns:
            Dictionary with husband, wife, and children
        """
        family = await self.get_family(family_id)
        if not family:
            raise ValueError(f"Family {family_id} not found")

        husband = None
        wife = None
        children = []

        husband_id = family.get("husband_id")
        if husband_id:
            husband = await self.get_person(husband_id)

        wife_id = family.get("wife_id")
        if wife_id:
            wife = await self.get_person(wife_id)

        for child_id in family.get("children", []):
            child = await self.get_person(child_id)
            if child:
                children.append(child)

        return {"husband": husband, "wife": wife, "children": children}

    async def create_family(self, family_data: dict[str, Any]) -> str:
        """Create a new family."""
        if "families" not in self._cache:
            await self._load_cache()

        # Generate new ID
        families = self._cache.get("families", {})
        max_id = 0
        for family_id in families:
            if family_id.startswith("F"):
                try:
                    num = int(family_id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    pass

        new_id = f"F{max_id + 1}"
        family_data["id"] = new_id

        # Build GEDCOM with new family
        gedcom_path = await self._build_gedcom_with_new_family(family_data)

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Created family {new_id}")
        return new_id

    async def update_family(self, family_id: str, family_data: dict[str, Any]) -> None:
        """Update an existing family."""
        if "families" not in self._cache:
            await self._load_cache()

        families = self._cache.get("families", {})
        if family_id not in families:
            raise ValueError(f"Family {family_id} not found")

        # Update cache
        family_data["id"] = family_id
        families[family_id] = family_data

        # Rebuild GEDCOM
        all_persons = list(self._cache.get("persons", {}).values())
        all_families = list(families.values())
        gedcom_path = await self._build_gedcom_with_persons_and_families(
            all_persons, all_families
        )

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Updated family {family_id}")

    def _update_parent_in_family(
        self, family: dict[str, Any], parent_id: str, role: str
    ) -> None:
        """Update parent in family (husband or wife)."""
        family[f"{role}_id"] = parent_id

    def _update_children_in_family(
        self, family: dict[str, Any], child_ids: list[str]
    ) -> None:
        """Update children list in family."""
        family["children"] = child_ids

    async def update_family_with_members(
        self,
        family_id: str,
        husband_id: str | None = None,
        wife_id: str | None = None,
        child_ids: list[str] | None = None,
    ) -> None:
        """
        Update family members (parents and children).

        Args:
            family_id: Family ID to update
            husband_id: Optional husband ID
            wife_id: Optional wife ID
            child_ids: Optional list of child IDs
        """
        family = await self.get_family(family_id)
        if not family:
            raise ValueError(f"Family {family_id} not found")

        if husband_id is not None:
            self._update_parent_in_family(family, husband_id, "husband")

        if wife_id is not None:
            self._update_parent_in_family(family, wife_id, "wife")

        if child_ids is not None:
            self._update_children_in_family(family, child_ids)

        await self.update_family(family_id, family)

    async def delete_family(self, family_id: str) -> None:
        """Delete a family."""
        if "families" not in self._cache:
            await self._load_cache()

        families = self._cache.get("families", {})
        if family_id not in families:
            raise ValueError(f"Family {family_id} not found")

        # Remove from cache
        del families[family_id]

        # Rebuild GEDCOM
        all_persons = list(self._cache.get("persons", {}).values())
        all_families = list(families.values())
        gedcom_path = await self._build_gedcom_with_persons_and_families(
            all_persons, all_families
        )

        # Import to .gwb
        await self._import_gedcom_to_gwb(gedcom_path)

        # Reload cache
        await self.invalidate_cache()
        await self._load_cache()

        log.info(f"Deleted family {family_id}")

    async def add_child_to_family(self, family_id: str, child_id: str) -> None:
        """Add a child to a family."""
        family = await self.get_family(family_id)
        if not family:
            raise ValueError(f"Family {family_id} not found")

        # Verify child exists
        child = await self.get_person(child_id)
        if not child:
            raise ValueError(f"Person {child_id} not found")

        # Add child
        children = family.get("children", [])
        if child_id not in children:
            children.append(child_id)
            family["children"] = children

        await self.update_family(family_id, family)

    async def get_person_parents(
        self, person_id: str
    ) -> dict[str, dict[str, Any] | None]:
        """Get parents of a person."""
        if "families" not in self._cache:
            await self._load_cache()

        families = self._cache.get("families", {})

        # Find family where person is a child
        for family in families.values():
            if person_id in family.get("children", []):
                husband_id = family.get("husband_id")
                wife_id = family.get("wife_id")

                father = await self.get_person(husband_id) if husband_id else None
                mother = await self.get_person(wife_id) if wife_id else None

                return {"father": father, "mother": mother}

        return {"father": None, "mother": None}

    async def get_person_families(self, person_id: str) -> list[dict[str, Any]]:
        """Get all families where person is a spouse."""
        if "families" not in self._cache:
            await self._load_cache()

        families = self._cache.get("families", {})
        result = []

        for family in families.values():
            if (
                family.get("husband_id") == person_id
                or family.get("wife_id") == person_id
            ):
                result.append(family)

        return result

    # =========================================================================
    # GEDCOM Conversion (Private)
    # =========================================================================

    async def _export_gwb_to_gedcom(self) -> Path:
        """
        Export .gwb to GEDCOM file.

        Returns:
            Path to exported GEDCOM file

        Raises:
            RuntimeError: If export fails
        """
        if not self.gwb_path or not self.gwb2ged_bin:
            raise RuntimeError("gwb_path or gwb2ged_bin not configured")

        # Create temporary file for GEDCOM output
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ged", delete=False) as tmp:
            gedcom_path = Path(tmp.name)

        try:
            # Run gwb2ged
            # Typical command: gwb2ged base -o output.ged
            base_name = self.gwb_path.stem
            base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent

            result = subprocess.run(  # noqa: S603
                [
                    str(self.gwb2ged_bin),
                    base_name,
                    "-o",
                    str(gedcom_path),
                ],
                cwd=base_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                raise RuntimeError(f"gwb2ged failed: {result.stderr or result.stdout}")

            log.debug(f"Exported .gwb to GEDCOM: {gedcom_path}")
            return gedcom_path

        except Exception as e:
            if gedcom_path.exists():
                gedcom_path.unlink()
            raise RuntimeError(f"Failed to export .gwb to GEDCOM: {e}") from e

    def _parse_gedcom_person_element(self, element: Any) -> tuple[str, dict[str, Any]]:
        """Parse GEDCOM person element into dictionary."""
        person_id = element.get_pointer()
        person: dict[str, Any] = {"id": person_id}

        for child in element.get_child_elements():
            tag = child.get_tag()

            if tag == "NAME":
                person["name"] = child.get_value()
            elif tag == "SEX":
                person["sex"] = child.get_value()
            elif tag == "BIRT":
                person["birth"] = self._parse_gedcom_event(child)
            elif tag == "DEAT":
                person["death"] = self._parse_gedcom_event(child)

        return person_id, person

    def _parse_gedcom_event(self, child: Any) -> dict[str, Any]:
        """Parse GEDCOM event (birth, death, etc.)."""
        event: dict[str, Any] = {}
        for subchild in child.get_child_elements():
            if subchild.get_tag() == "DATE":
                event["date"] = subchild.get_value()
            elif subchild.get_tag() == "PLAC":
                event["place"] = subchild.get_value()
        return event

    def _parse_gedcom_family_element(self, element: Any) -> tuple[str, dict[str, Any]]:
        """Parse GEDCOM family element into dictionary."""
        family_id = element.get_pointer()
        family: dict[str, Any] = {"id": family_id, "children": []}

        for child in element.get_child_elements():
            tag = child.get_tag()

            if tag == "HUSB":
                family["husband_id"] = child.get_value()
            elif tag == "WIFE":
                family["wife_id"] = child.get_value()
            elif tag == "CHIL":
                family["children"].append(child.get_value())

        return family_id, family

    async def _parse_gedcom(
        self, gedcom_path: Path
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Parse GEDCOM file into persons and families dictionaries.

        Args:
            gedcom_path: Path to GEDCOM file

        Returns:
            Tuple of (persons_dict, families_dict)
        """
        parser = GedcomParser()
        parser.parse_file(str(gedcom_path))

        persons: dict[str, Any] = {}
        families: dict[str, Any] = {}

        # Parse individuals
        for element in parser.get_element_list():
            if element.get_tag() == "INDI":
                person_id, person = self._parse_gedcom_person_element(element)
                persons[person_id] = person
            elif element.get_tag() == "FAM":
                family_id, family = self._parse_gedcom_family_element(element)
                families[family_id] = family

        return persons, families

    async def _build_gedcom_with_person(self, person_data: dict[str, Any]) -> Path:
        """
        Build GEDCOM file with existing persons + new person.

        Args:
            person_data: New person data

        Returns:
            Path to generated GEDCOM file
        """
        persons = list(self._cache.get("persons", {}).values())
        persons.append(person_data)

        return await self._build_gedcom_with_persons(persons)

    def _write_gedcom_person(self, f: Any, person: dict[str, Any]) -> None:
        """Write person to GEDCOM file."""
        f.write(f"0 @{person['id']}@ INDI\n")
        if "name" in person:
            f.write(f"1 NAME {person['name']}\n")
        if "sex" in person:
            f.write(f"1 SEX {person['sex']}\n")
        # Add birth/death if present

    def _write_gedcom_family(self, f: Any, family: dict[str, Any]) -> None:
        """Write family to GEDCOM file."""
        f.write(f"0 @{family['id']}@ FAM\n")
        if "husband_id" in family:
            f.write(f"1 HUSB @{family['husband_id']}@\n")
        if "wife_id" in family:
            f.write(f"1 WIFE @{family['wife_id']}@\n")
        for child_id in family.get("children", []):
            f.write(f"1 CHIL @{child_id}@\n")

    async def _build_gedcom_with_persons_and_families(
        self, persons: list[dict[str, Any]], families: list[dict[str, Any]]
    ) -> Path:
        """Build GEDCOM file with persons and families."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ged", delete=False) as tmp:
            gedcom_path = Path(tmp.name)

            # Write GEDCOM header
            tmp.write("0 HEAD\n")
            tmp.write("1 GEDC\n")
            tmp.write("2 VERS 5.5.1\n")

            # Write persons
            for person in persons:
                self._write_gedcom_person(tmp, person)

            # Write families
            for family in families:
                self._write_gedcom_family(tmp, family)

            # Write trailer
            tmp.write("0 TRLR\n")

        return gedcom_path

    async def _build_gedcom_with_new_family(self, family_data: dict[str, Any]) -> Path:
        """Build GEDCOM with existing families + new family."""
        families = list(self._cache.get("families", {}).values())
        families.append(family_data)

        persons = list(self._cache.get("persons", {}).values())

        return await self._build_gedcom_with_persons_and_families(persons, families)

    async def _build_gedcom_with_persons(self, persons: list[dict[str, Any]]) -> Path:
        """Build GEDCOM file with given persons."""
        families = list(self._cache.get("families", {}).values())
        return await self._build_gedcom_with_persons_and_families(persons, families)

    async def _import_gedcom_to_gwb(self, gedcom_path: Path) -> None:
        """
        Import GEDCOM file to .gwb.

        Args:
            gedcom_path: Path to GEDCOM file

        Raises:
            RuntimeError: If import fails
        """
        if not self.gwb_path or not self.ged2gwb_bin:
            raise RuntimeError("gwb_path or ged2gwb_bin not configured")

        try:
            # Run ged2gwb
            # Typical command: ged2gwb input.ged -o base
            base_name = self.gwb_path.stem
            base_dir = self.gwb_path if self.gwb_path.is_dir() else self.gwb_path.parent

            result = subprocess.run(  # noqa: S603
                [
                    str(self.ged2gwb_bin),
                    str(gedcom_path),
                    "-o",
                    base_name,
                ],
                cwd=base_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                raise RuntimeError(f"ged2gwb failed: {result.stderr or result.stdout}")

            log.debug(f"Imported GEDCOM to .gwb: {self.gwb_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to import GEDCOM to .gwb: {e}") from e
        finally:
            # Clean up temporary GEDCOM file
            if gedcom_path.exists():
                gedcom_path.unlink()
