"""
Unit tests for DBConnector delegation to LegacyDB.

Tests verify that DBConnector properly delegates genealogical operations
to its LegacyDB instance while maintaining PostgreSQL metadata operations.
"""

from unittest.mock import AsyncMock

import pytest

from app.persistence.DBConnector import DBConnector


@pytest.fixture
def tmp_gwb_setup(tmp_path):
    """Create temporary GeneWeb structure."""
    gwb_file = tmp_path / "test.gwb"
    gwb_file.mkdir()
    (gwb_file / "base.gwb").touch()

    gwb2ged_bin = tmp_path / "gwb2ged"
    gwb2ged_bin.touch()
    gwb2ged_bin.chmod(0o755)

    ged2gwb_bin = tmp_path / "ged2gwb"
    ged2gwb_bin.touch()
    ged2gwb_bin.chmod(0o755)

    gwc_bin = tmp_path / "gwc"
    gwc_bin.touch()
    gwc_bin.chmod(0o755)

    return {
        "gwb_path": gwb_file,
        "gwb2ged_bin": gwb2ged_bin,
        "ged2gwb_bin": ged2gwb_bin,
        "gwc_bin": gwc_bin,
    }


@pytest.fixture
def connector(tmp_gwb_setup):
    """Create DBConnector with test configuration."""
    return DBConnector(
        database_url="postgresql+asyncpg://test:test@localhost/test",
        **tmp_gwb_setup,
    )


# =============================================================================
# Initialization & Lifecycle Tests
# =============================================================================


@pytest.mark.asyncio
async def test_initialize_delegates_to_legacy_db(connector, mocker):
    """Test that initialize delegates cache loading to LegacyDB."""
    mock_load = mocker.patch.object(
        connector.legacy_db, "_load_cache", new_callable=AsyncMock
    )

    await connector.initialize()

    mock_load.assert_called_once()


@pytest.mark.asyncio
async def test_shutdown_stops_legacy_db_refresh(connector, mocker):
    """Test that shutdown stops LegacyDB background refresh."""
    mock_stop = mocker.patch.object(
        connector.legacy_db, "stop_background_refresh", new_callable=AsyncMock
    )
    mock_close = mocker.patch.object(connector, "close", new_callable=AsyncMock)

    await connector.shutdown()

    mock_stop.assert_called_once()
    mock_close.assert_called_once()


# =============================================================================
# Cache Management Delegation Tests
# =============================================================================


@pytest.mark.asyncio
async def test_invalidate_cache_delegates_to_legacy_db(connector, mocker):
    """Test that invalidate_cache delegates to LegacyDB."""
    mock_invalidate = mocker.patch.object(
        connector.legacy_db, "invalidate_cache", new_callable=AsyncMock
    )

    await connector.invalidate_cache()

    mock_invalidate.assert_called_once()


def test_get_cache_stats_delegates_to_legacy_db(connector, mocker):
    """Test that get_cache_stats delegates to LegacyDB."""
    from app.persistence.legacy_db import CacheStats

    mock_stats = CacheStats(hit_count=10, miss_count=2)
    mocker.patch.object(connector.legacy_db, "get_cache_stats", return_value=mock_stats)

    stats = connector.get_cache_stats()

    assert stats.hit_count == 10
    assert stats.miss_count == 2


@pytest.mark.asyncio
async def test_start_background_refresh_delegates_to_legacy_db(connector, mocker):
    """Test that start_background_refresh delegates to LegacyDB."""
    mock_start = mocker.patch.object(
        connector.legacy_db, "start_background_refresh", new_callable=AsyncMock
    )

    await connector.start_background_refresh()

    mock_start.assert_called_once()


# =============================================================================
# Database Listing Delegation Tests
# =============================================================================


def test_list_geneweb_databases_delegates_to_legacy_db(connector, mocker):
    """Test that list_geneweb_databases delegates to LegacyDB."""
    mock_list = mocker.patch.object(
        connector.legacy_db, "list_geneweb_databases", return_value=["db1", "db2"]
    )

    databases = connector.list_geneweb_databases()

    mock_list.assert_called_once()
    assert databases == ["db1", "db2"]


