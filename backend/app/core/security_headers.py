from typing import Any

from starlette.types import Receive, Scope, Send

from app.core.config import settings


class SecurityHeadersMiddleware:
    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:

        async def send_wrapper(message: dict[str, Any]) -> None:
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])

                # Basic security headers
                headers.append((b"x-frame-options", b"DENY"))                               # No <iframe> embedding
                headers.append((b"x-content-type-options", b"nosniff"))                     # No content or MIME-sniffing
                headers.append((b"referrer-policy", b"strict-origin-when-cross-origin"))    # No private data in referrer
                headers.append((b"permissions-policy", b"geolocation=()"))                  # No geolocation access

                # Cache control
                headers.append((b"cache-control", b"no-store"))

                # Content Security Policy
                csp = (
                    f"default-src 'self'; "                         # Allow resources same origin
                    f"script-src 'self'; "                          # Allow scripts from same origin
                    f"style-src 'self' 'unsafe-inline'; "           # Allow inline styles (for simplicity, but could be tightened)
                    f"img-src 'self' data:; "                       # Allow images from same origin
                    f"connect-src 'self' {settings.FRONTEND_URL}; " # Allow API calls to frontend
                    f"frame-ancestors 'none';"                      # Disallow framing
                )
                headers.append((b"content-security-policy", csp.encode()))

                # HSTS only in production
                if settings.ENVIRONMENT == "production":
                    headers.append(
                        (b"strict-transport-security", b"max-age=63072000; includeSubDomains; preload")
                    )

            await send(message)

        await self.app(scope, receive, send_wrapper)
