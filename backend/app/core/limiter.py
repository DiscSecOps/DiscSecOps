from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings  # adjust if your settings path differs

limiter = Limiter(key_func=get_remote_address)

# Disable rate limiting in non-production environments
if settings.ENVIRONMENT != "production":
    limiter.enabled = False
