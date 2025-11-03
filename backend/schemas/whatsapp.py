"""
WhatsApp API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from domain.messaging.whatsapp import MessageType, MessageStatus


# Message Schemas
class WhatsAppMessageBase(BaseModel):
    """Base WhatsApp message schema"""
    patient_id: Optional[int] = None
    recipient_phone: str = Field(..., description="Format: +52XXXXXXXXXX")
    recipient_name: Optional[str] = None
    message_type: MessageType
    message_body: str = Field(..., max_length=1600)
    scheduled_for: Optional[datetime] = None


class WhatsAppMessageCreate(WhatsAppMessageBase):
    """Create WhatsApp message"""
    pass


class WhatsAppMessageResponse(WhatsAppMessageBase):
    """WhatsApp message response"""
    id: int
    twilio_sid: Optional[str] = None
    status: MessageStatus
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime
    created_by_id: int
    is_scheduled: bool

    class Config:
        from_attributes = True


# Quick Send Schemas
class SendAppointmentReminderRequest(BaseModel):
    """Send appointment reminder"""
    patient_id: int
    patient_name: str
    patient_phone: str
    appointment_date: str  # Format: "Lunes 15 de Enero, 2024"
    appointment_time: str  # Format: "10:00 AM"
    nutritionist_name: str
    nutritionist_id: int


class SendMealPlanNotificationRequest(BaseModel):
    """Send meal plan notification"""
    patient_id: int
    patient_name: str
    patient_phone: str
    nutritionist_name: str
    nutritionist_id: int


class SendLabResultsNotificationRequest(BaseModel):
    """Send lab results notification"""
    patient_id: int
    patient_name: str
    patient_phone: str
    lab_type: str  # e.g., "Química Sanguínea", "Perfil Lipídico"
    nutritionist_id: int


class SendMotivationalMessageRequest(BaseModel):
    """Send motivational message"""
    patient_id: int
    patient_name: str
    patient_phone: str
    message_text: str = Field(..., max_length=1000)
    nutritionist_id: int


class SendFollowUpMessageRequest(BaseModel):
    """Send follow-up message"""
    patient_id: int
    patient_name: str
    patient_phone: str
    days_since_last_visit: int
    nutritionist_name: str
    nutritionist_id: int


class SendCustomMessageRequest(BaseModel):
    """Send custom message"""
    patient_id: Optional[int] = None
    recipient_phone: str
    recipient_name: Optional[str] = None
    message_body: str = Field(..., max_length=1600)
    nutritionist_id: int


# Template Schemas
class WhatsAppTemplateBase(BaseModel):
    """Base template schema"""
    name: str = Field(..., max_length=100)
    message_type: MessageType
    template_body: str = Field(..., max_length=1600)
    variables: Optional[List[str]] = None
    is_active: bool = True


class WhatsAppTemplateCreate(WhatsAppTemplateBase):
    """Create template"""
    pass


class WhatsAppTemplateUpdate(BaseModel):
    """Update template"""
    name: Optional[str] = None
    template_body: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None


class WhatsAppTemplateResponse(WhatsAppTemplateBase):
    """Template response"""
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True


# Campaign Schemas
class WhatsAppCampaignBase(BaseModel):
    """Base campaign schema"""
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    message_type: MessageType
    template_id: Optional[int] = None
    target_all_patients: bool = False
    target_patient_ids: Optional[List[int]] = None
    scheduled_for: Optional[datetime] = None


class WhatsAppCampaignCreate(WhatsAppCampaignBase):
    """Create campaign"""
    pass


class WhatsAppCampaignResponse(WhatsAppCampaignBase):
    """Campaign response"""
    id: int
    status: str
    total_recipients: int
    messages_sent: int
    messages_delivered: int
    messages_failed: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True


# Response Schemas
class MessageSentResponse(BaseModel):
    """Response after sending message"""
    success: bool
    message_id: Optional[int] = None
    twilio_sid: Optional[str] = None
    status: str
    sent_at: Optional[str] = None
    error: Optional[str] = None
    note: Optional[str] = None


class MessageListResponse(BaseModel):
    """List of messages with pagination"""
    items: List[WhatsAppMessageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
