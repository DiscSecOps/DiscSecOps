from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)

        # Basic security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"

        # CSP (Content Security Policy)
        response.headers["Content-Security-Policy"] = (
            f"default-src 'self'; "
            f"img-src 'self' data:; "
            f"script-src 'self'; "
            f"style-src 'self' 'unsafe-inline'; "
            f"connect-src 'self' {settings.FRONTEND_URL};"
        )

        # HSTS (only in production)
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )

        return response
