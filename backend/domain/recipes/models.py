"""
Recipe and meal planning domain models
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from sqlalchemy import JSON

class RecipeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    MORNING_SNACK = "morning_snack"
    LUNCH = "lunch"
    AFTERNOON_SNACK = "afternoon_snack"
    DINNER = "dinner"
    EVENING_SNACK = "evening_snack"

class DifficultyLevel(str, Enum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"

class Recipe(SQLModel, table=True):
    """Recipe model"""
    __tablename__ = "recipes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic information
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    
    # Author information
    author_type: str = Field(max_length=20)  # patient, nutritionist, system
    author_patient_id: Optional[int] = Field(default=None, foreign_key="patients.id")
    author_nutritionist_id: Optional[int] = Field(default=None, foreign_key="nutritionists.id")
    
    # Recipe details
    servings: int = Field(default=1)
    prep_time_minutes: Optional[int] = Field(default=None)
    cook_time_minutes: Optional[int] = Field(default=None)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    
    # Instructions
    instructions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    cooking_tips: Optional[str] = Field(default=None, max_length=1000)
    
    # Classification
    meal_types: Optional[List[MealType]] = Field(default=None, sa_column=Column(JSON))
    cuisine_type: Optional[str] = Field(default=None, max_length=50)
    dietary_tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Health considerations
    suitable_for_conditions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    allergen_warnings: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Cached nutritional totals (updated when ingredients change)
    total_calories: Optional[float] = Field(default=None)
    total_protein_g: Optional[float] = Field(default=None)
    total_carbs_g: Optional[float] = Field(default=None)
    total_fat_g: Optional[float] = Field(default=None)
    total_fiber_g: Optional[float] = Field(default=None)
    
    # Media and presentation
    image_url: Optional[str] = Field(default=None, max_length=500)
    video_url: Optional[str] = Field(default=None, max_length=500)
    
    # Moderation and approval
    status: RecipeStatus = Field(default=RecipeStatus.DRAFT)
    reviewed_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    reviewed_at: Optional[datetime] = Field(default=None)
    review_notes: Optional[str] = Field(default=None, max_length=500)
    
    # Engagement metrics
    rating_average: Optional[float] = Field(default=None)
    rating_count: int = Field(default=0)
    view_count: int = Field(default=0)
    
    # Version control
    version: int = Field(default=1)
    parent_recipe_id: Optional[int] = Field(default=None, foreign_key="recipes.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    items: List["RecipeItem"] = Relationship(back_populates="recipe")
    author_patient: Optional["Patient"] = Relationship(back_populates="recipes")
    author_nutritionist: Optional["Nutritionist"] = Relationship(back_populates="recipes")
    meal_entries: List["MealEntry"] = Relationship(back_populates="recipe")
    ratings: List["RecipeRating"] = Relationship(back_populates="recipe")
    
    @property
    def calories_per_serving(self) -> Optional[float]:
        if self.total_calories and self.servings:
            return self.total_calories / self.servings
        return None
    
    @property
    def total_time_minutes(self) -> Optional[int]:
        prep = self.prep_time_minutes or 0
        cook = self.cook_time_minutes or 0
        return prep + cook if prep or cook else None

class RecipeItem(SQLModel, table=True):
    """Individual ingredient in a recipe"""
    __tablename__ = "recipe_items"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.id", index=True)
    food_id: int = Field(foreign_key="foods.id", index=True)
    
    # Quantity
    quantity: float
    unit: str = Field(max_length=20)  # grams, cups, pieces, etc.
    
    # Optional preparation notes
    preparation: Optional[str] = Field(default=None, max_length=200)  # chopped, diced, etc.
    optional: bool = Field(default=False)
    
    # Display order
    order_index: int = Field(default=0)
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="items")
    food: "Food" = Relationship(back_populates="recipe_items")

class MealPlan(SQLModel, table=True):
    """Meal plan for a patient"""
    __tablename__ = "meal_plans"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    
    # Plan details
    name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    
    # Date range
    start_date: date
    end_date: Optional[date] = Field(default=None)
    
    # Daily targets (cached from nutritional goals)
    daily_calories_target: float
    daily_protein_target: float
    daily_carbs_target: float
    daily_fat_target: float
    
    # Plan generation
    generated_by: str = Field(max_length=20)  # manual, ai, template
    generation_params: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Status and approval
    is_active: bool = Field(default=True)
    approved_by_nutritionist: bool = Field(default=False)
    approved_at: Optional[datetime] = Field(default=None)
    
    # Metadata
    created_by_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: "Patient" = Relationship(back_populates="meal_plans")
    entries: List["MealEntry"] = Relationship(back_populates="meal_plan")

class MealEntry(SQLModel, table=True):
    """Individual meal entry within a meal plan"""
    __tablename__ = "meal_entries"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    meal_plan_id: int = Field(foreign_key="meal_plans.id", index=True)
    
    # Meal timing
    meal_date: date
    meal_type: MealType
    
    # Content - either recipe or ad-hoc items
    recipe_id: Optional[int] = Field(default=None, foreign_key="recipes.id")
    recipe_servings: Optional[float] = Field(default=1.0)
    
    # Alternative: ad-hoc food items (when not using a recipe)
    ad_hoc_items: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        sa_column=Column(JSON)
    )  # [{food_id, quantity, unit}, ...]
    
    # Consumption tracking
    consumed: bool = Field(default=False)
    consumed_at: Optional[datetime] = Field(default=None)
    consumption_notes: Optional[str] = Field(default=None, max_length=500)
    
    # Actual vs planned (if different)
    actual_items: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        sa_column=Column(JSON)
    )
    
    # Cached nutritional values
    planned_calories: Optional[float] = Field(default=None)
    actual_calories: Optional[float] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    meal_plan: MealPlan = Relationship(back_populates="entries")
    recipe: Optional[Recipe] = Relationship(back_populates="meal_entries")

class RecipeRating(SQLModel, table=True):
    """User ratings for recipes"""
    __tablename__ = "recipe_ratings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Rating
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    comment: Optional[str] = Field(default=None, max_length=1000)
    
    # Helpful for others
    helpful_votes: int = Field(default=0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="ratings")
    
    class Config:
        # Ensure one rating per user per recipe
        table_args = ({"unique": ("recipe_id", "user_id")},)