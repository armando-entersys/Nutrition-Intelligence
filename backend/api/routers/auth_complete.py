"""
Complete Authentication Endpoints
Login, Register, Password Recovery
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re

from core.database import get_session
from core.auth import create_access_token, create_refresh_token
from domain.auth.models import AuthUser, UserRole, AccountStatus
from domain.auth.password_reset import PasswordResetToken, TokenStatus
from core.logging import log_success, log_error

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ============================================================================
# SCHEMAS
# ============================================================================

class RegisterRequest(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    role: UserRole = Field(default=UserRole.PATIENT)

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate passwords match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, hyphens and underscores')
        return v

class LoginRequest(BaseModel):
    """Schema for login"""
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password"""
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    """Schema for reset password"""
    token: str = Field(..., min_length=32)
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate passwords match"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(BaseModel):
    """User information response"""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone: Optional[str]
    primary_role: UserRole
    account_status: AccountStatus
    is_email_verified: bool
    profile_completed: bool
    created_at: datetime

class LoginResponse(BaseModel):
    """Login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: UserResponse

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user

    - Creates a new user account
    - Validates email and username uniqueness
    - Enforces password strength requirements
    - Automatically activates patient accounts
    - Nutritionist accounts require verification
    """
    # Check if email already exists
    existing_email = session.exec(
        select(AuthUser).where(AuthUser.email == request.email)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = session.exec(
        select(AuthUser).where(AuthUser.username == request.username)
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create new user
    new_user = AuthUser(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        primary_role=request.role,
        account_status=AccountStatus.ACTIVE if request.role == UserRole.PATIENT else AccountStatus.PENDING_VERIFICATION,
        is_email_verified=False,
        profile_completed=False
    )

    # Set password
    new_user.set_password(request.password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    log_success(f"New user registered: {new_user.email} ({new_user.primary_role})")

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone=new_user.phone,
        primary_role=new_user.primary_role,
        account_status=new_user.account_status,
        is_email_verified=new_user.is_email_verified,
        profile_completed=new_user.profile_completed,
        created_at=new_user.created_at
    )

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    session: Session = Depends(get_session)
):
    """
    User login

    - Authenticates user with email and password
    - Returns access and refresh tokens
    - Updates last login timestamp
    - Tracks failed login attempts
    """
    # Find user by email
    user = session.exec(
        select(AuthUser).where(AuthUser.email == request.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not user.verify_password(request.password):
        # Track failed login attempt
        user.failed_login_attempts += 1
        user.last_failed_login = datetime.utcnow()
        session.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check account status
    if user.account_status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.account_status.value}. Please contact support."
        )

    # Generate tokens
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.primary_role.value
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Update login stats
    user.last_login = datetime.utcnow()
    user.login_count += 1
    user.failed_login_attempts = 0
    session.commit()
    session.refresh(user)

    log_success(f"User logged in: {user.email}")

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            primary_role=user.primary_role,
            account_status=user.account_status,
            is_email_verified=user.is_email_verified,
            profile_completed=user.profile_completed,
            created_at=user.created_at
        )
    )

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    http_request: Request,
    session: Session = Depends(get_session)
):
    """
    Request password reset

    - Generates a password reset token
    - Token expires in 1 hour
    - Sends reset email (if email service configured)
    - Always returns success to prevent email enumeration
    """
    # Find user by email
    user = session.exec(
        select(AuthUser).where(AuthUser.email == request.email)
    ).first()

    # Always return success to prevent email enumeration
    response_message = {
        "message": "If your email is registered, you will receive a password reset link shortly",
        "email": request.email
    }

    if not user:
        # Don't reveal that email doesn't exist
        return response_message

    # Revoke any existing active tokens for this user
    existing_tokens = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.status == TokenStatus.ACTIVE
        )
    ).all()

    for token in existing_tokens:
        token.revoke()

    # Create new reset token
    reset_token = PasswordResetToken.create_for_user(
        user_id=user.id,
        email=user.email,
        ip_address=http_request.client.host if http_request.client else None,
        user_agent=http_request.headers.get("user-agent")
    )

    session.add(reset_token)
    session.commit()

    # TODO: Send email with reset link
    # For now, return the token in the response (for development only)
    # In production, this should be sent via email
    log_success(f"Password reset requested for: {user.email}")

    return {
        **response_message,
        "reset_token": reset_token.token,  # Remove this in production
        "reset_url": f"/reset-password?token={reset_token.token}",  # Remove this in production
        "expires_at": reset_token.expires_at.isoformat()
    }

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    """
    Reset password with token

    - Validates reset token
    - Ensures token is not expired or used
    - Updates user password
    - Marks token as used
    """
    # Find token
    token_record = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token == request.token
        )
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Validate token
    if not token_record.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token is {token_record.status.value}"
        )

    # Get user
    user = session.get(AuthUser, token_record.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update password
    user.set_password(request.new_password)
    token_record.mark_as_used()

    session.commit()

    log_success(f"Password reset successful for: {user.email}")

    return {
        "message": "Password reset successfully",
        "email": user.email
    }

@router.post("/logout")
async def logout():
    """
    Logout user

    - Client should discard tokens
    - In production, implement token blacklist for enhanced security
    """
    return {"message": "Successfully logged out"}
