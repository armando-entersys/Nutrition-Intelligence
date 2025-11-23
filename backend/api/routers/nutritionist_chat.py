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
    """Provide intelligent fallback response when AI is not available"""
    lower_message = user_message.lower()

    # Tacos
    if 'tacos' in lower_message or 'taco' in lower_message:
        return {
            "response": "🌮 **Tacos Saludables**\n\nLos tacos pueden ser una excelente opción nutritiva si se preparan adecuadamente:\n\n• **Tortilla**: Prefiere tortillas de maíz integral (1 equivalente de cereal SMAE)\n• **Proteína**: Pollo, pescado o frijoles (1 equivalente de carne o leguminosa)\n• **Verduras**: Agrega lechuga, tomate, cebolla y cilantro (libre)\n• **Grasas**: Limita el aguacate a 1/4 de pieza (1 equivalente de grasa)\n\nUn taco bien balanceado aporta aproximadamente 150-200 kcal. Para mantener una comida equilibrada, considera 2-3 tacos con ensalada.\n\n¿Te gustaría saber sobre alguna preparación específica de tacos?",
            "tags": ['tradicional_mexicano', 'recetas', 'control_peso']
        }

    # Frijoles
    if 'frijol' in lower_message or 'frijoles' in lower_message:
        return {
            "response": "🫘 **Frijoles - Superalimento Mexicano**\n\nLos frijoles son uno de los alimentos más nutritivos de la dieta mexicana:\n\n**Beneficios nutricionales:**\n• Alto contenido de proteína vegetal (8g por media taza)\n• Rica fuente de fibra (7g por media taza)\n• Bajo índice glucémico\n• Vitaminas del complejo B y minerales (hierro, magnesio)\n\n**Equivalencia SMAE:** Media taza de frijoles cocidos = 1 equivalente de leguminosa\n\n**Recomendación:** Consúmelos de 3-4 veces por semana, de preferencia con cereales integrales para obtener proteína completa.\n\n¿Te gustaría conocer recetas saludables con frijoles?",
            "tags": ['alto_fibra', 'proteína_vegetal', 'tradicional_mexicano']
        }
    
    # Aguacate
    if 'aguacate' in lower_message or 'aguacates' in lower_message or 'avocado' in lower_message:
        return {
            "response": "🥑 **Aguacate - Grasa Saludable**\n\nEl aguacate es un alimento nutritivo rico en grasas monoinsaturadas:\n\n**Beneficios:**\n• Grasas saludables para el corazón\n• Vitamina E y antioxidantes\n• Ayuda a absorber vitaminas liposolubles\n• Rico en potasio\n\n**Equivalencia SMAE:** 1/3 de aguacate = 1 equivalente de grasa (~45 kcal)\n\n**Recomendación:** Consume con moderación. Aunque es saludable, es alto en calorías. Ideal para ensaladas o como topping en tus platillos.",
            "tags": ['grasa_saludable', 'tradicional_mexicano']
        }
    
    # Diabetes
    if 'diabetes' in lower_message or 'diabético' in lower_message or 'diabetico' in lower_message or 'glucosa' in lower_message or 'azúcar' in lower_message or 'azucar' in lower_message:
        return {
            "response": "🩺 **Manejo Nutricional de Diabetes**\n\nPara el control de la diabetes, considera estas recomendaciones:\n\n**Alimentos recomendados:**\n• Cereales integrales de bajo índice glucémico\n• Verduras sin límite (especialmente nopales)\n• Proteínas magras (pescado, pollo, leguminosas)\n• Frutas con moderación (preferir frutas enteras vs jugos)\n\n**Equivalencias SMAE útiles:**\n• 1/2 taza de frijoles = 1 equivalente de leguminosa\n• 1 tortilla de maíz = 1 equivalente de cereal\n• 1/4 de plato debe ser proteína, 1/4 cereales, 1/2 verduras\n\n**Importante:** Mantén horarios regulares de comida y controla porciones. Consulta con tu médico para un plan personalizado.",
            "tags": ['diabetes', 'control_glucosa'] 
        }
    
    # Peso / Adelgazar
    if any(word in lower_message for word in ['peso', 'adelgazar', 'bajar', 'perder', 'dieta', 'calorías', 'calorias']):
        return {
            "response": "⚖️ **Control de Peso Saludable**\n\nPara lograr tus metas de peso de forma saludable:\n\n**Principios básicos:**\n• Déficit calórico moderado (300-500 kcal/día)\n• Comidas balanceadas usando el Plato del Bien Comer\n• Prioriza proteína magra y fibra para saciedad\n• Hidrátate bien (2-3 litros de agua al día)\n\n**Tips prácticos:**\n• Controla porciones con el método del plato\n• Prefiere tacos de pollo/pescado vs carne roja\n• Sustituye refrescos por agua de jamaica sin azúcar\n• Incluye verduras en cada comida\n\n**SMAE te ayuda** a planear porciones correctas. ¿Te gustaría ejemplos de menús para control de peso?",
            "tags": ['control_peso', 'déficit_calórico']
        }
    
    # Recetas
    if any(word in lower_message for word in ['receta', 'recetas', 'preparar', 'cocinar', 'platillo', 'comida']):
        return {
            "response": "🍽️ **Recetas Saludables Mexicanas**\n\nPuedo ayudarte con recetas nutritivas de platillos tradicionales:\n\n**Opciones saludables:**\n• **Tacos de pescado a la plancha**: Alto en proteína, bajo en grasa\n• **Caldo de po llo con verduras**: Nutritivo y reconfortante\n• **Ensalada de nopales**: Rica en fibra, ideal para diabetes\n• **Chilaquiles verdes horneados**: Versión más ligera del clásico\n• **Frijoles de la olla**: Proteína vegetal sin grasa añadida\n\n¿Sobre qué platillo específico te gustaría conocer la versión saludable?",
            "tags": ['recetas', 'tradicional_mexicano']
        }
    
    # SMAE / Equivalencias
    if any(word in lower_message for word in ['smae', 'equivalente', 'equivalencia', 'porción', 'porcion', 'ración', 'racion']):
        return {
            "response": "📊 **Sistema Mexicano de Alimentos Equivalentes (SMAE)**\n\nEl SMAE agrupa alimentos con valor nutricional similar:\n\n**Grupos principales:**\n1. **Cereales**: Tortilla, pan, arroz (70 kcal/equivalente)\n2. **Leguminosas**: Frijoles, lentejas (120 kcal/equivalente)\n3. **Carnes**: Pollo, pescado, res (55-75 kcal/equivalente)\n4. **Frutas**: Manzana, naranja, papaya (60 kcal/equivalente)\n5. **Verduras**: Sin límite en la mayoría\n6. **Grasas**: Aceite, aguacate, nueces (45 kcal/equivalente)\n7. **Lácteos**: Leche, yogurt, queso (variable)\n\n¿Sobre qué grupo específico necesitas información?",
            "tags": ['smae', 'equivalencias']
        }
    
    # Etiquetas / NOM-051
    if any(word in lower_message for word in ['etiqueta', 'nom-051', 'nom051', 'sello', 'sellos', 'advertencia']):
        return {
            "response": "🏷️ **Etiquetado NOM-051**\n\nLa NOM-051 incluye sellos de advertencia cuando un producto EXCEDE:\n\n**Sellos octagonales:**\n• **Exceso calorías**: \u003e275 kcal/100g\n• **Exceso azúcares**: \u003e10% de energía de azúcares añadidos\n• **Exceso grasas saturadas**: \u003e10% de energía\n• **Exceso grasas trans**: \u003e1% de energía\n• **Exceso sodio**: \u003e300mg/100g o 100ml\n\n**Leyendas:**\n• \"Contiene cafeína - evitar en niños\"\n• \"Contiene edulcorantes - no recomendable en niños\"\n\n**Recomendación:** Evita productos con 2 o más sellos. Prefiere alimentos frescos sin etiqueta.",
            "tags": ['etiquetado', 'nom-051']
        }
    
    # Nopales
    if 'nopal' in lower_message:
        return {
            "response": "🌵 **Nopales - Tesoro Nutricional Mexicano**\n\nLos nopales son extraordinariamente nutritivos:\n\n**Beneficios:**\n• Solo 14 kcal por taza\n• Alto contenido de fibra soluble (ayuda a controlar glucosa)\n• Rico en calcio y vitamina C\n• Ayuda a reducir colesterol\n• Efecto saciante\n\n**Usos culinarios:**\n• Ensaladas de nopales\n• Tacos de nopales asados\n• Jugo verde con nopal\n• Guisados con carne o huevo\n\n**SMAE:** Los nopales se consideran verdura libre (consume sin límite).\n\nIdeal para diabetes, control de peso y salud cardiovascular.",
            "tags": ['nopales', 'alto_fibra', 'tradicional_mexicano']
        }
    
    # Chía / Amaranto
    if any(word in lower_message for word in ['chia', 'chía', 'amaranto']):
        return {
            "response": "🌾 **Superalimentos Mexicanos: Chía y Amaranto**\n\n**CHÍA:**\n• Omega-3 vegetal\n• Alta fibra (11g/onza)\n• 1 cucharada en agua = gelifica y da saciedad\n• SMAE: 1 cucharada = 1 equivalente de grasa\n\n**AMARANTO:**\n• Proteína completa (lisina)\n• Sin gluten\n• Rico en calcio y hierro\n• 1/2 taza cocida = 1 equivalente de cereal\n\n**Usos:**\n• Chía: Aguas frescas, yogurt, ensaladas\n• Amaranto: Alegrías, cereal, panqué\n\nAmbos son excelentes para nutrición vegetariana y deportiva.",
            "tags": ['superalimentos', 'tradicional_mexicano', 'omega3']
        }
    
    # Saludo / Hola
    if any(word in lower_message for word in ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi']):
        return {
            "response": "👋 ¡Hola! Soy tu Nutriólogo Virtual especializado en nutrición mexicana.\n\nPuedo ayudarte con:\n\n• 🌮 Análisis nutricional de platillos mexicanos\n• 📊 Equivalencias del Sistema SMAE\n• 🏷️ Interpretación de etiquetas NOM-051\n• 🍽️ Recetas saludables tradicionales\n• ⚖️ Control de peso y hábitos saludables\n• 🩺 Manejo nutricional de diabetes e hipertensión\n\n¿En qué puedo asesorarte el día de hoy?",
            "tags": ['saludo', 'consulta_general']
        }

    # Generic response (solo si no coincide con ninguno anterior)
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
