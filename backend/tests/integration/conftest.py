# backend/tests/integration/conftest.py
"""
Integration test fixtures - database and API client
Uses the development database (db)
"""

import os
from collections.abc import AsyncGenerator, Callable

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

from app.core.db import get_db
from app.core.security import get_password_hash
from app.db.models import Base, Circle, CircleMember, Post, User
from app.main import app
from app.schemas.social import CircleRole

# Import test data helpers
from tests.helpers.test_data import TEST_CIRCLES, get_circle, get_post, get_user

load_dotenv(".env.test")

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@127.0.0.1:5432/app_db")


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create async engine for integration tests"""
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional database session for integration tests"""
    async with async_engine.connect() as connection:
        transaction = await connection.begin()

        async_session_maker = async_sessionmaker(
            connection,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        session = async_session_maker()

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test client with database dependency override"""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ============================================================================
# USER FACTORIES
# ============================================================================


@pytest_asyncio.fixture
async def create_test_user(db_session: AsyncSession) -> Callable:
    """Create a user with data from TEST_USERS or custom"""

    async def _create_user(
        username: str = None, password: str = None, custom_data: dict = None
    ) -> User:
        if custom_data:
            hashed_pw = get_password_hash(custom_data["password"])
            user_data = custom_data
        elif username and password:
            user_data = get_user(username)
            hashed_pw = get_password_hash(password)
        else:
            raise ValueError("Either provide username+password or custom_data")

        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_pw,
            full_name=user_data.get("full_name", user_data["username"]),
            is_active=user_data.get("is_active", True),
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        return new_user

    return _create_user


# ============================================================================
# CIRCLE FACTORIES
# ============================================================================


@pytest_asyncio.fixture
async def create_test_circle(db_session: AsyncSession, create_test_user) -> Callable:
    """Create a circle with members from TEST_CIRCLES"""

    async def _create_circle(circle_name: str, owner: User = None) -> Circle:
        circle_data = None
        for data in TEST_CIRCLES.values():
            if data["name"] == circle_name:
                circle_data = data
                break

        if not circle_data:
            raise ValueError(f"Circle {circle_name} not found in TEST_CIRCLES")

        # Get or create owner
        if not owner:
            owner_data = get_user(circle_data["owner"])
            owner = await create_test_user(owner_data["username"])

        # Create circle
        circle = Circle(
            name=circle_data["name"],
            description=circle_data["description"],
            owner_id=owner.id,
        )
        db_session.add(circle)
        await db_session.flush()

        # Add owner as member
        owner_member = CircleMember(circle_id=circle.id, user_id=owner.id, role=CircleRole.OWNER)
        db_session.add(owner_member)

        # Add members
        for member_data in circle_data["members"]:
            member_user = await create_test_user(member_data["username"], member_data["password"])
            member = CircleMember(
                circle_id=circle.id,
                user_id=member_user.id,
                role=member_data["role"],
            )
            db_session.add(member)

        await db_session.commit()
        await db_session.refresh(circle)
        return circle

    return _create_circle


# ============================================================================
# POST FACTORIES
# ============================================================================


@pytest_asyncio.fixture
async def create_test_post(db_session: AsyncSession, create_test_circle) -> Callable:
    async def _create_post(post_title: str, author: User, circle: Circle = None) -> Post:
        post_data = get_post(post_title)

        if circle is None and post_data["circle"]:
            circle_data = get_circle(post_data["circle"])
            circle = await create_test_circle(circle_data["name"])

        post = Post(
            title=post_data["title"],
            content=post_data["content"],
            author_id=author.id,
            circle_id=circle.id if circle else None,
        )
        db_session.add(post)
        await db_session.commit()
        await db_session.refresh(post)
        return post

    return _create_post


# ============================================================================
# TEST USER FIXTURES (for common test users)
# ============================================================================


@pytest_asyncio.fixture
async def test_owner(create_test_user, client: AsyncClient, db_session: AsyncSession) -> dict:
    """Create user alice (owner) and login"""
    user_data = get_user("alice")

    user = await create_test_user(user_data["username"], user_data["password"])
    user.email = user_data["email"]
    await db_session.commit()
    await db_session.refresh(user)

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    session_token = login_data.get("session_token")
    assert session_token is not None

    return {"user": user, "session_token": session_token, "data": user_data}


@pytest_asyncio.fixture
async def test_moderator(create_test_user, client: AsyncClient, db_session: AsyncSession) -> dict:
    """Create user bob (moderator) and login"""
    user_data = get_user("bob")

    user = await create_test_user(user_data["username"], user_data["password"])
    user.email = user_data["email"]
    await db_session.commit()
    await db_session.refresh(user)

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    session_token = login_data.get("session_token")
    assert session_token is not None

    return {"user": user, "session_token": session_token, "data": user_data}


@pytest_asyncio.fixture
async def test_member(create_test_user, client: AsyncClient, db_session: AsyncSession) -> dict:
    """Create user charlie (member) and login"""
    user_data = get_user("charlie")

    user = await create_test_user(user_data["username"], user_data["password"])
    user.email = user_data["email"]
    await db_session.commit()
    await db_session.refresh(user)

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    session_token = login_data.get("session_token")
    assert session_token is not None

    return {"user": user, "session_token": session_token, "data": user_data}


# ============================================================================
# TEST CIRCLE FIXTURES (for common test circles)
# ============================================================================


@pytest_asyncio.fixture
async def test_circle(db_session: AsyncSession, test_owner: dict) -> Circle:
    """Create a simple test circle owned by alice"""
    owner = test_owner["user"]
    circle = Circle(
        name="Test Circle",
        description="Circle for integration tests",
        owner_id=owner.id,
    )
    db_session.add(circle)
    await db_session.flush()

    # Add owner as member
    db_session.add(CircleMember(circle_id=circle.id, user_id=owner.id, role=CircleRole.OWNER))

    await db_session.commit()
    await db_session.refresh(circle)
    return circle


@pytest_asyncio.fixture
async def test_family_circle(
    db_session: AsyncSession,
    test_owner: dict,
    test_moderator: dict,
    test_member: dict,
) -> Circle:
    """Create Family circle with owner, moderator, and member"""
    owner = test_owner["user"]
    moderator = test_moderator["user"]
    member = test_member["user"]

    circle = Circle(
        name="Family",
        description="Family circle for sharing memories",
        owner_id=owner.id,
    )
    db_session.add(circle)
    await db_session.flush()

    # Add owner as member
    db_session.add(CircleMember(circle_id=circle.id, user_id=owner.id, role=CircleRole.OWNER))

    # Add moderator
    db_session.add(
        CircleMember(circle_id=circle.id, user_id=moderator.id, role=CircleRole.MODERATOR)
    )

    # Add member
    db_session.add(CircleMember(circle_id=circle.id, user_id=member.id, role=CircleRole.MEMBER))

    await db_session.commit()
    await db_session.refresh(circle)
    return circle
