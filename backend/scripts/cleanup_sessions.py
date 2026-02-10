
import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import CursorResult, delete

from app.core.db import AsyncSessionLocal
from app.db.models import UserSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def cleanup_sessions() -> None:
    """Cleanup expired sessions."""
    async with AsyncSessionLocal() as db:
        try:
            now = datetime.utcnow()
            logger.info(f"Cleaning up sessions expired before {now}...")

            stmt = delete(UserSession).where(UserSession.expires_at < now)
            result = await db.execute(stmt)
            await db.commit()

            # Cast to CursorResult for type checking
            assert isinstance(result, CursorResult)
            logger.info(f"Deleted {result.rowcount} expired sessions.")

        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(cleanup_sessions())
