# backend/tests/unit/conftest.py
"""
Unit test fixtures - lightweight, no database needed
"""

import pytest

from app.core.security import get_password_hash
from app.db.models import User


@pytest.fixture
def sample_user_data():
    """Return sample user data for unit tests"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User",
    }


@pytest.fixture
def sample_hashed_password():
    """Return a hashed password for testing"""
    return get_password_hash("SecurePass123!")


@pytest.fixture
def sample_user(sample_user_data, sample_hashed_password):
    """Create a sample User model instance (not persisted)"""
    return User(
        username=sample_user_data["username"],
        email=sample_user_data["email"],
        hashed_password=sample_hashed_password,
        full_name=sample_user_data["full_name"],
    )
