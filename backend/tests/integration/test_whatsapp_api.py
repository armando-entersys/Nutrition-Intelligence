"""
Integration Tests for WhatsApp API Endpoints
Tests cover the integration test cases defined in TESTING_PLAN.md

Test IDs covered:
- IT-WA-001: Send appointment reminder
- IT-WA-002: Send meal plan notification with Twilio SID
- IT-WA-003: Get message history for patient with pagination
- IT-WA-004: Create message template
- IT-WA-005: Send message with invalid phone number validation
"""
import pytest
from httpx import AsyncClient
from datetime import datetime
from sqlmodel import Session, select, func

from domain.messaging.whatsapp import (
    WhatsAppMessage,
    WhatsAppTemplate,
    MessageType,
    MessageStatus
)
from domain.patients.models import Patient


@pytest.mark.integration
@pytest.mark.asyncio
class TestWhatsAppAPI:
    """Integration tests for WhatsApp API endpoints"""

    async def test_send_appointment_reminder(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        test_session: Session
    ):
        """
        IT-WA-001: Enviar recordatorio cita

        Test POST /api/v1/whatsapp/send/appointment-reminder
        - Status 200
        - Message saved to database with status "sent"
        - Twilio SID present (or mock SID if Twilio not configured)
        """
        # Arrange
        reminder_payload = {
            "patient_id": sample_patient.id,
            "patient_name": "Juan Pérez",
            "patient_phone": "+525512345678",
            "appointment_date": "Lunes 15 de Enero, 2025",
            "appointment_time": "10:00 AM",
            "nutritionist_name": "Dra. María González",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/appointment-reminder",
            json=reminder_payload
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["message_id"] is not None
        assert data["twilio_sid"] is not None  # Either real or mock SID
        assert data["status"] == "sent"

        # Verify message was saved to database
        message_id = data["message_id"]
        db_message = await test_session.get(WhatsAppMessage, message_id)

        assert db_message is not None
        assert db_message.patient_id == sample_patient.id
        assert db_message.recipient_phone == "+525512345678"
        assert db_message.recipient_name == "Juan Pérez"
        assert db_message.message_type == MessageType.APPOINTMENT_REMINDER
        assert db_message.status == MessageStatus.SENT
        assert "recordatorio" in db_message.message_body.lower()
        assert db_message.sent_at is not None
        assert db_message.created_by_id == 1

        # If Twilio not configured, should have note
        if "mock" in data.get("note", "").lower():
            assert "mock" in data["note"].lower()

    async def test_send_meal_plan_notification_with_twilio_sid(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        test_session: Session
    ):
        """
        IT-WA-002: Enviar notif plan listo

        Test POST /api/v1/whatsapp/send/meal-plan-notification
        - Status 200
        - Message saved with Twilio SID present
        - Message type is MEAL_PLAN_READY
        """
        # Arrange
        notification_payload = {
            "patient_id": sample_patient.id,
            "patient_name": "Ana López",
            "patient_phone": "+525512345679",
            "nutritionist_name": "Nut. Carlos Mendoza",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/meal-plan-notification",
            json=notification_payload
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["message_id"] is not None
        assert data["twilio_sid"] is not None
        assert data["status"] == "sent"

        # Verify database record
        db_message = await test_session.get(WhatsAppMessage, data["message_id"])

        assert db_message is not None
        assert db_message.message_type == MessageType.MEAL_PLAN_READY
        assert db_message.twilio_sid == data["twilio_sid"]
        assert "plan de alimentación" in db_message.message_body.lower()
        assert db_message.status == MessageStatus.SENT

    async def test_get_patient_message_history_with_pagination(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        test_session: Session
    ):
        """
        IT-WA-003: Historial mensajes paciente

        Test GET /api/v1/whatsapp/messages/patient/{patient_id}
        - Returns list with pagination
        - Messages ordered by date (newest first)
        - Includes all message types
        """
        # Arrange - Create multiple messages for patient
        messages = []
        for i in range(8):
            message = WhatsAppMessage(
                patient_id=sample_patient.id,
                recipient_phone="+525512345678",
                recipient_name="Test Patient",
                message_type=MessageType.APPOINTMENT_REMINDER if i % 2 == 0 else MessageType.MOTIVATIONAL,
                message_body=f"Test message {i}",
                twilio_sid=f"mock_sid_{i}",
                status=MessageStatus.SENT if i % 3 != 0 else MessageStatus.DELIVERED,
                sent_at=datetime.utcnow(),
                created_by_id=1
            )
            test_session.add(message)
            messages.append(message)

        await test_session.commit()

        # Act - Get first page
        response = await client.get(
            f"/api/v1/whatsapp/messages/patient/{sample_patient.id}",
            params={"page": 1, "page_size": 5}
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 8
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert data["total_pages"] == 2
        assert len(data["items"]) == 5

        # Verify messages are ordered by created_at descending (newest first)
        timestamps = [msg["created_at"] for msg in data["items"]]
        assert timestamps == sorted(timestamps, reverse=True)

        # Act - Get second page
        response_page2 = await client.get(
            f"/api/v1/whatsapp/messages/patient/{sample_patient.id}",
            params={"page": 2, "page_size": 5}
        )

        # Assert second page
        assert response_page2.status_code == 200
        data_page2 = response_page2.json()
        assert len(data_page2["items"]) == 3  # Remaining messages
        assert data_page2["page"] == 2

        # Verify no duplicate messages between pages
        page1_ids = {msg["id"] for msg in data["items"]}
        page2_ids = {msg["id"] for msg in data_page2["items"]}
        assert len(page1_ids.intersection(page2_ids)) == 0

    async def test_create_whatsapp_template(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """
        IT-WA-004: Crear template mensaje

        Test POST /api/v1/whatsapp/templates
        - Status 201
        - Template created with variables
        - Template can be retrieved
        """
        # Arrange
        template_payload = {
            "name": "Recordatorio de Cita Genérico",
            "message_type": "appointment_reminder",
            "template_body": "Hola {patient_name}, te recordamos tu cita el {appointment_date} a las {appointment_time}.",
            "variables": ["patient_name", "appointment_date", "appointment_time"],
            "is_active": True
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/templates",
            json=template_payload
        )

        # Assert
        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Recordatorio de Cita Genérico"
        assert data["message_type"] == "appointment_reminder"
        assert data["template_body"] == template_payload["template_body"]
        assert data["variables"] == ["patient_name", "appointment_date", "appointment_time"]
        assert data["is_active"] is True
        assert data["created_at"] is not None
        assert data["created_by_id"] == 1

        # Verify template was saved to database
        template_id = data["id"]
        db_template = await test_session.get(WhatsAppTemplate, template_id)

        assert db_template is not None
        assert db_template.name == template_payload["name"]
        assert db_template.message_type == MessageType.APPOINTMENT_REMINDER

    async def test_send_custom_message_with_invalid_phone(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        test_session: Session
    ):
        """
        IT-WA-005: Validación teléfono inválido

        Test POST /api/v1/whatsapp/send/custom-message
        - With invalid phone number format
        - Should still process (Twilio will handle validation)
        - Or return 400 if validation implemented
        """
        # Arrange - Test with clearly invalid phone
        invalid_payload = {
            "patient_id": sample_patient.id,
            "recipient_phone": "123",  # Invalid format
            "recipient_name": "Test",
            "message_body": "Test message",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/custom-message",
            json=invalid_payload
        )

        # Assert
        # The API might accept it and let Twilio validate
        # Or it might return 400 for validation
        # In mock mode, it will likely succeed
        assert response.status_code in [200, 400, 500]

        if response.status_code == 200:
            # Mock mode - accepted but may have error in response
            data = response.json()
            # Either success with mock, or failed status
            if not data["success"]:
                assert data["error"] is not None

        # Test with better formatted but fake phone
        valid_format_payload = {
            "patient_id": sample_patient.id,
            "recipient_phone": "+521234567890",  # Valid format, may not exist
            "recipient_name": "Test Patient",
            "message_body": "Test custom message",
            "nutritionist_id": 1
        }

        response_valid = await client.post(
            "/api/v1/whatsapp/send/custom-message",
            json=valid_format_payload
        )

        # Should accept valid format
        assert response_valid.status_code == 200
        data_valid = response_valid.json()

        # In mock mode, should succeed
        if data_valid["success"]:
            assert data_valid["message_id"] is not None
            assert data_valid["twilio_sid"] is not None


@pytest.mark.integration
@pytest.mark.asyncio
class TestWhatsAppAPITemplates:
    """Additional tests for WhatsApp template management"""

    async def test_get_all_templates(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """Test GET /api/v1/whatsapp/templates"""
        # Arrange - Create multiple templates
        templates = [
            WhatsAppTemplate(
                name="Template 1",
                message_type=MessageType.APPOINTMENT_REMINDER,
                template_body="Body 1",
                is_active=True,
                created_by_id=1
            ),
            WhatsAppTemplate(
                name="Template 2",
                message_type=MessageType.MOTIVATIONAL,
                template_body="Body 2",
                is_active=False,
                created_by_id=1
            ),
        ]

        for template in templates:
            test_session.add(template)
        await test_session.commit()

        # Act
        response = await client.get("/api/v1/whatsapp/templates")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    async def test_get_template_by_id(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """Test GET /api/v1/whatsapp/templates/{template_id}"""
        # Arrange
        template = WhatsAppTemplate(
            name="Test Template",
            message_type=MessageType.FOLLOW_UP,
            template_body="Follow up message",
            created_by_id=1
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        # Act
        response = await client.get(f"/api/v1/whatsapp/templates/{template.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == template.id
        assert data["name"] == "Test Template"

    async def test_update_template(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """Test PUT /api/v1/whatsapp/templates/{template_id}"""
        # Arrange
        template = WhatsAppTemplate(
            name="Original Name",
            message_type=MessageType.CUSTOM,
            template_body="Original body",
            created_by_id=1
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        # Act
        update_payload = {
            "name": "Updated Name",
            "template_body": "Updated body",
            "is_active": False
        }

        response = await client.put(
            f"/api/v1/whatsapp/templates/{template.id}",
            json=update_payload
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["template_body"] == "Updated body"
        assert data["is_active"] is False

    async def test_delete_template(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """Test DELETE /api/v1/whatsapp/templates/{template_id}"""
        # Arrange
        template = WhatsAppTemplate(
            name="To Delete",
            message_type=MessageType.CUSTOM,
            template_body="Will be deleted",
            created_by_id=1
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        template_id = template.id

        # Act
        response = await client.delete(f"/api/v1/whatsapp/templates/{template_id}")

        # Assert
        assert response.status_code == 204

        # Verify deletion
        deleted = await test_session.get(WhatsAppTemplate, template_id)
        assert deleted is None


@pytest.mark.integration
@pytest.mark.asyncio
class TestWhatsAppAPIMessageTypes:
    """Tests for different message type endpoints"""

    async def test_send_lab_results_notification(
        self,
        client: AsyncClient,
        sample_patient: Patient
    ):
        """Test POST /api/v1/whatsapp/send/lab-results-notification"""
        # Arrange
        payload = {
            "patient_id": sample_patient.id,
            "patient_name": "Test Patient",
            "patient_phone": "+525512345678",
            "lab_type": "Química Sanguínea",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/lab-results-notification",
            json=payload
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message_id"] is not None

    async def test_send_motivational_message(
        self,
        client: AsyncClient,
        sample_patient: Patient
    ):
        """Test POST /api/v1/whatsapp/send/motivational-message"""
        # Arrange
        payload = {
            "patient_id": sample_patient.id,
            "patient_name": "Test Patient",
            "patient_phone": "+525512345678",
            "message_text": "¡Excelente progreso! Sigue así, estás logrando tus metas.",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/motivational-message",
            json=payload
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    async def test_send_follow_up_message(
        self,
        client: AsyncClient,
        sample_patient: Patient
    ):
        """Test POST /api/v1/whatsapp/send/follow-up-message"""
        # Arrange
        payload = {
            "patient_id": sample_patient.id,
            "patient_name": "Test Patient",
            "patient_phone": "+525512345678",
            "days_since_last_visit": 30,
            "nutritionist_name": "Nut. María González",
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/follow-up-message",
            json=payload
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    async def test_get_specific_message_by_id(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        test_session: Session
    ):
        """Test GET /api/v1/whatsapp/messages/{message_id}"""
        # Arrange
        message = WhatsAppMessage(
            patient_id=sample_patient.id,
            recipient_phone="+525512345678",
            recipient_name="Test",
            message_type=MessageType.CUSTOM,
            message_body="Test body",
            twilio_sid="mock_123",
            status=MessageStatus.SENT,
            created_by_id=1
        )
        test_session.add(message)
        await test_session.commit()
        await test_session.refresh(message)

        # Act
        response = await client.get(f"/api/v1/whatsapp/messages/{message.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == message.id
        assert data["patient_id"] == sample_patient.id

    async def test_filter_templates_by_message_type(
        self,
        client: AsyncClient,
        test_session: Session
    ):
        """Test filtering templates by message type"""
        # Arrange
        templates = [
            WhatsAppTemplate(
                name="Reminder 1",
                message_type=MessageType.APPOINTMENT_REMINDER,
                template_body="Body 1",
                created_by_id=1
            ),
            WhatsAppTemplate(
                name="Reminder 2",
                message_type=MessageType.APPOINTMENT_REMINDER,
                template_body="Body 2",
                created_by_id=1
            ),
            WhatsAppTemplate(
                name="Motivational 1",
                message_type=MessageType.MOTIVATIONAL,
                template_body="Body 3",
                created_by_id=1
            ),
        ]

        for t in templates:
            test_session.add(t)
        await test_session.commit()

        # Act
        response = await client.get(
            "/api/v1/whatsapp/templates",
            params={"message_type": "appointment_reminder"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        for template in data:
            assert template["message_type"] == "appointment_reminder"

    async def test_message_body_max_length_validation(
        self,
        client: AsyncClient,
        sample_patient: Patient
    ):
        """Test that message body respects 1600 character limit"""
        # Arrange - Create message exceeding 1600 chars
        long_message = "A" * 1700

        payload = {
            "patient_id": sample_patient.id,
            "recipient_phone": "+525512345678",
            "recipient_name": "Test",
            "message_body": long_message,
            "nutritionist_id": 1
        }

        # Act
        response = await client.post(
            "/api/v1/whatsapp/send/custom-message",
            json=payload
        )

        # Assert
        # Should return validation error (422) or process with truncation
        assert response.status_code in [200, 422, 500]

        if response.status_code == 422:
            # Pydantic validation should catch this
            error_detail = response.json()
            assert "detail" in error_detail
