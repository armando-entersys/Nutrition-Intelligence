"""
Medicinal Plants schemas for API
Traditional Mexican Medicine Module
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from domain.medicinal_plants.models import (
    PlantCategory,
    EvidenceLevel,
    SafetyLevel,
    PreparationType
)

# ===== Base Schemas =====

class PreparationMethodSchema(BaseModel):
    """Schema for plant preparation method"""
    type: PreparationType
    dosage: str = Field(..., min_length=5, max_length=300)
    preparation: str = Field(..., min_length=10, max_length=1000)
    frequency: str = Field(..., min_length=5, max_length=200)
    duration: Optional[str] = Field(None, max_length=200)

class MedicinalPlantBase(BaseModel):
    """Base medicinal plant schema"""
    scientific_name: str = Field(..., min_length=3, max_length=300)
    botanical_family: Optional[str] = Field(None, max_length=200)
    popular_names: List[str] = Field(..., min_items=1)
    indigenous_names: Optional[Dict[str, str]] = None

    states_found: List[str] = Field(..., min_items=1)
    origin_region: Optional[str] = Field(None, max_length=200)
    growing_season: Optional[List[str]] = None

    primary_category: PlantCategory
    secondary_categories: Optional[List[PlantCategory]] = None

# ===== Create/Update Schemas =====

class MedicinalPlantCreate(MedicinalPlantBase):
    """Schema for creating a medicinal plant"""
    traditional_uses: List[str] = Field(..., min_items=1)
    indigenous_uses: Optional[Dict[str, List[str]]] = None

    preparation_methods: List[PreparationMethodSchema] = Field(..., min_items=1)

    active_compounds: Optional[List[str]] = None
    pharmacological_actions: Optional[List[str]] = None

    evidence_level: EvidenceLevel = EvidenceLevel.TRADITIONAL_ONLY
    clinical_studies_count: int = Field(default=0, ge=0)
    proven_effects: Optional[List[str]] = None

    safety_level: SafetyLevel = SafetyLevel.MODERATE
    precautions: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    adverse_effects: Optional[List[str]] = None
    drug_interactions: Optional[List[str]] = None

    safe_in_pregnancy: bool = Field(default=False)
    safe_in_lactation: bool = Field(default=False)
    safe_for_children: bool = Field(default=False)
    minimum_age_years: Optional[int] = Field(None, ge=0, le=18)

    availability_level: str = Field(default="MEDIUM")
    where_to_find: List[str] = Field(..., min_items=1)
    approximate_price_range: Optional[str] = Field(None, max_length=100)

    plant_description: Optional[str] = Field(None, max_length=5000)
    identification_features: Optional[List[str]] = None

    main_image_url: Optional[str] = Field(None, max_length=500)
    additional_images: Optional[List[str]] = None
    video_url: Optional[str] = Field(None, max_length=500)

    source: str = Field(default="UNAM", max_length=200)
    source_urls: Optional[List[str]] = None
    validated_by_expert: bool = Field(default=False)

    historical_notes: Optional[str] = Field(None, max_length=5000)
    ritual_ceremonial_use: Optional[str] = Field(None, max_length=5000)

class MedicinalPlantUpdate(BaseModel):
    """Schema for updating a medicinal plant"""
    scientific_name: Optional[str] = Field(None, min_length=3, max_length=300)
    botanical_family: Optional[str] = Field(None, max_length=200)
    popular_names: Optional[List[str]] = None
    indigenous_names: Optional[Dict[str, str]] = None

    states_found: Optional[List[str]] = None
    origin_region: Optional[str] = Field(None, max_length=200)
    growing_season: Optional[List[str]] = None

    primary_category: Optional[PlantCategory] = None
    secondary_categories: Optional[List[PlantCategory]] = None

    traditional_uses: Optional[List[str]] = None
    indigenous_uses: Optional[Dict[str, List[str]]] = None

    preparation_methods: Optional[List[Dict[str, Any]]] = None

    active_compounds: Optional[List[str]] = None
    pharmacological_actions: Optional[List[str]] = None

    evidence_level: Optional[EvidenceLevel] = None
    clinical_studies_count: Optional[int] = Field(None, ge=0)
    proven_effects: Optional[List[str]] = None

    safety_level: Optional[SafetyLevel] = None
    precautions: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    adverse_effects: Optional[List[str]] = None
    drug_interactions: Optional[List[str]] = None

    safe_in_pregnancy: Optional[bool] = None
    safe_in_lactation: Optional[bool] = None
    safe_for_children: Optional[bool] = None
    minimum_age_years: Optional[int] = Field(None, ge=0, le=18)

    availability_level: Optional[str] = None
    where_to_find: Optional[List[str]] = None
    approximate_price_range: Optional[str] = Field(None, max_length=100)

    plant_description: Optional[str] = Field(None, max_length=5000)
    identification_features: Optional[List[str]] = None

    main_image_url: Optional[str] = Field(None, max_length=500)
    additional_images: Optional[List[str]] = None
    video_url: Optional[str] = Field(None, max_length=500)

    source: Optional[str] = Field(None, max_length=200)
    source_urls: Optional[List[str]] = None
    validated_by_expert: Optional[bool] = None

    historical_notes: Optional[str] = Field(None, max_length=5000)
    ritual_ceremonial_use: Optional[str] = Field(None, max_length=5000)

    featured: Optional[bool] = None
    is_active: Optional[bool] = None

# ===== Response Schemas =====

class MedicinalPlantResponse(MedicinalPlantBase):
    """Schema for medicinal plant response"""
    id: int
    traditional_uses: List[str]
    indigenous_uses: Optional[Dict[str, List[str]]]

    preparation_methods: List[Dict[str, Any]]

    active_compounds: Optional[List[str]]
    pharmacological_actions: Optional[List[str]]

    evidence_level: EvidenceLevel
    clinical_studies_count: int
    proven_effects: Optional[List[str]]

    safety_level: SafetyLevel
    precautions: Optional[List[str]]
    contraindications: Optional[List[str]]
    adverse_effects: Optional[List[str]]
    drug_interactions: Optional[List[str]]

    safe_in_pregnancy: bool
    safe_in_lactation: bool
    safe_for_children: bool
    minimum_age_years: Optional[int]

    availability_level: str
    where_to_find: List[str]
    approximate_price_range: Optional[str]

    plant_description: Optional[str]
    identification_features: Optional[List[str]]

    main_image_url: Optional[str]
    additional_images: Optional[List[str]]
    video_url: Optional[str]

    source: str
    source_urls: Optional[List[str]]
    validated_by_expert: bool
    last_validated_at: Optional[datetime]

    historical_notes: Optional[str]
    ritual_ceremonial_use: Optional[str]

    created_at: datetime
    updated_at: datetime
    is_active: bool
    featured: bool
    view_count: int

    class Config:
        from_attributes = True

class MedicinalPlantSummary(BaseModel):
    """Abbreviated plant info for lists"""
    id: int
    scientific_name: str
    popular_names: List[str]
    primary_category: PlantCategory
    evidence_level: EvidenceLevel
    safety_level: SafetyLevel
    main_image_url: Optional[str]
    traditional_uses: List[str]

    class Config:
        from_attributes = True

# ===== User Plant Log Schemas =====

class UserPlantLogCreate(BaseModel):
    """Schema for creating user plant log"""
    plant_id: int = Field(..., gt=0)
    date_started: datetime

    preparation_type: PreparationType
    dosage_used: str = Field(..., min_length=5, max_length=300)
    frequency: str = Field(..., min_length=3, max_length=200)

    reason_for_use: str = Field(..., min_length=10, max_length=500)

    taking_medications: bool = Field(default=False)
    medications_list: Optional[List[str]] = None
    doctor_consulted: bool = Field(default=False)

    notes: Optional[str] = Field(None, max_length=2000)

class UserPlantLogUpdate(BaseModel):
    """Schema for updating user plant log"""
    date_ended: Optional[datetime] = None
    still_using: Optional[bool] = None

    dosage_used: Optional[str] = Field(None, min_length=5, max_length=300)
    frequency: Optional[str] = Field(None, min_length=3, max_length=200)

    observed_effects: Optional[str] = Field(None, max_length=2000)
    effectiveness_rating: Optional[int] = Field(None, ge=1, le=5)

    adverse_effects_experienced: Optional[str] = Field(None, max_length=2000)
    discontinued_reason: Optional[str] = Field(None, max_length=500)

    taking_medications: Optional[bool] = None
    medications_list: Optional[List[str]] = None
    doctor_consulted: Optional[bool] = None

    notes: Optional[str] = Field(None, max_length=2000)

class UserPlantLogResponse(BaseModel):
    """Schema for user plant log response"""
    id: int
    user_id: int
    plant_id: int

    date_started: datetime
    date_ended: Optional[datetime]
    still_using: bool

    preparation_type: PreparationType
    dosage_used: str
    frequency: str

    reason_for_use: str
    observed_effects: Optional[str]
    effectiveness_rating: Optional[int]

    adverse_effects_experienced: Optional[str]
    discontinued_reason: Optional[str]

    recommended_by_nutritionist: bool
    nutritionist_id: Optional[int]

    taking_medications: bool
    medications_list: Optional[List[str]]
    doctor_consulted: bool

    created_at: datetime
    updated_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True

# ===== Herbal Shop Schemas =====

class HerbalShopCreate(BaseModel):
    """Schema for creating herbal shop"""
    name: str = Field(..., min_length=3, max_length=300)
    shop_type: str = Field(..., max_length=100)

    address: str = Field(..., min_length=10, max_length=500)
    city: str = Field(..., min_length=3, max_length=100)
    state: str = Field(..., min_length=3, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=10)

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=300)

    hours_of_operation: Optional[Dict[str, str]] = None

class HerbalShopUpdate(BaseModel):
    """Schema for updating herbal shop"""
    name: Optional[str] = Field(None, min_length=3, max_length=300)
    shop_type: Optional[str] = Field(None, max_length=100)

    address: Optional[str] = Field(None, min_length=10, max_length=500)
    city: Optional[str] = Field(None, min_length=3, max_length=100)
    state: Optional[str] = Field(None, min_length=3, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=10)

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=300)

    hours_of_operation: Optional[Dict[str, str]] = None
    verified: Optional[bool] = None
    is_active: Optional[bool] = None

class HerbalShopResponse(BaseModel):
    """Schema for herbal shop response"""
    id: int
    name: str
    shop_type: str

    address: str
    city: str
    state: str
    postal_code: Optional[str]

    latitude: Optional[float]
    longitude: Optional[float]

    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]

    hours_of_operation: Optional[Dict[str, str]]

    average_rating: float
    total_reviews: int

    verified: bool
    verified_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# ===== Search and Filter Schemas =====

class PlantSearchFilters(BaseModel):
    """Schema for plant search filters"""
    categories: Optional[List[PlantCategory]] = None
    evidence_levels: Optional[List[EvidenceLevel]] = None
    safety_levels: Optional[List[SafetyLevel]] = None
    states: Optional[List[str]] = None
    safe_in_pregnancy: Optional[bool] = None
    safe_in_lactation: Optional[bool] = None
    safe_for_children: Optional[bool] = None
    availability_levels: Optional[List[str]] = None
    search_query: Optional[str] = None  # For searching by name, uses, etc.
    featured_only: Optional[bool] = None
    validated_only: Optional[bool] = None

class PlantListResponse(BaseModel):
    """Schema for paginated plant list response"""
    plants: List[MedicinalPlantSummary]
    total: int
    page: int
    page_size: int
    total_pages: int

# ===== AI Recommendation Schemas =====

class PlantRecommendationRequest(BaseModel):
    """Schema for requesting plant recommendations"""
    health_conditions: Optional[List[str]] = None
    symptoms: Optional[List[str]] = None
    user_preferences: Optional[Dict[str, Any]] = None

class PlantRecommendationResponse(BaseModel):
    """Schema for plant recommendation response"""
    id: int
    recommended_plants: List[int]  # List of plant IDs
    health_conditions: Optional[List[str]]
    symptoms: Optional[List[str]]
    ai_reasoning: Optional[str]
    confidence_score: Optional[float]
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True
