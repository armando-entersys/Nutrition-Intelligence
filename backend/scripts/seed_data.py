#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de muestra
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import init_database, AsyncSessionLocal
from domain.foods.models import Food, FoodStatus, FoodCategory
from domain.recipes.models import Recipe, RecipeStatus, MealType, DifficultyLevel

async def create_sample_foods():
    """Create sample food items"""

    foods_data = [
        {
            "name": "Arroz integral",
            "category": FoodCategory.CEREALS,
            "status": FoodStatus.APPROVED,
            "description": "Arroz integral rico en fibra",
            "calories_per_serving": 111,
            "protein_g": 2.6,
            "carbs_g": 22.0,
            "fat_g": 0.9,
            "fiber_g": 1.8,
            "common_names": ["arroz", "arroz cafe"],
            "search_keywords": ["cereal", "grano", "carbohidrato"]
        },
        {
            "name": "Pollo pechuga",
            "category": FoodCategory.ANIMAL_PRODUCTS,
            "status": FoodStatus.APPROVED,
            "description": "Pechuga de pollo sin piel",
            "calories_per_serving": 165,
            "protein_g": 31.0,
            "carbs_g": 0.0,
            "fat_g": 3.6,
            "fiber_g": 0.0,
            "common_names": ["pollo", "pechuga"],
            "search_keywords": ["proteina", "carne", "ave"]
        },
        {
            "name": "Brócoli",
            "category": FoodCategory.VEGETABLES,
            "status": FoodStatus.APPROVED,
            "description": "Brócoli fresco",
            "calories_per_serving": 34,
            "protein_g": 2.8,
            "carbs_g": 7.0,
            "fat_g": 0.4,
            "fiber_g": 2.6,
            "common_names": ["brocoli", "brocol"],
            "search_keywords": ["verdura", "vegetal", "verde"]
        },
        {
            "name": "Manzana",
            "category": FoodCategory.FRUITS,
            "status": FoodStatus.APPROVED,
            "description": "Manzana fresca",
            "calories_per_serving": 52,
            "protein_g": 0.3,
            "carbs_g": 14.0,
            "fat_g": 0.2,
            "fiber_g": 2.4,
            "common_names": ["manzana roja", "manzana verde"],
            "search_keywords": ["fruta", "dulce", "fibra"]
        },
        {
            "name": "Frijoles negros",
            "category": FoodCategory.LEGUMES,
            "status": FoodStatus.APPROVED,
            "description": "Frijoles negros cocidos",
            "calories_per_serving": 132,
            "protein_g": 8.9,
            "carbs_g": 23.0,
            "fat_g": 0.5,
            "fiber_g": 8.7,
            "common_names": ["frijol", "alubia negra"],
            "search_keywords": ["legumbre", "proteina vegetal", "fibra"]
        },
        {
            "name": "Aguacate",
            "category": FoodCategory.FATS,
            "status": FoodStatus.APPROVED,
            "description": "Aguacate fresco",
            "calories_per_serving": 160,
            "protein_g": 2.0,
            "carbs_g": 9.0,
            "fat_g": 15.0,
            "fiber_g": 7.0,
            "common_names": ["palta", "avocado"],
            "search_keywords": ["grasa saludable", "omega", "cremoso"]
        },
        {
            "name": "Leche descremada",
            "category": FoodCategory.DAIRY,
            "status": FoodStatus.APPROVED,
            "description": "Leche descremada",
            "calories_per_serving": 34,
            "protein_g": 3.4,
            "carbs_g": 5.0,
            "fat_g": 0.1,
            "fiber_g": 0.0,
            "common_names": ["leche light", "leche sin grasa"],
            "search_keywords": ["lacteo", "calcio", "proteina"]
        },
        {
            "name": "Agua natural",
            "category": FoodCategory.BEVERAGES,
            "status": FoodStatus.APPROVED,
            "description": "Agua purificada",
            "calories_per_serving": 0,
            "protein_g": 0.0,
            "carbs_g": 0.0,
            "fat_g": 0.0,
            "fiber_g": 0.0,
            "common_names": ["agua", "agua pura"],
            "search_keywords": ["hidratacion", "bebida", "liquido"]
        }
    ]

    async with AsyncSessionLocal() as session:
        try:
            print(f"📦 Creating {len(foods_data)} foods...")
            for i, food_data in enumerate(foods_data):
                print(f"  Creating food {i+1}: {food_data['name']}")
                food = Food(**food_data)
                session.add(food)

            print("💾 Committing to database...")
            await session.commit()
            print(f"✅ Created {len(foods_data)} sample foods")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error creating foods: {e}")
            import traceback
            traceback.print_exc()

