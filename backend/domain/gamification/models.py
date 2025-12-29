from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Badge(SQLModel, table=True):
    __tablename__ = "badges"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    icon: str # Emoji or URL
    description: str
    category: str # "NUTRITION", "FASTING", "STREAK"
    xp_reward: int = 50
    
    # Requirement logic (simplified)
    requirement_type: str # "STREAK_DAYS", "LOG_MEALS", "EAT_FOOD"
    requirement_value: int 

    user_badges: List["UserBadge"] = Relationship(back_populates="badge")

class UserGamificationProfile(SQLModel, table=True):
    __tablename__ = "user_gamification_profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    
    level: int = Field(default=1)
    current_xp: int = Field(default=0)
    total_xp: int = Field(default=0)
    
    current_streak: int = Field(default=0)
    max_streak: int = Field(default=0)
    last_activity_date: Optional[datetime] = Field(default=None)
    
    # user: Optional["User"] = Relationship(back_populates="gamification_profile")  # Disabled - mapper conflict

class UserBadge(SQLModel, table=True):
    __tablename__ = "user_badges"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    badge_id: int = Field(foreign_key="badges.id")
    
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    
    badge: Badge = Relationship(back_populates="user_badges")
    # user: Optional["User"] = Relationship(back_populates="badges")  # Disabled - mapper conflict
