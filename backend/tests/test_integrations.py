

from typing import Any  # Required for fixtures that use 'yield'

import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"
API_VERSION_PATH = "/api/v1"

TEST_USER1_JSON = {
    "username": "testuser123",
    "email": "testuser123@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User 1"
    }

TEST_USER2_JSON = {
    "username": "minimaluser789",
    "email": "minimaluser789@example.com",
    "password": "MinimalPass123!"
    }

# --- FIXTURES ---

@pytest.fixture(scope="session")
def api_client() -> Any:
    """Provides a persistent client for the whole test session."""
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        # Check if server is up before running any tests
        try:
            client.get("/health")
            yield client
        except httpx.ConnectError:
            pytest.fail(f"Server not found at {BASE_URL}. Is it running?")

@pytest.fixture(scope="session")
def authenticated_client(api_client: httpx.Client) -> Any:
    """Registers user then Logs in and returns a client with session cookies."""
    api_client.post(f"{API_VERSION_PATH}/auth/register", json=TEST_USER1_JSON) # ignore if user already exists

    response = api_client.post(f"{API_VERSION_PATH}/auth/login", json=TEST_USER1_JSON)
    assert response.status_code == 200
    assert "session_token" in response.cookies
    return api_client

# --- TESTS ---

class TestHealth:
    @pytest.mark.parametrize("endpoint", ["/", "/health", f"{API_VERSION_PATH}/health"])
    def test_health_endpoints(self, api_client: httpx.Client, endpoint: str) -> None:
        """Tests all health check variations."""
        response = api_client.get(endpoint)
        assert response.status_code == 200

class TestAuthentication:
    def test_user_registration_minimal(self, api_client: httpx.Client) -> None:
        """Test registration with only username, email and password."""
        response = api_client.post(f"{API_VERSION_PATH}/auth/register", json=TEST_USER2_JSON)
        assert response.status_code in [201, 400] # Allow 201 (Created) or 400 (Already exists)

    def test_login_wrong_password(self, api_client: httpx.Client) -> None:
        """Ensure 401 is returned for bad credentials."""
        bad_data = TEST_USER1_JSON.copy()
        bad_data["password"] = "WrongPassword!"
        response = api_client.post(f"{API_VERSION_PATH}/auth/login", json=bad_data)
        assert response.status_code == 401

    def test_logout_flow(self, authenticated_client: httpx.Client) -> None:
        """Tests the logout endpoint using an authenticated session."""
        response = authenticated_client.post(f"{API_VERSION_PATH}/auth/logout")
        assert response.status_code == 200
        assert response.json().get("success") is True

class TestErrorHandling:
    def test_duplicate_registration(self, api_client: httpx.Client) -> None:
        """Registration should fail if email is taken."""
        response = api_client.post(f"{API_VERSION_PATH}/auth/register", json=TEST_USER1_JSON)
        assert response.status_code == 400
