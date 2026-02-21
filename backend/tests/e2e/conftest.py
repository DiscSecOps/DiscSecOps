import os

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Import your FastAPI app's Base and Models (adjust paths to match your project)
# from my_app.database import Base
# from my_app.models import User
# from my_app.core.security import get_password_hash

# ==========================================
# 1. PLAYWRIGHT CONFIGURATION
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
# 2. ASYNC DATABASE CONFIGURATION
# ==========================================

# Point this to your local Docker Postgres container
# Note the '+asyncpg' which is required for async SQLAlchemy
DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)

@pytest.fixture(scope="session")
def event_loop():
    """
    Forces pytest to use a single async event loop for the whole test session.
    This is required so our DB engine doesn't close prematurely.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def async_engine():
    """Creates the SQLAlchemy async engine once per test run."""
    engine = create_async_engine(DATABASE_URL, echo=False)

    # Optional: If you need pytest to build your tables on startup:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(async_engine):
    """
    The Magic Fixture: Gives each test a clean database transaction,
    then ROLLS IT BACK when the test finishes. No cleanup needed!
    """
    async with async_engine.connect() as connection:
        transaction = await connection.begin()

        async_session_maker = sessionmaker(
            connection, class_=AsyncSession, expire_on_commit=False
        )
        session = async_session_maker()

        yield session  # This is where the test runs

        # Test is over. Close session and rollback everything.
        await session.close()
        await transaction.rollback()

# ==========================================
# 3. HELPER FIXTURES (Data Injection)
# ==========================================

@pytest_asyncio.fixture
async def create_test_user(db_session):
    """
    A factory fixture to instantly teleport a user into Postgres
    before Playwright tries to log them in.
    """
    async def _create_user(username: str, plain_password: str, role: str = "User"):
        # hashed_pw = get_password_hash(plain_password)
        # new_user = User(
        #     username=username,
        #     hashed_password=hashed_pw,
        #     global_role=role
        # )
        # db_session.add(new_user)
        # await db_session.commit()
        # await db_session.refresh(new_user)
        # return new_user
        pass # Replace with actual SQLAlchemy model logic above

    return _create_user
