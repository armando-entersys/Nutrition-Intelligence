"""
AI Services
===========

Servicios de inteligencia artificial para el sistema.

Componentes:
- gemini_service: Servicio de Google Gemini AI para chat y generación de texto
"""

from .gemini_service import GeminiService

__all__ = [
    'GeminiService',
]