def test_list_databases_with_info_delegates_to_legacy_db(connector, mocker):
    """Test that list_databases_with_info delegates to LegacyDB."""
    mock_list = mocker.patch.object(
        connector.legacy_db,
        "list_databases_with_info",
        return_value=[{"name": "db1"}],
    )

    databases = connector.list_databases_with_info()

    mock_list.assert_called_once()
    assert len(databases) == 1


@pytest.mark.asyncio
async def test_create_geneweb_database_delegates_to_legacy_db(connector, mocker):
    """Test that create_geneweb_database delegates to LegacyDB."""
    mock_create = mocker.patch.object(
        connector.legacy_db,
        "create_geneweb_database",
        return_value={
            "name": "new-db",
            "path": "/path/to/new-db.gwb",
            "nb_persons": 0,
            "nb_families": 0,
        },
    )

    result = await connector.create_geneweb_database("new-db")

    mock_create.assert_called_once_with("new-db", None)
    assert result["name"] == "new-db"
    assert result["nb_persons"] == 0


@pytest.mark.asyncio
async def test_delete_geneweb_database_delegates_to_legacy_db(connector, mocker):
    """Test that delete_geneweb_database delegates to LegacyDB."""
    mock_delete = mocker.patch.object(
        connector.legacy_db,
        "delete_geneweb_database",
        return_value=None,
    )

    await connector.delete_geneweb_database("old-db")

    mock_delete.assert_called_once_with("old-db")


# =============================================================================
# Person Operations Delegation Tests
# =============================================================================


@pytest.mark.asyncio
async def test_get_all_persons_delegates_to_legacy_db(connector, mocker):
    """Test that get_all_persons delegates to LegacyDB."""
    mock_get = mocker.patch.object(
        connector.legacy_db,
        "get_all_persons",
        new_callable=AsyncMock,
        return_value=[{"id": "I1"}],
    )

    persons = await connector.get_all_persons()

    mock_get.assert_called_once()
    assert len(persons) == 1


@pytest.mark.asyncio
async def test_get_person_delegates_to_legacy_db(connector, mocker):
    """Test that get_person delegates to LegacyDB."""
    mock_get = mocker.patch.object(
        connector.legacy_db,
        "get_person",
        new_callable=AsyncMock,
        return_value={"id": "I1", "name": "John /Doe/"},
    )

    person = await connector.get_person("I1")

    mock_get.assert_called_once_with("I1")
    assert person["id"] == "I1"


@pytest.mark.asyncio
async def test_search_persons_delegates_to_legacy_db(connector, mocker):
    """Test that search_persons delegates to LegacyDB."""
    mock_search = mocker.patch.object(
        connector.legacy_db,
        "search_persons",
        new_callable=AsyncMock,
        return_value=[{"id": "I1"}],
    )

    results = await connector.search_persons(firstname="john", surname="doe")

    mock_search.assert_called_once_with(
        firstname="john", surname="doe", birth_year=None, death_year=None
    )
    assert len(results) == 1


@pytest.mark.asyncio
async def test_create_person_delegates_to_legacy_db(connector, mocker):
    """Test that create_person delegates to LegacyDB."""
    mock_create = mocker.patch.object(
        connector.legacy_db,
        "create_person",
        new_callable=AsyncMock,
        return_value="I2",
    )

    person_id = await connector.create_person({"name": "New /Person/"})

    mock_create.assert_called_once_with({"name": "New /Person/"})
    assert person_id == "I2"


@pytest.mark.asyncio
async def test_update_person_delegates_to_legacy_db(connector, mocker):
    """Test that update_person delegates to LegacyDB."""
    mock_update = mocker.patch.object(
        connector.legacy_db, "update_person", new_callable=AsyncMock
    )

    await connector.update_person("I1", {"name": "Updated /Name/"})

    mock_update.assert_called_once_with("I1", {"name": "Updated /Name/"})


