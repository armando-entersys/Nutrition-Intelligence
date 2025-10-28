#!/usr/bin/env python3
"""
Simple script to test foods database connection directly
"""
import asyncio
import sys
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from domain.foods.models import Food
from core.config import get_settings

async def test_foods():
    """Test foods query directly"""

    settings = get_settings()
    print(f"Database URL: {settings.database_url}")

    # Create async engine
    async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    print(f"Async Database URL: {async_database_url}")

    async_engine = create_async_engine(
        async_database_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300
    )

    AsyncSessionLocal = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    try:
        async with AsyncSessionLocal() as session:
            print("Connected to database successfully")

            # Query all foods
            query = select(Food)
            result = await session.execute(query)
            foods = result.scalars().all()

            print(f"Found {len(foods)} foods")

            for food in foods:
                print(f"Food: {food.id} - {food.name} - {food.status} - {food.category}")
                print(f"  Allergens: {food.allergens} (type: {type(food.allergens)})")
                print(f"  Search keywords: {food.search_keywords} (type: {type(food.search_keywords)})")
                print(f"  Dietary flags: {food.dietary_flags} (type: {type(food.dietary_flags)})")
                print(f"  Seasonal availability: {food.seasonal_availability} (type: {type(food.seasonal_availability)})")
                break  # Just show first one

            return foods

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    asyncio.run(test_foods())