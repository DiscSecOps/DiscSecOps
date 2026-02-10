
import asyncio
import logging
import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from app.db.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_test_users() -> None:
    """Create test users for integration tests."""
    async with AsyncSessionLocal() as db:
        try:
            # Check if user exists
            result = await db.execute(select(User).where(User.username == "testuser"))
            user = result.scalar_one_or_none()

            if not user:
                logger.info("Creating testuser...")
                test_user = User(
                    username="testuser",
                    email="test@example.com",
                    full_name="Test User",
                    hashed_password=get_password_hash("password123"),
                    role="user",
                    is_active=True
                )
                db.add(test_user)
                await db.commit()
                logger.info("Test user 'testuser' created.")
            else:
                logger.info("Test user 'testuser' already exists.")

            # Create admin user
            result = await db.execute(select(User).where(User.username == "adminuser"))
            admin = result.scalar_one_or_none()
            if not admin:
                logger.info("Creating adminuser...")
                admin_user = User(
                    username="adminuser",
                    email="admin@example.com",
                    full_name="Admin User",
                    hashed_password=get_password_hash("admin123"),
                    role="admin",
                    is_active=True,
                    is_superuser=True
                )
                db.add(admin_user)
                await db.commit()
                logger.info("Admin user 'adminuser' created.")
            else:
                logger.info("Admin user 'adminuser' already exists.")

        except Exception as e:
            logger.error(f"Error creating test users: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(create_test_users())
