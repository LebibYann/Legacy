#!/usr/bin/env python3
"""
Script to initialize the GeneWeb database using SQLAlchemy models.
This script creates all tables defined in app.persistence.models

Usage:
    python scripts/setup_database.py [--drop-all]

Options:
    --drop-all    Drop all existing tables before creating new ones (DESTRUCTIVE!)
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


async def drop_all_tables(engine) -> None:
    """Drop all existing tables."""
    print("\n⚠️  DROPPING ALL TABLES...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ All tables dropped successfully\n")


async def create_all_tables(engine) -> None:
    """Create all tables defined in SQLAlchemy models."""
    print("🔨 Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully\n")


async def list_tables(engine) -> None:
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
        tables = [row[0] for row in result.fetchall()]

    if tables:
        print(f"📊 Tables in database ({len(tables)}):")
        for table in tables:
            print(f"   ✓ {table}")
    else:
        print("📊 No tables found in database")


async def main():
    """Main setup function."""
    import argparse

    parser = argparse.ArgumentParser(description="Setup GeneWeb database")
    parser.add_argument(
        "--drop-all",
        action="store_true",
        help="Drop all existing tables before creating (DESTRUCTIVE!)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🧬 GeneWeb Database Setup")
    print("=" * 60)
    print(
        f"Database URL: {settings.database_url.split('@')[1] if '@' in settings.database_url else settings.database_url}"
    )
    print()

    # Create engine
    engine = create_async_engine(settings.database_url, echo=False)

    try:
        # Test connection
        print("🔍 Testing database connection...")
        if not await check_connection(engine):
            print("\n❌ Setup aborted: Cannot connect to database")
            print("   Please check your DATABASE_URL in .env file")
            return 1
        print("✅ Database connection successful\n")

        # Drop tables if requested
        if args.drop_all:
            confirm = input("⚠️  Are you sure you want to DROP ALL TABLES? [y/N]: ")
            if confirm.lower() != "y":
                print("❌ Aborted by user")
                return 0
            await drop_all_tables(engine)

        # Create tables
        await create_all_tables(engine)

        # List created tables
        await list_tables(engine)

        print("\n" + "=" * 60)
        print("✅ Database setup completed successfully!")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. Run migrations: poetry run alembic upgrade head")
        print("   2. Load test data: python scripts/load_test_data.py")
        print("   3. Start the API: poetry run uvicorn app.main:app --reload")

        return 0

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback

        traceback.print_exc()
        return 1
    finally:
        await engine.dispose()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
