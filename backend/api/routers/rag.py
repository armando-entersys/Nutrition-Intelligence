"""
RAG Router
===========

Endpoints para el sistema RAG (Retrieval Augmented Generation).
Permite a la IA consultar datos relevantes para respuestas personalizadas.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.auth import get_current_user
from core.database import get_async_session
from models.user import User
from services.rag.search_service import RAGSearchService
from services.rag.context_builder import RAGContextBuilder
from services.ai.gemini_service import GeminiService


router = APIRouter(prefix="/rag", tags=["rag"])


# ============================================================================
# Pydantic Models
# ============================================================================

class SearchProductsRequest(BaseModel):
    """Request para búsqueda de productos"""
    query: str
    limit: int = 10
    verified_only: bool = False


class SearchFoodsRequest(BaseModel):
    """Request para búsqueda de alimentos"""
    query: str
    limit: int = 10
    category: Optional[str] = None


class SearchCombinedRequest(BaseModel):
    """Request para búsqueda combinada"""
    query: str
    search_products: bool = True
    search_foods: bool = True
    limit_per_source: int = 5


class BuildContextRequest(BaseModel):
    """Request para construir contexto de usuario"""
    include_scan_history: bool = True
    include_favorites: bool = True
    history_days: int = 30


class ChatRequest(BaseModel):
    """Request para chat con IA usando RAG"""
    message: str
    include_context: bool = True
    include_search_results: bool = True


# ============================================================================
# Search Endpoints
# ============================================================================

@router.post("/search/products")
async def search_products(
    request: SearchProductsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Buscar productos NOM-051

    Busca en la base de datos de productos usando similitud de texto.
    Retorna productos globales y productos privados del usuario.

    **Permisos**: Usuario autenticado
    """
    search_service = RAGSearchService(db)

    products = await search_service.search_products(
        query=request.query,
        user_id=current_user.id,
        limit=request.limit,
        verified_only=request.verified_only,
    )

    return {
        "query": request.query,
        "total_results": len(products),
        "products": products,
    }


