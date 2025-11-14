"""
Run migration and seed for medicinal plants
"""
import asyncio
import sys
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Import medicinal plants models to ensure they're registered
from domain.medicinal_plants.models import (
    MedicinalPlant,
    UserPlantLog,
    PlantHealthCondition,
    HerbalShop,
    PlantRecommendation
)

from core.config import get_settings

async def run_migration():
    """Create all tables in the database"""
    print("=" * 70)
    print("CREATING DATABASE TABLES")
    print("=" * 70)

    settings = get_settings()

    # Create async engine
    async_engine = create_async_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True
    )

    try:
        # Create all tables
        async with async_engine.begin() as conn:
            print("\n🔨 Creating all tables...")
            await conn.run_sync(SQLModel.metadata.create_all)
            print("✅ All tables created successfully!\n")

        await async_engine.dispose()
        return True

    except Exception as e:
        print(f"\n❌ Error creating tables: {str(e)}")
        await async_engine.dispose()
        return False

async def run_seed():
    """Run the medicinal plants seed"""
    print("=" * 70)
    print("RUNNING MEDICINAL PLANTS SEED")
    print("=" * 70)

    try:
        # Import and run seed
        sys.path.insert(0, '/app')
        from infrastructure.database.seeds.medicinal_plants_seed import seed_medicinal_plants

        await seed_medicinal_plants()
        return True

    except Exception as e:
        print(f"\n❌ Error running seed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("MEDICINAL PLANTS MIGRATION AND SEED")
    print("=" * 70 + "\n")

    # Run migration
    migration_success = await run_migration()
    if not migration_success:
        print("\n❌ Migration failed. Exiting...")
        sys.exit(1)

    # Run seed
    seed_success = await run_seed()
    if not seed_success:
        print("\n⚠️  Seed failed, but tables were created.")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("✅ MIGRATION AND SEED COMPLETED SUCCESSFULLY!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
