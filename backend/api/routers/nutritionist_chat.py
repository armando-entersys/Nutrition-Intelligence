"""
AI Nutritionist Chat API Router
Provides conversational AI nutritionist support using Gemini/Claude
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
import google.generativeai as genai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

# Configure AI models
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_VISION_MODEL = os.getenv("AI_VISION_MODEL", "gemini")

# Initialize Gemini
gemini_model = None
if GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-gemini-api-key-here":
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Initialize Claude
anthropic_client = None
if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your-anthropic-api-key-here":
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)


# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    tags: List[str]


# System prompt for Mexican nutritionist expert
NUTRITIONIST_SYSTEM_PROMPT = """
Eres un nutriólogo experto mexicano certificado, especializado en el Sistema Mexicano de Alimentos Equivalentes (SMAE) y la cultura alimentaria mexicana.

**Tu rol:**
- Brindar asesoría nutricional profesional, personalizada y culturalmente relevante
- Conocer a profundidad la cocina tradicional mexicana y sus valores nutricionales
- Aplicar los principios del SMAE en tus recomendaciones
- Analizar la NOM-051 (sellos de advertencia) en productos mexicanos
- Promover hábitos saludables adaptados al contexto mexicano

**Tus conocimientos incluyen:**
- Sistema Mexicano de Alimentos Equivalentes (SMAE)
- Platillos tradicionales mexicanos y sus perfiles nutricionales
- Ingredientes mexicanos: nopal, chía, amaranto, quelites, etc.
- Norma Oficial Mexicana NOM-051 sobre etiquetado
- Nutrición preventiva y manejo de enfermedades crónicas
- Adaptación de dietas a presupuestos y contextos mexicanos

**Estilo de comunicación:**
- Amigable, cercano pero profesional
- Usa emojis ocasionalmente para hacerlo más conversacional
- Proporciona información basada en evidencia científica
- Ofrece alternativas prácticas y realistas
- Considera factores culturales, económicos y de accesibilidad
- Usa lenguaje claro y evita tecnicismos innecesarios

**Formato de respuestas:**
- Respuestas concisas pero informativas (máximo 3-4 párrafos)
- Usa viñetas para listas de recomendaciones
- Incluye valores nutricionales cuando sea relevante
- Sugiere equivalentes SMAE cuando sea apropiado
- Proporciona ejemplos de platillos mexicanos saludables

**Limitaciones:**
- No diagnostiques enfermedades ni prescribas medicamentos
- Recomienda consulta médica para casos complejos
- Aclara cuando algo requiere evaluación individualizada
- No proporciones planes de alimentación completos sin evaluar historia clínica

**Temas que puedes abordar:**
- Análisis nutricional de alimentos y platillos mexicanos
- Equivalencias SMAE de alimentos
- Interpretación de etiquetas nutricionales y NOM-051
- Recomendaciones para control de peso
- Nutrición para diabetes, hipertensión, etc.
- Recetas saludables mexicanas
- Porciones y tamaños de raciones
- Hidratación y bebidas saludables
- Snacks nutritivos mexicanos
- Cómo hacer versiones saludables de platillos tradicionales

