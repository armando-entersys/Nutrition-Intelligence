"""
Gemini AI Service
=================

Servicio para integración con Google Gemini AI.
Proporciona funcionalidades de chat y generación de texto context-aware.
"""

import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Servicio de Gemini AI

    Maneja todas las interacciones con la API de Google Gemini,
    incluyendo chat context-aware para el sistema nutricional.
    """

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.gemini_api_key
        self.default_model = settings.default_ai_model

        if self.api_key:
            genai.configure(api_key=self.api_key)
            logger.info(f"Gemini AI service initialized with model: {self.default_model}")
        else:
            logger.warning("Gemini API key not configured. AI features will not work.")

    def _get_safety_settings(self) -> Dict:
        """
        Configuración de seguridad para Gemini

        Configuramos filtros de contenido para un contexto nutricional profesional.
        """
        return {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

    def _get_generation_config(self) -> Dict:
        """
        Configuración de generación de texto

        Ajustes optimizados para respuestas nutricionales:
        - Temperature: 0.7 (balance entre creatividad y precisión)
        - Max tokens: 2048 (respuestas detalladas pero no excesivas)
        """
        return {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    async def chat_with_context(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Chat con IA usando contexto

        Args:
            user_message: Mensaje del usuario
            system_prompt: Instrucciones del sistema para la IA
            context: Contexto adicional (historial, productos, etc.)

        Returns:
            Diccionario con la respuesta y metadatos
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Gemini API key not configured",
                "response": None,
            }

        try:
            # Inicializar modelo
            model = genai.GenerativeModel(
                model_name=self.default_model,
                generation_config=self._get_generation_config(),
                safety_settings=self._get_safety_settings(),
            )

            # Construir prompt completo
            full_prompt = self._build_prompt(
                user_message=user_message,
                system_prompt=system_prompt,
                context=context,
            )

            logger.info(f"Sending request to Gemini API (message length: {len(user_message)})")

            # Generar respuesta
            response = model.generate_content(full_prompt)

            # Verificar si la respuesta fue bloqueada
            if not response.text:
                logger.warning("Gemini response was blocked by safety filters")
                return {
                    "success": False,
                    "error": "Response blocked by safety filters",
                    "response": None,
                    "prompt_feedback": response.prompt_feedback,
                }

            logger.info(f"Gemini response received (length: {len(response.text)})")

            return {
                "success": True,
                "response": response.text,
                "model": self.default_model,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None,
                },
            }

        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "response": None,
            }

    def _build_prompt(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
    ) -> str:
        """
        Construir prompt completo para Gemini

        Args:
            user_message: Mensaje del usuario
            system_prompt: Instrucciones del sistema
            context: Contexto adicional

        Returns:
            Prompt completo formateado
        """
        parts = []

        # Sistema (instrucciones para la IA)
        if system_prompt:
            parts.append(f"# INSTRUCCIONES DEL SISTEMA\n{system_prompt}\n")
        else:
            parts.append(self._get_default_system_prompt())

        # Contexto (datos del usuario, productos, etc.)
        if context:
            parts.append(f"\n# CONTEXTO\n{context}\n")

        # Mensaje del usuario
        parts.append(f"\n# PREGUNTA DEL USUARIO\n{user_message}\n")

        # Instrucción final
        parts.append("\n# INSTRUCCIÓN\nProporciona una respuesta útil, precisa y empática basada en el contexto proporcionado.")

        return "\n".join(parts)

    def _get_default_system_prompt(self) -> str:
        """
        Prompt de sistema por defecto para chat nutricional

        Returns:
            Prompt de sistema en español
        """
        return """# INSTRUCCIONES DEL SISTEMA

Eres un asistente nutricional experto en México, especializado en:

1. **Normativa Mexicana NOM-051-SCFI/SSA1-2010**: Conoces perfectamente los sellos de advertencia y etiquetado frontal de alimentos y bebidas.

2. **Sistema Mexicano de Alimentos Equivalentes (SMAE)**: Tienes acceso a la base de datos completa de alimentos mexicanos con sus valores nutricionales.

3. **Nutrición Personalizada**: Proporcionas recomendaciones basadas en el historial del usuario, sus objetivos y restricciones alimentarias.

## Principios de tu trabajo:

