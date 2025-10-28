"""
Simplified Authentication endpoints for testing
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

# Basic schemas
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str

@router.post("/login")
async def login(request: LoginRequest):
    """Simplified login endpoint"""
    # For testing purposes, accept any login
    return {
        "access_token": "mock-jwt-token",
        "token_type": "bearer",
        "user_id": 1,
        "email": request.email
    }

@router.get("/me")
async def get_current_user():
    """Get current user info"""
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "roles": ["patient", "nutritionist"]
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "auth"}