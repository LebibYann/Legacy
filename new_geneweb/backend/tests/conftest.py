from __future__ import annotations

from collections.abc import AsyncIterator
import os

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def test_db_engine() -> AsyncIterator[AsyncEngine]:
    """Provide a test database engine."""
    # Use a test database URL, defaulting to a local test DB
    test_db_url = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/geneweb_test",
    )

    engine = create_async_engine(test_db_url, echo=False)
    yield engine
    await engine.dispose()
