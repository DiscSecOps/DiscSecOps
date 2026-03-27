# backend/tests/integration/test_users.py
"""
Tests for searching users to add to circles.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circle, CircleMember
from app.schemas.social import CircleRole
from tests.helpers.test_data import get_user


@pytest.mark.asyncio
async def test_search_users_by_username(
    client: AsyncClient, create_test_user, db_session: AsyncSession
) -> None:
    # 1. Create test users
    alice_data = get_user("alice")
    charlie_data = get_user("charlie")

    alice = await create_test_user(alice_data["username"], alice_data["password"])
    await create_test_user(get_user("bob")["username"], get_user("bob")["password"])
    await create_test_user(charlie_data["username"], charlie_data["password"])

    # 2. Create a circle owned by alice
    circle = Circle(name="Family", description="Test", owner_id=alice.id)
    db_session.add(circle)
    await db_session.flush()

    # 3. Add alice as owner
    db_session.add(CircleMember(circle_id=circle.id, user_id=alice.id, role=CircleRole.OWNER))
    await db_session.commit()

    # 4. Login as alice to get session token
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )
    session_token = login_response.json()["session_token"]

    # 5. Set cookie on client (this is the recommended way)
    client.cookies.set("session_token", session_token)

    # 6. Search for users with "char" in their username
    response = await client.get(
        f"/api/v1/users/search?query=char&circle_id={circle.id}",
    )

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["username"] == charlie_data["username"]


@pytest.mark.asyncio
async def test_search_users_empty_query(
    client: AsyncClient, create_test_user, db_session: AsyncSession
) -> None:
    """Test search with empty query returns empty list"""
    alice_data = get_user("alice")

    alice = await create_test_user(alice_data["username"], alice_data["password"])

    circle = Circle(name="Family", description="Test", owner_id=alice.id)
    db_session.add(circle)
    await db_session.flush()

    db_session.add(CircleMember(circle_id=circle.id, user_id=alice.id, role=CircleRole.OWNER))
    await db_session.commit()

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )
    session_token = login_response.json()["session_token"]
    client.cookies.set("session_token", session_token)

    response = await client.get(
        f"/api/v1/users/search?query=&circle_id={circle.id}",
    )

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0


@pytest.mark.asyncio
async def test_search_users_no_results(
    client: AsyncClient, create_test_user, db_session: AsyncSession
) -> None:
    """Test search with query that has no matches returns empty list"""
    alice_data = get_user("alice")

    alice = await create_test_user(alice_data["username"], alice_data["password"])

    circle = Circle(name="Family", description="Test", owner_id=alice.id)
    db_session.add(circle)
    await db_session.flush()

    db_session.add(CircleMember(circle_id=circle.id, user_id=alice.id, role=CircleRole.OWNER))
    await db_session.commit()

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )
    session_token = login_response.json()["session_token"]
    client.cookies.set("session_token", session_token)

    response = await client.get(
        f"/api/v1/users/search?query=nonexistent&circle_id={circle.id}",
    )

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient, create_test_user) -> None:
    """Test getting all users (paginated)"""
    alice_data = get_user("alice")
    bob_data = get_user("bob")
    charlie_data = get_user("charlie")

    # Create users (bob and charlie are created for the test)
    await create_test_user(alice_data["username"], alice_data["password"])
    await create_test_user(bob_data["username"], bob_data["password"])
    await create_test_user(charlie_data["username"], charlie_data["password"])

    # Login as alice
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )
    session_token = login_response.json()["session_token"]
    client.cookies.set("session_token", session_token)

    # Get all users (should exclude current user)
    response = await client.get("/api/v1/users/")

    assert response.status_code == 200
    results = response.json()
    # Should return bob and charlie (2 users), excluding alice
    assert len(results) == 2
    usernames = [u["username"] for u in results]
    assert bob_data["username"] in usernames
    assert charlie_data["username"] in usernames
