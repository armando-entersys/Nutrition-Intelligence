"""
Nutritionist endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from core.database import get_async_session
from core.security import get_current_user_id
from domain.nutritionists.models import Nutritionist

router = APIRouter()

@router.get("/")
async def get_nutritionists(
    session: Session = Depends(get_async_session)
):
    """Get list of verified nutritionists"""
    query = select(Nutritionist).where(Nutritionist.verification_status == "approved")
    result = await session.exec(query)
    return result.all()

@router.get("/me")
async def get_my_nutritionist_profile(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Get current nutritionist profile"""
    query = select(Nutritionist).where(Nutritionist.user_id == current_user_id)
    result = await session.exec(query)
    nutritionist = result.first()
    
    if not nutritionist:
        raise HTTPException(status_code=404, detail="Nutritionist profile not found")
    
    return nutritionist