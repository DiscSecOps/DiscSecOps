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
                headers.append((b"x-frame-options", b"DENY"))
                headers.append((b"x-content-type-options", b"nosniff"))
                headers.append((b"referrer-policy", b"strict-origin-when-cross-origin"))
                headers.append((b"permissions-policy", b"geolocation=()"))

                # Cache control
                headers.append((b"cache-control", b"no-store"))

                # Content Security Policy
                csp = (
                    f"default-src 'self'; "
                    f"script-src 'self'; "
                    f"style-src 'self' 'unsafe-inline'; "
                    f"img-src 'self' data:; "
                    f"connect-src 'self' {settings.FRONTEND_URL}; "
                    f"frame-ancestors 'none';"
                )
                headers.append((b"content-security-policy", csp.encode()))

                # HSTS only in production
                if settings.ENVIRONMENT == "production":
                    headers.append(
                        (b"strict-transport-security", b"max-age=63072000; includeSubDomains; preload")
                    )

            await send(message)

        await self.app(scope, receive, send_wrapper)
