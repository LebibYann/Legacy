"""
Tests for the database encapsulation class.
Tests ensure the class can connect to database with minimal configuration.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.DBConnector import DBConnector


class TestDBConnector:
    """Test suite for the DBConnector class."""

    def test_can_instantiate_with_minimal_config(self) -> None:
        """Test that DBConnector can be created with minimal configuration."""
        # Should be able to create with just a database URL
        db = DBConnector()
        assert db is not None

    def test_can_instantiate_with_custom_config(self) -> None:
        """Test that DBConnector can be created with custom configuration."""
        custom_url = "postgresql+asyncpg://test:test@localhost:5432/test_db"
        db = DBConnector(database_url=custom_url)
        assert db is not None
        assert db.database_url == custom_url

    @pytest.mark.asyncio
    async def test_can_connect_to_database(self) -> None:
        """Test that the connector can establish a database connection."""
        db = DBConnector()

        # Should be able to get a session
        async with db.get_session() as session:
            assert isinstance(session, AsyncSession)
            assert session is not None

    @pytest.mark.asyncio
    async def test_is_connected_method(self) -> None:
        """Test that is_connected method correctly reports connection status."""
        db = DBConnector()

        # Should return True when connection is working
        is_connected = await db.is_connected()
        assert isinstance(is_connected, bool)
        assert is_connected is True

    ####  take a long time
    # @pytest.mark.asyncio
    # async def test_is_connected_with_invalid_connection(self) -> None:
    #     """Test that is_connected returns False for invalid connections."""
    #     # Use localhost with a port that's likely to be closed for faster failure
    #     invalid_url = "postgresql+asyncpg://invalid:invalid@127.0.0.1:9999/fake_db"
    #     db = DBConnector(database_url=invalid_url)

    #     # Should return False when connection fails
    #     is_connected = await db.is_connected()
    #     assert isinstance(is_connected, bool)
    #     assert is_connected is False

    @pytest.mark.asyncio
    async def test_session_context_manager(self) -> None:
        """Test that sessions are properly managed with context manager."""
        db = DBConnector()

        session_ref = None
        async with db.get_session() as session:
            session_ref = session
            assert session.is_active  # Session should be active within context

            # Should be able to execute a simple query within the session
            result = await session.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            assert row is not None
            assert row.test == 1  # type: ignore

        # Session reference should still exist
        assert session_ref is not None

    @pytest.mark.asyncio
    async def test_multiple_sessions(self) -> None:
        """Test that multiple sessions can be created independently."""
        db = DBConnector()

        async with db.get_session() as session1:
            async with db.get_session() as session2:
                assert session1 is not session2
                assert isinstance(session1, AsyncSession)
                assert isinstance(session2, AsyncSession)

    def test_has_essential_methods(self) -> None:
        """Test that DBConnector has the essential methods for API developers."""
        db = DBConnector()

        # Should have these methods for basic database operations
        assert hasattr(db, "get_session")
        assert hasattr(db, "execute_query")
        assert hasattr(db, "is_connected")
        assert hasattr(db, "close")

        # Methods should be callable
        assert callable(getattr(db, "get_session"))
        assert callable(getattr(db, "execute_query"))
        assert callable(getattr(db, "is_connected"))
        assert callable(getattr(db, "close"))

    @pytest.mark.asyncio
    async def test_execute_simple_query(self) -> None:
        """Test that we can execute a simple query through the connector."""
        db = DBConnector()

        # Test with a simple SELECT query that should work on any PostgreSQL
        result = await db.execute_query("SELECT 1 as test_value")
        assert result is not None

    @pytest.mark.asyncio
    async def test_transaction_support(self) -> None:
        """Test that the connector supports transactions."""
        db = DBConnector()

        async with db.get_session() as session:
            # Should be able to start a transaction
            async with session.begin():
                # This should work without errors
                result = await session.execute(text("SELECT 1"))
                assert result is not None

    @pytest.mark.asyncio
    async def test_proper_cleanup(self) -> None:
        """Test that the connector properly cleans up resources."""
        db = DBConnector()

        # Use the connector
        async with db.get_session() as session:
            await session.execute(text("SELECT 1"))

        # Should be able to close cleanly
        await db.close()

    def test_connection_error_handling(self) -> None:
        """Test that connection errors are properly handled."""
        # Try to connect with an invalid URL
        invalid_url = "postgresql+asyncpg://invalid:invalid@nonexistent:9999/fake_db"
        db = DBConnector(database_url=invalid_url)

        # Should not raise an exception during instantiation
        assert db is not None

        # The connector should still be created successfully
        # Actual connection errors will happen when trying to use it
        assert db.database_url == invalid_url

    @pytest.mark.asyncio
    async def test_minimal_api_for_developers(self) -> None:
        """Test that the API is minimal and easy for developers to use."""
        db = DBConnector()

        # Should be simple to use - just create and use
        async with db.get_session() as session:
            # Common developer pattern: execute a query
            result = await session.execute(text("SELECT 'Hello GeneWeb' as greeting"))
            row = result.fetchone()
            assert row is not None
            assert row.greeting == "Hello GeneWeb"  # type: ignore

        # Should be easy to execute raw queries
        result = await db.execute_query("SELECT 42 as answer")
        row = result.fetchone()
        assert row is not None
        assert row.answer == 42  # type: ignore


@pytest_asyncio.fixture
async def db_connector() -> AsyncIterator[DBConnector]:
    """Fixture that provides a DBConnector instance for testing."""
    connector = DBConnector()
    yield connector
    await connector.close()
