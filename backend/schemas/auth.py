"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from core.security import UserRole

class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class NutritionistRegister(UserRegister):
    """Nutritionist registration schema"""
    license_number: str = Field(min_length=5, max_length=50)
    university: str = Field(min_length=5, max_length=200)
    graduation_year: int = Field(ge=1950, le=2024)
    specializations: Optional[List[str]] = None
    verification_documents: Optional[List[str]] = None

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: UserRole

class VerificationRequest(BaseModel):
    """Email verification request"""
    token: str
    
class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr
    
class PasswordReset(BaseModel):
    """Password reset with token"""
    token: str
    new_password: str = Field(min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v