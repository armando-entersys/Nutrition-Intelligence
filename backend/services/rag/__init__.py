"""
RAG (Retrieval Augmented Generation) Service
=============================================

Sistema de búsqueda y recuperación de información para IA

Este módulo proporciona funcionalidades de RAG para que la IA
pueda consultar y recuperar información relevante de la base de datos
para proporcionar respuestas personalizadas y context-aware.

Componentes:
- context_builder: Construye contexto para el prompt de IA
- product_search: Búsqueda de productos NOM-051
- food_search: Búsqueda de alimentos SMAE
- user_context: Recupera historial y datos del usuario
- patient_context: Recupera datos de pacientes (nutriólogos)
"""

from .context_builder import RAGContextBuilder
from .search_service import RAGSearchService

__all__ = [
    'RAGContextBuilder',
    'RAGSearchService',
]
