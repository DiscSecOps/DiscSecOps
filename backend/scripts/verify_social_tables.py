
import asyncio

from sqlalchemy import text

from app.db.database import get_db


async def verify_tables() -> None:
    print("Verifying database tables and columns...")
    async for session in get_db():
        # Check Tables
        result = await session.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        tables = set(row[0] for row in result.fetchall())
        print(f"Found tables: {tables}")

        required_tables = {"users", "posts", "circles", "circle_members"}
        missing_tables = required_tables - tables

        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            exit(1)

        # Check Columns
        # 1. users.email
        result = await session.execute(
            text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'users' AND column_name = 'email'"
            )
        )
        if not result.scalar():
            print("❌ Missing column: users.email")
            exit(1)

        # 2. circle_members.role (is_moderator)
        result = await session.execute(
            text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'circle_members' AND column_name = 'role'"
            )
        )
        if not result.scalar():
            print("❌ Missing column: circle_members.role"
            "(expected: 'owner', 'moderator', 'member')")
            exit(1)

        # 3. Optional: verify roles still exists if using new schema)
        if "roles" in tables:
            print("⚠️  Table 'roles' still exists - should be removed if using new schema")
            # exit(1)  # Don't fail yet, just warn

        print("✅ All social tables and new schema columns found!")
        exit(0)

if __name__ == "__main__":
    asyncio.run(verify_tables())
