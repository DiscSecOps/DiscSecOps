# backend/tests/integration/test_auth.py
"""
Comprehensive tests for async authentication endpoints
Tests username-based login, registration, and sessions
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.models import User
from tests.helpers.test_data import get_user

# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_health_check_root(client: AsyncClient) -> None:
    """Test root health endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check_health(client: AsyncClient) -> None:
    """Test /health endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_check_api(client: AsyncClient) -> None:
    """Test /api/health endpoint"""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# ============================================================================
# REGISTRATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient) -> None:
    """Test successful user registration"""
    user = get_user("test")
    user_data = {
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
        "full_name": "Test User",
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert data["username"] == user["username"]
    assert "user" in data
    assert data["user"]["username"] == user["username"]
    assert data["user"]["email"] == user["email"]


@pytest.mark.asyncio
async def test_register_minimal_data(client: AsyncClient) -> None:
    """Test registration with only username and password"""
    user = get_user("test")
    user_data = {
        "username": f"{user['username']}_minimal",
        "password": user["password"],
        "email": f"{user['username']}_minimal@example.com",
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert data["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient) -> None:
    """Test that duplicate username registration fails"""
    user = get_user("test")
    user_data = {
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
    }

    # First registration should succeed
    response1 = await client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 201

    # Second registration with same username should fail
    response2 = await client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "Username already taken" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Test that duplicate email registration fails"""
    user = get_user("test")
    user_data = {
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
    }

    # First registration should succeed
    response1 = await client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 201

    # Second registration with same email should fail
    user_data2 = {
        "username": f"{user['username']}_2",
        "password": user["password"],
        "email": user["email"],
    }
    response2 = await client.post("/api/v1/auth/register", json=user_data2)
    assert response2.status_code == 400
    assert "Email already taken" in response2.json()["detail"]


# ============================================================================
# LOGIN TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Test successful login returns session token"""
    user = get_user("test")

    # Register user first
    register_data = {
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
    }
    await client.post("/api/v1/auth/register", json=register_data)

    # Login with username
    login_data = {"username": user["username"], "password": user["password"]}
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["username"] == user["username"]
    assert "session_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    """Test login with incorrect password"""
    user = get_user("test")

    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": user["username"],
            "password": user["password"],
            "email": user["email"],
        },
    )

    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login", json={"username": user["username"], "password": "WrongPass123!"}
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient) -> None:
    """Test login with non-existent username"""
    response = await client.post(
        "/api/v1/auth/login", json={"username": "nonexistent", "password": "SomePass123!"}
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test that inactive users cannot login"""
    user = get_user("test")

    # Create inactive user directly in database
    inactive_user = User(
        username="inactive",
        email="inactive@example.com",
        hashed_password=get_password_hash(user["password"]),
        is_active=False,
    )
    db_session.add(inactive_user)
    await db_session.commit()

    # Try to login
    response = await client.post(
        "/api/v1/auth/login", json={"username": "inactive", "password": user["password"]}
    )

    assert response.status_code == 403
    assert "inactive" in response.json()["detail"].lower()


# ============================================================================
# LOGOUT TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient) -> None:
    """Test logout endpoint"""
    user = get_user("test")

    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": user["username"],
            "password": user["password"],
            "email": user["email"],
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login", json={"username": user["username"], "password": user["password"]}
    )
    session_token = login_response.json().get("session_token")
    assert session_token is not None

    # Logout
    response = await client.post("/api/v1/auth/logout", cookies={"session_token": session_token})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "logged out" in data["message"].lower()


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_username_case_sensitivity(client: AsyncClient) -> None:
    """Test username case sensitivity"""
    user = get_user("test")

    # Register user with uppercase first letter
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "CaseSensitive",
            "password": user["password"],
            "email": "case@example.com",
        },
    )

    # Try to login with different case
    response = await client.post(
        "/api/v1/auth/login", json={"username": "casesensitive", "password": user["password"]}
    )

    # Should fail as backend is case-sensitive
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient) -> None:
    """Test complete authentication flow: register -> login -> logout"""
    user = get_user("test")
    username = user["username"]
    password = user["password"]

    # 1. Register
    register_response = await client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": password, "email": user["email"]},
    )
    assert register_response.status_code == 201

    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login", json={"username": username, "password": password}
    )
    assert login_response.status_code == 200
    assert login_response.json()["success"] is True

    # 3. Logout
    session_token = login_response.json().get("session_token")
    logout_response = await client.post(
        "/api/v1/auth/logout", cookies={"session_token": session_token}
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["success"] is True
