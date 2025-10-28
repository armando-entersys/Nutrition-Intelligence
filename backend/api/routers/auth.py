"""
Authentication endpoints - Updated for Hybrid Roles System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta, datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field

from core.database import get_async_session
from core.auth import (
    AuthService, create_access_token, create_refresh_token, verify_token,
    get_current_user, get_current_active_user, 
    get_admin_user, get_nutritionist_user, get_patient_user,
    get_nutritionist_or_admin, get_patient_or_nutritionist
)
from domain.auth.models import (
    AuthUser, UserRole, AccountStatus, UserRoleAssignment,
    ROLE_PERMISSIONS, get_user_permissions
)
from core.logging import log_success, log_error

router = APIRouter()

# Schemas de entrada
class RegisterRequest(BaseModel):
    """Esquema para registro de usuario"""
    email: EmailStr = Field(..., description="Email único del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido")
    phone: Optional[str] = Field(None, description="Teléfono opcional")
    primary_role: UserRole = Field(..., description="Rol principal del usuario")

class LoginRequest(BaseModel):
    """Esquema para login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")

class RoleAssignmentRequest(BaseModel):
    """Esquema para asignar roles adicionales"""
    user_id: int = Field(..., description="ID del usuario")
    role: UserRole = Field(..., description="Rol a asignar")
    reason: Optional[str] = Field(None, description="Motivo de la asignación")

# Schemas de salida
class UserResponse(BaseModel):
    """Información básica del usuario"""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    phone: Optional[str]
    primary_role: UserRole
    secondary_roles: List[UserRole]
    account_status: AccountStatus
    is_email_verified: bool
    profile_completed: bool
    last_login: Optional[datetime]
    created_at: datetime

class LoginResponse(BaseModel):
    """Respuesta de login exitoso"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    permissions: List[str]
    dashboard_url: str

class TokenResponse(BaseModel):
    """Token response compatible"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: UserRole

class RoleInfoResponse(BaseModel):
    """Información detallada de roles"""
    role: UserRole
    name: str
    description: str
    permissions: List[str]
    default_dashboard: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_patient(
    user_data: RegisterRequest,
    session: Session = Depends(get_async_session)
):
    """Register a new patient"""
    
    # Check if email already exists
    existing_user = await session.exec(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=UserRole.PATIENT
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    # Generate tokens
    token_data = {"sub": str(new_user.id), "role": new_user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=new_user.id,
        role=new_user.role
    )

@router.post("/register/nutritionist")
async def register_nutritionist(
    user_data: NutritionistRegister,
    session: Session = Depends(get_async_session)
):
    """Register a new nutritionist (requires verification)"""
    
    # Check if email already exists
    existing_user = await session.exec(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user with pending verification
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=UserRole.NUTRITIONIST,
        status="pending_verification"
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    # Create nutritionist profile
    from domain.nutritionists.models import Nutritionist
    nutritionist = Nutritionist(
        user_id=new_user.id,
        license_number=user_data.license_number,
        university=user_data.university,
        graduation_year=user_data.graduation_year,
        specializations=user_data.specializations or [],
        verification_documents=user_data.verification_documents or []
    )
    
    session.add(nutritionist)
    await session.commit()
    
    # TODO: Send verification email
    # TODO: Schedule document review workflow
    
    return {
        "message": "Registration submitted successfully",
        "user_id": new_user.id,
        "status": "pending_verification",
        "next_steps": [
            "Check your email for verification instructions",
            "Upload required documents",
            "Wait for manual verification by our team"
        ]
    }

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_async_session)
):
    """User login"""
    
    # Find user by email
    user = await session.exec(
        select(User).where(User.email == form_data.username)
    )
    user = user.first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.status}. Please contact support."
        )
    
    # Generate tokens
    token_data = {"sub": str(user.id), "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    await session.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    session: Session = Depends(get_async_session)
):
    """Refresh access token"""
    
    # Verify refresh token
    payload = verify_token(refresh_token, TokenType.REFRESH)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user = await session.get(User, int(user_id))
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new tokens
    token_data = {"sub": str(user.id), "role": user.role}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role
    )

@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}

@router.post("/verify-email")
async def verify_email(
    verification_data: VerificationRequest,
    session: Session = Depends(get_async_session)
):
    """Verify user email"""
    # TODO: Implement email verification logic
    return {"message": "Email verification not implemented yet"}

@router.post("/forgot-password")
async def forgot_password(email: str):
    """Request password reset"""
    # TODO: Implement password reset logic
    return {"message": "Password reset not implemented yet"}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    """Reset password with token"""
    # TODO: Implement password reset logic
    return {"message": "Password reset not implemented yet"}