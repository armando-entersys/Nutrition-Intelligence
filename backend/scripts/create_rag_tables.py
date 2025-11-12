"""
Create RAG System Tables
========================

Este script crea las tablas necesarias para el sistema RAG:
- productos_nom051 (Productos NOM-051)
- foods_smae (Alimentos SMAE)
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from domain.foods.nom051_models import ProductoNOM051, FoodSMAE
from core.config import get_settings


async def create_tables():
    """Create all tables"""
    settings = get_settings()

    print("🔧 Connecting to database...")
    print(f"📍 Database URL: {settings.database_url}")

    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=True,  # Show SQL queries
    )

    print("\n🏗️  Creating tables...")
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)

    print("\n✅ Tables created successfully!")

    # Close engine
    await engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RAG System Table Creation")
    print("=" * 60)

    asyncio.run(create_tables())

    print("\n" + "=" * 60)
    print("✨ Done!")
    print("=" * 60)
