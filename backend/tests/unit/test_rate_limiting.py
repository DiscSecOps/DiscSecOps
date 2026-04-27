"""
Unit tests for rate limiting (slowapi)

Uses an isolated FastAPI test app with a fresh Limiter per test to avoid
state leakage between tests. No database required — purely tests the
rate limiting layer.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


async def _handle_rate_limit(request: Request, exc: Exception) -> JSONResponse:
    """Typed rate limit handler compatible with FastAPI's add_exception_handler."""
    return JSONResponse(status_code=429, content={"error": f"Rate limit exceeded: {exc}"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_app(limit: str = "3/minute") -> tuple[FastAPI, TestClient]:
    """
    Creates a fresh FastAPI app with its own Limiter instance and a single
    rate-limited endpoint.  A new app per test avoids shared counter state.
    """
    test_limiter = Limiter(key_func=get_remote_address)
    app = FastAPI()
    app.state.limiter = test_limiter
    app.add_exception_handler(RateLimitExceeded, _handle_rate_limit)

    @app.get("/limited")
    @test_limiter.limit(limit)
    def limited(request: Request) -> dict:
        return {"ok": True}

    @app.get("/unlimited")
    def unlimited() -> dict:
        return {"ok": True}

    return app, TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRateLimitingBasic:
    """Core rate limiting behaviour"""

    def test_requests_within_limit_return_200(self):
        """All requests up to the limit should succeed."""
        _, client = make_app("3/minute")
        for _ in range(3):
            response = client.get("/limited")
            assert response.status_code == 200

    def test_request_exceeding_limit_returns_429(self):
        """The request immediately after the limit is exhausted must return 429."""
        _, client = make_app("3/minute")
        for _ in range(3):
            client.get("/limited")
        response = client.get("/limited")
        assert response.status_code == 429

    def test_429_response_is_json(self):
        """slowapi returns a JSON body on 429 — not plain text."""
        _, client = make_app("2/minute")
        for _ in range(2):
            client.get("/limited")
        response = client.get("/limited")
        assert response.status_code == 429
        data = response.json()
        assert isinstance(data, dict)

    def test_429_response_contains_error_field(self):
        """slowapi includes an 'error' key in the 429 response body."""
        _, client = make_app("2/minute")
        for _ in range(2):
            client.get("/limited")
        response = client.get("/limited")
        assert response.status_code == 429
        data = response.json()
        assert "error" in data

    def test_unlimited_endpoint_never_rate_limited(self):
        """Endpoints without a @limiter.limit decorator are never throttled."""
        _, client = make_app("1/minute")
        for _ in range(10):
            response = client.get("/unlimited")
            assert response.status_code == 200


class TestRateLimitingHeaders:
    """Rate limit response headers"""

    def test_successful_response_has_standard_content_type(self):
        """Successful rate-limited responses still return JSON."""
        _, client = make_app("5/minute")
        response = client.get("/limited")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_429_response_has_json_content_type(self):
        """The 429 response from slowapi is JSON, not plain text."""
        _, client = make_app("2/minute")
        for _ in range(2):
            client.get("/limited")
        response = client.get("/limited")
        assert response.status_code == 429
        assert "application/json" in response.headers.get("content-type", "")


class TestRateLimitingEdgeCases:
    """Edge cases and boundary conditions"""

    def test_exactly_at_limit_still_succeeds(self):
        """The Nth request (exactly at the limit) should still return 200."""
        _, client = make_app("5/minute")
        responses = [client.get("/limited") for _ in range(5)]
        assert responses[-1].status_code == 200

    def test_first_request_after_multiple_429s_is_still_429(self):
        """Once throttled, subsequent requests within the window remain 429."""
        _, client = make_app("2/minute")
        for _ in range(2):
            client.get("/limited")
        for _ in range(3):
            response = client.get("/limited")
            assert response.status_code == 429

    def test_different_limit_values_enforced_correctly(self):
        """A limit of 1/minute allows exactly one request before throttling."""
        _, client = make_app("1/minute")
        assert client.get("/limited").status_code == 200
        assert client.get("/limited").status_code == 429

    def test_limiter_state_isolated_between_app_instances(self):
        """Two independent app instances do not share counter state."""
        _, client_a = make_app("1/minute")
        _, client_b = make_app("1/minute")

        # Exhaust client_a's limit
        client_a.get("/limited")
        assert client_a.get("/limited").status_code == 429

        # client_b should still be at zero — first request must succeed
        assert client_b.get("/limited").status_code == 200


class TestRateLimiterConfiguration:
    """Tests that verify the limiter is wired correctly in the real app"""

    def test_limiter_attached_to_real_app_state(self):
        """The production app must have a limiter on its state."""
        from app.main import app

        assert hasattr(app.state, "limiter"), (
            "app.state.limiter is not set — did you forget to wire slowapi in main.py?"
        )

    def test_limiter_instance_is_slowapi_limiter(self):
        """The object attached to app.state must be a slowapi Limiter."""
        from slowapi import Limiter as SlowApiLimiter

        from app.main import app

        assert isinstance(app.state.limiter, SlowApiLimiter)

    def test_ratelimitexceeded_handler_registered(self):
        """A handler for RateLimitExceeded must be registered so 429s are JSON."""
        from app.main import app

        assert RateLimitExceeded in app.exception_handlers, (
            "No exception handler for RateLimitExceeded registered in main.py"
        )
