"""
Admin Endpoints - Temporary endpoints for administration
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from core.database import get_session
from domain.auth.models import AuthUser, UserRole, AccountStatus

router = APIRouter(prefix="/admin", tags=["Admin"])

class UserListResponse:
    """User list response model"""
    def __init__(self, user: AuthUser):
        self.id = user.id
        self.email = user.email
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.full_name = f"{user.first_name} {user.last_name}"
        self.primary_role = user.primary_role
        self.account_status = user.account_status
        self.nutritionist_id = user.nutritionist_id
        self.created_at = user.created_at

@router.get("/users")
def list_all_users(
    session: Session = Depends(get_session)
):
    """
    List all registered users

    Returns user information including role and nutritionist assignments
    """
    users = session.exec(
        select(AuthUser).order_by(AuthUser.created_at.desc())
    ).all()

    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "nombre_completo": f"{user.first_name} {user.last_name}",
            "rol": user.primary_role.value,
            "estado": user.account_status.value,
            "email_verificado": user.is_email_verified,
            "nutritionist_id": user.nutritionist_id,
            "creado": user.created_at.isoformat() if user.created_at else None
        }

        # If has nutritionist, add name
        if user.nutritionist_id:
            nutritionist = session.get(AuthUser, user.nutritionist_id)
            if nutritionist:
                user_data["nutriologo"] = f"{nutritionist.first_name} {nutritionist.last_name}"

        user_list.append(user_data)

    return {
        "total": len(user_list),
        "users": user_list
    }
