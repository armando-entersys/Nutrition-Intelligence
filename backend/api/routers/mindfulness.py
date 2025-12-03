from typing import List, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.auth import get_current_user
from domain.auth.models import AuthUser
from services.mindfulness_service import MindfulnessService
from domain.mindfulness.models import HungerLog, STOPPractice, HungerLevel
from pydantic import BaseModel

router = APIRouter()

class HungerLogCreate(BaseModel):
    hunger_level_before: Optional[HungerLevel] = None
    emotion_before: Optional[str] = None
    hunger_level_after: Optional[HungerLevel] = None
    satisfaction_level: Optional[int] = None
    notes: Optional[str] = None

class STOPPracticeCreate(BaseModel):
    stress_level_before: int
    stress_level_after: int
    observations: Optional[str] = None

@router.post("/hunger", response_model=HungerLog)
async def log_hunger(
    log_data: HungerLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Log hunger/fullness."""
    service = MindfulnessService(db)
    return await service.log_hunger(current_user.id, log_data.dict(exclude_unset=True))

@router.get("/hunger", response_model=List[HungerLog])
async def get_hunger_logs(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get recent hunger logs."""
    service = MindfulnessService(db)
    return await service.get_hunger_logs(current_user.id, limit)

@router.post("/stop", response_model=STOPPractice)
async def log_stop_practice(
    practice_data: STOPPracticeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Log STOP practice."""
    service = MindfulnessService(db)
    return await service.log_stop_practice(current_user.id, practice_data.dict())

@router.get("/stop", response_model=List[STOPPractice])
async def get_stop_practices(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get recent STOP practices."""
    service = MindfulnessService(db)
    return await service.get_stop_practices(current_user.id, limit)

@router.get("/stats", response_model=Dict)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get mindfulness statistics."""
    service = MindfulnessService(db)
    return await service.get_stats(current_user.id)
