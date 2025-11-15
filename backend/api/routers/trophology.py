"""
Trophology API endpoints
Food combination validation based on Lezaeta's principles
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from pydantic import BaseModel, Field

from core.database import get_async_session
from services.trophology.trophology_service import TrophologyService
from domain.trophology.models import FoodCategory, FoodCompatibility

router = APIRouter()


# Request/Response models
class ValidateCombinationRequest(BaseModel):
    """Request to validate a food combination"""
    category_ids: List[int] = Field(
        ...,
        min_length=1,
        description="List of food category IDs to validate"
    )


class ValidateCombinationResponse(BaseModel):
    """Response from combination validation"""
    valid: bool
    issues: List[dict]
    suggestions: List[str]
    lezaeta_principle: str


class CategoryResponse(BaseModel):
    """Food category response"""
    id: int
    name: str
    description: str | None
    examples: str | None


class CompatibilityResponse(BaseModel):
    """Compatibility rule response"""
    id: int
    category1_id: int
    category1_name: str
    category2_id: int
    category2_name: str
    compatible: bool
    reason: str | None
    severity: str | None
    note: str | None
    page_reference: str | None


class CompatibilitiesForCategoryResponse(BaseModel):
    """Response with compatible/incompatible categories"""
    category: CategoryResponse
    compatible: List[CategoryResponse]
    incompatible: List[CategoryResponse]


@router.get(
    "/categories",
    response_model=List[CategoryResponse],
    summary="Listar categorías de alimentos",
    description="Obtiene las 9 categorías de alimentos según la Trofología de Lezaeta"
)
async def get_categories(
    db: Session = Depends(get_async_session)
):
    """
    Obtiene todas las categorías de alimentos según Lezaeta:

    1. Frutas Ácidas
    2. Frutas Dulces
    3. Frutas Aceitosas
    4. Frutas Harináceas
    5. Almidones
    6. Hortalizas/Verduras
    7. Proteínas
    8. Azúcares
    9. Grasas
    """
    service = TrophologyService(db)
    categories = service.get_all_categories()

    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            examples=cat.examples
        )
        for cat in categories
    ]


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="Obtener categoría específica",
    description="Obtiene una categoría de alimentos por ID"
)
async def get_category(
    category_id: int,
    db: Session = Depends(get_async_session)
):
    """Obtiene una categoría específica por ID"""
    service = TrophologyService(db)
    category = service.get_category_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )

    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        examples=category.examples
    )


@router.get(
    "/categories/{category_id}/compatibilities",
    response_model=CompatibilitiesForCategoryResponse,
    summary="Obtener compatibilidades de una categoría",
    description="Obtiene todas las categorías compatibles e incompatibles con una categoría dada"
)
async def get_compatibilities_for_category(
    category_id: int,
    db: Session = Depends(get_async_session)
):
    """
    Obtiene todas las categorías compatibles e incompatibles

    Útil para mostrar en UI: "Si eliges X, puedes/no puedes combinar con Y"
    """
    service = TrophologyService(db)

    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )

    compatibilities = service.get_compatibilities_for_category(category_id)

    return CompatibilitiesForCategoryResponse(
        category=CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            examples=category.examples
        ),
        compatible=[
            CategoryResponse(
                id=cat.id,
                name=cat.name,
                description=cat.description,
                examples=cat.examples
            )
            for cat in compatibilities["compatible"]
        ],
        incompatible=[
            CategoryResponse(
                id=cat.id,
                name=cat.name,
                description=cat.description,
                examples=cat.examples
            )
            for cat in compatibilities["incompatible"]
        ]
    )


@router.post(
    "/validate",
    response_model=ValidateCombinationResponse,
    summary="Validar combinación de alimentos",
    description="Valida si una combinación de categorías de alimentos es compatible según Lezaeta"
)
async def validate_combination(
    request: ValidateCombinationRequest,
    db: Session = Depends(get_async_session)
):
    """
    Valida una combinación de alimentos según las reglas de Lezaeta

    Principio fundamental de Lezaeta:
    "Para evitar los inconvenientes de las malas combinaciones, la mejor regla
    será simplificar cada comida a uno o dos productos" (Página 119)

    Retorna:
    - valid: Si la combinación es válida
    - issues: Lista de problemas encontrados (si los hay)
    - suggestions: Sugerencias para mejorar la combinación
    - lezaeta_principle: Principio relevante de Lezaeta
    """
    service = TrophologyService(db)

    # Validate that all category IDs exist
    for cat_id in request.category_ids:
        if not service.get_category_by_id(cat_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {cat_id} no encontrada"
            )

    result = service.validate_combination(request.category_ids)

    return ValidateCombinationResponse(
        valid=result["valid"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        lezaeta_principle=result["lezaeta_principle"]
    )


@router.get(
    "/compatibility-rules",
    response_model=List[CompatibilityResponse],
    summary="Listar todas las reglas de compatibilidad",
    description="Obtiene todas las reglas de compatibilidad/incompatibilidad entre categorías"
)
async def get_all_compatibility_rules(
    db: Session = Depends(get_async_session)
):
    """
    Obtiene todas las reglas de compatibilidad

    Útil para:
    - Documentación educativa
    - Mostrar tabla completa de combinaciones
    - Debugging
    """
    service = TrophologyService(db)
    rules = service.get_all_compatibility_rules()

    response = []
    for rule in rules:
        cat1 = service.get_category_by_id(rule.category1_id)
        cat2 = service.get_category_by_id(rule.category2_id)

        response.append(CompatibilityResponse(
            id=rule.id,
            category1_id=rule.category1_id,
            category1_name=cat1.name if cat1 else "Unknown",
            category2_id=rule.category2_id,
            category2_name=cat2.name if cat2 else "Unknown",
            compatible=rule.compatible,
            reason=rule.reason,
            severity=rule.severity.value if rule.severity else None,
            note=rule.note,
            page_reference=rule.page_reference
        ))

    return response


@router.get(
    "/search",
    response_model=List[CategoryResponse],
    summary="Buscar categoría por alimento",
    description="Busca a qué categoría pertenece un alimento específico"
)
async def search_food(
    q: str = Query(..., description="Nombre del alimento a buscar (ej: 'naranja', 'papa', 'nuez')"),
    db: Session = Depends(get_async_session)
):
    """
    Busca a qué categoría(s) pertenece un alimento

    Ejemplo:
    - q="naranja" → Retorna "Frutas Ácidas"
    - q="papa" → Retorna "Almidones"
    - q="nuez" → Retorna "Frutas Aceitosas"
    """
    service = TrophologyService(db)
    categories = service.search_categories_by_food(q)

    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            examples=cat.examples
        )
        for cat in categories
    ]
