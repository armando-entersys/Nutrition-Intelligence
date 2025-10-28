"""
Food schemas for API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from domain.foods.models import FoodCategory, FoodStatus, MeasurementUnit

class FoodBase(BaseModel):
    """Base food schema"""
    name: str = Field(min_length=2, max_length=200)
    common_names: Optional[List[str]] = None
    category: FoodCategory
    subcategory: Optional[str] = Field(None, max_length=100)
    base_unit: MeasurementUnit = MeasurementUnit.GRAMS
    serving_size: float = Field(gt=0, default=100.0)
    description: Optional[str] = Field(None, max_length=1000)

class NutritionalInfo(BaseModel):
    """Nutritional information schema"""
    calories_per_serving: float = Field(ge=0)
    protein_g: float = Field(ge=0, default=0.0)
    carbs_g: float = Field(ge=0, default=0.0)
    fat_g: float = Field(ge=0, default=0.0)
    fiber_g: float = Field(ge=0, default=0.0)
    sugar_g: float = Field(ge=0, default=0.0)
    sodium_mg: float = Field(ge=0, default=0.0)
    
    @validator('*', pre=True)
    def round_values(cls, v):
        if isinstance(v, (int, float)):
            return round(v, 2)
        return v

class FoodCreate(FoodBase, NutritionalInfo):
    """Schema for creating food"""
    vitamins: Optional[Dict[str, float]] = None
    minerals: Optional[Dict[str, float]] = None
    glycemic_index: Optional[int] = Field(None, ge=0, le=100)
    allergens: Optional[List[str]] = None
    dietary_flags: Optional[List[str]] = None
    disease_modifiers: Optional[Dict[str, Dict]] = None
    source: Optional[str] = Field(None, max_length=200)
    region: Optional[str] = Field(None, max_length=100)
    seasonal_availability: Optional[List[str]] = None
    average_cost_per_kg: Optional[float] = Field(None, ge=0)
    search_keywords: Optional[List[str]] = None
    barcode: Optional[str] = Field(None, max_length=50)

class FoodUpdate(BaseModel):
    """Schema for updating food"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    common_names: Optional[List[str]] = None
    category: Optional[FoodCategory] = None
    subcategory: Optional[str] = Field(None, max_length=100)
    serving_size: Optional[float] = Field(None, gt=0)
    calories_per_serving: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    fiber_g: Optional[float] = Field(None, ge=0)
    sugar_g: Optional[float] = Field(None, ge=0)
    sodium_mg: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    allergens: Optional[List[str]] = None
    dietary_flags: Optional[List[str]] = None

class FoodResponse(FoodBase, NutritionalInfo):
    """Schema for food response"""
    id: int
    status: FoodStatus
    vitamins: Optional[Dict[str, float]] = None
    minerals: Optional[Dict[str, float]] = None
    glycemic_index: Optional[int] = None
    allergens: Optional[List[str]] = []
    dietary_flags: Optional[List[str]] = []
    disease_modifiers: Optional[Dict[str, Dict]] = None
    source: Optional[str] = None
    image_url: Optional[str] = None
    barcode: Optional[str] = None
    region: Optional[str] = None
    seasonal_availability: Optional[List[str]] = []
    average_cost_per_kg: Optional[float] = None
    search_keywords: Optional[List[str]] = []
    ai_confidence_score: Optional[float] = None
    proposed_by_id: Optional[int] = None
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FoodSearchParams(BaseModel):
    """Food search parameters"""
    query: Optional[str] = None
    category: Optional[FoodCategory] = None
    status: Optional[FoodStatus] = FoodStatus.APPROVED
    dietary_flags: Optional[List[str]] = None
    allergen_free: Optional[List[str]] = None
    max_calories: Optional[float] = None
    min_protein: Optional[float] = None
    region: Optional[str] = None
    
class FoodSuggestion(BaseModel):
    """Food suggestion from AI"""
    name: str
    confidence: float = Field(ge=0, le=1)
    estimated_portion_grams: Optional[float] = None
    nutritional_estimate: Optional[NutritionalInfo] = None
    
class BatchFoodAnalysis(BaseModel):
    """Batch food analysis result"""
    image_url: str
    detected_foods: List[FoodSuggestion]
    total_estimated_calories: Optional[float] = None
    analysis_timestamp: datetime
    confidence_score: float = Field(ge=0, le=1)