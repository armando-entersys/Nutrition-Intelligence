"""
Trophology domain models - Food combination rules based on Manuel Lezaeta Acharan (1927)
"""
from .models import FoodCategory, FoodCompatibility, FoodCombinationIssue

__all__ = [
    "FoodCategory",
    "FoodCompatibility",
    "FoodCombinationIssue",
]
