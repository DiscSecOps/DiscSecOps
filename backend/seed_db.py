import asyncio
import logging
import os
import sys

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from app.core.db import AsyncSessionLocal, engine
from app.core.security import get_password_hash
from app.db.models import Base, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_data():
    """Seed the database with test users."""
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as db:
            logger.info("Seeding database...")

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

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_data())
