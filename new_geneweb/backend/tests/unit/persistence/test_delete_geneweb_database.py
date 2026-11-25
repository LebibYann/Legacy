"""
Tests for delete_geneweb_database method in LegacyDB.
"""

import pytest

from app.persistence.legacy_db import LegacyDB


class TestDeleteGenewebDatabase:
    """Test delete_geneweb_database method."""

    @pytest.mark.asyncio
    async def test_delete_geneweb_database_success(self, tmp_path):
        """Test successful database deletion."""
        # Setup: Create base directory and a database
        base_dir = tmp_path / "bases"
        base_dir.mkdir()

        # Create a fake database directory
        db_path = base_dir / "test-db.gwb"
        db_path.mkdir()
        (db_path / "base").write_text("fake content")
        (db_path / "base.acc").write_text("fake content")

        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        # Create fake binaries
        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()
        gwb2ged_bin.chmod(0o755)
        ged2gwb_bin.chmod(0o755)
        gwc_bin.chmod(0o755)

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Verify database exists before deletion
        assert db_path.exists()
        assert (db_path / "base").exists()

        # Execute deletion
        await legacy_db.delete_geneweb_database("test-db")

        # Assert database is deleted
        assert not db_path.exists()

    @pytest.mark.asyncio
    async def test_delete_database_removes_gwf_and_lck_files(self, tmp_path):
        """Test deletion also removes .gwf and .lck files."""
        # Setup
        base_dir = tmp_path / "bases"
        base_dir.mkdir()

        db_name = "testdb"
        db_path = base_dir / f"{db_name}.gwb"
        db_path.mkdir()

        # Create .gwf and .lck files
        gwf_file = base_dir / f"{db_name}.gwf"
        gwf_file.write_text("wizard_passwd=")

        lck_file = base_dir / f"{db_name}.lck"
        lck_file.touch()

        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin.touch()
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.chmod(0o755)
        gwb2ged_bin.chmod(0o755)
        ged2gwb_bin.chmod(0o755)

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Verify files exist
        assert db_path.exists()
        assert gwf_file.exists()
        assert lck_file.exists()

        # Execute
        await legacy_db.delete_geneweb_database(db_name)

        # Assert all files deleted
        assert not db_path.exists()
        assert not gwf_file.exists()
        assert not lck_file.exists()

    @pytest.mark.asyncio
    async def test_delete_geneweb_database_not_found(self, tmp_path):
        """Test deletion of non-existent database raises ValueError."""
        # Setup
        base_dir = tmp_path / "bases"
        base_dir.mkdir()
        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()
        gwb2ged_bin.chmod(0o755)
        ged2gwb_bin.chmod(0o755)
        gwc_bin.chmod(0o755)

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Execute and assert
        with pytest.raises(ValueError, match="does not exist"):
            await legacy_db.delete_geneweb_database("non-existent")

    @pytest.mark.asyncio
    async def test_delete_geneweb_database_no_gwb_path(self):
        """Test deletion without gwb_path raises RuntimeError."""
        legacy_db = LegacyDB(
            gwb_path=None,
            gwb2ged_bin=None,
            ged2gwb_bin=None,
            gwc_bin=None,
        )

        with pytest.raises(RuntimeError, match="No gwb_path configured"):
            await legacy_db.delete_geneweb_database("some-db")

    @pytest.mark.asyncio
    async def test_delete_geneweb_database_with_directory_gwb_path(self, tmp_path):
        """Test deletion when gwb_path is a directory."""
        # Setup: gwb_path points to the base directory itself
        base_dir = tmp_path / "bases"
        base_dir.mkdir()

        # Create a database to delete
        db_path = base_dir / "to-delete.gwb"
        db_path.mkdir()
        (db_path / "base").write_text("content")

        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()
        gwb2ged_bin.chmod(0o755)
        ged2gwb_bin.chmod(0o755)
        gwc_bin.chmod(0o755)

        # gwb_path is a directory (like /app/geneweb/distribution/bases)
        legacy_db = LegacyDB(
            gwb_path=base_dir,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Verify exists
        assert db_path.exists()

        # Execute
        await legacy_db.delete_geneweb_database("to-delete")

        # Assert deleted
        assert not db_path.exists()
