"""
AlchemyEncapsulation class for GeneWeb.
Provides a minimal interface for API developers to interact with the database.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.persistence.models import GenewebDatabase
from app.settings import settings


class DBConnector:
    """
    Database connector class that provides a clean abstraction layer.

    Designed to be ORM-agnostic and easily swappable with other database solutions.
    Handles connection management, session lifecycle, and data access operations.
    """

    def __init__(self, database_url: str | None = None) -> None:
        """
        Initialize the database connector.

        Args:
            database_url: Optional database URL. If not provided, uses
                settings.database_url
        """
        self.database_url = database_url or settings.database_url

        # Create async engine
        self._engine: AsyncEngine = create_async_engine(
            self.database_url,
            echo=False,
            future=True,  # Set to True for debugging SQL queries
        )

        # Create session factory
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, autoflush=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Get a database session with automatic cleanup.

        Returns:
            AsyncSession: Database session that will be automatically closed

        Example:
            async with db.get_session() as session:
                result = await session.execute(text("SELECT * FROM users"))
        """
        session = self._session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def execute_query(
        self, query: str, params: dict[str, Any] | None = None
    ) -> Any:
        """
        Execute a raw SQL query and return the result.

        Note:
            API developers should avoid using this method directly. Instead,
            create specific methods for your use cases to maintain proper
            encapsulation and data validation.

        Args:
            query: SQL query string
            params: Optional parameters for the query

        Returns:
            Query result

        Example:
            result = await db.execute_query(
                "SELECT * FROM users WHERE id = :user_id", {"user_id": 1}
            )
        """
        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            return result

    async def is_connected(self) -> bool:
        """
        Test if database connection is working.

        Returns:
            bool: True if connection is successful, False otherwise

        Example:
            if await db.is_connected():
                print("Database connection is working")
            else:
                print("Failed to connect to database")
        """
        try:
            import asyncio

            # Use a timeout to avoid long waits on connection failures
            async with asyncio.timeout(3):  # 3 second timeout
                async with self.get_session() as session:
                    await session.execute(text("SELECT 1"))
                    return True
        except Exception:
            return False

    async def close(self) -> None:
        """
        Close the database engine and clean up resources.

        Should be called when shutting down the application.
        """
        await self._engine.dispose()

    async def create_genealogy_database(
        self,
        name: str,
        description: str | None = None,
        owner: str | None = None,
        access_level: int = 1,
    ) -> GenewebDatabase:
        """
        Create a new empty genealogy database entry.

        This method creates a new entry in the geneweb_database table,
        which serves as the root for a separate genealogical database.
        The database will be empty with no individuals or families initially.

        Args:
            name: Unique name for the genealogy database
            description: Optional description of the database
            owner: Optional owner identifier
            access_level: Access level (0=private, 1=public, 2=restricted)

        Returns:
            GenewebDatabase: The created database object

        Raises:
            ValueError: If the database name already exists
            Exception: If database creation fails

        Example:
            db_entry = await db.create_genealogy_database(
                name="smith_family",
                description="Smith Family Genealogy",
                owner="john.smith@example.com",
                access_level=1
            )
        """
        async with self.get_session() as session:
            # Check if database with this name already exists
            existing = await session.execute(
                text("SELECT id FROM geneweb_database WHERE name = :name"),
                {"name": name},
            )
            if existing.fetchone() is not None:
                raise ValueError(f"Database with name '{name}' already exists")

            # Create new database entry
            new_db = GenewebDatabase(
                name=name,
                description=description,
                owner=owner,
                access_level=access_level,
                is_active=True,
                individual_count=0,
                family_count=0,
            )

            session.add(new_db)
            await session.commit()
            await session.refresh(new_db)

            return new_db

    @property
    def engine(self) -> AsyncEngine:
        """Get the underlying SQLAlchemy engine (for advanced usage)."""
        return self._engine
