"""
Database connector orchestrating PostgreSQL metadata and genealogical data operations.

This connector manages two independent data layers:
1. PostgreSQL: Direct session management for metadata (users, config, etc.)
2. DatabaseProvider: Polymorphic interface for genealogical data (persons, families)
   - Current: LegacyDB (.gwb files via GEDCOM)
   - Future: PostgresProvider (native PostgreSQL storage)

The provider can be swapped transparently thanks to the Strategy Pattern.

Usage:
    connector = DBConnector(
        database_url="postgresql+asyncpg://...",
        gwb_path="/data/base.gwb",
        gwb2ged_bin="/usr/bin/gwb2ged",
        ged2gwb_bin="/usr/bin/ged2gwb"
    )
    await connector.initialize()
    persons = await connector.get_all_persons()  # Delegates to provider
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.persistence.database_provider import CacheStats, DatabaseProvider
from app.persistence.legacy_db import LegacyDB
from app.settings import settings

log = logging.getLogger(__name__)


class DBConnector:
    """
    Orchestrator managing PostgreSQL metadata and genealogical data provider.

    Architecture:
    - PostgreSQL: Metadata operations (sessions, engine)
    - Provider: Genealogical operations (polymorphic: LegacyDB/PostgresProvider)
    """

    provider: DatabaseProvider
    legacy_db: DatabaseProvider

    def __init__(
        self,
        database_url: str | None = None,
        gwb_path: Path | str | None = None,
        gwb2ged_bin: Path | str | None = None,
        ged2gwb_bin: Path | str | None = None,
        gwc_bin: Path | str | None = None,
        cache_ttl_seconds: int = 300,
        use_postgres_cache: bool = False,
    ) -> None:
        """
        Initialize database connector.

        Args:
            database_url: PostgreSQL connection URL
            gwb_path: Path to .gwb database file
            gwb2ged_bin: Path to gwb2ged executable
            ged2gwb_bin: Path to ged2gwb executable
            gwc_bin: Path to gwc (GeneWeb Compiler) executable
            cache_ttl_seconds: Cache TTL in seconds
            use_postgres_cache: Enable PostgreSQL caching (Phase 2)
        """
        self.database_url = database_url or settings.database_url
        gwb_path = gwb_path or settings.gwb_path
        gwb2ged_bin = gwb2ged_bin or settings.gwb2ged_bin
        ged2gwb_bin = ged2gwb_bin or settings.ged2gwb_bin
        gwc_bin = gwc_bin or settings.gwc_bin

        self._engine: AsyncEngine = create_async_engine(
            self.database_url,
            echo=settings.database_echo,
            future=settings.database_future,
        )

        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, autoflush=False
        )

        self.provider: DatabaseProvider = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
            cache_ttl_seconds=cache_ttl_seconds,
        )
        self.legacy_db = self.provider

        self.use_postgres_cache = use_postgres_cache

        log.info(
            f"DBConnector initialized: postgres={bool(database_url)}, "
            f"gwb={bool(gwb_path)}, cache={use_postgres_cache}"
        )

    # =========================================================================
    # Lifecycle Management
    # =========================================================================

    async def initialize(self) -> None:
        """Initialize connector and load provider cache."""
        log.info("Initializing DBConnector...")
        await self.provider.initialize()
        log.info("✅ DBConnector ready")

    async def shutdown(self) -> None:
        """Shutdown connector and cleanup resources."""
        log.info("Shutting down DBConnector...")
        await self.provider.stop_background_refresh()
        await self.close()
        log.info("✅ DBConnector shutdown complete")

    async def is_connected(self) -> bool:
        """Test if database connection is working (delegates to provider)."""
        return await self.provider.is_connected()

    # =========================================================================
    # PostgreSQL Session Management
    # =========================================================================

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Get a PostgreSQL session with automatic cleanup."""
        session = self._session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def _execute_query(
        self, query: str, params: dict[str, Any] | None = None
    ) -> Any:
        """
        Execute raw SQL query (PRIVATE - for internal use only).

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            return result

    async def close(self) -> None:
        """Close PostgreSQL engine and cleanup resources."""
        await self._engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        """Get underlying SQLAlchemy engine (advanced usage)."""
        return self._engine

    # =========================================================================
    # Database Management
    # =========================================================================

    def list_geneweb_databases(self) -> list[str]:
        """List all available GeneWeb databases."""
        return self.provider.list_geneweb_databases()

    def get_database_info(self, db_name: str) -> dict[str, Any] | None:
        """Get detailed information about a specific database."""
        return self.provider.get_database_info(db_name)

    def list_databases_with_info(
        self, base_dir: Path | str | None = None
    ) -> list[dict[str, Any]]:
        """List all databases with detailed information."""
        return self.provider.list_databases_with_info(base_dir)

    async def create_geneweb_database(
        self, db_name: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Create a new GeneWeb database."""
        return await self.provider.create_geneweb_database(db_name, metadata)

    async def delete_geneweb_database(self, db_name: str) -> None:
        """Delete a GeneWeb database."""
        await self.provider.delete_geneweb_database(db_name)

    # =========================================================================
    # Cache Management
    # =========================================================================

    async def invalidate_cache(self) -> None:
        """Force cache reload on next access."""
        await self.provider.invalidate_cache()

    def get_cache_stats(self) -> CacheStats:
        """Get current cache statistics."""
        return self.provider.get_cache_stats()

    async def start_background_refresh(self) -> None:
        """Start background cache refresh task."""
        await self.provider.start_background_refresh()

    async def stop_background_refresh(self) -> None:
        """Stop background cache refresh task."""
        await self.provider.stop_background_refresh()

    # =========================================================================
    # Person Operations
    # =========================================================================

    async def get_all_persons(self) -> list[dict[str, Any]]:
        """Get all persons."""
        return await self.provider.get_all_persons()

    async def get_person(self, person_id: str) -> dict[str, Any] | None:
        """Get a person by ID."""
        return await self.provider.get_person(person_id)

    async def search_persons(
        self,
        firstname: str | None = None,
        surname: str | None = None,
        birth_year: int | None = None,
        death_year: int | None = None,
    ) -> list[dict[str, Any]]:
        """Search persons by criteria."""
        return await self.provider.search_persons(
            firstname=firstname,
            surname=surname,
            birth_year=birth_year,
            death_year=death_year,
        )

    async def search_by_surname(
        self, surname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Search persons by surname."""
        return await self.provider.search_by_surname(surname, limit)

    async def search_by_firstname(
        self, firstname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Search persons by firstname."""
        return await self.provider.search_by_firstname(firstname, limit)

    async def search_by_key(self, key: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search persons by GeneWeb key."""
        return await self.provider.search_by_key(key, limit)

    async def get_database_statistics(self) -> dict[str, Any]:
        """Calculate database statistics."""
        return await self.provider.get_database_statistics()

    async def create_person(self, person_data: dict[str, Any]) -> str:
        """Create a new person."""
        return await self.provider.create_person(person_data)

    async def update_person(self, person_id: str, person_data: dict[str, Any]) -> None:
        """Update an existing person."""
        await self.provider.update_person(person_id, person_data)

    async def delete_person(self, person_id: str) -> None:
        """Delete a person."""
        await self.provider.delete_person(person_id)

    # =========================================================================
    # Family Operations
    # =========================================================================

    async def get_family(self, family_id: str) -> dict[str, Any] | None:
        """Get a family by ID."""
        return await self.provider.get_family(family_id)

    async def get_all_families(self) -> list[dict[str, Any]]:
        """Get all families."""
        return await self.provider.get_all_families()

    async def get_family_members(
        self, family_id: str
    ) -> dict[str, dict[str, Any] | list[dict[str, Any]] | None]:
        """Get all members of a family (parents and children)."""
        return await self.provider.get_family_members(family_id)

    async def create_family(self, family_data: dict[str, Any]) -> str:
        """Create a new family."""
        return await self.provider.create_family(family_data)

    async def update_family(self, family_id: str, family_data: dict[str, Any]) -> None:
        """Update a family."""
        await self.provider.update_family(family_id, family_data)

    async def update_family_with_members(
        self,
        family_id: str,
        husband_id: str | None = None,
        wife_id: str | None = None,
        child_ids: list[str] | None = None,
    ) -> None:
        """Update family members."""
        await self.provider.update_family_with_members(
            family_id, husband_id, wife_id, child_ids
        )

    async def delete_family(self, family_id: str) -> None:
        """Delete a family."""
        await self.provider.delete_family(family_id)

    async def add_child_to_family(self, family_id: str, child_id: str) -> None:
        """Add a child to a family."""
        await self.provider.add_child_to_family(family_id, child_id)

    async def get_person_parents(
        self, person_id: str
    ) -> dict[str, dict[str, Any] | None]:
        """Get parents of a person."""
        return await self.provider.get_person_parents(person_id)

    async def get_person_families(self, person_id: str) -> list[dict[str, Any]]:
        """Get all families where person is a spouse."""
        return await self.provider.get_person_families(person_id)