@router.post("/search/foods")
async def search_foods(
    request: SearchFoodsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Buscar alimentos en base SMAE

    Busca en la base de datos de alimentos mexicanos (SMAE).

    **Permisos**: Usuario autenticado
    """
    search_service = RAGSearchService(db)

    foods = await search_service.search_foods(
        query=request.query,
        limit=request.limit,
        category=request.category,
    )

    return {
        "query": request.query,
        "category": request.category,
        "total_results": len(foods),
        "foods": foods,
    }


@router.post("/search/combined")
async def search_combined(
    request: SearchCombinedRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Búsqueda combinada en productos y alimentos

    Busca simultáneamente en productos NOM-051 y alimentos SMAE.
    Útil para búsquedas generales donde no se sabe si es producto o alimento.

    **Permisos**: Usuario autenticado
    """
    search_service = RAGSearchService(db)

    results = await search_service.search_combined(
        query=request.query,
        user_id=current_user.id,
        search_products=request.search_products,
        search_foods=request.search_foods,
        limit_per_source=request.limit_per_source,
    )

    return {
        "query": request.query,
        "total_products": len(results["products"]),
        "total_foods": len(results["foods"]),
        "results": results,
    }


# ============================================================================
# Context Endpoints
# ============================================================================

@router.post("/context/user")
async def get_user_context(
    request: BuildContextRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Obtener contexto completo del usuario

    Retorna el historial de escaneos, alimentos favoritos y estadísticas
    del usuario para que la IA pueda proporcionar respuestas personalizadas.

    **Permisos**: Usuario autenticado (solo ve sus propios datos)
    """
    context_builder = RAGContextBuilder(db)

    context = await context_builder.build_user_context(
        user_id=current_user.id,
        include_scan_history=request.include_scan_history,
        include_favorites=request.include_favorites,
        history_days=request.history_days,
    )

    return context


@router.get("/context/patient/{patient_id}")
async def get_patient_context(
    patient_id: int,
    history_days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Obtener contexto completo de un paciente

    Retorna el historial, favoritos y estadísticas de un paciente.
    Solo accesible para nutriólogos que tienen al paciente asignado.

    **Permisos**: Solo nutriólogos con acceso al paciente
    """
    # Verificar que el usuario actual es nutriólogo
    if current_user.role != "nutritionist":
        raise HTTPException(
            status_code=403,
            detail="Solo los nutriólogos pueden acceder a datos de pacientes"
        )

    context_builder = RAGContextBuilder(db)

    try:
        context = await context_builder.build_patient_context(
            patient_id=patient_id,
            nutritionist_id=current_user.id,
        )
        return context

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


@router.post("/context/search")
async def get_search_context(
    query: str = Query(..., min_length=1, max_length=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Obtener contexto basado en búsqueda

    Realiza una búsqueda y retorna resultados estructurados para la IA.

    **Permisos**: Usuario autenticado
    """
    context_builder = RAGContextBuilder(db)

    context = await context_builder.build_search_context(
        query=query,
        user_id=current_user.id,
    )

    return context


# ============================================================================
# AI Chat Endpoint (Main RAG Endpoint)
# ============================================================================

@router.post("/chat")
async def chat_with_rag(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Chat con IA usando RAG

    Endpoint principal para chat con IA context-aware.
    Automáticamente recupera contexto del usuario y resultados de búsqueda.

    **Flujo**:
    1. Analiza el mensaje del usuario
    2. Recupera contexto relevante (historial, favoritos, etc.)
    3. Realiza búsquedas si es necesario
    4. Construye prompt para la IA con contexto
    5. Envía a la IA y retorna respuesta

    **Permisos**: Usuario autenticado
    """
    context_builder = RAGContextBuilder(db)

    # Construir contexto del usuario
    user_context = None
    if request.include_context:
        user_context = await context_builder.build_user_context(
            user_id=current_user.id,
            include_scan_history=True,
            include_favorites=True,
            history_days=30,
        )

    # Realizar búsqueda si es necesario
    search_results = None
    if request.include_search_results:
        search_context = await context_builder.build_search_context(
            query=request.message,
            user_id=current_user.id,
        )
        search_results = search_context["results"]

    # Formatear contexto para el prompt
    formatted_context = ""
    if user_context:
        formatted_context = context_builder.format_context_for_prompt(
            context=user_context,
            max_products=20,
        )

    # Inicializar servicio de IA
    gemini_service = GeminiService()

    # Construir prompt para la IA
    system_prompt = """Eres un asistente nutricional experto en México.
Tienes acceso a la base de datos de productos NOM-051 y alimentos SMAE.
Proporciona respuestas personalizadas basadas en el historial del usuario.

Siempre:
- Sé empático y motivador
- Basa tus respuestas en datos científicos
- Considera el contexto mexicano (NOM-051, alimentos tradicionales)
- Proporciona alternativas saludables cuando sea posible
- Explica los sellos de advertencia cuando aparezcan productos
"""

    # Generar respuesta con Gemini AI
    ai_response = await gemini_service.chat_with_context(
        user_message=request.message,
        system_prompt=system_prompt,
        context=formatted_context,
    )

    # Verificar si hubo error
    if not ai_response.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Error generating AI response: {ai_response.get('error', 'Unknown error')}"
        )

    return {
        "message": request.message,
        "user_id": current_user.id,
        "context_included": request.include_context,
        "search_included": request.include_search_results,
        "ai_response": ai_response.get("response"),
        "model": ai_response.get("model"),
        "usage": ai_response.get("usage"),
        "user_context_summary": {
            "scan_count": len(user_context.get("scan_history", [])) if user_context else 0,
            "favorite_foods_count": len(user_context.get("favorite_foods", [])) if user_context else 0,
        } if user_context else None,
        "search_results_summary": {
            "products_count": len(search_results.get("products", [])) if search_results else 0,
            "foods_count": len(search_results.get("foods", [])) if search_results else 0,
        } if search_results else None,
    }


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health")
async def rag_health():
    """
    Health check del servicio RAG

    Verifica que el servicio RAG esté disponible.
    """
    return {
        "status": "healthy",
        "service": "RAG (Retrieval Augmented Generation)",
        "version": "1.0.0",
        "endpoints": {
            "search": [
                "/rag/search/products",
                "/rag/search/foods",
                "/rag/search/combined",
            ],
            "context": [
                "/rag/context/user",
                "/rag/context/patient/{patient_id}",
                "/rag/context/search",
            ],
            "chat": [
                "/rag/chat",
            ],
        },
    }
