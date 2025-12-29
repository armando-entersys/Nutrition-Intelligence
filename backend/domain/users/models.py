"""
User domain models
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import JSON

from core.security import UserRole

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(SQLModel, table=True):
    """Base user model"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.PATIENT)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    
    # Profile information
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    last_login: Optional[datetime] = Field(default=None)
    
    # Verification
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    
    # Relationships
    nutritionist: Optional["Nutritionist"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Nutritionist.user_id]"}
    )
    patient: Optional["Patient"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Patient.user_id]"}
    )
    audit_logs: List["AuditLog"] = Relationship(back_populates="actor")

    # Note: Fasting, Digestion, Mindfulness, Gamification relationships temporarily disabled
    # These models use a different SQLModel registry causing mapper conflicts
    # TODO: Fix model registry to enable these relationships
    # fasting_window: Optional["FastingWindow"] = Relationship(back_populates="user")
    # fasting_logs: List["FastingLog"] = Relationship(back_populates="user")
    # digestion_logs: List["DigestionLog"] = Relationship(back_populates="user")
    # hunger_logs: List["HungerLog"] = Relationship(back_populates="user")
    # stop_practices: List["STOPPractice"] = Relationship(back_populates="user")
    # gamification_profile: Optional["UserGamificationProfile"] = Relationship(back_populates="user")
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def is_nutritionist(self) -> bool:
        return self.role == UserRole.NUTRITIONIST
    
    def is_patient(self) -> bool:
        return self.role == UserRole.PATIENT
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

class UserSettings(SQLModel, table=True):
    """User preferences and settings"""
    __tablename__ = "user_settings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    
    # Notification preferences
    email_notifications: bool = Field(default=True)
    push_notifications: bool = Field(default=True)
    
    # Privacy settings
    share_profile: bool = Field(default=False)
    share_progress: bool = Field(default=False)
    
    # App preferences
    language: str = Field(default="es", max_length=5)
    timezone: str = Field(default="America/Mexico_City", max_length=50)
    theme: str = Field(default="light", max_length=10)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

class AuditLog(SQLModel, table=True):
    """Audit log for compliance"""
    __tablename__ = "audit_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    actor_id: int = Field(foreign_key="users.id", index=True)
    
    # Action details
    action: str = Field(max_length=100, index=True)
    entity_type: str = Field(max_length=50, index=True)
    entity_id: Optional[int] = Field(default=None, index=True)
    
    # Context
    changed_fields: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    request_id: Optional[str] = Field(default=None, max_length=36)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Relationships
    actor: User = Relationship(back_populates="audit_logs")