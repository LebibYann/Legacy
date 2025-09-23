from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import settings

# Creation of an async engine
engine: AsyncEngine = create_async_engine(settings.database_url, future=True, echo=False)

# Session factory
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that opens a DB session per request"""
    async with SessionLocal() as session:
        yield session


# Practical alias for injection
DbSession = Annotated[AsyncSession, Depends(get_session)]
