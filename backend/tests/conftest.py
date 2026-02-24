
import asyncio
import os
from collections.abc import AsyncGenerator, Callable, Coroutine, Generator
from typing import Any

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

# Import your app components
from app.core.db import get_db
from app.core.security import get_password_hash
from app.db.models import Base, User
from app.main import app

load_dotenv()


# Point to the new Docker test_db (Port 5434)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://user:password@test_db:5432/test_db"
)

# ==========================================
# 1. PLAYWRIGHT CONFIGURATION (For E2E Tests)
# ==========================================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Configures Playwright.
    Setting the base_url means your step definitions can just use:
    page.goto("/login") instead of page.goto("http://localhost:3000/login")
    """
    return {
        **browser_context_args,
        "base_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "viewport": {"width": 1280, "height": 720},
    }

# ==========================================
# 2.ASYNC DATABASE CONFIGURATION (Shared by API & E2E)
# ==========================================
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Forces pytest to use a single async event loop for the whole test session.
    This is required so our DB engine doesn't close prematurely.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def async_engine()-> AsyncGenerator[AsyncEngine, None]:
    """Creates the SQLAlchemy async engine once per test run."""
    # NullPool is great for tests to prevent connection state issues
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

    # Create tables once per test session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a transactional database session for a test,
    then ROLLS IT BACK when the test finishes. No cleanup needed!
    """
    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        async_session_maker = async_sessionmaker(
            connection, class_=AsyncSession, expire_on_commit=False
        )
        session = async_session_maker()

        yield session  # This is where the test runs

        # Test is over. Close session and rollback everything.
        await session.close()
        await transaction.rollback()

# ==========================================
# 3. FASTAPI TEST CLIENT (For API Tests)
# ==========================================
@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test client with overridden database dependency."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def create_test_user(
    db_session: AsyncSession
) -> AsyncGenerator[Callable[[str, str, str], Coroutine[Any, Any, User]], None]:
    """
    Async factory to create a user.
    The nested function must be awaited in your step definitions.
    """
    async def _create_user(username: str, plain_password: str, role: str = "User") -> User:
        hashed_pw = get_password_hash(plain_password)
        new_user = User(
            username=username,
            hashed_password=hashed_pw,
            global_role=role
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        return new_user

    yield _create_user
