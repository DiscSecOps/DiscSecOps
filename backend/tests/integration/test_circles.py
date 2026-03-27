"""
Tests for Circle endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.helpers.test_data import get_user


@pytest.mark.asyncio
async def test_get_my_circles_empty(client: AsyncClient, create_test_user) -> None:
    """GET /circles/my returns empty list if user has no circles"""
    alice_data = get_user("alice")

    # Login as alice
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"username": alice_data["username"], "password": alice_data["password"]},
    )
    session_token = login_response.json()["session_token"]
    client.cookies.set("session_token", session_token)

    response = await client.get("/api/v1/circles/my")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_my_circles_with_circle(client: AsyncClient, test_owner, test_circle) -> None:
    """GET /circles/my returns circle where user is a member"""
    # Set cookie from test_owner
    client.cookies.set("session_token", test_owner["session_token"])

    response = await client.get("/api/v1/circles/my")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Test Circle"
    assert results[0]["member_count"] == 1
    assert results[0]["owner_name"] == test_owner["data"]["username"]


@pytest.mark.asyncio
async def test_create_circle(client: AsyncClient, test_owner) -> None:
    """POST /circles/ creates a new circle"""
    client.cookies.set("session_token", test_owner["session_token"])

    circle_data = {"name": "My New Circle", "description": "This is a test circle"}

    response = await client.post("/api/v1/circles/", json=circle_data)

    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "My New Circle"
    assert result["description"] == "This is a test circle"
    assert result["owner_id"] == test_owner["user"].id
    assert result["member_count"] == 1
    assert result["owner_name"] == test_owner["data"]["username"]


@pytest.mark.asyncio
async def test_create_circle_duplicate_name(client: AsyncClient, test_owner) -> None:
    """POST /circles/ returns 400 if circle name already exists"""
    client.cookies.set("session_token", test_owner["session_token"])

    circle_data = {"name": "Duplicate Circle", "description": "First circle"}

    # Create first circle
    response1 = await client.post("/api/v1/circles/", json=circle_data)
    assert response1.status_code == 201

    # Try to create second with same name
    response2 = await client.post("/api/v1/circles/", json=circle_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]
