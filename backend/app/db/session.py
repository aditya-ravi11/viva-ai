"""Async SQLAlchemy engine + session factory.

Auto-converts a standard `postgresql://` URL to the asyncpg variant so the
same DATABASE_URL works for psql, alembic offline mode, and the async app.
"""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


def _async_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


engine = create_async_engine(
    _async_url(settings.database_url),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: yield an async session, close on exit."""
    async with AsyncSessionLocal() as session:
        yield session
