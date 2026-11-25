"""
Test for create_geneweb_database method.
"""

from unittest.mock import Mock, patch

import pytest

from app.persistence.legacy_db import LegacyDB


class TestCreateGenewebDatabase:
    """Test create_geneweb_database method."""

    @pytest.mark.asyncio
    async def test_create_geneweb_database_success(self, tmp_path):
        """Test successful database creation."""
        # Setup
        base_dir = tmp_path / "bases"
        base_dir.mkdir()
        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        # Create fake binaries
        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()
        gwc_bin.chmod(0o755)

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Mock subprocess.run to avoid calling real gwc
        # We need to simulate gwc creating the .gwb directory
        def fake_gwc_run(*args, **kwargs):
            # Create the .gwb directory that gwc would create
            new_db_path = base_dir / "new_db.gwb"
            new_db_path.mkdir(exist_ok=True)
            return Mock(returncode=0, stdout="", stderr="")

        with patch("subprocess.run", side_effect=fake_gwc_run) as mock_run:
            # Execute
            result = await legacy_db.create_geneweb_database("new_db")

            # Assert
            assert result["name"] == "new_db"
            assert "path" in result
            assert result["nb_persons"] == 0
            assert result["nb_families"] == 0
            assert "created" in result

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            assert str(call_args[0]).endswith("gwc")
            assert "-o" in call_args

    @pytest.mark.asyncio
    async def test_create_geneweb_database_already_exists(self, tmp_path):
        """Test error when database already exists."""
        # Setup
        base_dir = tmp_path / "bases"
        base_dir.mkdir()
        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        # Create the target database file
        existing_db = base_dir / "new_db.gwb"
        existing_db.touch()

        # Create fake binaries
        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Execute & Assert
        with pytest.raises(ValueError, match="already exists"):
            await legacy_db.create_geneweb_database("new_db")

    @pytest.mark.asyncio
    async def test_create_geneweb_database_no_gwb_path(self):
        """Test error when no gwb_path configured."""
        legacy_db = LegacyDB(
            gwb_path=None,
            gwb2ged_bin="/usr/bin/gwb2ged",
            ged2gwb_bin="/usr/bin/ged2gwb",
            gwc_bin="/usr/bin/gwc",
        )

        with pytest.raises(RuntimeError, match="No gwb_path configured"):
            await legacy_db.create_geneweb_database("new_db")

    @pytest.mark.asyncio
    async def test_create_geneweb_database_subprocess_fails(self, tmp_path):
        """Test error handling when gwc fails."""
        # Setup
        base_dir = tmp_path / "bases"
        base_dir.mkdir()
        gwb_path = base_dir / "existing.gwb"
        gwb_path.touch()

        # Create fake binaries
        gwb2ged_bin = tmp_path / "gwb2ged"
        ged2gwb_bin = tmp_path / "ged2gwb"
        gwc_bin = tmp_path / "gwc"
        gwb2ged_bin.touch()
        ged2gwb_bin.touch()
        gwc_bin.touch()
        gwc_bin.chmod(0o755)

        legacy_db = LegacyDB(
            gwb_path=gwb_path,
            gwb2ged_bin=gwb2ged_bin,
            ged2gwb_bin=ged2gwb_bin,
            gwc_bin=gwc_bin,
        )

        # Mock subprocess.run to simulate failure
        import subprocess

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "gwc", stderr="Failed to create database"
            )

            # Execute & Assert
            with pytest.raises(RuntimeError, match="Failed to create database"):
                await legacy_db.create_geneweb_database("new_db")
