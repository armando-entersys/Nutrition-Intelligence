"""
API endpoints para sistema de equivalencias dinámicas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Dict, Optional
from datetime import date, datetime

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role
from domain.foods.equivalences import (
    FoodEquivalence, EquivalenceGroup, EquivalenceGroupStandard,
    PatientEquivalenceGoal, DailyEquivalenceTracking, SMAE_GROUP_STANDARDS
)
from domain.foods.models import Food

router = APIRouter()

@router.get("/groups", response_model=List[Dict])
async def get_equivalence_groups(
    session: Session = Depends(get_async_session)
):
    """Obtener todos los grupos de equivalencias con sus estándares"""
    groups = []
    for group, standards in SMAE_GROUP_STANDARDS.items():
        groups.append({
            "group": group.value,
            "name": standards["name"],
            "description": standards["description"],
            "color": standards["color"],
            "standard_calories": standards["calories"],
            "standard_protein": standards["protein"],
            "standard_carbs": standards["carbs"],
            "standard_fat": standards["fat"],
            "min_daily": standards["min_daily"],
            "max_daily": standards["max_daily"]
        })
    return groups

@router.get("/foods/{food_id}/equivalences")
async def get_food_equivalences(
    food_id: int,
    session: Session = Depends(get_async_session)
):
    """Obtener equivalencias de un alimento específico"""
    result = await session.execute(
        select(FoodEquivalence)
        .where(FoodEquivalence.food_id == food_id)
        .where(FoodEquivalence.is_active == True)
    )
    equivalences = result.scalars().all()
    
    if not equivalences:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron equivalencias para este alimento"
        )
    
    return equivalences

@router.get("/groups/{group}/alternatives")
async def get_group_alternatives(
    group: EquivalenceGroup,
    session: Session = Depends(get_async_session),
    limit: int = Query(50, ge=1, le=100)
):
    """Obtener alimentos alternativos del mismo grupo de equivalencias"""
    result = await session.execute(
        select(FoodEquivalence, Food)
        .join(Food, FoodEquivalence.food_id == Food.id)
        .where(FoodEquivalence.equivalence_group == group)
        .where(FoodEquivalence.is_active == True)
        .where(Food.status == "approved")
        .limit(limit)
    )
    
    alternatives = []
    for equivalence, food in result:
        alternatives.append({
            "food_id": food.id,
            "food_name": food.name,
            "standard_portion": equivalence.standard_portion,
            "standard_unit": equivalence.standard_unit,
            "calories_per_equivalent": equivalence.calories_per_equivalent,
            "protein_per_equivalent": equivalence.protein_per_equivalent,
            "carbs_per_equivalent": equivalence.carbs_per_equivalent,
            "fat_per_equivalent": equivalence.fat_per_equivalent,
            "notes": equivalence.notes
        })
    
    return {
        "group": group.value,
        "group_info": SMAE_GROUP_STANDARDS[group],
        "alternatives": alternatives
    }

@router.post("/calculate-equivalents")
async def calculate_equivalents(
    food_portions: List[Dict],  # [{"food_id": 1, "quantity": 100, "unit": "g"}]
    session: Session = Depends(get_async_session)
):
    """Calcular equivalentes totales consumidos por grupo"""
    equivalents_by_group = {}
    total_nutrition = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0
    }
    
    for portion in food_portions:
        food_id = portion["food_id"]
        quantity = portion["quantity"]
        unit = portion["unit"]
        
        # Buscar equivalencia del alimento
        result = await session.execute(
            select(FoodEquivalence)
            .where(FoodEquivalence.food_id == food_id)
            .where(FoodEquivalence.is_active == True)
        )
        equivalence = result.scalars().first()
        
        if not equivalence:
            continue
        
        # Calcular cuántos equivalentes representa esta porción
        if equivalence.standard_unit == unit:
            equivalents_consumed = quantity / equivalence.standard_portion
        else:
            # Conversión de unidades (simplificada)
            equivalents_consumed = quantity / equivalence.standard_portion
        
        group = equivalence.equivalence_group.value
        if group not in equivalents_by_group:
            equivalents_by_group[group] = 0
        
        equivalents_by_group[group] += equivalents_consumed
        
        # Sumar nutrición total
        total_nutrition["calories"] += equivalents_consumed * equivalence.calories_per_equivalent
        total_nutrition["protein"] += equivalents_consumed * equivalence.protein_per_equivalent
        total_nutrition["carbs"] += equivalents_consumed * equivalence.carbs_per_equivalent
        total_nutrition["fat"] += equivalents_consumed * equivalence.fat_per_equivalent
    
    return {
        "equivalents_by_group": equivalents_by_group,
        "total_nutrition": total_nutrition,
        "timestamp": datetime.utcnow()
    }

@router.get("/patient/{patient_id}/goals")
async def get_patient_equivalence_goals(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Obtener metas de equivalentes de un paciente"""
    result = await session.execute(
        select(PatientEquivalenceGoal)
        .where(PatientEquivalenceGoal.patient_id == patient_id)
        .where(PatientEquivalenceGoal.is_active == True)
    )
    goals = result.scalars().all()
    
    # Formatear con información del grupo
    goals_with_info = []
    for goal in goals:
        group_info = SMAE_GROUP_STANDARDS[goal.equivalence_group]
        goals_with_info.append({
            "id": goal.id,
            "equivalence_group": goal.equivalence_group.value,
            "group_name": group_info["name"],
            "group_color": group_info["color"],
            "daily_target": goal.daily_target_equivalents,
            "min_equivalents": goal.min_equivalents,
            "max_equivalents": goal.max_equivalents,
            "standard_calories": group_info["calories"],
            "target_calories": goal.daily_target_equivalents * group_info["calories"],
            "notes": goal.notes
        })
    
    return goals_with_info

