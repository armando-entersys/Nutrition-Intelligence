"""
Patient endpoints - Expediente Clínico Digital CRUD
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, datetime

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role, UserRole
from domain.patients.models import (
    Patient,
    AnthropometricRecord,
    MedicalHistory,
    Gender,
    ActivityLevel
)
from domain.auth.models import AuthUser
from pydantic import BaseModel, Field

router = APIRouter()

# ============================================================================
# SCHEMAS / DTOs
# ============================================================================

class PatientCreate(BaseModel):
    """Create patient profile"""
    date_of_birth: date
    gender: Gender
    primary_goal: str = Field(max_length=500)
    target_weight_kg: Optional[float] = None
    target_body_fat_pct: Optional[float] = None
    activity_level: ActivityLevel = ActivityLevel.SEDENTARY
    occupation: Optional[str] = None
    share_feed: bool = False
    allow_data_research: bool = False


class PatientUpdate(BaseModel):
    """Update patient profile"""
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    primary_goal: Optional[str] = None
    target_weight_kg: Optional[float] = None
    target_body_fat_pct: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    occupation: Optional[str] = None
    share_feed: Optional[bool] = None
    allow_data_research: Optional[bool] = None
    active_nutritionist_id: Optional[int] = None


class AnthropometricRecordCreate(BaseModel):
    """Create anthropometric record"""
    weight_kg: float
    height_cm: Optional[float] = None
    body_fat_pct: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    bone_mass_kg: Optional[float] = None
    water_pct: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    chest_cm: Optional[float] = None
    arm_cm: Optional[float] = None
    thigh_cm: Optional[float] = None
    triceps_mm: Optional[float] = None
    biceps_mm: Optional[float] = None
    subscapular_mm: Optional[float] = None
    suprailiac_mm: Optional[float] = None
    measurement_date: Optional[date] = None
    notes: Optional[str] = None


class AnthropometricRecordUpdate(BaseModel):
    """Update anthropometric record"""
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    body_fat_pct: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    bone_mass_kg: Optional[float] = None
    water_pct: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    chest_cm: Optional[float] = None
    arm_cm: Optional[float] = None
    thigh_cm: Optional[float] = None
    triceps_mm: Optional[float] = None
    biceps_mm: Optional[float] = None
    subscapular_mm: Optional[float] = None
    suprailiac_mm: Optional[float] = None
    measurement_date: Optional[date] = None
    notes: Optional[str] = None


class MedicalHistoryCreate(BaseModel):
    """Create or update medical history"""
    conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    intolerances: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    family_history: Optional[dict] = None
    lab_results: Optional[dict] = None
    lab_date: Optional[date] = None
    eating_preferences: Optional[List[str]] = None
    food_aversions: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    smoking: bool = False
    alcohol_consumption: str = "none"
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None


class MedicalHistoryUpdate(BaseModel):
    """Update medical history"""
    conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    intolerances: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    family_history: Optional[dict] = None
    lab_results: Optional[dict] = None
    lab_date: Optional[date] = None
    eating_preferences: Optional[List[str]] = None
    food_aversions: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    smoking: Optional[bool] = None
    alcohol_consumption: Optional[str] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None


# ============================================================================
# PATIENT ENDPOINTS - Datos Generales
# ============================================================================

@router.get("/me", response_model=Patient)
async def get_my_patient_profile(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current patient profile"""
    query = select(Patient).where(Patient.user_id == current_user_id)
    result = await session.exec(query)
    patient = result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    return patient