✅ **Siempre**:
- Sé empático, motivador y profesional
- Basa tus respuestas en datos científicos y evidencia
- Considera el contexto cultural mexicano (alimentos tradicionales, NOM-051)
- Explica los sellos de advertencia cuando aparezcan productos
- Proporciona alternativas saludables específicas
- Usa el contexto del usuario para personalizar respuestas

❌ **Nunca**:
- Diagnostiques enfermedades (remite a profesionales de salud)
- Proporciones información médica específica sin advertencias
- Juzgues las elecciones alimentarias del usuario
- Inventes datos nutricionales (usa solo los proporcionados)

## Formato de respuestas:

- **Conciso**: Respuestas claras de 2-4 párrafos
- **Estructurado**: Usa bullets, negritas y secciones cuando sea apropiado
- **Accionable**: Proporciona pasos concretos que el usuario pueda seguir
- **Contextual**: Referencia productos específicos del historial del usuario cuando sea relevante

## Sellos de Advertencia NOM-051:

Cuando un producto tenga sellos, explícalos:
- 🔴 **Exceso calorías**: Más de 275 kcal por 100g
- 🔴 **Exceso azúcares**: Más de 10g por 100g
- 🔴 **Exceso grasas saturadas**: Más de 4g por 100g
- 🔴 **Exceso grasas trans**: Más de 0.5g por 100g
- 🔴 **Exceso sodio**: Más de 300mg por 100g

Siempre sugiere alternativas sin sellos o con menos sellos cuando sea posible.
"""

    async def nutritional_analysis(
        self,
        product_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Análisis nutricional de un producto

        Args:
            product_data: Datos del producto a analizar

        Returns:
            Análisis nutricional generado por IA
        """
        # Construir prompt de análisis
        product_name = product_data.get("nombre", "Producto desconocido")
        marca = product_data.get("marca", "Sin marca")
        calorias = product_data.get("calorias", "N/A")
        azucares = product_data.get("azucares", "N/A")
        grasas = product_data.get("grasas_saturadas", "N/A")
        sodio = product_data.get("sodio", "N/A")

        sellos = []
        if product_data.get("exceso_calorias"):
            sellos.append("Exceso calorías")
        if product_data.get("exceso_azucares"):
            sellos.append("Exceso azúcares")
        if product_data.get("exceso_grasas_saturadas"):
            sellos.append("Exceso grasas saturadas")
        if product_data.get("exceso_sodio"):
            sellos.append("Exceso sodio")

        prompt = f"""Analiza este producto alimenticio según la NOM-051:

Producto: {product_name} - {marca}
Calorías: {calorias} kcal
Azúcares: {azucares}g
Grasas saturadas: {grasas}g
Sodio: {sodio}mg
Sellos de advertencia: {', '.join(sellos) if sellos else 'Ninguno'}

Proporciona:
1. Evaluación nutricional (2-3 líneas)
2. Impacto de los sellos de advertencia
3. Recomendaciones de consumo
4. Alternativas más saludables (2-3 opciones)

Respuesta concisa y práctica."""

        return await self.chat_with_context(
            user_message=prompt,
            system_prompt=self._get_default_system_prompt(),
        )

    async def meal_plan_suggestions(
        self,
        user_profile: Dict[str, Any],
        dietary_restrictions: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Generar sugerencias de plan alimenticio

        Args:
            user_profile: Perfil del usuario (edad, peso, objetivo, etc.)
            dietary_restrictions: Restricciones alimentarias

        Returns:
            Sugerencias de plan alimenticio
        """
        age = user_profile.get("edad", "N/A")
        weight = user_profile.get("peso_kg", "N/A")
        height = user_profile.get("altura_cm", "N/A")
        goal = user_profile.get("objetivo_nutricional", "mantener peso")
        restrictions = dietary_restrictions or user_profile.get("restricciones_alimentarias", [])

        prompt = f"""Crea sugerencias de plan alimenticio para:

Edad: {age} años
Peso: {weight} kg
Altura: {height} cm
Objetivo: {goal}
Restricciones: {', '.join(restrictions) if restrictions else 'Ninguna'}

Proporciona:
1. Distribución de macronutrientes recomendada
2. Calorías diarias aproximadas
3. 3 ejemplos de comidas (desayuno, comida, cena)
4. Snacks saludables recomendados

Usa alimentos mexicanos tradicionales cuando sea posible."""

        return await self.chat_with_context(
            user_message=prompt,
            system_prompt=self._get_default_system_prompt(),
        )
