from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.trophology_service import TrophologyService
from domain.trophology.models import FoodCategory, FoodCompatibility, FoodCombinationIssue
from pydantic import BaseModel

router = APIRouter()

class ValidationRequest(BaseModel):
    category_ids: List[int]

class ValidationResponse(BaseModel):
    valid: bool
    issues: List[FoodCombinationIssue]
    suggestions: List[str]

@router.get("/categories", response_model=List[FoodCategory])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """List all food categories."""
    service = TrophologyService(db)
    return await service.get_categories()

@router.get("/compatibilities", response_model=List[FoodCompatibility])
async def get_compatibilities(
    db: AsyncSession = Depends(get_db)
):
    """List all compatibility rules."""
    service = TrophologyService(db)
    return await service.get_compatibilities()

@router.post("/validate", response_model=ValidationResponse)
async def validate_combination(
    request: ValidationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Validate a combination of foods."""
    service = TrophologyService(db)
    result = await service.validate_combination(request.category_ids)
    return result
