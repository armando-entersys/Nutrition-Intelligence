# Import core models first (no dependencies)
from .users.models import User
from .foods.models import Food, FoodCategory

# Import auth models
from .auth.models import AuthUser, UserRole, UserSession, UserRoleAssignment

# Import models with minimal dependencies
from .nutritionists.models import Nutritionist
from .patients.models import Patient

# Import recipe models (depend on users/foods)
from .recipes.models import (
    Recipe, RecipeItem, MealPlan, MealEntry, RecipeRating,
    RecipeStatus, MealType, DifficultyLevel
)

__all__ = [
    # Users
    "User",
    # Auth
    "AuthUser", "UserRole", "UserSession", "UserRoleAssignment",
    # Nutritionists
    "Nutritionist", 
    # Patients
    "Patient",
    # Foods
    "Food", "FoodCategory",
    # Recipes
    "Recipe", "RecipeItem", "MealPlan", "MealEntry", "RecipeRating",
    "RecipeStatus", "MealType", "DifficultyLevel"
]