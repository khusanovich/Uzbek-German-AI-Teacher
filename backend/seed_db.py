"""
Seed the database with initial curriculum data.
Run this script after setting DATABASE_URL to initialize the database.

Usage:
    python seed_db.py
"""
import sys
from pathlib import Path

# Add backend to path so we can import app modules
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.database import init_db, SessionLocal
from app.models import Unit as UnitModel
from app.curriculum.units import A1_1_UNITS


def seed_units():
    """Seed A1.1 units from curriculum/units.py into the database."""
    db = SessionLocal()
    try:
        # Create tables if they don't exist
        print("Creating database tables...")
        init_db()

        # Check if units already exist
        existing_count = db.query(UnitModel).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} units. Skipping seed.")
            print("To re-seed, delete all units first or drop the database.")
            return

        # Seed A1.1 units
        print(f"Seeding {len(A1_1_UNITS)} A1.1 units...")
        for unit in A1_1_UNITS:
            db_unit = UnitModel(
                id=unit.id,
                level=unit.level.value,  # Convert CEFR enum to string
                title=unit.title,
                objectives=unit.objectives,
                target_vocab=unit.target_vocab,
            )
            db.add(db_unit)

        db.commit()
        print(f"Successfully seeded {len(A1_1_UNITS)} units!")

        # Display seeded units
        print("\nSeeded units:")
        for unit in A1_1_UNITS:
            print(f"  - {unit.id}: {unit.title}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_units()
