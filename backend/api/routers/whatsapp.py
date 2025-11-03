"""
WhatsApp API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Form, Request
from fastapi.responses import Response
from sqlmodel import Session, select, desc, func
from typing import List, Optional
from datetime import datetime

from core.database import get_session
from domain.messaging.whatsapp import WhatsAppMessage, WhatsAppTemplate, MessageType, MessageStatus
from domain.patients.models import Patient
from schemas.whatsapp import (
    WhatsAppMessageCreate,
    WhatsAppMessageResponse,
    MessageListResponse,
    SendAppointmentReminderRequest,
    SendMealPlanNotificationRequest,
    SendLabResultsNotificationRequest,
    SendMotivationalMessageRequest,
    SendFollowUpMessageRequest,
    SendCustomMessageRequest,
    MessageSentResponse,
    WhatsAppTemplateCreate,
    WhatsAppTemplateUpdate,
    WhatsAppTemplateResponse,
)
from services.whatsapp.twilio_service import whatsapp_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])


# ============================================================================
# WEBHOOK ENDPOINT FOR INCOMING MESSAGES
# ============================================================================

@router.post("/webhook", response_class=Response)
async def whatsapp_webhook(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Webhook endpoint for receiving incoming WhatsApp messages from Twilio

    This endpoint receives POST requests from Twilio when a user sends a message
    to your WhatsApp number. It saves the message to the database and can send
    an automated response.

    Configure this URL in Twilio Console:
    https://console.twilio.com/us1/develop/sms/settings/whatsapp-senders

    Webhook URL: https://your-domain.com/api/whatsapp/webhook
    """
    try:
        # Parse form data from Twilio
        form_data = await request.form()

        # Extract message data
        from_number = form_data.get("From", "")  # Format: whatsapp:+5219841372369
        to_number = form_data.get("To", "")      # Your WhatsApp number
        message_body = form_data.get("Body", "")
        message_sid = form_data.get("MessageSid", "")
        num_media = int(form_data.get("NumMedia", "0"))

        # Clean phone number (remove whatsapp: prefix)
        sender_phone = from_number.replace("whatsapp:", "")

        logger.info(f"Received WhatsApp message from {sender_phone}: {message_body[:50]}...")

        # Try to find patient by phone number
        query = select(Patient).where(Patient.telefono == sender_phone)
        patient = session.exec(query).first()

        # Save incoming message to database
        incoming_message = WhatsAppMessage(
            patient_id=patient.id if patient else None,
            recipient_phone=sender_phone,
            recipient_name=patient.nombre if patient else "Unknown",
            message_type=MessageType.CUSTOM,
            message_body=message_body,
            twilio_sid=message_sid,
            status=MessageStatus.DELIVERED,
            delivered_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            created_by_id=1  # System user
        )

        session.add(incoming_message)
        session.commit()

        logger.info(f"Incoming message saved. Patient: {patient.nombre if patient else 'Unknown'}")

        # Optional: Send automatic response
        response_text = None
        if patient:
            response_text = f"¡Hola {patient.nombre}! 👋 Gracias por contactarnos. Tu nutriólogo revisará tu mensaje pronto."
        else:
            response_text = "¡Hola! 👋 Gracias por contactarnos. Para brindarte mejor atención, por favor proporciona tu nombre completo."

        # Respond with TwiML (Twilio Markup Language)
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>"""

        return Response(content=twiml_response, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}")
        # Always return 200 to Twilio to avoid retries
        return Response(content="<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response></Response>",
                       media_type="application/xml",
                       status_code=200)


# ============================================================================
# MESSAGE ENDPOINTS
# ============================================================================

@router.post("/send/appointment-reminder", response_model=MessageSentResponse)
async def send_appointment_reminder(
    request: SendAppointmentReminderRequest,
    session: Session = Depends(get_session)
):
    """Send appointment reminder via WhatsApp"""
    try:
        # Send via Twilio
        result = await whatsapp_service.send_appointment_reminder(
            patient_name=request.patient_name,
            patient_phone=request.patient_phone,
            appointment_date=request.appointment_date,
            appointment_time=request.appointment_time,
            nutritionist_name=request.nutritionist_name
        )

        # Save to database
        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.patient_phone,
            recipient_name=request.patient_name,
            message_type=MessageType.APPOINTMENT_REMINDER,
            message_body=f"Recordatorio de cita: {request.appointment_date} a las {request.appointment_time}",
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Appointment reminder sent to patient {request.patient_id}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending appointment reminder: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.post("/send/meal-plan-notification", response_model=MessageSentResponse)
async def send_meal_plan_notification(
    request: SendMealPlanNotificationRequest,
    session: Session = Depends(get_session)
):
    """Send meal plan ready notification"""
    try:
        result = await whatsapp_service.send_meal_plan_notification(
            patient_name=request.patient_name,
            patient_phone=request.patient_phone,
            nutritionist_name=request.nutritionist_name
        )

        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.patient_phone,
            recipient_name=request.patient_name,
            message_type=MessageType.MEAL_PLAN_READY,
            message_body="Plan de alimentación listo",
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Meal plan notification sent to patient {request.patient_id}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending meal plan notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.post("/send/lab-results-notification", response_model=MessageSentResponse)
async def send_lab_results_notification(
    request: SendLabResultsNotificationRequest,
    session: Session = Depends(get_session)
):
    """Send lab results notification"""
    try:
        result = await whatsapp_service.send_lab_results_notification(
            patient_name=request.patient_name,
            patient_phone=request.patient_phone,
            lab_type=request.lab_type
        )

        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.patient_phone,
            recipient_name=request.patient_name,
            message_type=MessageType.LAB_RESULTS,
            message_body=f"Resultados de {request.lab_type} disponibles",
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Lab results notification sent to patient {request.patient_id}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending lab results notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.post("/send/motivational-message", response_model=MessageSentResponse)
async def send_motivational_message(
    request: SendMotivationalMessageRequest,
    session: Session = Depends(get_session)
):
    """Send motivational message"""
    try:
        result = await whatsapp_service.send_motivational_message(
            patient_name=request.patient_name,
            patient_phone=request.patient_phone,
            message_text=request.message_text
        )

        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.patient_phone,
            recipient_name=request.patient_name,
            message_type=MessageType.MOTIVATIONAL,
            message_body=request.message_text,
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Motivational message sent to patient {request.patient_id}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending motivational message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.post("/send/follow-up-message", response_model=MessageSentResponse)
async def send_follow_up_message(
    request: SendFollowUpMessageRequest,
    session: Session = Depends(get_session)
):
    """Send follow-up message"""
    try:
        result = await whatsapp_service.send_follow_up_message(
            patient_name=request.patient_name,
            patient_phone=request.patient_phone,
            days_since_last_visit=request.days_since_last_visit,
            nutritionist_name=request.nutritionist_name
        )

        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.patient_phone,
            recipient_name=request.patient_name,
            message_type=MessageType.FOLLOW_UP,
            message_body=f"Seguimiento después de {request.days_since_last_visit} días",
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Follow-up message sent to patient {request.patient_id}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending follow-up message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.post("/send/custom-message", response_model=MessageSentResponse)
async def send_custom_message(
    request: SendCustomMessageRequest,
    session: Session = Depends(get_session)
):
    """Send custom message"""
    try:
        result = await whatsapp_service.send_message(
            to_phone=request.recipient_phone,
            message_body=request.message_body
        )

        db_message = WhatsAppMessage(
            patient_id=request.patient_id,
            recipient_phone=request.recipient_phone,
            recipient_name=request.recipient_name,
            message_type=MessageType.CUSTOM,
            message_body=request.message_body,
            twilio_sid=result.get("twilio_sid"),
            status=MessageStatus.SENT if result["success"] else MessageStatus.FAILED,
            error_message=result.get("error"),
            sent_at=datetime.utcnow() if result["success"] else None,
            created_by_id=request.nutritionist_id
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Custom message sent to {request.recipient_phone}")

        return MessageSentResponse(
            success=result["success"],
            message_id=db_message.id,
            twilio_sid=result.get("twilio_sid"),
            status=result["status"],
            sent_at=result.get("sent_at"),
            error=result.get("error"),
            note=result.get("note")
        )

    except Exception as e:
        logger.error(f"Error sending custom message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )


@router.get("/messages/patient/{patient_id}", response_model=MessageListResponse)
async def get_patient_messages(
    patient_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """Get all messages for a patient"""
    # Verify patient exists
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )

    # Get total count
    count_query = select(func.count()).select_from(WhatsAppMessage).where(WhatsAppMessage.patient_id == patient_id)
    total = session.exec(count_query).one()

    # Get messages with pagination
    offset = (page - 1) * page_size
    query = (
        select(WhatsAppMessage)
        .where(WhatsAppMessage.patient_id == patient_id)
        .order_by(desc(WhatsAppMessage.created_at))
        .offset(offset)
        .limit(page_size)
    )

    messages = session.exec(query).all()

    total_pages = (total + page_size - 1) // page_size

    return MessageListResponse(
        items=messages,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/messages/{message_id}", response_model=WhatsAppMessageResponse)
async def get_message(
    message_id: int,
    session: Session = Depends(get_session)
):
    """Get specific message"""
    message = session.get(WhatsAppMessage, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with id {message_id} not found"
        )
    return message


# ============================================================================
# TEMPLATE ENDPOINTS
# ============================================================================

@router.post("/templates", response_model=WhatsAppTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template: WhatsAppTemplateCreate,
    nutritionist_id: int = 1,
    session: Session = Depends(get_session)
):
    """Create WhatsApp message template"""
    try:
        db_template = WhatsAppTemplate(
            **template.model_dump(),
            created_by_id=nutritionist_id
        )

        session.add(db_template)
        session.commit()
        session.refresh(db_template)

        logger.info(f"Created WhatsApp template: {db_template.name}")
        return db_template

    except Exception as e:
        logger.error(f"Error creating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating template: {str(e)}"
        )


@router.get("/templates", response_model=List[WhatsAppTemplateResponse])
async def get_templates(
    message_type: Optional[MessageType] = None,
    is_active: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    """Get all message templates"""
    query = select(WhatsAppTemplate)

    if message_type:
        query = query.where(WhatsAppTemplate.message_type == message_type)
    if is_active is not None:
        query = query.where(WhatsAppTemplate.is_active == is_active)

    query = query.order_by(WhatsAppTemplate.name)
    templates = session.exec(query).all()

    return templates


@router.get("/templates/{template_id}", response_model=WhatsAppTemplateResponse)
async def get_template(
    template_id: int,
    session: Session = Depends(get_session)
):
    """Get specific template"""
    template = session.get(WhatsAppTemplate, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )
    return template


@router.put("/templates/{template_id}", response_model=WhatsAppTemplateResponse)
async def update_template(
    template_id: int,
    template_update: WhatsAppTemplateUpdate,
    session: Session = Depends(get_session)
):
    """Update template"""
    db_template = session.get(WhatsAppTemplate, template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )

    update_data = template_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)

    session.add(db_template)
    session.commit()
    session.refresh(db_template)

    logger.info(f"Updated WhatsApp template {template_id}")
    return db_template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: int,
    session: Session = Depends(get_session)
):
    """Delete template"""
    db_template = session.get(WhatsAppTemplate, template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )

    session.delete(db_template)
    session.commit()

    logger.info(f"Deleted WhatsApp template {template_id}")
    return None
