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

from app.persistence.DBConnector import DatabaseInfo, DBConnector
from app.persistence.models import GenewebDatabase


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
        assert callable(db.get_session)
        assert callable(db.execute_query)
        assert callable(db.is_connected)
        assert callable(db.close)

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


class TestCreateGenealogyDatabase:
    """Test suite for the create_genealogy_database method."""

    @pytest.mark.asyncio
    async def test_create_genealogy_database_minimal(
        self, db_connector: DBConnector
    ) -> None:
        """Test creating a genealogy database with minimal parameters."""
        # Create a database with just a name
        db_name = "test_minimal_db"

        db_entry = await db_connector.create_genealogy_database(name=db_name)

        # Verify the returned object
        assert isinstance(db_entry, GenewebDatabase)
        assert db_entry.name == db_name
        assert db_entry.id is not None
        assert db_entry.is_active is True
        assert db_entry.individual_count == 0
        assert db_entry.family_count == 0
        assert db_entry.access_level == 1  # default value
        assert db_entry.description is None
        assert db_entry.owner is None

        # Clean up: delete the test database
        async with db_connector.get_session() as session:
            await session.execute(
                text("DELETE FROM geneweb_database WHERE name = :name"),
                {"name": db_name},
            )
            await session.commit()

    @pytest.mark.asyncio
    async def test_create_genealogy_database_full(
        self, db_connector: DBConnector
    ) -> None:
        """Test creating a genealogy database with all parameters."""
        # Create a database with all parameters
        db_name = "test_full_db"
        description = "A test genealogy database"
        owner = "test_owner@example.com"
        access_level = 2

        db_entry = await db_connector.create_genealogy_database(
            name=db_name,
            description=description,
            owner=owner,
            access_level=access_level,
        )

        # Verify the returned object
        assert isinstance(db_entry, GenewebDatabase)
        assert db_entry.name == db_name
        assert db_entry.description == description
        assert db_entry.owner == owner
        assert db_entry.access_level == access_level
        assert db_entry.id is not None
        assert db_entry.is_active is True
        assert db_entry.individual_count == 0
        assert db_entry.family_count == 0

        # Clean up: delete the test database
        async with db_connector.get_session() as session:
            await session.execute(
                text("DELETE FROM geneweb_database WHERE name = :name"),
                {"name": db_name},
            )
            await session.commit()

    @pytest.mark.asyncio
    async def test_create_genealogy_database_duplicate_name(
        self, db_connector: DBConnector
    ) -> None:
        """Test that creating a database with duplicate name raises ValueError."""
        db_name = "test_duplicate_db"

        # Create the first database
        db_entry1 = await db_connector.create_genealogy_database(name=db_name)
        assert db_entry1.name == db_name

        # Try to create a second database with the same name
        with pytest.raises(ValueError, match="already exists"):
            await db_connector.create_genealogy_database(name=db_name)

        # Clean up: delete the test database
        async with db_connector.get_session() as session:
            await session.execute(
                text("DELETE FROM geneweb_database WHERE name = :name"),
                {"name": db_name},
            )
            await session.commit()

    @pytest.mark.asyncio
    async def test_create_genealogy_database_persisted(
        self, db_connector: DBConnector
    ) -> None:
        """Test that the created database is persisted in the database."""
        db_name = "test_persisted_db"

        # Create the database
        db_entry = await db_connector.create_genealogy_database(name=db_name)
        created_id = db_entry.id

        # Verify it's in the database by querying
        async with db_connector.get_session() as session:
            result = await session.execute(
                text(
                    "SELECT id, name, is_active, individual_count, family_count "
                    "FROM geneweb_database WHERE name = :name"
                ),
                {"name": db_name},
            )
            row = result.fetchone()

            assert row is not None
            assert row.id == created_id  # type: ignore
            assert row.name == db_name  # type: ignore
            assert row.is_active is True  # type: ignore
            assert row.individual_count == 0  # type: ignore
            assert row.family_count == 0  # type: ignore

            # Clean up
            await session.execute(
                text("DELETE FROM geneweb_database WHERE name = :name"),
                {"name": db_name},
            )
            await session.commit()

    @pytest.mark.asyncio
    async def test_create_multiple_genealogy_databases(
        self, db_connector: DBConnector
    ) -> None:
        """Test creating multiple genealogy databases."""
        db_names = ["test_db_1", "test_db_2", "test_db_3"]
        created_ids = []

        # Create multiple databases
        for db_name in db_names:
            db_entry = await db_connector.create_genealogy_database(name=db_name)
            created_ids.append(db_entry.id)

        # Verify all are in the database
        async with db_connector.get_session() as session:
            for i, db_name in enumerate(db_names):
                result = await session.execute(
                    text("SELECT id, name FROM geneweb_database WHERE name = :name"),
                    {"name": db_name},
                )
                row = result.fetchone()
                assert row is not None
                assert row.id == created_ids[i]  # type: ignore
                assert row.name == db_name  # type: ignore

            # Clean up
            for db_name in db_names:
                await session.execute(
                    text("DELETE FROM geneweb_database WHERE name = :name"),
                    {"name": db_name},
                )
            await session.commit()


