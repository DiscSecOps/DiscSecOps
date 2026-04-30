"""
Main FastAPI application (ASYNC with PostgreSQL)
Initializes the API with authentication endpoints, CORS, security headers,
logging middleware and rate limiting.
"""

import logging
import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.endpoints import auth, circle_members, circles, posts, users
from app.core.config import settings
from app.core.db import engine
from app.core.security_headers import SecurityHeadersMiddleware

# -----------------------------
# RATE LIMITER CONFIG
# -----------------------------
limiter = Limiter(key_func=get_remote_address)


# -----------------------------
# LOGGING CONFIG
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


# -----------------------------
# LIFESPAN HANDLER
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await engine.dispose()


# -----------------------------
# INITIALIZE APP
# -----------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Social application backend with authentication and circles",
    lifespan=lifespan
)

app.state.limiter = limiter


# -----------------------------
# GLOBAL RATE LIMIT HANDLER
# -----------------------------
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    client_ip = request.client.host if request.client else "unknown"
    logger.warning({
        "event": "rate_limit_exceeded",
        "ip": client_ip,
        "path": request.url.path
    })
    print(f"⚠️  RATE LIMIT: {client_ip} - {request.url.path} - Too many requests")
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Try again later."}
    )


# -----------------------------
# LOGGING MIDDLEWARE
# -----------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.time()

    response = await call_next(request)

    duration = (time.time() - start_time) * 1000
    client_ip = request.client.host if request.client else "unknown"

    logger.info({
        "event": "http_request",
        "method": request.method,
        "url": request.url.path,
        "status_code": response.status_code,
        "duration_ms": round(duration, 2),
        "ip": client_ip
    })

    print(f"📡 {request.method} {request.url.path} - {response.status_code} - {round(duration, 2)}ms - {client_ip}")

    return response


# -----------------------------
# CORS + SECURITY HEADERS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)


# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(circles.router, prefix=settings.API_V1_STR)
app.include_router(posts.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(circle_members.router, prefix=settings.API_V1_STR)


# -----------------------------
# HEALTH ENDPOINTS
# -----------------------------
@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "message": "DevSecOps Social App API",
        "version": settings.VERSION,
        "status": "running",
        "database": "PostgreSQL (Async)"
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "database": "PostgreSQL"}


@app.get("/api/health")
async def api_health() -> dict[str, str]:
    return {"status": "healthy", "api_version": settings.VERSION}


@app.get(f"{settings.API_V1_STR}/health")
async def api_v1_health() -> dict[str, str]:
    return {"status": "healthy", "api_version": settings.VERSION, "api": "v1"}
