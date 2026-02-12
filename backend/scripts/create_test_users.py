import asyncio
import os
import sys

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from app.db.models import Role, User


async def create_test_users() -> None:
    """Create test users for E2E tests"""
    async with AsyncSessionLocal() as session:
        # Seed Roles
        roles = ["admin", "user", "manager"]
        role_map = {}

        for role_name in roles:
            result = await session.execute(select(Role).where(Role.name == role_name))
            role = result.scalar_one_or_none()
            if not role:
                print(f"Creating role: {role_name}")
                new_role = Role(name=role_name, description=f"System {role_name} role")
                session.add(new_role)
                await session.commit()
                await session.refresh(new_role)
                role_map[role_name] = new_role.id
            else:
                role_map[role_name] = role.id

        # Check if user exists
        email = "test@example.com"
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            print(f"Creating test user: {email}")
            new_user = User(
                username="testuser",
                email=email,
                full_name="Test User",
                hashed_password=get_password_hash("password123"),
                role_id=role_map["user"],
                is_active=True,
                is_superuser=False,
            )
            session.add(new_user)
            await session.commit()
        else:
            print("Test user already exists")


if __name__ == "__main__":
    asyncio.run(create_test_users())
