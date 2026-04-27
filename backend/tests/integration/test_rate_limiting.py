"""
Integration tests for rate limiting on authentication endpoints.

Uses the real FastAPI app (via ASGITransport) and resets the in-memory
limiter storage before every test so counters are always at zero.

Tests exercise the real 5/minute limits configured on /register and /login.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401 - used in fixture signatures

from app.core.limiter import limiter


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_limiter_storage():
    """
    Reset the in-memory rate limit counters before every test in this module.
    This ensures no counter state leaks between tests.
    """
    limiter._storage.reset()
    yield
    limiter._storage.reset()  # clean up after too, for safety


# ---------------------------------------------------------------------------
# Shared test data helpers
# ---------------------------------------------------------------------------

def _register_payload(suffix: str) -> dict:
    return {
        "username": f"ratelimit_{suffix}",
        "email": f"ratelimit_{suffix}@test.com",
        "password": "SecurePass123!",
        "full_name": "Rate Limit Tester",
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRegisterRateLimiting:
    """Rate limiting integration tests for POST /api/v1/auth/register"""

    @pytest.mark.asyncio
    async def test_register_first_request_not_rate_limited(
        self, client: AsyncClient
    ) -> None:
        """First request to /register is never rate-limited."""
        response = await client.post(
            "/api/v1/auth/register", json=_register_payload("first")
        )
        # 201 = created, 400 = validation/duplicate — either way NOT 429
        assert response.status_code in (201, 400, 422)

    @pytest.mark.asyncio
    async def test_register_rate_limited_after_threshold(
        self, client: AsyncClient
    ) -> None:
        """Exceeding the 5/minute limit on /register returns 429."""
        # Exhaust the limit (5 requests)
        for i in range(5):
            await client.post(
                "/api/v1/auth/register",
                json=_register_payload(f"exhaust_{i}"),
            )

        # 6th request must be rate-limited
        response = await client.post(
            "/api/v1/auth/register", json=_register_payload("overflow")
        )
        assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_register_429_returns_json_body(
        self, client: AsyncClient
    ) -> None:
        """A rate-limited /register response has a JSON body with an 'error' field."""
        for i in range(5):
            await client.post("/api/v1/auth/register", json=_register_payload(f"json_{i}"))

        response = await client.post(
            "/api/v1/auth/register", json=_register_payload("json_over")
        )
        assert response.status_code == 429
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_register_exactly_at_limit_still_succeeds(
        self, client: AsyncClient
    ) -> None:
        """The 5th request (exactly at the limit) must NOT be rate-limited."""
        for i in range(4):
            await client.post("/api/v1/auth/register", json=_register_payload(f"boundary_{i}"))

        # 5th request — exactly at the limit
        response = await client.post(
            "/api/v1/auth/register", json=_register_payload("boundary_4")
        )
        assert response.status_code in (201, 400, 422)  # NOT 429

    @pytest.mark.asyncio
    async def test_register_reset_storage_clears_counters(
        self, client: AsyncClient
    ) -> None:
        """After manually resetting storage, the first request succeeds again."""
        for i in range(5):
            await client.post("/api/v1/auth/register", json=_register_payload(f"rst_{i}"))

        blocked = await client.post(
            "/api/v1/auth/register", json=_register_payload("rst_over")
        )
        assert blocked.status_code == 429

        # Reset — counters are now zero
        limiter._storage.reset()

        response = await client.post(
            "/api/v1/auth/register", json=_register_payload("rst_after")
        )
        assert response.status_code in (201, 400, 422)  # NOT 429


class TestLoginRateLimiting:
    """Rate limiting integration tests for POST /api/v1/auth/login"""

    @pytest.mark.asyncio
    async def test_login_first_request_not_rate_limited(
        self, client: AsyncClient
    ) -> None:
        """First login attempt is never rate-limited (200 or 401, never 429)."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "Pass123!"},
        )
        assert response.status_code in (200, 401, 403)

    @pytest.mark.asyncio
    async def test_login_rate_limited_after_threshold(
        self, client: AsyncClient, create_test_user
    ) -> None:
        """Exceeding the 5/minute limit on /login returns 429."""
        await create_test_user("rl_login_user", "SecurePass123!")

        # Exhaust the limit with wrong-password attempts
        for _ in range(5):
            await client.post(
                "/api/v1/auth/login",
                json={"username": "rl_login_user", "password": "WrongPass!"},
            )

        # 6th attempt must be blocked
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "rl_login_user", "password": "SecurePass123!"},
        )
        assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_login_429_returns_json_body(
        self, client: AsyncClient
    ) -> None:
        """A rate-limited /login response has a JSON body with an 'error' field."""
        for _ in range(5):
            await client.post(
                "/api/v1/auth/login",
                json={"username": "nouser", "password": "WrongPass!"},
            )
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "nouser", "password": "WrongPass!"},
        )
        assert response.status_code == 429
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_successful_login_within_limit(
        self, client: AsyncClient, create_test_user
    ) -> None:
        """A valid login on the first attempt returns 200 with a session token."""
        await create_test_user("rl_login_success", "SecurePass123!")

        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "rl_login_success", "password": "SecurePass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_token" in data

    @pytest.mark.asyncio
    async def test_login_exactly_at_limit_still_processed(
        self, client: AsyncClient, create_test_user
    ) -> None:
        """The 5th login attempt is still processed (not yet blocked)."""
        await create_test_user("rl_login_boundary", "SecurePass123!")

        for _ in range(4):
            await client.post(
                "/api/v1/auth/login",
                json={"username": "rl_login_boundary", "password": "WrongPass!"},
            )

        # 5th attempt — at the limit, not yet over
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "rl_login_boundary", "password": "SecurePass123!"},
        )
        assert response.status_code in (200, 401)  # processed, NOT 429


class TestRateLimitingIsolation:
    """Verify rate limits on /register and /login are counted separately."""

    @pytest.mark.asyncio
    async def test_register_and_login_counters_are_independent(
        self, client: AsyncClient
    ) -> None:
        """Exhausting /register counter does NOT block /login requests."""
        # Exhaust /register
        for i in range(6):
            await client.post("/api/v1/auth/register", json=_register_payload(f"iso_{i}"))

        register_blocked = await client.post(
            "/api/v1/auth/register", json=_register_payload("iso_over")
        )
        assert register_blocked.status_code == 429

        # /login uses a separate counter — must still be reachable
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent_user", "password": "Pass123!"},
        )
        # 401 = processed by backend → not rate-limited
        assert login_response.status_code != 429

    @pytest.mark.asyncio
    async def test_health_endpoints_never_rate_limited(
        self, client: AsyncClient
    ) -> None:
        """Health check endpoints are never rate-limited, regardless of other traffic."""
        # Exhaust both auth endpoints first
        for i in range(6):
            await client.post("/api/v1/auth/register", json=_register_payload(f"health_{i}"))
        for _ in range(6):
            await client.post(
                "/api/v1/auth/login",
                json={"username": "nouser", "password": "WrongPass!"},
            )

        # Health endpoints must still return 200
        for _ in range(5):
            response = await client.get("/health")
            assert response.status_code == 200

