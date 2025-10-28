"""
Database seeding script for Nutrition Intelligence Platform
Seeds initial data including Mexican food database
"""
import asyncio
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db_transaction
from domain.foods.models import Food, FoodCategory, FoodStatus, MeasurementUnit
from domain.users.models import User
from core.security import hash_password
from domain.users.models import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mexican food database - Sistema Mexicano de Alimentos Equivalentes (SMAE)
MEXICAN_FOODS_DATA = [
    # Cereales
    {
        "name": "Arroz blanco cocido",
        "category": FoodCategory.CEREALS,
        "calories_per_serving": 130,
        "protein_g": 2.7,
        "carbs_g": 28.0,
        "fat_g": 0.3,
        "fiber_g": 0.4,
        "serving_size": 100,
        "source": "SMAE",
        "region": "Nacional"
    },
    {
        "name": "Tortilla de maíz",
        "category": FoodCategory.CEREALS,
        "calories_per_serving": 85,
        "protein_g": 2.3,
        "carbs_g": 17.0,
        "fat_g": 1.1,
        "fiber_g": 2.9,
        "serving_size": 30,
        "base_unit": MeasurementUnit.PIECES,
        "source": "SMAE",
        "region": "Nacional"
    },
    {
        "name": "Avena cocida",
        "category": FoodCategory.CEREALS,
        "calories_per_serving": 68,
        "protein_g": 2.4,
        "carbs_g": 12.0,
        "fat_g": 1.4,
        "fiber_g": 1.7,
        "serving_size": 100,
        "source": "SMAE"
    },
    
    # Verduras
    {
        "name": "Nopales",
        "category": FoodCategory.VEGETABLES,
        "calories_per_serving": 16,
        "protein_g": 1.3,
        "carbs_g": 3.3,
        "fat_g": 0.1,
        "fiber_g": 3.2,
        "serving_size": 100,
        "source": "SMAE",
        "region": "México",
        "dietary_flags": ["low_calorie", "high_fiber"]
    },
    {
        "name": "Chile poblano",
        "category": FoodCategory.VEGETABLES,
        "calories_per_serving": 20,
        "protein_g": 1.0,
        "carbs_g": 4.6,
        "fat_g": 0.2,
        "fiber_g": 2.0,
        "serving_size": 100,
        "source": "SMAE",
        "region": "México"
    },
    {
        "name": "Quelites",
        "category": FoodCategory.VEGETABLES,
        "calories_per_serving": 22,
        "protein_g": 3.2,
        "carbs_g": 2.8,
        "fat_g": 0.3,
        "fiber_g": 4.1,
        "serving_size": 100,
        "source": "SMAE",
        "region": "México"
    },
    
    # Frutas
    {
        "name": "Tuna (fruto del nopal)",
        "category": FoodCategory.FRUITS,
        "calories_per_serving": 41,
        "protein_g": 0.7,
        "carbs_g": 9.6,
        "fat_g": 0.5,
        "fiber_g": 3.6,
        "serving_size": 100,
        "source": "SMAE",
        "region": "México"
    },
    {
        "name": "Guayaba",
        "category": FoodCategory.FRUITS,
        "calories_per_serving": 68,
        "protein_g": 2.6,
        "carbs_g": 14.3,
        "fat_g": 1.0,
        "fiber_g": 5.4,
        "serving_size": 100,
        "source": "SMAE",
        "region": "Tropical"
    },
    
    # Leguminosas
    {
        "name": "Frijoles negros cocidos",
        "category": FoodCategory.LEGUMES,
        "calories_per_serving": 132,
        "protein_g": 8.9,
        "carbs_g": 23.0,
        "fat_g": 0.5,
        "fiber_g": 8.7,
        "serving_size": 100,
        "source": "SMAE",
        "region": "Nacional"
    },
    {
        "name": "Frijoles pintos cocidos",
        "category": FoodCategory.LEGUMES,
        "calories_per_serving": 143,
        "protein_g": 9.0,
        "carbs_g": 26.2,
        "fat_g": 0.6,
        "fiber_g": 9.0,
        "serving_size": 100,
        "source": "SMAE"
    },
    
    # Productos de origen animal
    {
        "name": "Pechuga de pollo sin piel",
        "category": FoodCategory.ANIMAL_PRODUCTS,
        "calories_per_serving": 165,
        "protein_g": 31.0,
        "carbs_g": 0.0,
        "fat_g": 3.6,
        "fiber_g": 0.0,
        "serving_size": 100,
        "source": "SMAE",
        "region": "Nacional"
    },
    {
        "name": "Pescado blanco (tilapia)",
        "category": FoodCategory.ANIMAL_PRODUCTS,
        "calories_per_serving": 96,
        "protein_g": 20.1,
        "carbs_g": 0.0,
        "fat_g": 1.7,
        "fiber_g": 0.0,
        "serving_size": 100,
        "source": "SMAE"
    },
    {
        "name": "Huevos de gallina",
        "category": FoodCategory.ANIMAL_PRODUCTS,
        "calories_per_serving": 155,
        "protein_g": 13.0,
        "carbs_g": 1.1,
        "fat_g": 11.0,
        "fiber_g": 0.0,
        "serving_size": 100,
        "base_unit": MeasurementUnit.PIECES,
        "source": "SMAE"
    }
]

