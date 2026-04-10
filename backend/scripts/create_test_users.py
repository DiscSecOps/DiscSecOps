# backend/scripts/create_test_users.py
"""
Seed database with test users for development and testing
Reads user data from .env.test for consistency
"""

import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from app.db.models import User

load_dotenv(".env.test")

# Define which users to create (order matters)
USER_KEYS = ["TEST", "ALICE", "BOB", "CHARLIE", "NEW_USER_USERNAME", "NEW_USER2_USERNAME"]


async def create_test_users():
    """Create test users if they don't exist"""
    async with AsyncSessionLocal() as session:
        created = []
        existed = []

        for key in USER_KEYS:
            username = os.getenv(f"{key}_USERNAME")
            email = os.getenv(f"{key}_EMAIL")
            password = os.getenv(f"{key}_PASSWORD")
            full_name = os.getenv(f"{key}_FULL_NAME", key.capitalize())

            if not username or not password:
                print(f"⚠️ Skipping {key}: missing username or password in .env.test")
                continue

            result = await session.execute(select(User).where(User.username == username))
            existing = result.scalar_one_or_none()

            if existing:
                existed.append(username)
            else:
                print(f"Creating user: {username}")
                new_user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    hashed_password=get_password_hash(password),
                    is_active=True,
                )
                session.add(new_user)
                created.append(username)

        await session.commit()

        print("\n✅ Test users created!")
        print(f"   Created: {', '.join(created) if created else 'none'}")
        print(f"   Already existed: {', '.join(existed) if existed else 'none'}")


if __name__ == "__main__":
    asyncio.run(create_test_users())