@router.post("/patient/{patient_id}/track-daily")
async def track_daily_equivalents(
    patient_id: int,
    equivalents_data: Dict[str, float],  # {"cereales": 6.5, "frutas": 2.0, ...}
    tracking_date: Optional[date] = None,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Registrar equivalentes consumidos en un día"""
    if tracking_date is None:
        tracking_date = date.today()
    
    # Verificar si ya existe registro para este día
    result = await session.execute(
        select(DailyEquivalenceTracking)
        .where(DailyEquivalenceTracking.patient_id == patient_id)
        .where(DailyEquivalenceTracking.tracking_date == tracking_date)
    )
    existing_tracking = result.scalars().first()
    
    # Obtener metas del paciente
    goals_result = await session.execute(
        select(PatientEquivalenceGoal)
        .where(PatientEquivalenceGoal.patient_id == patient_id)
        .where(PatientEquivalenceGoal.is_active == True)
    )
    goals = {goal.equivalence_group.value: goal.daily_target_equivalents 
             for goal in goals_result.scalars().all()}
    
    # Calcular progreso
    goals_met = 0
    total_goals = len(goals)
    total_calories = 0
    
    macros = {"protein": 0, "carbs": 0, "fat": 0}
    
    for group_key, consumed in equivalents_data.items():
        if group_key in goals:
            target = goals[group_key]
            if 0.8 <= consumed / target <= 1.2:  # ±20% tolerancia
                goals_met += 1
        
        # Calcular nutrición
        if group_key in [g.value for g in EquivalenceGroup]:
            group_enum = EquivalenceGroup(group_key)
            standards = SMAE_GROUP_STANDARDS[group_enum]
            total_calories += consumed * standards["calories"]
            macros["protein"] += consumed * standards["protein"]
            macros["carbs"] += consumed * standards["carbs"]
            macros["fat"] += consumed * standards["fat"]
    
    completion_percentage = (goals_met / total_goals * 100) if total_goals > 0 else 0
    
    if existing_tracking:
        # Actualizar registro existente
        existing_tracking.equivalences_consumed = equivalents_data
        existing_tracking.goals_met_count = goals_met
        existing_tracking.total_goals_count = total_goals
        existing_tracking.completion_percentage = completion_percentage
        existing_tracking.total_calories_from_equivalents = total_calories
        existing_tracking.macros_distribution = macros
        session.add(existing_tracking)
    else:
        # Crear nuevo registro
        new_tracking = DailyEquivalenceTracking(
            patient_id=patient_id,
            tracking_date=tracking_date,
            equivalences_consumed=equivalents_data,
            goals_met_count=goals_met,
            total_goals_count=total_goals,
            completion_percentage=completion_percentage,
            total_calories_from_equivalents=total_calories,
            macros_distribution=macros
        )
        session.add(new_tracking)
    
    await session.commit()
    
    return {
        "success": True,
        "goals_met": goals_met,
        "total_goals": total_goals,
        "completion_percentage": completion_percentage,
        "total_calories": total_calories,
        "macros_distribution": macros
    }

@router.get("/patient/{patient_id}/progress")
async def get_patient_progress(
    patient_id: int,
    days: int = Query(7, ge=1, le=30),
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """Obtener progreso de equivalentes de los últimos días"""
    from sqlalchemy import and_, func
    from datetime import timedelta
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    result = await session.execute(
        select(DailyEquivalenceTracking)
        .where(and_(
            DailyEquivalenceTracking.patient_id == patient_id,
            DailyEquivalenceTracking.tracking_date >= start_date,
            DailyEquivalenceTracking.tracking_date <= end_date
        ))
        .order_by(DailyEquivalenceTracking.tracking_date.desc())
    )
    
    daily_progress = result.scalars().all()
    
    # Calcular estadísticas
    if daily_progress:
        avg_completion = sum(p.completion_percentage for p in daily_progress) / len(daily_progress)
        best_day = max(daily_progress, key=lambda x: x.completion_percentage)
        total_days_tracked = len(daily_progress)
    else:
        avg_completion = 0
        best_day = None
        total_days_tracked = 0
    
    return {
        "daily_progress": [
            {
                "date": p.tracking_date,
                "completion_percentage": p.completion_percentage,
                "goals_met": p.goals_met_count,
                "total_goals": p.total_goals_count,
                "calories": p.total_calories_from_equivalents,
                "equivalences": p.equivalences_consumed
            }
            for p in daily_progress
        ],
        "summary": {
            "avg_completion_percentage": round(avg_completion, 1),
            "days_tracked": total_days_tracked,
            "best_day": {
                "date": best_day.tracking_date if best_day else None,
                "completion": best_day.completion_percentage if best_day else None
            }
        }
    }

@router.get("/meal-builder/suggestions")
async def get_meal_builder_suggestions(
    target_group: EquivalenceGroup,
    target_equivalents: float = Query(..., ge=0.1, le=10.0),
    exclude_foods: List[int] = Query(default=[]),
    session: Session = Depends(get_async_session)
):
    """Sugerencias para el constructor de comidas basado en equivalentes"""
    query = (
        select(FoodEquivalence, Food)
        .join(Food, FoodEquivalence.food_id == Food.id)
        .where(FoodEquivalence.equivalence_group == target_group)
        .where(FoodEquivalence.is_active == True)
        .where(Food.status == "approved")
    )
    
    if exclude_foods:
        query = query.where(Food.id.notin_(exclude_foods))
    
    result = await session.execute(query.limit(20))
    
    suggestions = []
    for equivalence, food in result:
        # Calcular porción necesaria para alcanzar los equivalentes objetivo
        portion_needed = target_equivalents * equivalence.standard_portion
        
        suggestions.append({
            "food_id": food.id,
            "food_name": food.name,
            "portion_needed": round(portion_needed, 2),
            "unit": equivalence.standard_unit,
            "calories": round(target_equivalents * equivalence.calories_per_equivalent, 1),
            "protein": round(target_equivalents * equivalence.protein_per_equivalent, 1),
            "carbs": round(target_equivalents * equivalence.carbs_per_equivalent, 1),
            "fat": round(target_equivalents * equivalence.fat_per_equivalent, 1)
        })
    
    return {
        "target_group": target_group.value,
        "target_equivalents": target_equivalents,
        "group_info": SMAE_GROUP_STANDARDS[target_group],
        "suggestions": suggestions
    }