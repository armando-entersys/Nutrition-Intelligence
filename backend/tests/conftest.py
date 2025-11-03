"""
Test configuration and fixtures for the Nutrition Intelligence API.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from main import app
from core.config import get_settings
from infrastructure.database.connection import get_async_session
from domain.foods.models import Food, FoodStatus, FoodCategory
from domain.patients.models import Patient
from domain.recipes.models import Recipe


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Drop all tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with dependency overrides."""

    def get_test_session():
        return test_session

    app.dependency_overrides[get_async_session] = get_test_session

    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_food(test_session: AsyncSession) -> Food:
    """Create a sample food for testing."""
    food = Food(
        id=1,
        name="Apple",
        description="Fresh red apple",
        category=FoodCategory.FRUITS,
        status=FoodStatus.APPROVED,
        calories_per_100g=52.0,
        protein_per_100g=0.3,
        carbs_per_100g=14.0,
        fat_per_100g=0.2,
        fiber_per_100g=2.4,
        barcode="123456789",
        brand="Fresh Farms"
    )
    test_session.add(food)
    await test_session.commit()
    await test_session.refresh(food)
    return food


@pytest.fixture
async def sample_patient(test_session: AsyncSession) -> Patient:
    """Create a sample patient for testing."""
    patient = Patient(
        id=1,
        email="test@example.com",
        username="testpatient",
        full_name="Test Patient",
        hashed_password="$2b$12$test_hash",
        age=30,
        weight_kg=70.0,
        height_cm=175.0,
        is_active=True,
        is_verified=True
    )
    test_session.add(patient)
    await test_session.commit()
    await test_session.refresh(patient)
    return patient


@pytest.fixture
async def sample_recipe(test_session: AsyncSession, sample_patient: Patient) -> Recipe:
    """Create a sample recipe for testing."""
    recipe = Recipe(
        id=1,
        name="Apple Salad",
        description="Simple apple salad",
        instructions="1. Cut apple\n2. Serve",
        prep_time_minutes=5,
        servings=1,
        author_patient_id=sample_patient.id,
        total_calories=100.0,
        total_protein=2.0,
        total_carbs=25.0,
        total_fat=1.0
    )
    test_session.add(recipe)
    await test_session.commit()
    await test_session.refresh(recipe)
    return recipe


@pytest.fixture
def sample_lab_data_dict() -> dict:
    """Sample laboratory data dictionary for testing."""
    from datetime import date
    return {
        "patient_id": 1,
        "study_date": date(2025, 1, 15),
        "test_type": "blood_chemistry",
        "laboratory_name": "Laboratorio Chopo",
        "ordering_physician": "Dr. Juan Pérez",
        "fasting_glucose_mgdl": 95.0,
        "hemoglobin_a1c_pct": 5.5,
        "total_cholesterol_mgdl": 180.0,
        "ldl_cholesterol_mgdl": 100.0,
        "hdl_cholesterol_mgdl": 55.0,
        "triglycerides_mgdl": 125.0,
        "creatinine_mgdl": 0.9,
        "alt_tgp_UI_l": 25.0,
        "hemoglobin_g_dl": 14.5,
        "vitamin_d_ng_ml": 35.0
    }


@pytest.fixture
def sample_lab_data_high_values() -> dict:
    """Sample laboratory data with high values for testing alerts."""
    from datetime import date
    return {
        "patient_id": 1,
        "study_date": date(2025, 1, 15),
        "test_type": "blood_chemistry",
        "laboratory_name": "Laboratorio Chopo",
        "fasting_glucose_mgdl": 300.0,  # Very high - should trigger alert
        "hemoglobin_a1c_pct": 8.5,  # Diabetes range
        "total_cholesterol_mgdl": 250.0,  # High
        "hdl_cholesterol_mgdl": 30.0,  # Low HDL
        "triglycerides_mgdl": 250.0,  # High
        "creatinine_mgdl": 2.5  # Elevated - kidney concern
    }


@pytest.fixture
def sample_whatsapp_message_dict() -> dict:
    """Sample WhatsApp message data for testing."""
    return {
        "patient_id": 1,
        "recipient_phone": "+525512345678",
        "recipient_name": "Test Patient",
        "message_type": "appointment_reminder",
        "message_body": "Recordatorio de cita para mañana a las 10:00 AM"
    }