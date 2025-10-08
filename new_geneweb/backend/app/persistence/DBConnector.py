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
            echo=settings.database_echo,
            future=settings.database_future,
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

    @property
    def engine(self) -> AsyncEngine:
        """Get the underlying SQLAlchemy engine (for advanced usage)."""
        return self._engine
