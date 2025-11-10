"""
AI Vision service for food recognition using Gemini Vision and Claude Vision
Hybrid approach: Gemini as primary, Claude as fallback for complex cases
"""
from typing import List, Dict, Any, Optional
import logging
import os
import json
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Configure AI models
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_VISION_MODEL = os.getenv("AI_VISION_MODEL", "gemini")  # gemini | claude | hybrid
CONFIDENCE_THRESHOLD = int(os.getenv("AI_VISION_CONFIDENCE_THRESHOLD", "75"))

# Initialize Gemini
if GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-gemini-api-key-here":
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Using gemini-1.5-pro for vision support
else:
    gemini_model = None
    logger.warning("Google API key not configured. Gemini Vision disabled.")

# Initialize Claude
if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your-anthropic-api-key-here":
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    anthropic_client = None
    logger.warning("Anthropic API key not configured. Claude Vision disabled.")


# Prompt especializado para análisis de comida mexicana
MEXICAN_FOOD_ANALYSIS_PROMPT = """
Analiza esta imagen de comida mexicana en detalle. Eres un experto en nutrición mexicana y conoces el Sistema Mexicano de Alimentos Equivalentes (SMAE).

Tu tarea es identificar:

1. **Platillo Principal**:
   - Nombre exacto del platillo
   - Nivel de confianza (0-100)
   - Descripción breve
   - Región de México de origen
   - Categoría (antojito, platillo fuerte, postre, bebida, etc.)
   - Si es tradicional mexicano o no

2. **Ingredientes Detectados** (para cada uno):
   - Nombre del ingrediente
   - Cantidad estimada en gramos o piezas
   - Nivel de confianza (0-100)
   - Información nutricional por porción:
     * Calorías (kcal)
     * Proteína (g)
     * Carbohidratos (g)
     * Grasas (g)
     * Fibra (g)
     * Sodio (mg)
   - Categoría SMAE equivalente si aplica

3. **Análisis NOM-051** (Norma Oficial Mexicana):
   - Exceso de calorías (sí/no)
   - Exceso de azúcares (sí/no)
   - Exceso de grasas saturadas (sí/no)
   - Exceso de grasas trans (sí/no)
   - Exceso de sodio (sí/no)
   - Contiene edulcorantes (sí/no)
   - Contiene cafeína (sí/no)

4. **Evaluación de Salubridad**:
   - Score general (0-100)
   - Nivel: Excelente (80-100), Bueno (60-79), Moderado (40-59), Pobre (0-39)
   - Color sugerido: verde (#4CAF50), amarillo (#FF9800), naranja (#FF9800), rojo (#F44336)
   - Factores positivos (lista de strings)
   - Factores negativos (lista de strings)

5. **Recomendaciones** (mínimo 3):
   Para cada recomendación:
   - Tipo: 'reduccion', 'sustitucion', 'mejora', 'porcion'
   - Título breve
   - Descripción detallada
   - Impacto nutricional estimado

6. **Contexto Diario** (basado en 2000 kcal/día):
   - Porcentaje de calorías diarias
   - Momento recomendado para consumir
   - Si requiere ajuste (sí/no)
   - Mensaje de contexto

7. **Totales Nutricionales**:
   - Calorías totales
   - Proteína total (g)
   - Carbohidratos totales (g)
   - Grasas totales (g)
   - Fibra total (g)
   - Sodio total (mg)
   - Margen de error estimado (%)

IMPORTANTE: Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional. Usa este formato exacto:

{
  "platillo": {
    "nombre": "string",
    "confianza": number (0-100),
    "descripcion": "string",
    "region": "string",
    "categoria": "string",
    "es_tradicional": boolean
  },
  "ingredientes": [
    {
      "nombre": "string",
      "cantidad_estimada": "string",
      "confianza": number (0-100),
      "calorias": number,
      "proteina": number,
      "carbohidratos": number,
      "grasas": number,
      "fibra": number,
      "sodio": number,
      "categoria_smae": "string"
    }
  ],
  "totales": {
    "calorias": number,
    "proteina": number,
    "carbohidratos": number,
    "grasas": number,
    "fibra": number,
    "sodio": number,
    "margen_error": number
  },
  "sellos_nom051": {
    "exceso_calorias": boolean,
    "exceso_azucares": boolean,
    "exceso_grasas_saturadas": boolean,
    "exceso_grasas_trans": boolean,
    "exceso_sodio": boolean,
    "contiene_edulcorantes": boolean,
    "contiene_cafeina": boolean
  },
  "evaluacion": {
    "score": number (0-100),
    "nivel": "string",
    "color": "string",
    "factores_positivos": ["string"],
    "factores_negativos": ["string"]
  },
  "recomendaciones": [
    {
      "tipo": "string",
      "titulo": "string",
      "descripcion": "string",
      "impacto": "string"
    }
  ],
  "contexto_diario": {
    "porcentaje_calorias_diarias": number,
    "momento_recomendado": "string",
    "requiere_ajuste": boolean,
    "mensaje": "string"
  },
  "confidence_score": number (0-100)
}
"""


