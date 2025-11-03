"""
WhatsApp service using Twilio API
"""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio Sandbox default

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID != "your-twilio-account-sid":
    try:
        from twilio.rest import Client
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("Twilio WhatsApp client initialized successfully")
    except ImportError:
        logger.warning("Twilio library not installed. WhatsApp functionality disabled.")
    except Exception as e:
        logger.error(f"Error initializing Twilio client: {e}")
else:
    logger.warning("Twilio credentials not configured. WhatsApp functionality disabled.")


class WhatsAppService:
    """Service for sending WhatsApp messages via Twilio"""

    def __init__(self):
        self.client = twilio_client
        self.from_number = TWILIO_WHATSAPP_NUMBER
        self.is_available = twilio_client is not None

    async def send_message(
        self,
        to_phone: str,
        message_body: str,
        media_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message

        Args:
            to_phone: Recipient phone number (format: +52XXXXXXXXXX)
            message_body: Message text (max 1600 chars)
            media_url: Optional media URL for images/files

        Returns:
            Dict with message details including Twilio SID
        """
        if not self.is_available:
            logger.warning("Twilio client not available. Returning mock response.")
            return self._get_mock_response(to_phone, message_body)

        try:
            # Format phone number for WhatsApp
            if not to_phone.startswith("whatsapp:"):
                to_phone = f"whatsapp:{to_phone}"

            # Prepare message params
            message_params = {
                "from_": self.from_number,
                "to": to_phone,
                "body": message_body
            }

            if media_url:
                message_params["media_url"] = [media_url]

            # Send message via Twilio
            message = self.client.messages.create(**message_params)

            logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")

            return {
                "success": True,
                "twilio_sid": message.sid,
                "status": message.status,
                "to": to_phone,
                "sent_at": datetime.utcnow().isoformat(),
                "error": None
            }

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return {
                "success": False,
                "twilio_sid": None,
                "status": "failed",
                "to": to_phone,
                "sent_at": None,
                "error": str(e)
            }

    async def send_appointment_reminder(
        self,
        patient_name: str,
        patient_phone: str,
        appointment_date: str,
        appointment_time: str,
        nutritionist_name: str
    ) -> Dict[str, Any]:
        """Send appointment reminder"""
        message = f"""
🗓️ *Recordatorio de Cita - Nutrition Intelligence*

Hola {patient_name},

Te recordamos tu próxima cita con {nutritionist_name}:

📅 Fecha: {appointment_date}
🕐 Hora: {appointment_time}

Por favor confirma tu asistencia respondiendo a este mensaje.

Si necesitas reprogramar, contáctanos con anticipación.

¡Te esperamos! 💚
        """.strip()

        return await self.send_message(patient_phone, message)

    async def send_meal_plan_notification(
        self,
        patient_name: str,
        patient_phone: str,
        nutritionist_name: str
    ) -> Dict[str, Any]:
        """Notify patient that meal plan is ready"""
        message = f"""
📋 *Plan de Alimentación Listo*

Hola {patient_name},

¡Tu nuevo plan de alimentación ya está disponible! 🎉

{nutritionist_name} ha preparado un plan personalizado para ti.

Ingresa a tu cuenta en Nutrition Intelligence para revisarlo:
👉 https://nutrition-intelligence.app

Si tienes dudas, no dudes en contactarnos.

¡Éxito en tu camino hacia una mejor salud! 💪
        """.strip()

        return await self.send_message(patient_phone, message)

    async def send_lab_results_notification(
        self,
        patient_name: str,
        patient_phone: str,
        lab_type: str
    ) -> Dict[str, Any]:
        """Notify patient about new lab results"""
        message = f"""
🔬 *Resultados de Laboratorio Disponibles*

Hola {patient_name},

Tus resultados de {lab_type} ya están disponibles en tu expediente.

Ingresa a tu cuenta para revisarlos:
👉 https://nutrition-intelligence.app

Tu nutriólogo revisará los resultados y te contactará si es necesario.

Cuida tu salud 💚
        """.strip()

        return await self.send_message(patient_phone, message)

    async def send_motivational_message(
        self,
        patient_name: str,
        patient_phone: str,
        message_text: str
    ) -> Dict[str, Any]:
        """Send custom motivational message"""
        message = f"""
💪 *Mensaje Motivacional*

Hola {patient_name},

{message_text}

¡Sigue adelante! Estamos contigo en cada paso.

Tu equipo de Nutrition Intelligence 💚
        """.strip()

        return await self.send_message(patient_phone, message)

    async def send_follow_up_message(
        self,
        patient_name: str,
        patient_phone: str,
        days_since_last_visit: int,
        nutritionist_name: str
    ) -> Dict[str, Any]:
        """Send follow-up message"""
        message = f"""
👋 *Seguimiento - Nutrition Intelligence*

Hola {patient_name},

Han pasado {days_since_last_visit} días desde tu última consulta.

¿Cómo vas con tu plan de alimentación? ¿Tienes alguna duda?

{nutritionist_name} está disponible para apoyarte.

Agenda tu próxima cita o contáctanos por WhatsApp.

¡Estamos aquí para ayudarte! 💚
        """.strip()

        return await self.send_message(patient_phone, message)

    def _get_mock_response(self, to_phone: str, message_body: str) -> Dict[str, Any]:
        """Generate mock response when Twilio is not available"""
        return {
            "success": True,
            "twilio_sid": f"mock_sid_{datetime.utcnow().timestamp()}",
            "status": "sent",
            "to": to_phone,
            "sent_at": datetime.utcnow().isoformat(),
            "error": None,
            "note": "Mock response - Twilio not configured"
        }

    async def get_message_status(self, twilio_sid: str) -> Optional[Dict[str, Any]]:
        """Get message status from Twilio"""
        if not self.is_available:
            return None

        try:
            message = self.client.messages(twilio_sid).fetch()
            return {
                "sid": message.sid,
                "status": message.status,
                "to": message.to,
                "from": message.from_,
                "date_sent": message.date_sent.isoformat() if message.date_sent else None,
                "error_code": message.error_code,
                "error_message": message.error_message
            }
        except Exception as e:
            logger.error(f"Error fetching message status: {e}")
            return None


# Service instance
whatsapp_service = WhatsAppService()


# Convenience functions
async def send_message(to_phone: str, message_body: str, media_url: Optional[str] = None) -> Dict[str, Any]:
    """Send WhatsApp message"""
    return await whatsapp_service.send_message(to_phone, message_body, media_url)


async def send_appointment_reminder(
    patient_name: str,
    patient_phone: str,
    appointment_date: str,
    appointment_time: str,
    nutritionist_name: str
) -> Dict[str, Any]:
    """Send appointment reminder"""
    return await whatsapp_service.send_appointment_reminder(
        patient_name, patient_phone, appointment_date, appointment_time, nutritionist_name
    )
