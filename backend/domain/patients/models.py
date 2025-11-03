"""
Patient domain models
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from sqlalchemy import JSON

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"          # Little to no exercise
    LIGHTLY_ACTIVE = "lightly_active"  # Light exercise 1-3 days/week
    MODERATELY_ACTIVE = "moderately_active"  # Moderate exercise 3-5 days/week
    VERY_ACTIVE = "very_active"      # Hard exercise 6-7 days/week
    EXTREMELY_ACTIVE = "extremely_active"  # Very hard exercise, physical job

class Patient(SQLModel, table=True):
    """Patient profile extending User"""
    __tablename__ = "patients"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    
    # Basic information
    date_of_birth: date
    gender: Gender
    
    # Assigned nutritionist
    active_nutritionist_id: Optional[int] = Field(
        default=None, 
        foreign_key="nutritionists.id"
    )
    
    # Objectives and goals
    primary_goal: str = Field(max_length=500)  # Weight loss, muscle gain, etc.
    target_weight_kg: Optional[float] = Field(default=None)
    target_body_fat_pct: Optional[float] = Field(default=None)
    
    # Activity and lifestyle
    activity_level: ActivityLevel = Field(default=ActivityLevel.SEDENTARY)
    occupation: Optional[str] = Field(default=None, max_length=100)
    
    # Privacy and sharing
    share_feed: bool = Field(default=False)
    allow_data_research: bool = Field(default=False)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: "User" = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"foreign_keys": "[Patient.user_id]"}
    )
    nutritionist: Optional["Nutritionist"] = Relationship(
        back_populates="patients",
        sa_relationship_kwargs={"foreign_keys": "[Patient.active_nutritionist_id]"}
    )
    anthropometric_records: List["AnthropometricRecord"] = Relationship(back_populates="patient")
    medical_history: Optional["MedicalHistory"] = Relationship(back_populates="patient")
    meal_plans: List["MealPlan"] = Relationship(back_populates="patient")
    consultations: List["Consultation"] = Relationship(back_populates="patient")
    recipes: List["Recipe"] = Relationship(back_populates="author_patient")
    laboratory_records: List["LaboratoryData"] = Relationship(back_populates="patient")
    clinical_files: List["ClinicalFile"] = Relationship(back_populates="patient")
    
    @property
    def current_age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

class AnthropometricRecord(SQLModel, table=True):
    """Anthropometric measurements record"""
    __tablename__ = "anthropometric_records"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    
    # Basic measurements
    weight_kg: float
    height_cm: Optional[float] = Field(default=None)
    
    # Body composition
    body_fat_pct: Optional[float] = Field(default=None)
    muscle_mass_kg: Optional[float] = Field(default=None)
    bone_mass_kg: Optional[float] = Field(default=None)
    water_pct: Optional[float] = Field(default=None)
    
    # Circumferences (cm)
    waist_cm: Optional[float] = Field(default=None)
    hip_cm: Optional[float] = Field(default=None)
    chest_cm: Optional[float] = Field(default=None)
    arm_cm: Optional[float] = Field(default=None)
    thigh_cm: Optional[float] = Field(default=None)
    
    # Skinfold measurements (mm)
    triceps_mm: Optional[float] = Field(default=None)
    biceps_mm: Optional[float] = Field(default=None)
    subscapular_mm: Optional[float] = Field(default=None)
    suprailiac_mm: Optional[float] = Field(default=None)
    
    # Calculated fields
    bmi: Optional[float] = Field(default=None)
    waist_hip_ratio: Optional[float] = Field(default=None)
    
    # Measurement context
    measurement_date: date = Field(default_factory=date.today)
    notes: Optional[str] = Field(default=None, max_length=1000)
    measured_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    patient: Patient = Relationship(back_populates="anthropometric_records")

class MedicalHistory(SQLModel, table=True):
    """Patient medical history and health conditions"""
    __tablename__ = "medical_histories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", unique=True)
    
    # Medical conditions
    conditions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    allergies: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    intolerances: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    medications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Family history
    family_history: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Laboratory results (latest)
    lab_results: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    lab_date: Optional[date] = Field(default=None)
    
    # Eating patterns and preferences
    eating_preferences: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    food_aversions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    dietary_restrictions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Lifestyle factors
    smoking: bool = Field(default=False)
    alcohol_consumption: str = Field(default="none", max_length=20)
    sleep_hours: Optional[float] = Field(default=None)
    stress_level: Optional[int] = Field(default=None)  # 1-10 scale
    
    # Emergency contact
    emergency_contact_name: Optional[str] = Field(default=None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)
    emergency_contact_relationship: Optional[str] = Field(default=None, max_length=50)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: Patient = Relationship(back_populates="medical_history")