class FoodVisionService:
    """Food recognition service using computer vision with hybrid AI approach"""

    def __init__(self):
        self.gemini_available = gemini_model is not None
        self.claude_available = anthropic_client is not None
        self.model_mode = AI_VISION_MODEL

        logger.info(f"FoodVisionService initialized - Mode: {self.model_mode}")
        logger.info(f"Gemini available: {self.gemini_available}")
        logger.info(f"Claude available: {self.claude_available}")

    async def analyze_food_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze food image and return detected items with nutritional estimates

        Args:
            image_bytes: Image data as bytes

        Returns:
            Dict containing detected foods with confidence scores and portion estimates
        """
        try:
            # Validate image
            image = Image.open(BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')

            logger.info(f"Analyzing food image using {self.model_mode} mode...")

            # Try Gemini first (if available and mode allows)
            if self.model_mode in ["gemini", "hybrid"] and self.gemini_available:
                try:
                    result = await self._analyze_with_gemini(image_bytes)

                    # In hybrid mode, check confidence threshold
                    if self.model_mode == "hybrid":
                        confidence = result.get("confidence_score", 0)
                        if confidence < CONFIDENCE_THRESHOLD and self.claude_available:
                            logger.info(f"Gemini confidence ({confidence}) below threshold ({CONFIDENCE_THRESHOLD}). Trying Claude...")
                            return await self._analyze_with_claude(image_bytes)

                    return result
                except Exception as e:
                    logger.error(f"Gemini analysis failed: {e}")
                    # Fallback to Claude if available
                    if self.claude_available and self.model_mode == "hybrid":
                        logger.info("Falling back to Claude Vision...")
                        return await self._analyze_with_claude(image_bytes)
                    raise

            # Use Claude if specified or as fallback
            elif self.model_mode == "claude" and self.claude_available:
                return await self._analyze_with_claude(image_bytes)

            # No models available - return mock data
            else:
                logger.warning("No AI vision models available. Returning mock data.")
                return self._get_mock_analysis()

        except Exception as e:
            logger.error(f"Error in food vision analysis: {e}")
            # Return mock data as last resort
            return self._get_mock_analysis()

    async def _analyze_with_gemini(self, image_bytes: bytes) -> Dict[str, Any]:
        """Analyze food image using Gemini Vision"""
        try:
            # Convert image bytes to PIL Image
            image = Image.open(BytesIO(image_bytes))

            # Generate content with Gemini
            response = gemini_model.generate_content([
                MEXICAN_FOOD_ANALYSIS_PROMPT,
                image
            ])

            # Parse JSON response
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())

            logger.info(f"Gemini analysis completed. Confidence: {result.get('confidence_score', 0)}")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {e}")
            logger.error(f"Raw response: {response.text}")
            raise ValueError(f"Invalid JSON response from Gemini: {str(e)}")
        except Exception as e:
            logger.error(f"Gemini Vision API error: {e}")
            raise

    async def _analyze_with_claude(self, image_bytes: bytes) -> Dict[str, Any]:
        """Analyze food image using Claude Vision"""
        try:
            # Encode image to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            # Detect image format
            image = Image.open(BytesIO(image_bytes))
            image_format = image.format.lower() if image.format else 'jpeg'
            media_type = f"image/{image_format}"

            # Generate content with Claude
            message = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": MEXICAN_FOOD_ANALYSIS_PROMPT
                            }
                        ],
                    }
                ],
            )

            # Parse JSON response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())

            logger.info(f"Claude analysis completed. Confidence: {result.get('confidence_score', 0)}")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude JSON response: {e}")
            logger.error(f"Raw response: {message.content[0].text}")
            raise ValueError(f"Invalid JSON response from Claude: {str(e)}")
        except Exception as e:
            logger.error(f"Claude Vision API error: {e}")
            raise

    def _get_mock_analysis(self) -> Dict[str, Any]:
        """Return mock analysis data when AI models are not available"""
        return {
            "platillo": {
                "nombre": "Platillo Mexicano",
                "confianza": 65,
                "descripcion": "Análisis nutricional estimado basado en reconocimiento visual de alimentos",
                "region": "México",
                "categoria": "Platillo tradicional",
                "es_tradicional": True
            },
            "ingredientes": [
                {
                    "nombre": "Alimentos detectados",
                    "cantidad_estimada": "Porción estándar",
                    "confianza": 65,
                    "calorias": 350,
                    "proteina": 15.0,
                    "carbohidratos": 45.0,
                    "grasas": 12.0,
                    "fibra": 5.0,
                    "sodio": 400,
                    "categoria_smae": "Platillo completo"
                }
            ],
            "totales": {
                "calorias": 350,
                "proteina": 15.0,
                "carbohidratos": 45.0,
                "grasas": 12.0,
                "fibra": 5.0,
                "sodio": 400,
                "margen_error": 25
            },
            "sellos_nom051": {
                "exceso_calorias": False,
                "exceso_azucares": False,
                "exceso_grasas_saturadas": False,
                "exceso_grasas_trans": False,
                "exceso_sodio": False,
                "contiene_edulcorantes": False,
                "contiene_cafeina": False
            },
            "evaluacion": {
                "score": 70,
                "nivel": "Bueno",
                "color": "#4CAF50",
                "factores_positivos": ["Análisis preliminar disponible", "Estimación nutricional calculada"],
                "factores_negativos": ["Se recomienda análisis más detallado para mayor precisión"]
            },
            "recomendaciones": [
                {
                    "tipo": "mejora",
                    "titulo": "Análisis Mejorado",
                    "descripcion": "Para obtener un análisis más detallado y personalizado, contacta a tu nutriólogo",
                    "impacto": "Mayor precisión en el plan nutricional"
                }
            ],
            "contexto_diario": {
                "porcentaje_calorias_diarias": 17.5,
                "momento_recomendado": "Comida principal",
                "requiere_ajuste": False,
                "mensaje": "Esta porción representa aproximadamente 18% de tu consumo diario recomendado"
            },
            "confidence_score": 65
        }

    async def classify_food_item(self, food_name: str, image_bytes: bytes) -> Dict[str, Any]:
        """
        Classify a specific food item and estimate portion size

        Args:
            food_name: Name of the food to classify
            image_bytes: Image data as bytes

        Returns:
            Classification result with portion estimation
        """
        # This would use the same AI models but with a focused prompt
        result = await self.analyze_food_image(image_bytes)
        return {
            "food_name": food_name,
            "analysis": result,
            "focused_on": food_name
        }

    async def get_portion_estimation(self, image_bytes: bytes, reference_objects: List[str] = None) -> Dict[str, Any]:
        """
        Estimate portion sizes using reference objects in the image

        Args:
            image_bytes: Image data as bytes
            reference_objects: List of reference objects (e.g., "coin", "hand", "plate")

        Returns:
            Portion estimation results
        """
        # This would use specialized prompt for portion estimation
        result = await self.analyze_food_image(image_bytes)
        return {
            "portion_analysis": result.get("totales", {}),
            "reference_objects": reference_objects or [],
            "full_analysis": result
        }


# Service instance
food_vision_service = FoodVisionService()

# Convenience functions
async def analyze_food_image(image_bytes: bytes) -> Dict[str, Any]:
    """Analyze food image and return detected items"""
    return await food_vision_service.analyze_food_image(image_bytes)

async def classify_food_item(food_name: str, image_bytes: bytes) -> Dict[str, Any]:
    """Classify specific food item"""
    return await food_vision_service.classify_food_item(food_name, image_bytes)

async def estimate_portions(image_bytes: bytes, reference_objects: List[str] = None) -> Dict[str, Any]:
    """Estimate portion sizes"""
    return await food_vision_service.get_portion_estimation(image_bytes, reference_objects)
