"""
Tests for Post endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.helpers.test_data import get_user


@pytest.mark.asyncio
async def test_get_feed_empty(client: AsyncClient, create_test_user) -> None:
    """GET /posts/feed returns empty list if user has no circles"""
    alice_data = get_user("alice")

    await create_test_user(alice_data["username"], alice_data["password"])

    await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )

    response = await client.get("/api/v1/posts/feed")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_feed_with_posts(
    client: AsyncClient, create_test_user, create_test_circle, create_test_post
) -> None:
    alice_data = get_user("alice")

    alice = await create_test_user(alice_data["username"], alice_data["password"])
    circle = await create_test_circle("Family", owner=alice)

    await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )

    await create_test_post("family_welcome", author=alice, circle=circle)

    response = await client.get("/api/v1/posts/feed")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Welcome to Family Circle!"
