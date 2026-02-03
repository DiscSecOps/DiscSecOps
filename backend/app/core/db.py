from collections.abc import AsyncGenerator

from backend.app.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Create an asynchronous engine to connect to the PostgreSQL database
# The DATABASE_URL is loaded from settings, which defaults to the local dev container DB
# or can be overridden by an environment variable (e.g., for Neon).
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a sessionmaker for asynchronous sessions
# expire_on_commit=False prevents objects from being expired after commit,
# which can be useful for accessing attributes outside of the session.
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an asynchronous database session.

    Yields an AsyncSession object that can be used for database operations.
    The session is automatically closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        yield session
