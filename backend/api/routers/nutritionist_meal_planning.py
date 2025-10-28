"""
API para gestión de planes de comidas por nutriólogos
Incluye cálculo de perfiles nutricionales, asignación de recetas y seguimiento
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Dict, Optional
from datetime import date, datetime, timedelta

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role
from domain.patients.nutritional_profile import NutritionalProfile, ProfileStatus
from domain.patients.nutrition_calculator import (
    NutritionalCalculator, EquivalenceDistributor, NutritionalGoal, 
    create_nutritional_profile
)
from domain.meal_plans.weekly_planner import (
    WeeklyMealPlan, DailyMealPlan, MealAssignment, PlanStatus, WeekDay
)
from domain.recipes.models import Recipe, MealType
from domain.patients.models import Patient, AnthropometricRecord

router = APIRouter()

# ====== PERFILES NUTRICIONALES ======

@router.post("/patients/{patient_id}/nutritional-profile")
async def create_patient_nutritional_profile(
    patient_id: int,
    goal: NutritionalGoal,
    custom_adjustments: Optional[Dict] = None,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Crear perfil nutricional calculado para un paciente"""
    
    # Obtener paciente
    result = await session.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalars().first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Obtener último registro antropométrico
    anthro_result = await session.execute(
        select(AnthropometricRecord)
        .where(AnthropometricRecord.patient_id == patient_id)
        .order_by(AnthropometricRecord.measurement_date.desc())
    )
    latest_anthropometric = anthro_result.scalars().first()
    
    if not latest_anthropometric:
        raise HTTPException(
            status_code=400, 
            detail="Se requieren datos antropométricos para calcular el perfil"
        )
    
    # Crear perfil usando el calculador
    calculator = NutritionalCalculator(patient, latest_anthropometric)
    
    bmr = calculator.calculate_bmr()
    tdee = calculator.calculate_tdee(bmr)
    target_calories = calculator.calculate_target_calories(goal, tdee)
    macros = calculator.calculate_macronutrients(target_calories, goal)
    
    # Distribuir en equivalentes
    distributor = EquivalenceDistributor(target_calories, goal)
    equivalents = distributor.distribute_to_equivalents()
    
    # Aplicar ajustes personalizados
    if custom_adjustments:
        for group, adjustment in custom_adjustments.items():
            if group in equivalents:
                equivalents[group] = max(0, equivalents[group] + adjustment)
    
    # Crear registro en base de datos
    nutritional_profile = NutritionalProfile(
        patient_id=patient_id,
        nutritional_goal=goal,
        status=ProfileStatus.PENDING_APPROVAL,
        
        # Datos antropométricos
        calculation_weight_kg=latest_anthropometric.weight_kg,
        calculation_height_cm=latest_anthropometric.height_cm or 0,
        calculation_age=patient.current_age,
        calculation_bmi=latest_anthropometric.bmi,
        calculation_body_fat_pct=latest_anthropometric.body_fat_pct,
        
        # Cálculos metabólicos
        bmr_calculated=bmr,
        tdee_calculated=tdee,
        target_calories=target_calories,
        
        # Macronutrientes
        target_protein_g=macros["protein_g"],
        target_carbs_g=macros["carbs_g"],
        target_fat_g=macros["fat_g"],
        
        # Equivalentes
        equivalents_distribution=equivalents,
        
        # Auditoría
        created_by_id=current_user_id,
        custom_adjustments=custom_adjustments
    )
    
    session.add(nutritional_profile)
    await session.commit()
    await session.refresh(nutritional_profile)
    
    return {
        "profile_id": nutritional_profile.id,
        "calculations": {
            "bmr": bmr,
            "tdee": tdee,
            "target_calories": target_calories
        },
        "macronutrients": macros,
        "equivalents_distribution": equivalents,
        "status": nutritional_profile.status
    }

# Resto de endpoints... (por brevedad, continúo con la aplicación web)