# Rate Limiting Implementation

**Branch:** `feature/rate-limiting`  
**Date:** 2026-04-27  
**Author:** GitHub Copilot (assisted)

---

## Background

The authentication endpoints `/auth/register` and `/auth/login` were completely unprotected against brute-force and credential-stuffing attacks. Any client could make unlimited requests per second with no consequences. Adding rate limiting was identified as a high-priority security hardening task for the production deployment on Render.

---

## What Was Implemented

### Library Choice — `slowapi`

We chose [`slowapi`](https://github.com/laurentS/slowapi) for the following reasons:

- Built specifically for FastAPI / Starlette — integrates as standard middleware
- Fully async-compatible (works with our `asyncpg` + SQLAlchemy async stack)
- No external dependencies (no Redis required — uses in-memory storage by default, which is fine for a single-instance Render deployment)
- Simple decorator-based API — one line per endpoint
- Actively maintained and widely used in the FastAPI ecosystem

Alternatives considered and rejected:
- **`fastapi-limiter`** — requires Redis, overkill for free-tier Render
- **Custom middleware** — more maintenance burden, reinventing the wheel
- **Nginx rate limiting** — not available on Render free tier

---

## Files Changed

| File | Type | Description |
|------|------|-------------|
| `backend/pyproject.toml` | Modified | Added `slowapi>=0.1.9` to production dependencies |
| `backend/app/core/limiter.py` | **New** | Shared `Limiter` singleton — isolated to avoid circular imports |
| `backend/app/main.py` | Modified | Wired `app.state.limiter` and typed `RateLimitExceeded` exception handler |
| `backend/app/api/v1/endpoints/auth.py` | Modified | Added `@limiter.limit("5/minute")` to `/register` and `/login`; added `request: Request` parameter to `register` |
| `backend/tests/unit/test_rate_limiting.py` | **New** | 14 unit tests — isolated test app, no database required |
| `backend/tests/integration/test_rate_limiting.py` | **New** | 12 integration tests — real app + real database |
| `backend/tests/conftest.py` | Modified | Added `limiter._storage.reset()` inside the `client` fixture to prevent counter bleed between tests |

---

## Implementation Details

### Shared Limiter Module (`app/core/limiter.py`)

The limiter is created once as a module-level singleton:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

Keeping it in its own module (`core/limiter.py`) is intentional — if the limiter were defined inside `auth.py` or `main.py`, it would create a circular import. Any other endpoint that needs rate limiting in the future can simply import this same instance.

### Wiring into the App (`app/main.py`)

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter

app.state.limiter = limiter

async def _handle_rate_limit_exceeded(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=429, content={"error": f"Rate limit exceeded: {exc}"})

app.add_exception_handler(RateLimitExceeded, _handle_rate_limit_exceeded)
```

Note: We wrote our own typed exception handler wrapper rather than using `slowapi`'s built-in `_rate_limit_exceeded_handler`. The built-in handler has a type signature that mypy considers incompatible with Starlette's `add_exception_handler` — our wrapper satisfies `Callable[[Request, Exception], Response]` while producing identical JSON output.

### Protected Endpoints (`app/api/v1/endpoints/auth.py`)

```python
@router.post("/register", ...)
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserCreate, ...) -> SessionResponse:
    ...

@router.post("/login", ...)
@limiter.limit("5/minute")
async def login(credentials: UserLogin, request: Request, ...) -> SessionResponse:
    ...
```

The limit of **5 requests per minute per IP** was chosen to:
- Allow normal user behaviour (a user won't register or login 5 times in one minute)
- Block automated brute-force tools which typically make hundreds of attempts per minute
- Align with the `API_RATE_LIMIT` setting already discussed in the team's configuration notes

---

## Test Coverage

### Unit Tests (`tests/unit/test_rate_limiting.py`) — 14 tests

These tests use a completely isolated FastAPI test app with a fresh `Limiter` instance per test. No database is required. They verify the rate limiting layer independently of any business logic.

| Test class | What is tested |
|------------|---------------|
| `TestRateLimitingBasic` | Requests within limit → 200; over limit → 429; JSON body; `error` field present; unlimited endpoints unaffected |
| `TestRateLimitingHeaders` | JSON content-type on success and on 429 |
| `TestRateLimitingEdgeCases` | Exact boundary behaviour; sustained 429 after throttle; `1/minute` limit; isolated state between independent app instances |
| `TestRateLimiterConfiguration` | Real app has `limiter` on state; correct type; `RateLimitExceeded` handler registered |

### Integration Tests (`tests/integration/test_rate_limiting.py`) — 12 tests

These tests run against the real FastAPI app with a real test database (via ASGITransport). They verify that rate limiting works end-to-end through the full request stack.

| Test class | What is tested |
|------------|---------------|
| `TestRegisterRateLimiting` | First request not limited; blocked after 5; 429 JSON body; boundary at exactly 5; storage reset clears counters |
| `TestLoginRateLimiting` | First attempt not limited; blocked after 5 (including wrong-password attempts); 429 JSON body; successful login works within limit; boundary at exactly 5 |
| `TestRateLimitingIsolation` | `/register` and `/login` counters are independent; health endpoints are never rate-limited |

**Total: 26 tests, all passing.**

---

## A Tricky Testing Problem — and How We Solved It

Adding rate limiting broke ~20 previously passing integration tests across `test_auth.py`, `test_circles.py`, `test_posts.py`, and `test_circle_members.py`. They were all getting unexpected 429 responses.

### Why It Happened

The rate limiter uses a single in-memory storage instance shared across the entire test session. The `test_rate_limiting.py` tests deliberately exhaust the limit (making 5+ requests per IP). When the next test file ran, the counter was still at its maximum — so the very first `/auth/login` call in a fixture like `test_owner` immediately got a 429.

### Why the First Fix Wasn't Enough

Our first attempt added a reset in the `clean_database_before_test` autouse fixture. This looked correct but failed for a subtle reason: pytest resolves fixture order **by dependency graph**, not declaration order. Fixtures like `test_owner` explicitly depend on `client`, but have no dependency relationship with `clean_database_before_test`. So pytest was free to run `test_owner` (and its login call) before the autouse reset ran.

### The Correct Fix

The reset was moved into the **`client` fixture** itself:

```python
@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    limiter._storage.reset()  # ← always runs before any login fixture call
    ...
```

This works permanently because every fixture that calls a login endpoint (`test_owner`, `test_moderator`, `test_member`, `test_author`, etc.) explicitly lists `client` as a dependency. Pytest guarantees that `client` setup finishes before any dependent fixture setup begins — so the counter is always zero before the first login call in any test, in any file, regardless of test ordering.

---

## CI Failures Encountered and Fixed

During development, the CI pipeline caught three separate issues:

1. **Ruff I001 (import sorting)** — The test files had imports in the wrong alphabetical order. Fixed with `ruff --fix`.

2. **mypy arg-type error in `main.py`** — `slowapi`'s built-in `_rate_limit_exceeded_handler` has a type signature incompatible with Starlette's `add_exception_handler`. Fixed by writing a properly typed wrapper function.

3. **429 counter bleed** — Described in detail in the section above.

---

## Result

All backend tests pass:

```
62 passed, 1 xfailed, 5 warnings
```

The one `xfailed` test is a pre-existing expected failure unrelated to this work (circle delete endpoint not yet implemented in frontend).

The `feature/rate-limiting` branch is ready for review and merge.
