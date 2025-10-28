"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from core.database import get_async_session
from core.security import get_current_user_id, UserRole
from domain.users.models import User

router = APIRouter()

@router.get("/me")
async def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Get current user profile"""
    user = await session.get(User, current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "role": user.role,
        "status": user.status,
        "created_at": user.created_at,
        "last_login": user.last_login
    }

@router.put("/me")
async def update_current_user(
    update_data: dict,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Update current user profile"""
    # TODO: Implement user profile update
    return {"message": "User update not implemented yet"}