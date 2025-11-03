"""
Food and nutrition domain models
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import JSON

class FoodStatus(str, Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"

class FoodCategory(str, Enum):
    CEREALS = "CEREALS"
    VEGETABLES = "VEGETABLES"
    FRUITS = "FRUITS"
    LEGUMES = "LEGUMES"
    ANIMAL_PRODUCTS = "ANIMAL_PRODUCTS"
    FATS = "FATS"
    SUGARS = "SUGARS"
    FREE_FOODS = "FREE_FOODS"
    DAIRY = "DAIRY"
    BEVERAGES = "BEVERAGES"

class MeasurementUnit(str, Enum):
    GRAMS = "g"
    MILLILITERS = "ml"
    PIECES = "pcs"
    CUPS = "cups"
    TABLESPOONS = "tbsp"
    TEASPOONS = "tsp"
    SLICES = "slices"

class Food(SQLModel, table=True):
    """Food item in the database"""
    __tablename__ = "foods"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic information
    name: str = Field(max_length=200, index=True)
    common_names: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    category: FoodCategory
    subcategory: Optional[str] = Field(default=None, max_length=100)
    
    # Measurement
    base_unit: MeasurementUnit = Field(default=MeasurementUnit.GRAMS)
    serving_size: float = Field(default=100.0)  # Amount per base unit
    
    # Nutritional information (per serving_size)
    calories_per_serving: float
    protein_g: float = Field(default=0.0)
    carbs_g: float = Field(default=0.0)
    fat_g: float = Field(default=0.0)
    fiber_g: float = Field(default=0.0)
    sugar_g: float = Field(default=0.0)
    sodium_mg: float = Field(default=0.0)
    
    # Micronutrients (optional)
    vitamins: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    minerals: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    
    # Health considerations
    glycemic_index: Optional[int] = Field(default=None)
    allergens: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    dietary_flags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # vegan, gluten-free, etc.
    
    # Medical conditions modifiers
    disease_modifiers: Optional[Dict[str, Dict[str, Any]]] = Field(
        default=None, 
        sa_column=Column(JSON)
    )  # diabetes, renal, etc.
    
    # Administration
    status: FoodStatus = Field(default=FoodStatus.PENDING)
    proposed_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    approved_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    approved_at: Optional[datetime] = Field(default=None)
    
    # Metadata
    description: Optional[str] = Field(default=None, max_length=1000)
    source: Optional[str] = Field(default=None, max_length=200)  # SMAE, USDA, etc.
    image_url: Optional[str] = Field(default=None, max_length=500)
    barcode: Optional[str] = Field(default=None, max_length=50)
    
    # Regional information
    region: Optional[str] = Field(default=None, max_length=100)
    seasonal_availability: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    average_cost_per_kg: Optional[float] = Field(default=None)
    
    # Search and AI
    search_keywords: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    ai_confidence_score: Optional[float] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    recipe_items: List["RecipeItem"] = Relationship(back_populates="food")
    
    @property
    def calories_per_100g(self) -> float:
        """Standardize calories per 100g"""
        if self.serving_size == 100:
            return self.calories_per_serving
        return (self.calories_per_serving / self.serving_size) * 100
    
    @property
    def macros_per_100g(self) -> Dict[str, float]:
        """Get macronutrients per 100g"""
        multiplier = 100 / self.serving_size
        return {
            "protein": self.protein_g * multiplier,
            "carbs": self.carbs_g * multiplier,
            "fat": self.fat_g * multiplier,
            "fiber": self.fiber_g * multiplier
        }

class FoodEquivalent(SQLModel, table=True):
    """Food equivalents for diabetic exchanges"""
    __tablename__ = "food_equivalents"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    food_id: int = Field(foreign_key="foods.id", index=True)
    
    # Exchange system equivalents
    cereal_exchanges: float = Field(default=0.0)
    vegetable_exchanges: float = Field(default=0.0)
    fruit_exchanges: float = Field(default=0.0)
    legume_exchanges: float = Field(default=0.0)
    meat_exchanges: float = Field(default=0.0)
    fat_exchanges: float = Field(default=0.0)
    milk_exchanges: float = Field(default=0.0)
    
    # Portion sizes for each exchange
    portion_for_exchange: Optional[Dict[str, str]] = Field(
        default=None, 
        sa_column=Column(JSON)
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

class NutritionalGoal(SQLModel, table=True):
    """Nutritional goals and targets"""
    __tablename__ = "nutritional_goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    
    # Energy targets
    daily_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    
    # Micronutrient targets
    sodium_mg: Optional[float] = Field(default=None)
    potassium_mg: Optional[float] = Field(default=None)
    calcium_mg: Optional[float] = Field(default=None)
    iron_mg: Optional[float] = Field(default=None)
    
    # Medical condition adjustments
    condition_adjustments: Optional[Dict[str, Dict[str, Any]]] = Field(
        default=None, 
        sa_column=Column(JSON)
    )
    
    # Calculation method used
    calculation_method: str = Field(max_length=50)  # Harris-Benedict, Mifflin, etc.
    calculation_details: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Goal period
    effective_from: datetime = Field(default_factory=datetime.utcnow)
    effective_until: Optional[datetime] = Field(default=None)
    
    # Metadata
    created_by_id: int = Field(foreign_key="users.id")
    notes: Optional[str] = Field(default=None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)