@pytest_asyncio.fixture
async def db_connector() -> AsyncIterator[DBConnector]:
    """Fixture that provides a DBConnector instance for testing."""
    connector = DBConnector()
    yield connector
    await connector.close()


class TestListDatabases:
    """Test suite for the list_databases method."""

    @pytest.mark.asyncio
    async def test_list_databases_returns_list(self, db_connector: DBConnector) -> None:
        """Test that list_databases returns a list."""
        databases = await db_connector.list_databases()
        assert isinstance(databases, list)

    @pytest.mark.asyncio
    async def test_list_databases_returns_database_info_objects(
        self, db_connector: DBConnector
    ) -> None:
        """Test that list_databases returns DatabaseInfo objects."""
        # Create a test database first
        db_name = "test_list_db_1"
        await db_connector.create_genealogy_database(name=db_name)

        try:
            databases = await db_connector.list_databases()

            # Should have at least one database
            assert len(databases) > 0

            # All items should be DatabaseInfo objects
            for db_info in databases:
                assert isinstance(db_info, DatabaseInfo)
                assert hasattr(db_info, "name")
                assert isinstance(db_info.name, str)
        finally:
            # Clean up
            async with db_connector.get_session() as session:
                await session.execute(
                    text("DELETE FROM geneweb_database WHERE name = :name"),
                    {"name": db_name},
                )
                await session.commit()

    @pytest.mark.asyncio
    async def test_list_databases_with_multiple_databases(
        self, db_connector: DBConnector
    ) -> None:
        """Test listing multiple databases."""
        db_names = ["test_list_db_a", "test_list_db_b", "test_list_db_c"]

        # Create multiple test databases
        for db_name in db_names:
            await db_connector.create_genealogy_database(name=db_name)

        try:
            databases = await db_connector.list_databases()

            # Get the names from the returned list
            returned_names = [db.name for db in databases]

            # All created databases should be in the list
            for db_name in db_names:
                assert db_name in returned_names
        finally:
            # Clean up
            async with db_connector.get_session() as session:
                for db_name in db_names:
                    await session.execute(
                        text("DELETE FROM geneweb_database WHERE name = :name"),
                        {"name": db_name},
                    )
                await session.commit()

    @pytest.mark.asyncio
    async def test_list_databases_empty(self, db_connector: DBConnector) -> None:
        """Test listing databases when database is empty."""
        # First, clean up all test databases
        async with db_connector.get_session() as session:
            await session.execute(
                text("DELETE FROM geneweb_database WHERE name LIKE 'test_%'")
            )
            await session.commit()

        databases = await db_connector.list_databases()

        # Should return an empty list or only non-test databases
        assert isinstance(databases, list)
        # Verify no test databases exist
        test_dbs = [db for db in databases if db.name.startswith("test_")]
        assert len(test_dbs) == 0

    @pytest.mark.asyncio
    async def test_list_databases_sorted_alphabetically(
        self, db_connector: DBConnector
    ) -> None:
        """Test that databases are returned in alphabetical order."""
        db_names = ["test_zebra_db", "test_alpha_db", "test_middle_db"]
        expected_order = sorted(db_names)

        # Create databases in random order
        for db_name in db_names:
            await db_connector.create_genealogy_database(name=db_name)

        try:
            databases = await db_connector.list_databases()

            # Filter only our test databases
            test_databases = [db for db in databases if db.name in db_names]
            test_db_names = [db.name for db in test_databases]

            # Should be in alphabetical order
            assert test_db_names == expected_order
        finally:
            # Clean up
            async with db_connector.get_session() as session:
                for db_name in db_names:
                    await session.execute(
                        text("DELETE FROM geneweb_database WHERE name = :name"),
                        {"name": db_name},
                    )
                await session.commit()

    @pytest.mark.asyncio
    async def test_list_databases_dataclass_structure(
        self, db_connector: DBConnector
    ) -> None:
        """Test that DatabaseInfo has the correct dataclass structure."""
        db_name = "test_dataclass_db"
        await db_connector.create_genealogy_database(name=db_name)

        try:
            databases = await db_connector.list_databases()

            # Find our test database
            test_db = next((db for db in databases if db.name == db_name), None)
            assert test_db is not None

            # Verify it's a dataclass with the expected field
            assert isinstance(test_db, DatabaseInfo)
            assert test_db.name == db_name

            # Verify we can create DatabaseInfo manually
            manual_db_info = DatabaseInfo(name="manual_test")
            assert manual_db_info.name == "manual_test"
        finally:
            # Clean up
            async with db_connector.get_session() as session:
                await session.execute(
                    text("DELETE FROM geneweb_database WHERE name = :name"),
                    {"name": db_name},
                )
                await session.commit()
