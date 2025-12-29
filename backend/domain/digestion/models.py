from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class StoolConsistency(str, Enum):
    LIQUID = "liquid"
    SOFT = "soft"
    NORMAL = "normal"
    HARD = "hard"
    PELLETS = "pellets"

class StoolColor(str, Enum):
    BROWN = "brown"
    BRONZE = "bronze" # Lezaeta's ideal
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"
    PALE = "pale"

class DigestionLog(SQLModel, table=True):
    """
    Daily digestion log
    Tracks Lezaeta's "Señales de buena digestión"
    """
    __tablename__ = "digestion_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    log_date: date = Field(default_factory=date.today, index=True)

    # Stool characteristics
    stool_consistency: Optional[StoolConsistency] = Field(default=None)
    stool_color: Optional[StoolColor] = Field(default=None)
    stool_odor: Optional[str] = Field(default=None) # "inodoro", "fuerte", etc.
    
    # Symptoms
    bloating: bool = Field(default=False)
    gas: bool = Field(default=False)
    acidity: bool = Field(default=False)
    abdominal_pain: bool = Field(default=False)
    
    # Overall rating (1-10)
    comfort_level: int = Field(default=5)
    
    notes: Optional[str] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    # user: Optional["User"] = Relationship(back_populates="digestion_logs")  # Disabled - mapper conflict
