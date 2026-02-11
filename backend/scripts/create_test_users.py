import asyncio
import os
import sys

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from app.db.models import User


async def create_test_users() -> None:
    """Create test users for E2E tests"""
    async with AsyncSessionLocal() as session:
        # Check if user exists
        result = await session.execute(select(User).where(User.username == "testuser"))
        user = result.scalar_one_or_none()

        if not user:
            print("Creating test user: testuser")
            new_user = User(
                username="testuser",
                email="test@example.com",
                full_name="Test User",
                hashed_password=get_password_hash("password123"),
                role="user",
                is_active=True,
                is_superuser=False,
            )
            session.add(new_user)
            await session.commit()
        else:
            print("Test user already exists")


if __name__ == "__main__":
    asyncio.run(create_test_users())