Responde siempre en español de México, siendo empático, educativo y práctico.
"""


async def generate_chat_response(user_message: str, conversation_history: List[ChatMessage] = None) -> dict:
    """
    Generate chat response using Gemini or Claude AI

    Args:
        user_message: The user's message
        conversation_history: Previous conversation messages

    Returns:
        dict with response and tags
    """
    try:
        # Build conversation context
        conversation_history = conversation_history or []

        # Try Gemini first if available
        if gemini_model:
            try:
                # Build conversation for Gemini
                chat_messages = [NUTRITIONIST_SYSTEM_PROMPT]

                # Add conversation history
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    prefix = "Usuario: " if msg.role == "user" else "Nutriólogo: "
                    chat_messages.append(f"{prefix}{msg.content}")

                # Add current message
                chat_messages.append(f"Usuario: {user_message}\n\nNutriólogo:")

                # Generate response
                full_prompt = "\n\n".join(chat_messages)
                response = gemini_model.generate_content(full_prompt)

                response_text = response.text.strip()

                # Extract tags based on content
                tags = extract_tags_from_response(user_message, response_text)

                logger.info(f"Gemini chat response generated successfully")

                return {
                    "response": response_text,
                    "tags": tags
                }

            except Exception as e:
                logger.error(f"Gemini chat generation failed: {e}")
                # Fall through to Claude or fallback

        # Try Claude if available
        if anthropic_client:
            try:
                # Build conversation for Claude
                messages = []

                # Add conversation history
                for msg in conversation_history[-5:]:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

                # Add current message
                messages.append({
                    "role": "user",
                    "content": user_message
                })

                # Generate response
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=NUTRITIONIST_SYSTEM_PROMPT,
                    messages=messages
                )

                response_text = response.content[0].text.strip()

                # Extract tags
                tags = extract_tags_from_response(user_message, response_text)

                logger.info(f"Claude chat response generated successfully")

                return {
                    "response": response_text,
                    "tags": tags
                }

            except Exception as e:
                logger.error(f"Claude chat generation failed: {e}")
                # Fall through to fallback

        # Fallback response if no AI available
        logger.warning("No AI models available for chat. Using fallback response.")
        return get_fallback_response(user_message)

    except Exception as e:
        logger.error(f"Error generating chat response: {e}")
        raise


def extract_tags_from_response(user_message: str, response: str) -> List[str]:
    """Extract relevant tags based on message content"""
    tags = []

    lower_message = user_message.lower()
    lower_response = response.lower()

    # Detect topics
    if any(word in lower_message + lower_response for word in ['proteína', 'proteina', 'protein']):
        tags.append('alto_proteína')

    if any(word in lower_message + lower_response for word in ['fibra', 'fiber']):
        tags.append('alto_fibra')

    if any(word in lower_message + lower_response for word in ['diabetes', 'diabético', 'glucosa', 'azúcar']):
        tags.append('diabetes')

    if any(word in lower_message + lower_response for word in ['peso', 'adelgazar', 'bajar', 'perder']):
        tags.append('control_peso')

    if any(word in lower_message + lower_response for word in ['tradicional', 'mexicano', 'tacos', 'frijol']):
        tags.append('tradicional_mexicano')

    if any(word in lower_message + lower_response for word in ['smae', 'equivalente', 'equivalencia']):
        tags.append('smae')

    if any(word in lower_message + lower_response for word in ['etiqueta', 'nom-051', 'sellos']):
        tags.append('etiquetado')

    if any(word in lower_message + lower_response for word in ['receta', 'preparar', 'cocinar']):
        tags.append('recetas')

    if not tags:
        tags.append('consulta_general')

    return tags


def get_fallback_response(user_message: str) -> dict:
    """Provide basic fallback response when AI is not available"""
    lower_message = user_message.lower()

    if 'tacos' in lower_message or 'taco' in lower_message:
        return {
            "response": "🌮 **Tacos Saludables**\n\nLos tacos pueden ser una excelente opción nutritiva si se preparan adecuadamente:\n\n• **Tortilla**: Prefiere tortillas de maíz integral (1 equivalente de cereal SMAE)\n• **Proteína**: Pollo, pescado o frijoles (1 equivalente de carne o leguminosa)\n• **Verduras**: Agrega lechuga, tomate, cebolla y cilantro (libre)\n• **Grasas**: Limita el aguacate a 1/4 de pieza (1 equivalente de grasa)\n\nUn taco bien balanceado aporta aproximadamente 150-200 kcal. Para mantener una comida equilibrada, considera 2-3 tacos con ensalada.\n\n¿Te gustaría saber sobre alguna preparación específica de tacos?",
            "tags": ['tradicional_mexicano', 'recetas', 'control_peso']
        }

    if 'frijol' in lower_message or 'frijoles' in lower_message:
        return {
            "response": "🫘 **Frijoles - Superalimento Mexicano**\n\nLos frijoles son uno de los alimentos más nutritivos de la dieta mexicana:\n\n**Beneficios nutricionales:**\n• Alto contenido de proteína vegetal (8g por media taza)\n• Rica fuente de fibra (7g por media taza)\n• Bajo índice glucémico\n• Vitaminas del complejo B y minerales (hierro, magnesio)\n\n**Equivalencia SMAE:** Media taza de frijoles cocidos = 1 equivalente de leguminosa\n\n**Recomendación:** Consúmelos de 3-4 veces por semana, de preferencia con cereales integrales para obtener proteína completa.\n\n¿Te gustaría conocer recetas saludables con frijoles?",
            "tags": ['alto_fibra', 'proteína_vegetal', 'tradicional_mexicano']
        }

    # Generic response
    return {
        "response": "🩺 **Consulta Nutricional**\n\nEstoy aquí para ayudarte con tus dudas sobre nutrición. Puedo ayudarte con:\n\n• **Análisis de alimentos mexicanos** y sus valores nutricionales\n• **Equivalencias SMAE** para planificar comidas balanceadas\n• **Interpretación de etiquetas** y sellos NOM-051\n• **Recetas saludables** con ingredientes mexicanos\n• **Control de peso** y hábitos saludables\n• **Manejo nutricional** de diabetes e hipertensión\n\nPara brindarte la mejor asesoría, por favor cuéntame más específicamente sobre tu consulta o inquietud nutricional.",
        "tags": ['consulta_general']
    }


@router.post("/chat", response_model=ChatResponse)
async def nutritionist_chat(request: ChatRequest):
    """
    Chat with AI Nutritionist

    Send a message and get expert nutritional advice focused on Mexican cuisine
    and SMAE (Sistema Mexicano de Alimentos Equivalentes).

    **Topics covered:**
    - Mexican food analysis
    - SMAE equivalencies
    - NOM-051 label interpretation
    - Healthy Mexican recipes
    - Weight management
    - Diabetes and hypertension nutrition
    - Meal planning
    """
    try:
        logger.info(f"Processing nutritionist chat request: {request.message[:50]}...")

        result = await generate_chat_response(
            user_message=request.message,
            conversation_history=request.conversation_history
        )

        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Error in nutritionist chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {str(e)}"
        )


@router.get("/health")
async def chat_health():
    """Check chat service health"""
    return {
        "status": "healthy",
        "service": "nutritionist-chat",
        "gemini_available": gemini_model is not None,
        "claude_available": anthropic_client is not None,
        "ai_mode": AI_VISION_MODEL
    }