async def seed_foods():
    """Seed food database with Mexican foods"""
    logger.info("Seeding food database...")
    
    async with get_db_transaction() as session:
        # Check if foods already exist
        existing_count = len(await session.exec(select(Food)).all())
        if existing_count > 0:
            logger.info(f"Food database already contains {existing_count} items, skipping seed")
            return
        
        # Add Mexican foods
        for food_data in MEXICAN_FOODS_DATA:
            food = Food(
                **food_data,
                status=FoodStatus.APPROVED,
                search_keywords=[food_data["name"].lower()],
                created_at=datetime.utcnow()
            )
            session.add(food)
        
        logger.info(f"Added {len(MEXICAN_FOODS_DATA)} Mexican foods to database")

async def seed_admin_user():
    """Create admin user for testing"""
    logger.info("Creating admin user...")
    
    async with get_db_transaction() as session:
        # Check if admin exists
        from sqlmodel import select
        result = await session.execute(
            select(User).where(User.email == "admin@nutrition.com")
        )
        existing_admin = result.scalars().first()
        if existing_admin:
            logger.info("Admin user already exists, skipping")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@nutrition.com",
            hashed_password=hash_password("admin123"),
            first_name="Admin",
            last_name="Sistema",
            role=UserRole.ADMIN,
            status="active",
            email_verified=True,
            created_at=datetime.utcnow()
        )
        session.add(admin_user)
        logger.info("Admin user created: admin@nutrition.com / admin123")

async def seed_test_users():
    """Create test users for development"""
    logger.info("Creating test users...")
    
    test_users = [
        {
            "email": "nutriologo@test.com",
            "password": "test123",
            "first_name": "Dr. María",
            "last_name": "González",
            "role": UserRole.NUTRITIONIST
        },
        {
            "email": "paciente@test.com", 
            "password": "test123",
            "first_name": "Juan",
            "last_name": "Pérez",
            "role": UserRole.PATIENT
        }
    ]
    
    async with get_db_transaction() as session:
        for user_data in test_users:
            # Check if user exists
            existing_user = await session.exec(
                select(User).where(User.email == user_data["email"])
            )
            if existing_user.first():
                continue
            
            user = User(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                status="active",
                email_verified=True,
                created_at=datetime.utcnow()
            )
            session.add(user)
            logger.info(f"Created test user: {user_data['email']} / {user_data['password']}")

async def main():
    """Main seeding function"""
    logger.info("Starting database seeding...")
    
    try:
        await seed_admin_user()
        await seed_test_users()
        await seed_foods()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())