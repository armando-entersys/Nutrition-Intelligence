from typing import List, Dict, Any, Optional
from datetime import time, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.auth import get_current_user
from domain.auth.models import AuthUser
from services.fasting_service import FastingService
from domain.fasting.models import FastingWindow, FastingLog, FastingStats
from pydantic import BaseModel

router = APIRouter()

class WindowConfig(BaseModel):
    start_time: str  # "HH:MM"
    end_time: str    # "HH:MM"

class LogMealRequest(BaseModel):
    meal_time: Optional[datetime] = None

@router.get("/window", response_model=Optional[FastingWindow])
async def get_window(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get current user's fasting window."""
    service = FastingService(db)
    return await service.get_window(current_user.id)

@router.post("/window", response_model=FastingWindow)
async def configure_window(
    config: WindowConfig,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Configure fasting window."""
    service = FastingService(db)
    
    try:
        start = datetime.strptime(config.start_time, "%H:%M").time()
        end = datetime.strptime(config.end_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")

    return await service.configure_window(current_user.id, start, end)

@router.get("/status", response_model=FastingStats)
async def get_status(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Get real-time fasting status."""
    service = FastingService(db)
    return await service.get_current_status(current_user.id)

@router.post("/log", response_model=FastingLog)
async def log_meal(
    request: LogMealRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Log a meal."""
    service = FastingService(db)
    return await service.log_meal(current_user.id, request.meal_time)

@router.post("/start", response_model=FastingLog)
async def start_fast(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Start fasting (log last meal time as now)."""
    service = FastingService(db)
    # When starting fast, we are finishing our last meal
    return await service.log_meal(current_user.id, datetime.now())

@router.post("/end", response_model=FastingLog)
async def end_fast(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """End fasting (log first meal time as now)."""
    service = FastingService(db)
    # When ending fast, we are starting our first meal
    # We need to ensure we are logging for the correct day/cycle
    return await service.log_meal(current_user.id, datetime.now())