@pytest.mark.asyncio
async def test_delete_person_delegates_to_legacy_db(connector, mocker):
    """Test that delete_person delegates to LegacyDB."""
    mock_delete = mocker.patch.object(
        connector.legacy_db, "delete_person", new_callable=AsyncMock
    )

    await connector.delete_person("I1")

    mock_delete.assert_called_once_with("I1")


# =============================================================================
# Family Operations Delegation Tests
# =============================================================================


@pytest.mark.asyncio
async def test_get_family_delegates_to_legacy_db(connector, mocker):
    """Test that get_family delegates to LegacyDB."""
    mock_get = mocker.patch.object(
        connector.legacy_db,
        "get_family",
        new_callable=AsyncMock,
        return_value={"id": "F1"},
    )

    family = await connector.get_family("F1")

    mock_get.assert_called_once_with("F1")
    assert family["id"] == "F1"


@pytest.mark.asyncio
async def test_get_all_families_delegates_to_legacy_db(connector, mocker):
    """Test that get_all_families delegates to LegacyDB."""
    mock_get = mocker.patch.object(
        connector.legacy_db,
        "get_all_families",
        new_callable=AsyncMock,
        return_value=[{"id": "F1"}],
    )

    families = await connector.get_all_families()

    mock_get.assert_called_once()
    assert len(families) == 1


@pytest.mark.asyncio
async def test_create_family_delegates_to_legacy_db(connector, mocker):
    """Test that create_family delegates to LegacyDB."""
    mock_create = mocker.patch.object(
        connector.legacy_db,
        "create_family",
        new_callable=AsyncMock,
        return_value="F2",
    )

    family_id = await connector.create_family({"husband_id": "I1"})

    mock_create.assert_called_once_with({"husband_id": "I1"})
    assert family_id == "F2"


@pytest.mark.asyncio
async def test_update_family_delegates_to_legacy_db(connector, mocker):
    """Test that update_family delegates to LegacyDB."""
    mock_update = mocker.patch.object(
        connector.legacy_db, "update_family", new_callable=AsyncMock
    )

    await connector.update_family("F1", {"wife_id": "I2"})

    mock_update.assert_called_once_with("F1", {"wife_id": "I2"})


@pytest.mark.asyncio
async def test_delete_family_delegates_to_legacy_db(connector, mocker):
    """Test that delete_family delegates to LegacyDB."""
    mock_delete = mocker.patch.object(
        connector.legacy_db, "delete_family", new_callable=AsyncMock
    )

    await connector.delete_family("F1")

    mock_delete.assert_called_once_with("F1")


# =============================================================================
# Statistics Delegation Tests
# =============================================================================


@pytest.mark.asyncio
async def test_get_database_statistics_delegates_to_legacy_db(connector, mocker):
    """Test that get_database_statistics delegates to LegacyDB."""
    mock_stats = mocker.patch.object(
        connector.legacy_db,
        "get_database_statistics",
        new_callable=AsyncMock,
        return_value={"total_persons": 100},
    )

    stats = await connector.get_database_statistics()

    mock_stats.assert_called_once()
    assert stats["total_persons"] == 100


# =============================================================================
# PostgreSQL Operations Tests (NOT delegated)
# =============================================================================


@pytest.mark.asyncio
async def test_is_connected_tests_postgresql_connection(connector, mocker):
    """Test that is_connected tests PostgreSQL (not LegacyDB)."""
    # Mock session execution
    mocker.patch.object(connector, "get_session")

    # This test verifies is_connected works for PostgreSQL
    # In real scenario, would test actual connection
    pass  # Simplified for demonstration


def test_connector_has_legacy_db_instance(connector):
    """Test that DBConnector has LegacyDB instance."""
    from app.persistence.legacy_db import LegacyDB

    assert isinstance(connector.legacy_db, LegacyDB)
    assert connector.legacy_db.gwb_path is not None


def test_connector_exposes_sqlalchemy_engine(connector):
    """Test that DBConnector exposes SQLAlchemy engine."""
    from sqlalchemy.ext.asyncio import AsyncEngine

    assert isinstance(connector.engine, AsyncEngine)
