"""
Intermittent Fasting domain models
Integrates with Lezaeta's principle: "Dejar descansar los órganos"
Validated by research 2024-2025 on autophagy and gut rest
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date, time

class FastingWindow(SQLModel, table=True):
    """
    User's configured fasting window (eating window)

    Example:
    - start_time: 10:00 (window opens at 10am)
    - end_time: 18:00 (window closes at 6pm)
    - duration_hours: 8 (8-hour eating window)
    - Implies: 16-hour fasting window (16:8 protocol)
    """
    __tablename__ = "fasting_windows"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to user
    user_id: int = Field(foreign_key="users.id", index=True)

    # Window configuration
    start_time: time = Field()  # When eating window opens (e.g., 10:00)
    end_time: time = Field()    # When eating window closes (e.g., 18:00)
    duration_hours: int = Field()  # Duration of eating window (e.g., 8)

    # Status
    active: bool = Field(default=True)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationships
    # user: Optional["User"] = Relationship(back_populates="fasting_window")  # Disabled - mapper conflict
    logs: List["FastingLog"] = Relationship(back_populates="window")


class FastingLog(SQLModel, table=True):
    """
    Daily fasting log - tracks actual fasting compliance

    Records:
    - First meal time (breaks fast)
    - Last meal time (starts fast)
    - Calculated fasting hours
    - Autophagy hours (hours >12, when autophagy activates)
    - Adherence to configured window
    """
    __tablename__ = "fasting_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    user_id: int = Field(foreign_key="users.id", index=True)
    window_id: int = Field(foreign_key="fasting_windows.id", index=True)

    # Date of this log
    log_date: date = Field(index=True)

    # Actual meal times
    first_meal_time: Optional[datetime] = Field(default=None)
    last_meal_time: Optional[datetime] = Field(default=None)

    # Calculated metrics
    fasting_hours: Optional[float] = Field(default=None)  # Total hours fasted
    autophagy_hours: Optional[float] = Field(default=None)  # Hours >12 (autophagy activated)

    # Compliance
    adherence: Optional[bool] = Field(default=None)  # Did user follow configured window?

    # User notes
    notes: Optional[str] = Field(default=None)

    # Energy level during fast (1-10)
    energy_level: Optional[int] = Field(default=None)

    # Mental clarity during fast (1-10)
    mental_clarity: Optional[int] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationships
    # user: Optional["User"] = Relationship(back_populates="fasting_logs")  # Disabled - mapper conflict
    window: FastingWindow = Relationship(back_populates="logs")


class FastingStats(SQLModel):
    """
    Pydantic model (not a table) for fasting statistics
    Used in API responses for dashboard
    """
    # Current status
    in_fasting_window: bool
    current_fast_hours: float
    autophagy_active: bool

    # Window info
    window_start: str  # "10:00"
    window_end: str    # "18:00"

    # Time tracking
    time_until_window_start: int  # minutes
    time_until_window_end: int    # minutes

    # Recent performance
    adherence_7d: float   # % adherence last 7 days
    adherence_30d: float  # % adherence last 30 days
    total_autophagy_hours_7d: float
    total_autophagy_hours_30d: float
    avg_fasting_hours_7d: float
    avg_fasting_hours_30d: float

    # Streak
    current_streak: int  # consecutive days of adherence
    longest_streak: int
