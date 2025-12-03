from typing import List, Optional, Dict
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.auth import get_current_user
from domain.auth.models import AuthUser
from services.digestion_service import DigestionService
from domain.digestion.models import DigestionLog, StoolConsistency, StoolColor
from pydantic import BaseModel

router = APIRouter()

class DigestionLogCreate(BaseModel):
    stool_consistency: Optional[StoolConsistency] = None
    stool_color: Optional[StoolColor] = None
    stool_odor: Optional[str] = None
    bloating: bool = False
    gas: bool = False
    acidity: bool = False
    abdominal_pain: bool = False
    comfort_level: int = 5
    notes: Optional[str] = None

@router.post("/log", response_model=DigestionLog)
async def log_digestion(
    log_data: DigestionLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Log digestion details for today."""
    service = DigestionService(db)
    return await service.log_digestion(current_user.id, log_data.dict(exclude_unset=True))

@router.get("/today", response_model=Optional[DigestionLog])
async def get_today_log(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get digestion log for today."""
    service = DigestionService(db)
    return await service.get_today_log(current_user.id)

@router.get("/history", response_model=List[DigestionLog])
async def get_history(
    limit: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get digestion history."""
    service = DigestionService(db)
    return await service.get_history(current_user.id, limit)

@router.get("/stats", response_model=Dict)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get digestion statistics."""
    service = DigestionService(db)
    return await service.get_stats(current_user.id)
