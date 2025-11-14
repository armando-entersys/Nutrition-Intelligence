"""
Medicinal Plants Domain Models - Traditional Mexican Medicine
Based on UNAM's Atlas de las Plantas de la Medicina Tradicional Mexicana
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import JSON, Text

class PlantCategory(str, Enum):
    """Categories of medicinal plants by primary health benefit"""
    DIGESTIVE = "DIGESTIVE"  # Digestivas
    RESPIRATORY = "RESPIRATORY"  # Respiratorias
    CALMING = "CALMING"  # Calm antes/Ansiedad
    METABOLIC = "METABOLIC"  # Metabólicas/Diabetes
    CIRCULATORY = "CIRCULATORY"  # Circulatorias
    ANTI_INFLAMMATORY = "ANTI_INFLAMMATORY"  # Antiinflamatorias
    IMMUNOLOGICAL = "IMMUNOLOGICAL"  # Inmunológicas
    DERMATOLOGICAL = "DERMATOLOGICAL"  # Para la piel
    ANALGESIC = "ANALGESIC"  # Analgésicas
    GYNECOLOGICAL = "GYNECOLOGICAL"  # Ginecológicas
    OTHER = "OTHER"

class EvidenceLevel(str, Enum):
    """Scientific evidence level for medicinal plant efficacy"""
    HIGH = "HIGH"  # Alta evidencia científica
    MODERATE = "MODERATE"  # Evidencia moderada / uso tradicional
    LOW = "LOW"  # Poca evidencia / usar con precaución
    TRADITIONAL_ONLY = "TRADITIONAL_ONLY"  # Solo uso tradicional documentado

class SafetyLevel(str, Enum):
    """Safety level for plant consumption"""
    VERY_SAFE = "VERY_SAFE"  # Muy segura
    SAFE = "SAFE"  # Segura con dosis adecuadas
    MODERATE = "MODERATE"  # Seguridad moderada, precauciones necesarias
    CAUTION = "CAUTION"  # Usar con precaución
    RESTRICTED = "RESTRICTED"  # Uso restringido, solo bajo supervisión

class PreparationType(str, Enum):
    """Methods of preparing medicinal plants"""
    TEA = "TEA"  # Té/Infusión
    DECOCTION = "DECOCTION"  # Cocimiento/Decocción
    TINCTURE = "TINCTURE"  # Tintura
    POULTICE = "POULTICE"  # Cataplasma
    SYRUP = "SYRUP"  # Jarabe
    EXTRACT = "EXTRACT"  # Extracto
    FRESH = "FRESH"  # Fresco/directo
    POWDER = "POWDER"  # Polvo
    BATH = "BATH"  # Baño
    INHALATION = "INHALATION"  # Inhalación/Vapor

class MedicinalPlant(SQLModel, table=True):
    """Mexican Medicinal Plant - Main model"""
    __tablename__ = "medicinal_plants"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic botanical information
    scientific_name: str = Field(max_length=300, index=True, unique=True)
    botanical_family: Optional[str] = Field(default=None, max_length=200)
    popular_names: List[str] = Field(sa_column=Column(JSON))  # Nombres comunes
    indigenous_names: Optional[Dict[str, str]] = Field(default=None, sa_column=Column(JSON))  # {language: name}

    # Regional information
    states_found: List[str] = Field(sa_column=Column(JSON))  # Mexican states where it grows
    origin_region: Optional[str] = Field(default=None, max_length=200)  # Native/naturalized info
    growing_season: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # Months available

    # Classification
    primary_category: PlantCategory
    secondary_categories: Optional[List[PlantCategory]] = Field(default=None, sa_column=Column(JSON))

    # Traditional uses
    traditional_uses: List[str] = Field(sa_column=Column(JSON))  # Traditional indications
    indigenous_uses: Optional[Dict[str, List[str]]] = Field(
        default=None,
        sa_column=Column(JSON)
    )  # {culture: [uses]}

    # Preparation methods with detailed instructions
    preparation_methods: List[Dict[str, Any]] = Field(sa_column=Column(JSON))
    # Example: [{
    #     "type": "TEA",
    #     "dosage": "1 cucharada de flores por taza",
    #     "preparation": "Hervir agua, agregar flores, reposar 5 min",
    #     "frequency": "2-3 tazas al día",
    #     "duration": "Hasta mejoría de síntomas"
    # }]

    # Active compounds and pharmacology
    active_compounds: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    pharmacological_actions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Scientific validation
    evidence_level: EvidenceLevel
    clinical_studies_count: int = Field(default=0)
    proven_effects: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Safety information
    safety_level: SafetyLevel
    precautions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    contraindications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    adverse_effects: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    drug_interactions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Special populations
    safe_in_pregnancy: bool = Field(default=False)
    safe_in_lactation: bool = Field(default=False)
    safe_for_children: bool = Field(default=False)
    minimum_age_years: Optional[int] = Field(default=None)

    # Availability in Mexico
    availability_level: str = Field(default="MEDIUM")  # HIGH/MEDIUM/LOW
    where_to_find: List[str] = Field(sa_column=Column(JSON))  # Markets, herbalists, etc.
    approximate_price_range: Optional[str] = Field(default=None, max_length=100)  # e.g. "$15-30 MXN por 50g"

    # Botanical description
    plant_description: Optional[str] = Field(default=None, sa_column=Column(Text))
    identification_features: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Media
    main_image_url: Optional[str] = Field(default=None, max_length=500)
    additional_images: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    video_url: Optional[str] = Field(default=None, max_length=500)  # Preparation guide video

    # Source and validation
    source: str = Field(default="UNAM", max_length=200)  # UNAM, scientific literature, etc.
    source_urls: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    validated_by_expert: bool = Field(default=False)
    last_validated_at: Optional[datetime] = Field(default=None)

    # Cultural and historical context
    historical_notes: Optional[str] = Field(default=None, sa_column=Column(Text))
    ritual_ceremonial_use: Optional[str] = Field(default=None, sa_column=Column(Text))

    # Relationships
    user_logs: List["UserPlantLog"] = Relationship(back_populates="plant")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    featured: bool = Field(default=False)  # Featured plants for homepage
    view_count: int = Field(default=0)


class UserPlantLog(SQLModel, table=True):
    """User log of medicinal plant usage and effects"""
    __tablename__ = "user_plant_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    # User relationship
    user_id: int = Field(foreign_key="users.id", index=True)

    # Plant relationship
    plant_id: int = Field(foreign_key="medicinal_plants.id", index=True)
    plant: MedicinalPlant = Relationship(back_populates="user_logs")

    # Usage details
    date_started: datetime
    date_ended: Optional[datetime] = Field(default=None)
    still_using: bool = Field(default=True)

    # Preparation used
    preparation_type: PreparationType
    dosage_used: str = Field(max_length=300)
    frequency: str = Field(max_length=200)  # "2 veces al día", etc.

    # Purpose and effects
    reason_for_use: str = Field(max_length=500)  # Why they're using it
    observed_effects: Optional[str] = Field(default=None, sa_column=Column(Text))  # Subjective effects
    effectiveness_rating: Optional[int] = Field(default=None)  # 1-5 stars

    # Safety monitoring
    adverse_effects_experienced: Optional[str] = Field(default=None, sa_column=Column(Text))
    discontinued_reason: Optional[str] = Field(default=None, max_length=500)

    # Nutritionist involvement
    recommended_by_nutritionist: bool = Field(default=False)
    nutritionist_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Medication interaction tracking
    taking_medications: bool = Field(default=False)
    medications_list: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    doctor_consulted: bool = Field(default=False)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None, sa_column=Column(Text))


class PlantHealthCondition(SQLModel, table=True):
    """Mapping between plants and health conditions they address"""
    __tablename__ = "plant_health_conditions"

    id: Optional[int] = Field(default=None, primary_key=True)

    plant_id: int = Field(foreign_key="medicinal_plants.id", index=True)

    # Health condition
    condition_name: str = Field(max_length=200, index=True)  # e.g., "Diabetes tipo 2"
    condition_category: str = Field(max_length=100)  # e.g., "METABOLIC"

    # Effectiveness for this condition
    effectiveness_level: EvidenceLevel
    traditional_use: bool = Field(default=True)
    scientific_evidence: bool = Field(default=False)

    # Details
    mechanism_of_action: Optional[str] = Field(default=None, sa_column=Column(Text))
    recommended_dosage: Optional[str] = Field(default=None, max_length=500)
    treatment_duration: Optional[str] = Field(default=None, max_length=200)

    # Supporting evidence
    studies_references: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)


class HerbalShop(SQLModel, table=True):
    """Herbal shops and markets where plants can be purchased"""
    __tablename__ = "herbal_shops"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Shop information
    name: str = Field(max_length=300)
    shop_type: str = Field(max_length=100)  # HERBOLARIA, MERCADO, TIENDA_BIENESTAR, FARMACIA

    # Location
    address: str = Field(max_length=500)
    city: str = Field(max_length=100, index=True)
    state: str = Field(max_length=100, index=True)
    postal_code: Optional[str] = Field(default=None, max_length=10)

    # Geographic coordinates
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    # Contact
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=200)
    website: Optional[str] = Field(default=None, max_length=300)

    # Operating hours
    hours_of_operation: Optional[Dict[str, str]] = Field(default=None, sa_column=Column(JSON))

    # Community rating
    average_rating: float = Field(default=0.0)
    total_reviews: int = Field(default=0)

    # Verification
    verified: bool = Field(default=False)
    verified_at: Optional[datetime] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class PlantRecommendation(SQLModel, table=True):
    """AI-generated plant recommendations for users"""
    __tablename__ = "plant_recommendations"

    id: Optional[int] = Field(default=None, primary_key=True)

    # User relationship
    user_id: int = Field(foreign_key="users.id", index=True)

    # Recommended plants (ordered by relevance)
    recommended_plants: List[int] = Field(sa_column=Column(JSON))  # List of plant IDs

    # Recommendation context
    based_on_health_profile: bool = Field(default=True)
    health_conditions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    symptoms: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # AI reasoning
    ai_reasoning: Optional[str] = Field(default=None, sa_column=Column(Text))
    confidence_score: Optional[float] = Field(default=None)  # 0.0 - 1.0

    # User interaction
    user_viewed: bool = Field(default=False)
    user_accepted: Optional[bool] = Field(default=None)
    user_feedback: Optional[str] = Field(default=None, max_length=500)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)  # Recommendations expire after 30 days