@router.post("/me", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient_profile(
    profile_data: PatientCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Create patient profile"""
    # Check if profile already exists
    query = select(Patient).where(Patient.user_id == current_user_id)
    result = await session.exec(query)
    existing = result.first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient profile already exists"
        )

    # Create new patient
    patient = Patient(
        user_id=current_user_id,
        **profile_data.model_dump()
    )

    session.add(patient)
    await session.commit()
    await session.refresh(patient)

    return patient


@router.put("/me", response_model=Patient)
async def update_patient_profile(
    profile_data: PatientUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update patient profile"""
    query = select(Patient).where(Patient.user_id == current_user_id)
    result = await session.exec(query)
    patient = result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    patient.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(patient)

    return patient


@router.get("/{patient_id}", response_model=Patient)
async def get_patient_by_id(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get patient by ID

    Authorization:
    - Admins: Can access any patient
    - Nutritionists: Can only access their assigned patients
    - Patients: Can only access their own profile
    """
    # Get patient
    query = select(Patient).where(Patient.id == patient_id)
    result = await session.exec(query)
    patient = result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Authorization checks
    if current_user_role == UserRole.ADMIN:
        # Admins can access any patient
        return patient
    elif current_user_role == UserRole.NUTRITIONIST:
        # Nutritionists can only access their assigned patients
        # Get the auth_user record to find assigned nutritionist
        user_query = select(AuthUser).where(AuthUser.id == patient.user_id)
        user_result = await session.exec(user_query)
        patient_user = user_result.first()

        if not patient_user or patient_user.nutritionist_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this patient's data"
            )
        return patient
    elif current_user_role == UserRole.PATIENT:
        # Patients can only access their own profile
        if patient.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own patient profile"
            )
        return patient
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )


# ============================================================================
# ANTHROPOMETRIC RECORDS - Mediciones Antropométricas
# ============================================================================

@router.get("/me/anthropometrics", response_model=List[AnthropometricRecord])
async def get_my_anthropometric_records(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Get anthropometric records for current patient"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get records
    query = (
        select(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient.id)
        .order_by(AnthropometricRecord.measurement_date.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.exec(query)
    records = result.all()

    return records


@router.post("/me/anthropometrics", response_model=AnthropometricRecord, status_code=status.HTTP_201_CREATED)
async def create_anthropometric_record(
    record_data: AnthropometricRecordCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Create new anthropometric record"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Calculate BMI if height and weight are provided
    bmi = None
    if record_data.height_cm and record_data.weight_kg:
        height_m = record_data.height_cm / 100
        bmi = record_data.weight_kg / (height_m ** 2)

    # Calculate waist-hip ratio if both are provided
    waist_hip_ratio = None
    if record_data.waist_cm and record_data.hip_cm:
        waist_hip_ratio = record_data.waist_cm / record_data.hip_cm

    # Create record
    record = AnthropometricRecord(
        patient_id=patient.id,
        measured_by_id=current_user_id,
        bmi=bmi,
        waist_hip_ratio=waist_hip_ratio,
        measurement_date=record_data.measurement_date or date.today(),
        **record_data.model_dump(exclude={'measurement_date'})
    )

    session.add(record)
    await session.commit()
    await session.refresh(record)

    return record


@router.get("/me/anthropometrics/{record_id}", response_model=AnthropometricRecord)
async def get_anthropometric_record(
    record_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get specific anthropometric record"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get record
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.id == record_id,
        AnthropometricRecord.patient_id == patient.id
    )
    result = await session.exec(query)
    record = result.first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    return record


@router.put("/me/anthropometrics/{record_id}", response_model=AnthropometricRecord)
async def update_anthropometric_record(
    record_id: int,
    record_data: AnthropometricRecordUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update anthropometric record"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get record
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.id == record_id,
        AnthropometricRecord.patient_id == patient.id
    )
    result = await session.exec(query)
    record = result.first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    # Update fields
    update_data = record_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    # Recalculate BMI if needed
    if record.height_cm and record.weight_kg:
        height_m = record.height_cm / 100
        record.bmi = record.weight_kg / (height_m ** 2)

    # Recalculate waist-hip ratio if needed
    if record.waist_cm and record.hip_cm:
        record.waist_hip_ratio = record.waist_cm / record.hip_cm

    await session.commit()
    await session.refresh(record)

    return record


@router.delete("/me/anthropometrics/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_anthropometric_record(
    record_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete anthropometric record"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get record
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.id == record_id,
        AnthropometricRecord.patient_id == patient.id
    )
    result = await session.exec(query)
    record = result.first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    await session.delete(record)
    await session.commit()

    return None


# ============================================================================
# MEDICAL HISTORY - Historia Clínica
# ============================================================================

@router.get("/me/medical-history", response_model=MedicalHistory)
async def get_my_medical_history(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get medical history for current patient"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get medical history
    query = select(MedicalHistory).where(MedicalHistory.patient_id == patient.id)
    result = await session.exec(query)
    history = result.first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found"
        )

    return history


@router.post("/me/medical-history", response_model=MedicalHistory, status_code=status.HTTP_201_CREATED)
async def create_medical_history(
    history_data: MedicalHistoryCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Create medical history for current patient"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Check if history already exists
    existing_query = select(MedicalHistory).where(MedicalHistory.patient_id == patient.id)
    existing_result = await session.exec(existing_query)
    existing = existing_result.first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical history already exists. Use PUT to update."
        )

    # Create history
    history = MedicalHistory(
        patient_id=patient.id,
        **history_data.model_dump()
    )

    session.add(history)
    await session.commit()
    await session.refresh(history)

    return history


@router.put("/me/medical-history", response_model=MedicalHistory)
async def update_medical_history(
    history_data: MedicalHistoryUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update medical history for current patient"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get medical history
    query = select(MedicalHistory).where(MedicalHistory.patient_id == patient.id)
    result = await session.exec(query)
    history = result.first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found. Use POST to create."
        )

    # Update fields
    update_data = history_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(history, field, value)

    history.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(history)

    return history


@router.delete("/me/medical-history", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_history(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete medical history for current patient"""
    # Get patient
    patient_query = select(Patient).where(Patient.user_id == current_user_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    # Get medical history
    query = select(MedicalHistory).where(MedicalHistory.patient_id == patient.id)
    result = await session.exec(query)
    history = result.first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found"
        )

    await session.delete(history)
    await session.commit()

    return None


# ============================================================================
# NUTRITIONIST ENDPOINTS - For accessing patient data
# ============================================================================

@router.get("/{patient_id}/anthropometrics", response_model=List[AnthropometricRecord])
async def get_patient_anthropometric_records(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Get anthropometric records for a patient

    Authorization:
    - Admins: Can access any patient's records
    - Nutritionists: Can only access their assigned patients' records
    - Patients: Can only access their own records
    """
    # Get patient to verify ownership
    patient_query = select(Patient).where(Patient.id == patient_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Authorization checks
    if current_user_role == UserRole.ADMIN:
        # Admins can access any patient's data
        pass
    elif current_user_role == UserRole.NUTRITIONIST:
        # Nutritionists can only access their assigned patients
        user_query = select(AuthUser).where(AuthUser.id == patient.user_id)
        user_result = await session.exec(user_query)
        patient_user = user_result.first()

        if not patient_user or patient_user.nutritionist_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this patient's data"
            )
    elif current_user_role == UserRole.PATIENT:
        # Patients can only access their own records
        if patient.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own anthropometric records"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    # Get records
    query = (
        select(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient_id)
        .order_by(AnthropometricRecord.measurement_date.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.exec(query)
    records = result.all()

    return records


@router.get("/{patient_id}/medical-history", response_model=MedicalHistory)
async def get_patient_medical_history(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get medical history for a patient

    Authorization:
    - Admins: Can access any patient's medical history
    - Nutritionists: Can only access their assigned patients' medical history
    - Patients: Can only access their own medical history
    """
    # Get patient to verify ownership
    patient_query = select(Patient).where(Patient.id == patient_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Authorization checks
    if current_user_role == UserRole.ADMIN:
        # Admins can access any patient's data
        pass
    elif current_user_role == UserRole.NUTRITIONIST:
        # Nutritionists can only access their assigned patients
        user_query = select(AuthUser).where(AuthUser.id == patient.user_id)
        user_result = await session.exec(user_query)
        patient_user = user_result.first()

        if not patient_user or patient_user.nutritionist_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this patient's data"
            )
    elif current_user_role == UserRole.PATIENT:
        # Patients can only access their own medical history
        if patient.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own medical history"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    # Get medical history
    query = select(MedicalHistory).where(MedicalHistory.patient_id == patient_id)
    result = await session.exec(query)
    history = result.first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found"
        )

    return history


# ============================================================================
# COMPLETE PATIENT RECORD - Expediente Completo con Progreso
# ============================================================================

class PatientCompleteRecordResponse(BaseModel):
    """Complete patient record with progress data - Digital Clinical Record"""
    patient: Patient
    user_info: Dict[str, Any] = {}
    latest_record: Optional[AnthropometricRecord] = None
    records_count: int = 0
    medical_history: Optional[MedicalHistory] = None
    progress_summary: Dict[str, Any] = {}
    active_meal_plans_count: int = 0

    class Config:
        arbitrary_types_allowed = True


@router.get("/{patient_id}/complete-record", response_model=PatientCompleteRecordResponse)
async def get_complete_patient_record(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get complete patient record including profile, latest measurements,
    medical history, and progress summary.

    This is a comprehensive endpoint for the "Digital Clinical Record" view.

    Authorization:
    - Admins: Can access any patient's complete record
    - Nutritionists: Can only access their assigned patients' complete records
    - Patients: Can only access their own complete record
    """
    # Get patient
    patient_query = select(Patient).where(Patient.id == patient_id)
    patient_result = await session.exec(patient_query)
    patient = patient_result.first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Authorization checks
    if current_user_role == UserRole.PATIENT:
        # Patients can only access their own record
        if patient.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Patients can only access their own record"
            )
    elif current_user_role == UserRole.NUTRITIONIST:
        # Nutritionists can only access their assigned patients
        # Get user to check nutritionist_id
        user_query = select(AuthUser).where(AuthUser.id == patient.user_id)
        user_result = await session.exec(user_query)
        user = user_result.first()

        if not user or user.nutritionist_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nutritionists can only access their assigned patients"
            )
    # Admins have full access - no additional checks needed

    # Get user information
    user_query = select(AuthUser).where(AuthUser.id == patient.user_id)
    user_result = await session.exec(user_query)
    user = user_result.first()

    user_info = {}
    if user:
        user_info = {
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role.value if user.role else None
        }

    # Get latest anthropometric record
    latest_record_query = (
        select(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient_id)
        .order_by(AnthropometricRecord.measurement_date.desc())
        .limit(1)
    )
    latest_record_result = await session.exec(latest_record_query)
    latest_record = latest_record_result.first()

    # Count total anthropometric records
    records_count_query = (
        select(func.count())
        .select_from(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient_id)
    )
    records_count_result = await session.exec(records_count_query)
    records_count = records_count_result.one()

    # Get medical history
    history_query = select(MedicalHistory).where(MedicalHistory.patient_id == patient_id)
    history_result = await session.exec(history_query)
    medical_history = history_result.first()

    # Calculate progress summary (last 30 days)
    from datetime import datetime, timedelta

    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    progress_records_query = (
        select(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient_id)
        .where(AnthropometricRecord.measurement_date >= thirty_days_ago)
        .order_by(AnthropometricRecord.measurement_date.asc())
    )
    progress_records_result = await session.exec(progress_records_query)
    progress_records = progress_records_result.all()

    progress_summary = {
        "period_days": 30,
        "records_count": len(progress_records),
        "has_progress": len(progress_records) >= 2
    }

    if len(progress_records) >= 2:
        first_record = progress_records[0]
        last_record = progress_records[-1]

        # Weight change
        if first_record.weight_kg and last_record.weight_kg:
            weight_change = last_record.weight_kg - first_record.weight_kg
            weight_change_pct = (weight_change / first_record.weight_kg) * 100

            progress_summary.update({
                "initial_weight": first_record.weight_kg,
                "current_weight": last_record.weight_kg,
                "weight_change": weight_change,
                "weight_change_percentage": round(weight_change_pct, 2),
                "weight_trend": "stable" if abs(weight_change) < 0.5 else ("decreasing" if weight_change < 0 else "increasing")
            })

        # BMI change
        if first_record.bmi and last_record.bmi:
            bmi_change = last_record.bmi - first_record.bmi

            progress_summary.update({
                "initial_bmi": first_record.bmi,
                "current_bmi": last_record.bmi,
                "bmi_change": round(bmi_change, 2),
                "bmi_trend": "stable" if abs(bmi_change) < 0.5 else ("decreasing" if bmi_change < 0 else "increasing")
            })

    # Count active meal plans
    from domain.recipes.models import MealPlan

    active_meal_plans_query = (
        select(func.count())
        .select_from(MealPlan)
        .where(MealPlan.patient_id == patient_id)
        .where(MealPlan.is_active == True)
    )
    active_meal_plans_result = await session.exec(active_meal_plans_query)
    active_meal_plans_count = active_meal_plans_result.one()

    return PatientCompleteRecordResponse(
        patient=patient,
        user_info=user_info,
        latest_record=latest_record,
        records_count=records_count,
        medical_history=medical_history,
        progress_summary=progress_summary,
        active_meal_plans_count=active_meal_plans_count
    )
