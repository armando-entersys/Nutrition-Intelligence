# Import models that User depends on FIRST (before User is imported)
from .fasting.models import FastingWindow, FastingLog
from .digestion.models import DigestionLog
from .mindfulness.models import HungerLog, STOPPractice
from .gamification.models import UserGamificationProfile, Badge, UserBadge

# Import core models
from .users.models import User, UserSettings, AuditLog
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

# Import trophology models
from .trophology.models import FoodCategory as TrophologyFoodCategory, FoodCompatibility

__all__ = [
    # Fasting (must be first due to User relationships)
    "FastingWindow", "FastingLog",
    # Digestion
    "DigestionLog",
    # Mindfulness
    "HungerLog", "STOPPractice",
    # Gamification
    "UserGamificationProfile", "Badge", "UserBadge",
    # Users
    "User", "UserSettings", "AuditLog",
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
    "RecipeStatus", "MealType", "DifficultyLevel",
    # Trophology
    "TrophologyFoodCategory", "FoodCompatibility",
]