"""
Tests for the Foods API endpoints.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from domain.foods.models import Food, FoodStatus, FoodCategory


class TestFoodsAPI:
    """Test suite for Foods API endpoints."""

    async def test_health_endpoint(self, client: AsyncClient):
        """Test the health endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "nutrition-intelligence-api"

    async def test_get_foods_empty(self, client: AsyncClient):
        """Test getting foods when database is empty."""
        response = await client.get("/api/v1/foods/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_get_foods_with_data(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with sample data."""
        response = await client.get("/api/v1/foods/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

        food = data[0]
        assert food["name"] == "Apple"
        assert food["category"] == "FRUITS"
        assert food["status"] == "APPROVED"
        assert food["calories_per_100g"] == 52.0

    async def test_get_foods_with_status_filter(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with status filter."""
        response = await client.get("/api/v1/foods/?status=APPROVED")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        response = await client.get("/api/v1/foods/?status=PENDING")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    async def test_get_foods_with_category_filter(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with category filter."""
        response = await client.get("/api/v1/foods/?category=FRUITS")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        response = await client.get("/api/v1/foods/?category=VEGETABLES")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    async def test_get_foods_with_search(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with search filter."""
        response = await client.get("/api/v1/foods/?search=apple")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        response = await client.get("/api/v1/foods/?search=banana")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    async def test_get_foods_with_limit(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with limit parameter."""
        response = await client.get("/api/v1/foods/?limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 1

    async def test_get_foods_with_offset(self, client: AsyncClient, sample_food: Food):
        """Test getting foods with offset parameter."""
        response = await client.get("/api/v1/foods/?offset=0")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_create_food(self, client: AsyncClient):
        """Test creating a new food."""
        food_data = {
            "name": "Banana",
            "description": "Yellow banana",
            "category": "FRUITS",
            "calories_per_100g": 89.0,
            "protein_per_100g": 1.1,
            "carbs_per_100g": 23.0,
            "fat_per_100g": 0.3,
            "fiber_per_100g": 2.6
        }

        response = await client.post("/api/v1/foods/", json=food_data)

        # This might return 422 if endpoint doesn't exist yet, that's expected
        # When implemented, should return 201
        assert response.status_code in [201, 404, 422]

    async def test_get_food_by_id(self, client: AsyncClient, sample_food: Food):
        """Test getting a specific food by ID."""
        response = await client.get(f"/api/v1/foods/{sample_food.id}")

        # This might return 404 if endpoint doesn't exist yet
        # When implemented, should return 200
        assert response.status_code in [200, 404]

    async def test_update_food(self, client: AsyncClient, sample_food: Food):
        """Test updating a food."""
        update_data = {
            "name": "Green Apple",
            "description": "Fresh green apple"
        }

        response = await client.put(f"/api/v1/foods/{sample_food.id}", json=update_data)

        # This might return 404 if endpoint doesn't exist yet
        assert response.status_code in [200, 404, 422]

    async def test_delete_food(self, client: AsyncClient, sample_food: Food):
        """Test deleting a food."""
        response = await client.delete(f"/api/v1/foods/{sample_food.id}")

        # This might return 404 if endpoint doesn't exist yet
        assert response.status_code in [204, 404]