async def create_sample_recipes():
    """Create sample recipes"""

    recipes_data = [
        {
            "title": "Pollo con Brócoli",
            "description": "Deliciosa combinación de pollo y brócoli al vapor",
            "meal_type": MealType.LUNCH,
            "difficulty": DifficultyLevel.EASY,
            "prep_time_minutes": 20,
            "cook_time_minutes": 15,
            "servings": 2,
            "status": RecipeStatus.PUBLISHED,
            "instructions": [
                "Cortar el pollo en tiras",
                "Cocinar el pollo en sartén con poco aceite",
                "Cocer el brócoli al vapor",
                "Servir junto con arroz"
            ],
            "tags": ["saludable", "proteina", "bajo en grasa"],
            "nutritional_info": {
                "calories_per_serving": 280,
                "protein_per_serving": 35,
                "carbs_per_serving": 8,
                "fat_per_serving": 12
            }
        },
        {
            "title": "Ensalada de Aguacate",
            "description": "Ensalada fresca con aguacate y vegetales",
            "meal_type": MealType.LUNCH,
            "difficulty": DifficultyLevel.EASY,
            "prep_time_minutes": 10,
            "cook_time_minutes": 0,
            "servings": 1,
            "status": RecipeStatus.PUBLISHED,
            "instructions": [
                "Lavar y cortar los vegetales",
                "Cortar el aguacate en cubos",
                "Mezclar todos los ingredientes",
                "Agregar aliño al gusto"
            ],
            "tags": ["vegetariano", "ensalada", "fresco"],
            "nutritional_info": {
                "calories_per_serving": 200,
                "protein_per_serving": 4,
                "carbs_per_serving": 12,
                "fat_per_serving": 16
            }
        },
        {
            "title": "Smoothie de Manzana",
            "description": "Smoothie refrescante de manzana con leche",
            "meal_type": MealType.BREAKFAST,
            "difficulty": DifficultyLevel.EASY,
            "prep_time_minutes": 5,
            "cook_time_minutes": 0,
            "servings": 1,
            "status": RecipeStatus.PUBLISHED,
            "instructions": [
                "Lavar y cortar la manzana",
                "Agregar la manzana a la licuadora",
                "Añadir leche descremada",
                "Licuar hasta obtener consistencia suave"
            ],
            "tags": ["desayuno", "licuado", "frutas"],
            "nutritional_info": {
                "calories_per_serving": 120,
                "protein_per_serving": 6,
                "carbs_per_serving": 25,
                "fat_per_serving": 1
            }
        }
    ]

    async with AsyncSessionLocal() as session:
        try:
            for recipe_data in recipes_data:
                recipe = Recipe(**recipe_data)
                session.add(recipe)

            await session.commit()
            print(f"✅ Created {len(recipes_data)} sample recipes")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error creating recipes: {e}")

async def main():
    """Main function to seed all data"""
    print("🌱 Starting database seeding...")

    try:
        # Initialize database connection
        print("🔌 Initializing database...")
        init_database()
        print("✅ Database initialized")

        print("🍎 Creating sample foods...")
        await create_sample_foods()
        print("✅ Foods created")

        print("🍽️ Creating sample recipes...")
        await create_sample_recipes()
        print("✅ Recipes created")

        print("🎉 Database seeding completed successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())