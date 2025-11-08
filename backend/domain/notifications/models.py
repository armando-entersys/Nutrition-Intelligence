"""
Notification Models
System for user notifications and alerts
"""
from sqlmodel import SQLModel, Field, Column
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from sqlalchemy import JSON


class NotificationType(str, Enum):
    """Types of notifications"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    APPOINTMENT = "appointment"
    MEAL_PLAN = "meal_plan"
    PROGRESS = "progress"
    SYSTEM = "system"


class NotificationPriority(str, Enum):
    """Priority levels for notifications"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationStatus(str, Enum):
    """Status of a notification"""
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class Notification(SQLModel, table=True):
    """
    User notifications
    Stores all types of notifications for users
    """
    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)

    # User relationship
    user_id: int = Field(foreign_key="auth_users.id", index=True)

    # Notification content
    title: str = Field(max_length=255)
    message: str = Field(max_length=1000)
    icon: Optional[str] = Field(default=None, max_length=50, description="Emoji or icon identifier")

    # Classification
    type: NotificationType = Field(default=NotificationType.INFO, index=True)
    priority: NotificationPriority = Field(default=NotificationPriority.MEDIUM, index=True)
    status: NotificationStatus = Field(default=NotificationStatus.UNREAD, index=True)

    # Action/Navigation
    action: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Action payload (e.g., {type: 'navigate', target: 'appointments'})"
    )
    action_url: Optional[str] = Field(default=None, max_length=500, description="URL to navigate to")
    action_label: Optional[str] = Field(default=None, max_length=100, description="Action button label")

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Additional metadata for the notification"
    )

    # Related entities
    related_entity_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Type of related entity (patient, meal_plan, appointment, etc.)"
    )
    related_entity_id: Optional[int] = Field(
        default=None,
        description="ID of the related entity"
    )

    # Scheduling
    scheduled_for: Optional[datetime] = Field(
        default=None,
        description="When to show this notification (for scheduled notifications)"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="When this notification expires and should be auto-archived"
    )

    # Read tracking
    read_at: Optional[datetime] = Field(default=None)
    archived_at: Optional[datetime] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: Optional[datetime] = Field(default=None)

    @property
    def is_read(self) -> bool:
        """Check if notification is read"""
        return self.status == NotificationStatus.READ or self.read_at is not None

    @property
    def is_expired(self) -> bool:
        """Check if notification is expired"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False

    @property
    def time_ago(self) -> str:
        """Get human-readable time ago"""
        delta = datetime.utcnow() - self.created_at

        if delta.days > 365:
            years = delta.days // 365
            return f"hace {years} año{'s' if years > 1 else ''}"
        elif delta.days > 30:
            months = delta.days // 30
            return f"hace {months} mes{'es' if months > 1 else ''}"
        elif delta.days > 0:
            return f"hace {delta.days} día{'s' if delta.days > 1 else ''}"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"hace {hours} hora{'s' if hours > 1 else ''}"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "hace unos segundos"

    def mark_as_read(self) -> None:
        """Mark notification as read"""
        if self.status == NotificationStatus.UNREAD:
            self.status = NotificationStatus.READ
            self.read_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def mark_as_unread(self) -> None:
        """Mark notification as unread"""
        if self.status == NotificationStatus.READ:
            self.status = NotificationStatus.UNREAD
            self.read_at = None
            self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive notification"""
        self.status = NotificationStatus.ARCHIVED
        self.archived_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


# Helper functions for creating notifications
def create_appointment_notification(
    user_id: int,
    appointment_date: datetime,
    patient_name: str,
    appointment_id: int
) -> Notification:
    """Create an appointment reminder notification"""
    return Notification(
        user_id=user_id,
        title="Cita Programada",
        message=f"Tienes una cita con {patient_name} programada",
        icon="📅",
        type=NotificationType.APPOINTMENT,
        priority=NotificationPriority.HIGH,
        action={
            "type": "navigate",
            "target": f"appointments/{appointment_id}"
        },
        action_label="Ver cita",
        related_entity_type="appointment",
        related_entity_id=appointment_id,
        scheduled_for=appointment_date
    )


def create_meal_plan_notification(
    user_id: int,
    meal_plan_name: str,
    meal_plan_id: int
) -> Notification:
    """Create a meal plan update notification"""
    return Notification(
        user_id=user_id,
        title="Plan Alimenticio Actualizado",
        message=f"Tu plan '{meal_plan_name}' ha sido actualizado",
        icon="🍽️",
        type=NotificationType.MEAL_PLAN,
        priority=NotificationPriority.MEDIUM,
        action={
            "type": "navigate",
            "target": f"meal-plans/{meal_plan_id}"
        },
        action_label="Ver plan",
        related_entity_type="meal_plan",
        related_entity_id=meal_plan_id
    )


def create_progress_notification(
    user_id: int,
    message: str,
    priority: NotificationPriority = NotificationPriority.LOW
) -> Notification:
    """Create a progress tracking notification"""
    return Notification(
        user_id=user_id,
        title="Actualización de Progreso",
        message=message,
        icon="📊",
        type=NotificationType.PROGRESS,
        priority=priority,
        action={
            "type": "navigate",
            "target": "progress"
        },
        action_label="Ver progreso"
    )


def create_system_notification(
    user_id: int,
    title: str,
    message: str,
    priority: NotificationPriority = NotificationPriority.LOW
) -> Notification:
    """Create a system notification"""
    return Notification(
        user_id=user_id,
        title=title,
        message=message,
        icon="🔔",
        type=NotificationType.SYSTEM,
        priority=priority
    )
