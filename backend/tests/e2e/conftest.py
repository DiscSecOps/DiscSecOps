# backend/tests/e2e/conftest.py
"""
E2E test fixtures - Playwright, test database setup, and test data factories
Uses the test database (test_db)
"""

import asyncio
import os
from collections.abc import Generator

import nest_asyncio
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.security import get_password_hash
from app.db.models import Base, Circle, CircleMember, Post, User

# Load test environment variables
load_dotenv(".env.test", override=True)


# E2E tests use the test database
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://user:password@test_db:5432/test_db"
)

# Patch asyncio to allow nested event loops (Fixes Playwright sync + Async DB conflicts)
nest_asyncio.apply()


# ==========================================
# 1. PLAYWRIGHT CONFIGURATION
# ==========================================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configure Playwright with base URL"""
    return {
        **browser_context_args,
        "base_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Single async event loop for the whole test session"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    nest_asyncio.apply(loop)
    yield loop


# ==========================================
# 1a. PLAYWRIGHT PAGE FIXTURE (optional headless / slowmo)
# ==========================================


@pytest.fixture(scope="function")
def page():
    """Provides a Playwright page with optional headless/slowmo settings."""
    headless = os.getenv("HEADLESS", "1") == "1"
    slow_mo = int(os.getenv("SLOW_MO_MS", "0"))

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless, slow_mo=slow_mo)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        yield page
        browser.close()


# ==========================================
# 2. DATABASE SETUP (for test_db)
# ==========================================
@pytest.fixture(scope="session", autouse=True)
def setup_test_database_schema():
    """Create all tables before E2E tests run"""
    print("\n" + "=" * 50)
    print("🔥🔥🔥 CREATING TABLES IN test_db 🔥🔥🔥")
    print("=" * 50)

    async def _init_db():
        engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
        print(f"Connected to: {TEST_DATABASE_URL}")
        async with engine.begin() as conn:
            print("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully!")
        await engine.dispose()

    asyncio.run(_init_db())


@pytest.fixture(autouse=True)
def clean_database_before_e2e_test(request):
    """Wipe database before each E2E test"""
    if "e2e" not in str(request.node.path):
        yield
        return

    async def _truncate():
        engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
        async with engine.begin() as conn:
            tables = [table.name for table in Base.metadata.sorted_tables]
            if tables:
                table_string = ", ".join(tables)
                await conn.execute(text(f"TRUNCATE TABLE {table_string} RESTART IDENTITY CASCADE;"))
        await engine.dispose()

    asyncio.run(_truncate())
    yield


# ==========================================
# 3. TEST DATA FACTORIES (for E2E)
# ==========================================

# ==========================================
# 3a. USER FACTORY
# ==========================================
@pytest.fixture
def create_test_user_synchronous():
    """Synchronous factory to create a test user (for E2E)"""

    def _create_user(username: str, plain_password: str, full_name: str):
        async def _insert():
            engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
            async_session_maker = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )

            async with async_session_maker() as session:
                hashed_pw = get_password_hash(plain_password)
                email = replace_variables("<TEST_EMAIL>")
                new_user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    hashed_password=hashed_pw,
                )
                session.add(new_user)
                await session.commit()
            await engine.dispose()

        asyncio.run(_insert())

    yield _create_user


# ==========================================
# 4. CIRCLE & POST FACTORIES
# ==========================================
@pytest.fixture
def setup_user_circles_synchronous():
    """Seed database with circles and assign roles"""

    def _setup(username: str, circles_data: list[dict]):
        async def _insert():
            engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
            async_session_maker = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )

            async with async_session_maker() as session:
                user_res = await session.execute(select(User).where(User.username == username))
                user = user_res.scalar_one()

                admin_res = await session.execute(
                    select(User).where(User.username == "circle_admin")
                )
                admin = admin_res.scalar_one_or_none()
                if not admin:
                    admin = User(
                        username="circle_admin", email="admin@system.com", hashed_password="xxx"
                    )
                    session.add(admin)
                    await session.flush()

                for row in circles_data:
                    role = row["role"].lower()
                    circle_owner_id = user.id if role == "owner" else admin.id

                    circle = Circle(
                        name=row["circle_name"],
                        description=f"Automated test circle for {row['circle_name']}",
                        owner_id=circle_owner_id,
                    )
                    session.add(circle)
                    await session.flush()

                    member = CircleMember(circle_id=circle.id, user_id=user.id, role=role)
                    session.add(member)

                await session.commit()
            await engine.dispose()

        asyncio.run(_insert())

    yield _setup


# ==========================================
# 5. POST FACTORY
# ==========================================
@pytest.fixture
def create_circle_post_synchronous():
    """Create a post inside a specific circle"""

    def _create_post(circle_name: str, author_username: str, title: str, content: str):
        async def _insert():
            engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
            async_session_maker = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )

            async with async_session_maker() as session:
                user = (
                    await session.execute(select(User).where(User.username == author_username))
                ).scalar_one()
                circle = (
                    await session.execute(select(Circle).where(Circle.name == circle_name))
                ).scalar_one()

                post = Post(title=title, content=content, author_id=user.id, circle_id=circle.id)
                session.add(post)
                await session.commit()
            await engine.dispose()

        asyncio.run(_insert())

    yield _create_post


# ==========================================
# 6. PYTEST MAGIC HOOK
# ==========================================
def pytest_collection_modifyitems(config, items):
    """Mark @todo and @bug scenarios as expected failures"""
    for item in items:
        if "todo" in item.keywords:
            item.add_marker(pytest.mark.xfail(reason="Known todo: Implementation pending"))
        if "bug" in item.keywords:
            item.add_marker(pytest.mark.xfail(reason="Known bug: Fix pending"))


# ==========================================
# 6. PLACEHOLDER REPLACEMENT UTILITY
# ==========================================
def replace_variables(text: str) -> str:
    """Replace placeholders like <VAR> with environment variables."""
    if text.startswith("<") and text.endswith(">"):
        var_name = text[1:-1]
        return os.getenv(var_name, text)
    return text
