"""
Nutritionist domain models
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from sqlalchemy import JSON

class VerificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

class Nutritionist(SQLModel, table=True):
    """Nutritionist profile extending User"""
    __tablename__ = "nutritionists"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    
    # Professional information
    license_number: str = Field(unique=True, max_length=50)
    university: str = Field(max_length=200)
    graduation_year: int
    
    # Specializations
    specializations: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    certifications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Practice information
    clinic_name: Optional[str] = Field(default=None, max_length=200)
    clinic_address: Optional[str] = Field(default=None, max_length=500)
    consultation_fee: Optional[float] = Field(default=None)
    
    # Verification
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    verification_documents: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    verified_at: Optional[datetime] = Field(default=None)
    verified_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Professional bio
    bio: Optional[str] = Field(default=None, max_length=2000)
    years_experience: Optional[int] = Field(default=None)
    languages: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Availability and preferences
    available_for_new_patients: bool = Field(default=True)
    max_patients: Optional[int] = Field(default=None)
    consultation_modes: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: "User" = Relationship(
        back_populates="nutritionist",
        sa_relationship_kwargs={"foreign_keys": "[Nutritionist.user_id]"}
    )
    patients: List["Patient"] = Relationship(
        back_populates="nutritionist",
        sa_relationship_kwargs={"foreign_keys": "[Patient.active_nutritionist_id]"}
    )
    consultations: List["Consultation"] = Relationship(back_populates="nutritionist")
    recipes: List["Recipe"] = Relationship(back_populates="author_nutritionist")
    
    @property
    def current_patient_count(self) -> int:
        return len([p for p in self.patients if p.active_nutritionist_id == self.id])
    
    @property
    def is_available_for_patients(self) -> bool:
        if not self.available_for_new_patients:
            return False
        if self.max_patients and self.current_patient_count >= self.max_patients:
            return False
        return self.verification_status == VerificationStatus.APPROVED

class Consultation(SQLModel, table=True):
    """Consultation record between nutritionist and patient"""
    __tablename__ = "consultations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    nutritionist_id: int = Field(foreign_key="nutritionists.id", index=True)
    
    # Consultation details
    consultation_date: datetime
    duration_minutes: Optional[int] = Field(default=None)
    consultation_type: str = Field(max_length=50)  # initial, follow_up, urgent
    
    # Clinical notes
    subjective_notes: Optional[str] = Field(default=None, max_length=2000)  # What patient reports
    objective_notes: Optional[str] = Field(default=None, max_length=2000)  # Measurements, observations
    assessment: Optional[str] = Field(default=None, max_length=2000)       # Professional assessment
    plan: Optional[str] = Field(default=None, max_length=2000)             # Treatment plan
    
    # Recommendations
    dietary_recommendations: Optional[str] = Field(default=None, max_length=2000)
    lifestyle_recommendations: Optional[str] = Field(default=None, max_length=2000)
    next_appointment: Optional[date] = Field(default=None)
    
    # Attachments and media
    attachments: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: "Patient" = Relationship(back_populates="consultations")
    nutritionist: Nutritionist = Relationship(back_populates="consultations")

class NutritionistAvailability(SQLModel, table=True):
    """Nutritionist availability schedule"""
    __tablename__ = "nutritionist_availability"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nutritionist_id: int = Field(foreign_key="nutritionists.id", index=True)
    
    # Schedule
    day_of_week: int = Field()  # 0=Monday, 6=Sunday
    start_time: str = Field(max_length=5)  # HH:MM format
    end_time: str = Field(max_length=5)    # HH:MM format
    
    # Availability settings
    is_available: bool = Field(default=True)
    consultation_duration_minutes: int = Field(default=60)
    break_between_consultations: int = Field(default=15)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)