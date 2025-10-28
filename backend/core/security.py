"""
Security utilities for authentication and authorization
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from enum import Enum
import logging

from core.config import get_settings

logger = logging.getLogger(__name__)

# Password hasher
ph = PasswordHasher()

# Security scheme
security = HTTPBearer()

class UserRole(str, Enum):
    ADMIN = "admin"
    NUTRITIONIST = "nutritionist" 
    PATIENT = "patient"

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

def hash_password(password: str) -> str:
    """Hash password using Argon2"""
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create access token"""
    settings = get_settings()
    
    to_encode = data.copy()
    to_encode["type"] = TokenType.ACCESS
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create refresh token"""
    settings = get_settings()
    
    to_encode = data.copy()
    to_encode["type"] = TokenType.REFRESH
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

def verify_token(token: str, token_type: TokenType = TokenType.ACCESS) -> Dict[str, Any]:
    """Verify and decode token"""
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Extract current user ID from token"""
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return int(user_id)

async def get_current_user_role(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserRole:
    """Extract current user role from token"""
    payload = verify_token(credentials.credentials)
    role = payload.get("role")
    
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return UserRole(role)

def require_roles(*required_roles: UserRole):
    """Decorator to require specific roles"""
    async def role_checker(
        current_role: UserRole = Depends(get_current_user_role)
    ):
        if current_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_role
    
    return role_checker

# Role-specific dependencies
require_admin = require_roles(UserRole.ADMIN)
require_nutritionist = require_roles(UserRole.NUTRITIONIST, UserRole.ADMIN)
require_patient = require_roles(UserRole.PATIENT, UserRole.NUTRITIONIST, UserRole.ADMIN)