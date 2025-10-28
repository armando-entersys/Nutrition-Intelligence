"""
Meal plan endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import date
from core.database import get_async_session
from core.security import get_current_user_id
from domain.recipes.models import MealPlan

router = APIRouter()

@router.get("/{patient_id}/today")
async def get_today_meal_plan(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Get today's meal plan for patient"""
    today = date.today()
    
    query = select(MealPlan).where(
        MealPlan.patient_id == patient_id,
        MealPlan.start_date <= today,
        (MealPlan.end_date >= today) | (MealPlan.end_date.is_(None)),
        MealPlan.is_active == True
    )
    
    result = await session.exec(query)
    meal_plan = result.first()
    
    if not meal_plan:
        return {"message": "No active meal plan found for today"}
    
    return meal_plan

@router.post("/{patient_id}")
async def create_meal_plan(
    patient_id: int,
    meal_plan_data: dict,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Create meal plan for patient"""
    # TODO: Implement meal plan creation
    return {"message": "Meal plan creation not implemented yet"}