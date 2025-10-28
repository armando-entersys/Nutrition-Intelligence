"""
Patient endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from core.database import get_async_session
from core.security import get_current_user_id
from domain.patients.models import Patient

router = APIRouter()

@router.get("/me")
async def get_my_patient_profile(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Get current patient profile"""
    query = select(Patient).where(Patient.user_id == current_user_id)
    result = await session.exec(query)
    patient = result.first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    return patient

@router.post("/me")
async def create_patient_profile(
    profile_data: dict,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Create patient profile"""
    # TODO: Implement patient profile creation
    return {"message": "Patient profile creation not implemented yet"}