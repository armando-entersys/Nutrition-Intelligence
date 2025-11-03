"""
WhatsApp messaging models
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Type of WhatsApp message"""
    APPOINTMENT_REMINDER = "appointment_reminder"
    MEAL_PLAN_READY = "meal_plan_ready"
    LAB_RESULTS = "lab_results"
    MOTIVATIONAL = "motivational"
    FOLLOW_UP = "follow_up"
    CUSTOM = "custom"


class MessageStatus(str, Enum):
    """Status of WhatsApp message"""
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class WhatsAppMessage(SQLModel, table=True):
    """WhatsApp message record"""
    __tablename__ = "whatsapp_messages"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Recipient information
    patient_id: Optional[int] = Field(default=None, foreign_key="patients.id", index=True)
    recipient_phone: str = Field(max_length=20)  # Format: +52XXXXXXXXXX
    recipient_name: Optional[str] = Field(default=None, max_length=200)

    # Message content
    message_type: MessageType
    message_body: str = Field(max_length=1600)  # WhatsApp limit

    # Twilio details
    twilio_sid: Optional[str] = Field(default=None, max_length=100)
    status: MessageStatus = Field(default=MessageStatus.QUEUED)
    error_message: Optional[str] = Field(default=None, max_length=500)

    # Metadata
    sent_at: Optional[datetime] = Field(default=None)
    delivered_at: Optional[datetime] = Field(default=None)
    read_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: int = Field(foreign_key="users.id")  # Nutritionist who sent it

    # Scheduling
    scheduled_for: Optional[datetime] = Field(default=None)
    is_scheduled: bool = Field(default=False)


class WhatsAppTemplate(SQLModel, table=True):
    """Pre-defined WhatsApp message templates"""
    __tablename__ = "whatsapp_templates"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100, unique=True)
    message_type: MessageType
    template_body: str = Field(max_length=1600)

    # Variables that can be replaced in template
    # Example: "Hola {patient_name}, tu cita es el {appointment_date}"
    variables: Optional[str] = Field(default=None)  # Store as JSON string

    # Metadata
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: int = Field(foreign_key="users.id")


class WhatsAppCampaign(SQLModel, table=True):
    """WhatsApp campaigns for bulk messaging"""
    __tablename__ = "whatsapp_campaigns"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    message_type: MessageType
    template_id: Optional[int] = Field(default=None, foreign_key="whatsapp_templates.id")

    # Target audience
    target_all_patients: bool = Field(default=False)
    target_patient_ids: Optional[str] = Field(default=None)  # Store as JSON string of patient IDs

    # Campaign status
    status: str = Field(max_length=20, default="draft")  # draft, scheduled, sending, completed, failed
    total_recipients: int = Field(default=0)
    messages_sent: int = Field(default=0)
    messages_delivered: int = Field(default=0)
    messages_failed: int = Field(default=0)

    # Scheduling
    scheduled_for: Optional[datetime] = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: int = Field(foreign_key="users.id")
