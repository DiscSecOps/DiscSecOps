# backend/tests/conftest.py
"""
Shared fixtures for both API and E2E tests,
including async database setup and a test client for FastAPI.
"""
import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import nest_asyncio
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
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

# Patch asyncio to allow nested event loops (Fixes Playwright sync + Async DB conflicts)
nest_asyncio.apply()

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
    Forces pytest to use a single async event loop for the whole test session,
    while respecting Playwright's existing loop if it's already running.
    """
    try:
        # Try to grab Playwright's running loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # If no loop is running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # EXPLICITLY patch THIS specific loop so it allows nesting
    nest_asyncio.apply(loop)

    yield loop

    # Note: We purposely DO NOT close the loop here anymore (loop.close()).
    # If Playwright started the loop, closing it will crash the browser teardown!

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

    try:
        yield session  # This is where the test runs
    finally:
        # Test is over. Safely close session and rollback, even if the test crashed!
        try:
            await session.close()
            await transaction.rollback()
        except Exception as teardown_err:
            print(f"Failed to cleanly rollback DB: {teardown_err}")

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

@pytest.fixture
def create_test_user():
    """
    Bulletproof Synchronous Factory.
    No teardown needed because `clean_database_before_test` handles it!
    """
    def _create_user(username: str, plain_password: str):
        async def _insert():
            engine = create_async_engine(TEST_DATABASE_URL)
            async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

            async with async_session_maker() as session:
                hashed_pw = get_password_hash(plain_password)
                new_user = User(
                    username=username,
                    email=f"{username.lower()}@example.com",
                    hashed_password=hashed_pw
                )
                session.add(new_user)
                await session.commit()
            await engine.dispose()

        asyncio.run(_insert())

    # We just yield the function. No try/finally block needed anymore!
    yield _create_user

@pytest.fixture(scope="session", autouse=True)
def setup_test_database_schema():
    """
    Runs once per test session.
    Guarantees that all tables exist in the test database before any tests run.
    """
    async def _init_db():
        engine = create_async_engine(TEST_DATABASE_URL)
        async with engine.begin() as conn:
            # Tell SQLAlchemy to look at your models and generate the CREATE TABLE statements
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    # We use our bulletproof synchronous wrapper so it doesn't fight Playwright!
    asyncio.run(_init_db())

@pytest.fixture(autouse=True)
def clean_database_before_test():
    """
    Automatically wipes all database tables before every test.
    Using 'autouse=True' means no test can ever inherit dirty data.
    """
    async def _truncate():
        # Create a short-lived engine just for this operation
        engine = create_async_engine(TEST_DATABASE_URL)

        async with engine.begin() as conn:
            # Dynamically grab every table name defined in your SQLAlchemy models
            tables = [table.name for table in Base.metadata.sorted_tables]

            if tables:
                table_string = ", ".join(tables)
                # RESTART IDENTITY: Resets the ID counters back to 1
                # CASCADE: Safely handles foreign key dependencies
                await conn.execute(text(f"TRUNCATE TABLE {table_string} RESTART IDENTITY CASCADE;"))

        await engine.dispose()

    # Run the async cleanup synchronously to protect the Playwright thread
    asyncio.run(_truncate())

    yield # The actual Playwright test runs here!

# ==========================================
# PYTEST MAGIC HOOK
# ==========================================
def pytest_collection_modifyitems(config, items):
    """
    This hook runs after Pytest reads the feature file but before the tests execute.
    It looks for any scenario tagged with @bug and safely marks it as an Expected Failure.
    """
    for item in items:
        # 'item.keywords' contains all the Gherkin tags!
        if "todo" in item.keywords:
            item.add_marker(
                pytest.mark.xfail(reason="Known backend todo: Implementation pending")
            )
