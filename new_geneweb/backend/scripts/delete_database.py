#!/usr/bin/env python3
"""
Script to teardown the GeneWeb database (drop all tables).
This script removes all tables defined in app.persistence.models

⚠️  WARNING: This is DESTRUCTIVE and will delete ALL data!

Usage:
    python scripts/delete_database.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.persistence.models import Base
from app.settings import settings


async def check_connection(engine) -> bool:
    """Test database connection."""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def list_tables(engine) -> list[str]:
    """List all tables in the database."""
    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
            )
        )
        return [row[0] for row in result.fetchall()]


async def drop_all_tables(engine) -> None:
    """Drop all existing tables."""
    print("\n🗑️  Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ All tables dropped successfully\n")


async def main():
    """Main teardown function."""
    print("=" * 60)
    print("🗑️  GeneWeb Database Teardown")
    print("=" * 60)
    db_url_display = (
        settings.database_url.split("@")[1]
        if "@" in settings.database_url
        else settings.database_url
    )
    print(f"Database URL: {db_url_display}")
    print()

    # Create engine
    engine = create_async_engine(settings.database_url, echo=False)

    try:
        # Test connection
        print("🔍 Testing database connection...")
        if not await check_connection(engine):
            print("\n❌ Teardown aborted: Cannot connect to database")
            return 1
        print("✅ Database connection successful\n")

        # List existing tables
        tables = await list_tables(engine)
        if not tables:
            print("ℹ️  No tables found in database. Nothing to teardown.")
            return 0

        print(f"📊 Found {len(tables)} table(s):")
        for table in tables:
            print(f"   • {table}")
        print()

        # Confirmation
        print("⚠️  " + "=" * 56)
        print("⚠️  WARNING: This will DELETE ALL DATA from these tables!")
        print("⚠️  " + "=" * 56)

        confirm = input("\n❓ Are you sure you want to continue? [y/N]: ")
        if confirm.lower() != "y":
            print("\n✅ Teardown cancelled. No changes made.")
            return 0

        # Additional confirmation for safety
        confirm2 = input("❓ Type 'DELETE' to confirm: ")
        if confirm2 != "DELETE":
            print("\n✅ Teardown cancelled. No changes made.")
            return 0

        # Drop tables
        await drop_all_tables(engine)

        # Verify tables are gone
        remaining_tables = await list_tables(engine)
        if remaining_tables:
            print(f"⚠️  Warning: {len(remaining_tables)} table(s) still exist:")
            for table in remaining_tables:
                print(f"   • {table}")
        else:
            print("✅ Verified: All tables have been removed")

        print("\n" + "=" * 60)
        print("✅ Database teardown completed!")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"\n❌ Error during teardown: {e}")
        import traceback

        traceback.print_exc()
        return 1
    finally:
        await engine.dispose()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
