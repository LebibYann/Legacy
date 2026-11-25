"""
Database Provider Interface for GeneWeb genealogical data.

This module defines the abstract interface that all database providers must implement,
allowing seamless switching between legacy .gwb files and PostgreSQL storage.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class CacheStats:
    """In-memory cache statistics."""

    hit_count: int = 0
    miss_count: int = 0
    last_refresh: datetime | None = None
    persons_count: int = 0
    families_count: int = 0

    @property
    def hit_rate(self) -> float:
        """Cache hit rate (0.0 to 1.0)."""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0


class DatabaseProvider(ABC):
    """
    Abstract interface for genealogical database operations.

    Implementations:
    - LegacyGenewebProvider: Uses .gwb files + GEDCOM parsing
    - PostgresProvider: Uses PostgreSQL with SQLAlchemy models
    """

    # =========================================================================
    # Database Management
    # =========================================================================

    @abstractmethod
    async def is_connected(self) -> bool:
        """
        Test if database connection is working.

        Returns:
            bool: True if connection is successful, False otherwise

        Note:
            For LegacyDB: Checks if .gwb file exists and binaries are accessible
            For PostgresProvider: Tests PostgreSQL connection
        """
        pass

    @abstractmethod
    def list_geneweb_databases(self) -> list[str]:
        """
        List all available GeneWeb databases.

        Returns:
            List of database names
        """
        pass

    @abstractmethod
    def get_database_info(self, db_name: str) -> dict[str, Any] | None:
        """
        Get detailed information about a specific database.

        Args:
            db_name: Name of the database

        Returns:
            Dictionary with database metadata or None if not found

        Note:
            For LegacyDB: Uses self.gwb_path.parent as base directory
            For PostgresDB: Queries geneweb_database table
        """
        pass

    @abstractmethod
    async def create_geneweb_database(
        self, db_name: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Create a new GeneWeb database.

        Args:
            db_name: Name of the new database
            metadata: Optional metadata (description, owner, etc.)

        Returns:
            Dictionary with created database information

        Raises:
            ValueError: If database already exists
            RuntimeError: If creation fails

        Note:
            For LegacyDB: Creates .gwb file using ged2gwb
            For PostgresProvider: Inserts into geneweb_database table
        """
        pass

    @abstractmethod
    async def delete_geneweb_database(self, db_name: str) -> None:
        """
        Delete a GeneWeb database.

        Args:
            db_name: Name of the database to delete

        Raises:
            ValueError: If database does not exist
            RuntimeError: If deletion fails

        Note:
            For LegacyDB: Removes .gwb directory
            For PostgresProvider: Deletes from geneweb_database table
        """
        pass

    @abstractmethod
    def list_databases_with_info(
        self, base_dir: Path | str | None = None
    ) -> list[dict[str, Any]]:
        """
        List all databases with their detailed information.

        Args:
            base_dir: Optional base directory path

        Returns:
            List of dictionaries containing database metadata
        """
        pass

    # =========================================================================
    # Cache Management
    # =========================================================================

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the provider (load initial data, start background tasks, etc.).

        Note:
            For LegacyDB: Loads cache from .gwb file
            For PostgresProvider: May prepare connection pools, etc.
        """
        pass

    @abstractmethod
    async def invalidate_cache(self) -> None:
        """Force cache reload on next access."""
        pass

    @abstractmethod
    def get_cache_stats(self) -> CacheStats:
        """
        Get current cache statistics.

        Returns:
            CacheStats object with hit/miss counts and rates
        """
        pass

    @abstractmethod
    async def start_background_refresh(self) -> None:
        """Start background task to refresh cache periodically."""
        pass

    @abstractmethod
    async def stop_background_refresh(self) -> None:
        """Stop background cache refresh task."""
        pass

    # =========================================================================
    # Person Operations
    # =========================================================================

    @abstractmethod
    async def get_all_persons(self) -> list[dict[str, Any]]:
        """
        Get all persons from the database.

        Returns:
            List of person dictionaries
        """
        pass

    @abstractmethod
    async def get_person(self, person_id: str) -> dict[str, Any] | None:
        """
        Get a specific person by ID.

        Args:
            person_id: Person identifier

        Returns:
            Person dictionary or None if not found
        """
        pass

    @abstractmethod
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
            firstname: First name to search for
            surname: Surname to search for
            birth_year: Birth year to filter by
            death_year: Death year to filter by

        Returns:
            List of matching persons
        """
        pass

    @abstractmethod
    async def search_by_surname(
        self, surname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Search persons by surname with limit."""
        pass

    @abstractmethod
    async def search_by_firstname(
        self, firstname: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Search persons by first name with limit."""
        pass

    @abstractmethod
    async def search_by_key(self, key: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search persons by GeneWeb key format with limit."""
        pass

    @abstractmethod
    async def create_person(self, person_data: dict[str, Any]) -> str:
        """
        Create a new person.

        Args:
            person_data: Person attributes

        Returns:
            New person ID
        """
        pass

    @abstractmethod
    async def update_person(self, person_id: str, updates: dict[str, Any]) -> None:
        """Update an existing person."""
        pass

    @abstractmethod
    async def delete_person(self, person_id: str) -> None:
        """Delete a person."""
        pass

    # =========================================================================
    # Family Operations
    # =========================================================================

    @abstractmethod
    async def get_family(self, family_id: str) -> dict[str, Any] | None:
        """Get a specific family by ID."""
        pass

    @abstractmethod
    async def get_all_families(self) -> list[dict[str, Any]]:
        """Get all families from the database."""
        pass

    @abstractmethod
    async def get_family_members(
        self, family_id: str
    ) -> dict[str, dict[str, Any] | list[dict[str, Any]] | None]:
        """Get family members (husband, wife, children)."""
        pass

    @abstractmethod
    async def create_family(self, family_data: dict[str, Any]) -> str:
        """
        Create a new family.

        Args:
            family_data: Family attributes

        Returns:
            New family ID
        """
        pass

    @abstractmethod
    async def update_family(self, family_id: str, updates: dict[str, Any]) -> None:
        """Update an existing family."""
        pass

    @abstractmethod
    async def delete_family(self, family_id: str) -> None:
        """Delete a family."""
        pass

    @abstractmethod
    async def add_child_to_family(self, family_id: str, child_id: str) -> None:
        """Add a child to a family."""
        pass

    @abstractmethod
    async def update_family_with_members(
        self,
        family_id: str,
        husband_id: str | None = None,
        wife_id: str | None = None,
        child_ids: list[str] | None = None,
    ) -> None:
        """Update family members (husband, wife, children)."""
        pass

    @abstractmethod
    async def get_person_parents(
        self, person_id: str
    ) -> dict[str, dict[str, Any] | None]:
        """Get parents of a person (father and mother)."""
        pass

    @abstractmethod
    async def get_person_families(self, person_id: str) -> list[dict[str, Any]]:
        """Get all families where person is a spouse."""
        pass

    # =========================================================================
    # Statistics
    # =========================================================================

    @abstractmethod
    async def get_database_statistics(self) -> dict[str, Any]:
        """
        Calculate comprehensive database statistics.

        Returns:
            Dictionary with counts, ages, longevity records, etc.
        """
        pass
