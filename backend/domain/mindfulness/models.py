from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
from enum import Enum

class HungerLevel(int, Enum):
    STARVING = 1
    VERY_HUNGRY = 2
    HUNGRY = 3
    NEUTRAL = 4
    SATISFIED = 5
    FULL = 6
    STUFFED = 7
    SICK = 8

class HungerLog(SQLModel, table=True):
    """
    Mindful Eating: Hunger/Fullness Scale
    """
    __tablename__ = "hunger_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    log_date: date = Field(default_factory=date.today, index=True)
    log_time: datetime = Field(default_factory=datetime.utcnow)

    # Before eating
    hunger_level_before: Optional[HungerLevel] = Field(default=None)
    emotion_before: Optional[str] = Field(default=None) # Emotional eating check
    
    # After eating
    hunger_level_after: Optional[HungerLevel] = Field(default=None)
    satisfaction_level: Optional[int] = Field(default=None) # 1-10
    
    notes: Optional[str] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    # user: Optional["User"] = Relationship(back_populates="hunger_logs")  # Disabled - mapper conflict

class STOPPractice(SQLModel, table=True):
    """
    STOP Mindfulness Practice
    S: Stop
    T: Take a breath
    O: Observe
    P: Proceed
    """
    __tablename__ = "stop_practices"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    practice_time: datetime = Field(default_factory=datetime.utcnow)
    
    stress_level_before: int = Field(default=0) # 1-10
    stress_level_after: int = Field(default=0) # 1-10
    
    observations: Optional[str] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    # user: Optional["User"] = Relationship(back_populates="stop_practices")  # Disabled - mapper conflict
