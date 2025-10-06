#!/usr/bin/env python3
"""
Script to load test data into the GeneWeb database.
This script creates sample genealogical data using SQLAlchemy models.

Usage:
    python scripts/load_test_data.py
"""

import asyncio
import sys
from datetime import date
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.persistence.models import (
    Child,
    Event,
    Family,
    FamilyEvent,
    GenewebDatabase,
    Individual,
    IndividualEvent,
)
from app.settings import settings


async def create_test_database(session: AsyncSession) -> GenewebDatabase:
    """Create a test database entry."""
    db = GenewebDatabase(
        name="test_family",
        description="Test family database for development",
        owner="admin",
        access_level=1,
        is_active=True,
    )
    session.add(db)
    await session.flush()
    return db


async def create_test_individuals(session: AsyncSession, database_id: int) -> dict:
    """Create test individuals (grandparents, parents, children)."""
    # Grandfather
    grandfather = Individual(
        database_id=database_id,
        first_name="Jean",
        last_name="Dupont",
        gender_id=1,  # Male
        birth_date_1=date(1920, 3, 15),
        birth_place="Paris, France",
        death_status_id=2,  # Dead
        death_date_1=date(1995, 8, 20),
    )

    # Grandmother
    grandmother = Individual(
        database_id=database_id,
        first_name="Marie",
        last_name="Martin",
        public_name="Marie Dupont",
        gender_id=2,  # Female
        birth_date_1=date(1922, 7, 20),
        birth_place="Lyon, France",
        death_status_id=2,
        death_date_1=date(2000, 5, 10),
    )

    # Father
    father = Individual(
        database_id=database_id,
        first_name="Pierre",
        last_name="Dupont",
        gender_id=1,
        birth_date_1=date(1945, 5, 10),
        birth_place="Paris, France",
        death_status_id=1,  # Alive
    )

    # Mother
    mother = Individual(
        database_id=database_id,
        first_name="Sophie",
        last_name="Bernard",
        public_name="Sophie Dupont",
        gender_id=2,
        birth_date_1=date(1947, 11, 3),
        birth_place="Marseille, France",
        death_status_id=1,
    )

    # Children
    child1 = Individual(
        database_id=database_id,
        first_name="Lucas",
        last_name="Dupont",
        gender_id=1,
        birth_date_1=date(1975, 8, 22),
        birth_place="Paris, France",
        death_status_id=0,  # Unknown
    )

    child2 = Individual(
        database_id=database_id,
        first_name="Emma",
        last_name="Dupont",
        gender_id=2,
        birth_date_1=date(1978, 3, 15),
        birth_place="Paris, France",
        death_status_id=0,
    )

    session.add_all([grandfather, grandmother, father, mother, child1, child2])
    await session.flush()

    return {
        "grandfather": grandfather,
        "grandmother": grandmother,
        "father": father,
        "mother": mother,
        "child1": child1,
        "child2": child2,
    }


async def create_test_families(
    session: AsyncSession, database_id: int, individuals: dict
) -> dict:
    """Create test family units."""
    # Grandparents family
    grandparents_family = Family(
        database_id=database_id,
        father_id=individuals["grandfather"].id,
        mother_id=individuals["grandmother"].id,
        same_sex_couple=False,
    )

    # Parents family
    parents_family = Family(
        database_id=database_id,
        father_id=individuals["father"].id,
        mother_id=individuals["mother"].id,
        same_sex_couple=False,
    )

    session.add_all([grandparents_family, parents_family])
    await session.flush()

    # Link children to families
    # Pierre is child of Jean and Marie
    child_link1 = Child(
        family_id=grandparents_family.id, subject_id=individuals["father"].id
    )

    # Lucas and Emma are children of Pierre and Sophie
    child_link2 = Child(
        family_id=parents_family.id, subject_id=individuals["child1"].id
    )
    child_link3 = Child(
        family_id=parents_family.id, subject_id=individuals["child2"].id
    )

    session.add_all([child_link1, child_link2, child_link3])
    await session.flush()

    return {
        "grandparents_family": grandparents_family,
        "parents_family": parents_family,
    }


async def create_test_events(
    session: AsyncSession, database_id: int, families: dict, individuals: dict
) -> None:
    """Create test events (marriages, etc.)."""
    # Marriage of grandparents
    marriage1 = Event(
        database_id=database_id,
        event_name="marriage",
        place="Paris, France",
        event_date_1=date(1944, 6, 15),
    )

    # Marriage of parents
    marriage2 = Event(
        database_id=database_id,
        event_name="marriage",
        place="Lyon, France",
        event_date_1=date(1970, 9, 12),
    )

    session.add_all([marriage1, marriage2])
    await session.flush()

    # Link marriages to families
    family_event1 = FamilyEvent(
        family_id=families["grandparents_family"].id, event_id=marriage1.id
    )
    family_event2 = FamilyEvent(
        family_id=families["parents_family"].id, event_id=marriage2.id
    )

    session.add_all([family_event1, family_event2])
    await session.flush()


async def main():
    """Main function to load test data."""
    print("=" * 60)
    print("📊 Loading Test Data into GeneWeb Database")
    print("=" * 60)
    print(
        f"Database URL: {settings.database_url.split('@')[1] if '@' in settings.database_url else settings.database_url}"
    )
    print()

    # Create engine and session
    engine = create_async_engine(settings.database_url, echo=False)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with SessionLocal() as session:
            print("🔨 Creating test database entry...")
            db = await create_test_database(session)
            print(f"✅ Created database: {db.name} (ID: {db.id})")

            print("\n👥 Creating test individuals...")
            individuals = await create_test_individuals(session, db.id)
            print(f"✅ Created {len(individuals)} individuals")

            print("\n👨‍👩‍👧‍👦 Creating test families...")
            families = await create_test_families(session, db.id, individuals)
            print(f"✅ Created {len(families)} families with children links")

            print("\n💒 Creating test events...")
            await create_test_events(session, db.id, families, individuals)
            print("✅ Created marriage events")

            print("\n💾 Committing changes to database...")
            await session.commit()
            print("✅ All test data committed successfully")

        print("\n" + "=" * 60)
        print("✅ Test Data Loading Completed!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"   • 1 test database")
        print(f"   • 6 individuals (grandparents, parents, children)")
        print(f"   • 2 families")
        print(f"   • 2 marriage events")
        print("\n💡 You can now query this data through the API")

        return 0

    except Exception as e:
        print(f"\n❌ Error loading test data: {e}")
        import traceback

        traceback.print_exc()
        return 1
    finally:
        await engine.dispose()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
