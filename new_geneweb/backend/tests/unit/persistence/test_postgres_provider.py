"""
Unit tests for PostgresProvider (skeleton only).

Full implementation will be added in Phase 2/3.
"""

import pytest

from app.persistence.postgres_provider import PostgresProvider


class TestPostgresProviderSkeleton:
    """Test that PostgresProvider skeleton is importable and follows interface."""

    def test_postgres_provider_can_be_instantiated(self):
        """Test that PostgresProvider can be instantiated."""
        provider = PostgresProvider(session_factory=None)
        assert provider is not None
        assert provider.session_factory is None

    def test_postgres_provider_raises_not_implemented(self):
        """Test that all methods raise NotImplementedError."""
        provider = PostgresProvider(session_factory=None)

        # Database management
        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            provider.list_geneweb_databases()

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            provider.get_database_info("test")

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            provider.list_databases_with_info()

    @pytest.mark.asyncio
    async def test_postgres_provider_person_methods_raise(self):
        """Test that person methods raise NotImplementedError."""
        provider = PostgresProvider(session_factory=None)

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.get_all_persons()

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.get_person("p123")

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.search_persons("Dupont")

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.create_person({"name": "Test"})

    @pytest.mark.asyncio
    async def test_postgres_provider_family_methods_raise(self):
        """Test that family methods raise NotImplementedError."""
        provider = PostgresProvider(session_factory=None)

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.get_family("f123")

        with pytest.raises(NotImplementedError, match="Phase 2/3 not yet implemented"):
            await provider.create_family({"husband_id": "p1"})

    @pytest.mark.asyncio
    async def test_postgres_provider_cache_methods_no_op(self):
        """Test that cache methods are no-ops."""
        provider = PostgresProvider(session_factory=None)

        # These should not raise
        await provider.invalidate_cache()
        stats = provider.get_cache_stats()
        assert stats.hit_count == 0
        assert stats.miss_count == 0
        assert stats.persons_count == 0
        assert stats.families_count == 0
        await provider.start_background_refresh()
        await provider.stop_background_refresh()
