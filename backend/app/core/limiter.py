"""
Rate limiter instance (shared across app to avoid circular imports)
Uses slowapi with in-memory storage (no Redis required)
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
