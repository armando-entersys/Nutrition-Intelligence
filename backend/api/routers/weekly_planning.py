"""
API Router para Planificación Semanal
Endpoints para que nutricionistas creen y gestionen planes semanales
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from datetime import datetime, date, timedelta

from core.database import get_async_session
from core.auth import get_nutritionist_or_admin, get_patient_or_nutritionist, get_current_active_user
from domain.meal_plans.weekly_planner import (
    WeeklyMealPlan, DailyMealPlan, MealAssignment, PlanFeedback, PlanTemplate,
    WeekDay, PlanStatus, MEAL_TIME_INFO, WEEKDAY_INFO
)
from domain.recipes.models import MealType
from domain.auth.models import AuthUser
from domain.nutritionists.kilocalorie_calculator import KilocalorieCalculator, PatientProfile
from core.logging import log_success, log_error

router = APIRouter()

# Schemas de entrada
class CreateWeeklyPlanRequest(BaseModel):
    """Esquema para crear plan semanal"""
    patient_id: int = Field(..., description="ID del paciente")
    plan_name: str = Field(..., min_length=1, max_length=200, description="Nombre del plan")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción del plan")
    start_date: date = Field(..., description="Fecha de inicio (debe ser lunes)")
    duration_weeks: int = Field(default=1, ge=1, le=12, description="Duración en semanas")
    
    # Configuración nutricional
    target_calories_per_day: float = Field(..., gt=0, description="Calorías objetivo por día")
    target_equivalents: Dict[str, float] = Field(..., description="Distribución de equivalentes SMAE")
    
    # Configuración de flexibilidad
    allow_substitutions: bool = Field(default=True, description="Permitir sustituciones")
    substitution_notes: Optional[str] = Field(None, max_length=500)
    
    # Instrucciones
    patient_instructions: Optional[str] = Field(None, max_length=1000)

class MealAssignmentRequest(BaseModel):
    """Esquema para asignar comida"""
    recipe_id: int = Field(..., description="ID de la receta")
    meal_time: MealType = Field(..., description="Tiempo de comida")
    servings: float = Field(default=1.0, gt=0, description="Número de porciones")
    planned_time: Optional[str] = Field(None, description="Hora planeada (HH:MM)")
    preparation_notes: Optional[str] = Field(None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5, description="Prioridad (1=alta, 5=baja)")

class PlanFeedbackRequest(BaseModel):
    """Esquema para feedback del plan"""
    overall_satisfaction: int = Field(..., ge=1, le=5)
    recipe_variety: int = Field(..., ge=1, le=5)
    portion_adequacy: int = Field(..., ge=1, le=5)
    preparation_difficulty: int = Field(..., ge=1, le=5)
    taste_satisfaction: int = Field(..., ge=1, le=5)
    
    liked_most: Optional[str] = Field(None, max_length=500)
    disliked_most: Optional[str] = Field(None, max_length=500)
    suggested_changes: Optional[str] = Field(None, max_length=1000)
    
    days_followed_completely: int = Field(..., ge=0, le=7)
    missed_meals_count: int = Field(default=0, ge=0)

# Schemas de salida
class WeeklyPlanResponse(BaseModel):
    """Respuesta de plan semanal"""
    id: int
    patient_id: int
    nutritionist_id: int
    plan_name: str
    description: Optional[str]
    week_start_date: date
    week_end_date: date
    status: PlanStatus
    target_calories_per_day: float
    target_equivalents: Dict[str, float]
    completion_percentage: float
    adherence_score: Optional[float]
    created_at: datetime
    published_at: Optional[datetime]

class DailyPlanResponse(BaseModel):
    """Respuesta de plan diario"""
    id: int
    plan_date: date
    week_day: WeekDay
    daily_calorie_target: float
    daily_equivalents_target: Dict[str, float]
    planned_calories: float
    planned_equivalents: Dict[str, float]
    is_completed: bool
    adherence_percentage: float
    meal_assignments: List[Dict[str, Any]]

class MealAssignmentResponse(BaseModel):
    """Respuesta de asignación de comida"""
    id: int
    meal_type: MealType
    meal_time_display: str
    recipe_id: int
    recipe_name: str
    servings: float
    calculated_calories: float
    calculated_equivalents: Dict[str, float]
    planned_time: Optional[str]
    is_consumed: bool
    patient_rating: Optional[int]

# Endpoints principales

@router.post("/create-weekly-plan", response_model=WeeklyPlanResponse)
async def create_weekly_plan(
    request: CreateWeeklyPlanRequest,
    current_user: AuthUser = Depends(get_nutritionist_or_admin),
    session: Session = Depends(get_async_session)
):
    """
    Crea un nuevo plan semanal para un paciente
    """
    try:
        # Validar que la fecha de inicio sea lunes
        if request.start_date.weekday() != 0:  # 0 = lunes
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be a Monday"
            )
        
        # Calcular fecha de fin
        end_date = request.start_date + timedelta(days=(request.duration_weeks * 7) - 1)
        
        # Crear plan semanal
        weekly_plan = WeeklyMealPlan(
            patient_id=request.patient_id,
            nutritionist_id=current_user.id,
            plan_name=request.plan_name,
            description=request.description,
            week_start_date=request.start_date,
            week_end_date=end_date,
            target_calories_per_day=request.target_calories_per_day,
            target_equivalents=request.target_equivalents,
            allow_substitutions=request.allow_substitutions,
            substitution_notes=request.substitution_notes,
            patient_instructions=request.patient_instructions,
            status=PlanStatus.DRAFT
        )
        
        session.add(weekly_plan)
        await session.commit()
        await session.refresh(weekly_plan)
        
        # Crear planes diarios automáticamente
        current_date = request.start_date
        weekday_names = list(WeekDay)
        
        for week in range(request.duration_weeks):
            for day_num in range(7):
                day_date = current_date + timedelta(days=(week * 7) + day_num)
                weekday = weekday_names[day_num]
                
                daily_plan = DailyMealPlan(
                    weekly_plan_id=weekly_plan.id,
                    plan_date=day_date,
                    week_day=weekday,
                    daily_calorie_target=request.target_calories_per_day,
                    daily_equivalents_target=request.target_equivalents,
                    daily_notes=None
                )
                
                session.add(daily_plan)
        
        await session.commit()
        
        log_success(
            f"Plan semanal creado: {request.plan_name} para paciente {request.patient_id}",
            business_context={
                "action": "weekly_plan_creation",
                "plan_id": weekly_plan.id,
                "patient_id": request.patient_id,
                "nutritionist_id": current_user.id,
                "duration_weeks": request.duration_weeks
            }
        )
        
        return WeeklyPlanResponse(
            id=weekly_plan.id,
            patient_id=weekly_plan.patient_id,
            nutritionist_id=weekly_plan.nutritionist_id,
            plan_name=weekly_plan.plan_name,
            description=weekly_plan.description,
            week_start_date=weekly_plan.week_start_date,
            week_end_date=weekly_plan.week_end_date,
            status=weekly_plan.status,
            target_calories_per_day=weekly_plan.target_calories_per_day,
            target_equivalents=weekly_plan.target_equivalents,
            completion_percentage=weekly_plan.completion_percentage,
            adherence_score=weekly_plan.adherence_score,
            created_at=weekly_plan.created_at,
            published_at=weekly_plan.published_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error creando plan semanal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create weekly plan"
        )

@router.get("/weekly-plans", response_model=List[WeeklyPlanResponse])
async def get_weekly_plans(
    patient_id: Optional[int] = None,
    nutritionist_id: Optional[int] = None,
    status_filter: Optional[PlanStatus] = None,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Obtiene planes semanales con filtros opcionales
    """
    try:
        # Construir query base
        statement = select(WeeklyMealPlan)
        
        # Aplicar filtros basados en rol
        if current_user.has_role("patient") and not current_user.has_role("nutritionist"):
            # Pacientes solo ven sus propios planes
            statement = statement.where(WeeklyMealPlan.patient_id == current_user.id)
        elif current_user.has_role("nutritionist") and not current_user.has_role("admin"):
            # Nutricionistas ven sus propios planes creados
            statement = statement.where(WeeklyMealPlan.nutritionist_id == current_user.id)
        
        # Aplicar filtros adicionales
        if patient_id:
            statement = statement.where(WeeklyMealPlan.patient_id == patient_id)
        
        if nutritionist_id:
            statement = statement.where(WeeklyMealPlan.nutritionist_id == nutritionist_id)
            
        if status_filter:
            statement = statement.where(WeeklyMealPlan.status == status_filter)
        
        # Ordenar por fecha más reciente
        statement = statement.order_by(WeeklyMealPlan.created_at.desc())
        
        result = await session.exec(statement)
        plans = result.all()
        
        response = []
        for plan in plans:
            response.append(WeeklyPlanResponse(
                id=plan.id,
                patient_id=plan.patient_id,
                nutritionist_id=plan.nutritionist_id,
                plan_name=plan.plan_name,
                description=plan.description,
                week_start_date=plan.week_start_date,
                week_end_date=plan.week_end_date,
                status=plan.status,
                target_calories_per_day=plan.target_calories_per_day,
                target_equivalents=plan.target_equivalents,
                completion_percentage=plan.completion_percentage,
                adherence_score=plan.adherence_score,
                created_at=plan.created_at,
                published_at=plan.published_at
            ))
        
        return response
        
    except Exception as e:
        log_error(f"Error obteniendo planes semanales: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch weekly plans"
        )

@router.get("/weekly-plans/{plan_id}", response_model=WeeklyPlanResponse)
async def get_weekly_plan_details(
    plan_id: int,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Obtiene detalles de un plan semanal específico
    """
    try:
        statement = select(WeeklyMealPlan).where(WeeklyMealPlan.id == plan_id)
        result = await session.exec(statement)
        plan = result.first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Weekly plan not found"
            )
        
        # Verificar permisos
        if (current_user.has_role("patient") and plan.patient_id != current_user.id) or \
           (current_user.has_role("nutritionist") and not current_user.has_role("admin") and plan.nutritionist_id != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this plan"
            )
        
        return WeeklyPlanResponse(
            id=plan.id,
            patient_id=plan.patient_id,
            nutritionist_id=plan.nutritionist_id,
            plan_name=plan.plan_name,
            description=plan.description,
            week_start_date=plan.week_start_date,
            week_end_date=plan.week_end_date,
            status=plan.status,
            target_calories_per_day=plan.target_calories_per_day,
            target_equivalents=plan.target_equivalents,
            completion_percentage=plan.completion_percentage,
            adherence_score=plan.adherence_score,
            created_at=plan.created_at,
            published_at=plan.published_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error obteniendo detalles del plan {plan_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch plan details"
        )

@router.get("/weekly-plans/{plan_id}/daily-plans", response_model=List[DailyPlanResponse])
async def get_daily_plans(
    plan_id: int,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Obtiene los planes diarios de un plan semanal
    """
    try:
        # Verificar que el plan existe y el usuario tiene permisos
        plan_statement = select(WeeklyMealPlan).where(WeeklyMealPlan.id == plan_id)
        plan_result = await session.exec(plan_statement)
        plan = plan_result.first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Weekly plan not found"
            )
        
        # Verificar permisos (misma lógica que arriba)
        if (current_user.has_role("patient") and plan.patient_id != current_user.id) or \
           (current_user.has_role("nutritionist") and not current_user.has_role("admin") and plan.nutritionist_id != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this plan"
            )
        
        # Obtener planes diarios
        daily_statement = select(DailyMealPlan).where(
            DailyMealPlan.weekly_plan_id == plan_id
        ).order_by(DailyMealPlan.plan_date)
        
        daily_result = await session.exec(daily_statement)
        daily_plans = daily_result.all()
        
        response = []
        for daily_plan in daily_plans:
            # Por simplicidad, mock de datos para planned_calories y planned_equivalents
            response.append(DailyPlanResponse(
                id=daily_plan.id,
                plan_date=daily_plan.plan_date,
                week_day=daily_plan.week_day,
                daily_calorie_target=daily_plan.daily_calorie_target,
                daily_equivalents_target=daily_plan.daily_equivalents_target,
                planned_calories=daily_plan.daily_calorie_target,  # Simplificado
                planned_equivalents=daily_plan.daily_equivalents_target,  # Simplificado
                is_completed=daily_plan.is_completed,
                adherence_percentage=0.0,  # Simplificado
                meal_assignments=[]  # Simplificado
            ))
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error obteniendo planes diarios para plan {plan_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch daily plans"
        )

@router.post("/weekly-plans/{plan_id}/publish")
async def publish_weekly_plan(
    plan_id: int,
    current_user: AuthUser = Depends(get_nutritionist_or_admin),
    session: Session = Depends(get_async_session)
):
    """
    Publica un plan semanal (lo activa para el paciente)
    """
    try:
        statement = select(WeeklyMealPlan).where(WeeklyMealPlan.id == plan_id)
        result = await session.exec(statement)
        plan = result.first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Weekly plan not found"
            )
        
        # Verificar que sea el nutricionista que creó el plan o admin
        if not current_user.has_role("admin") and plan.nutritionist_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the creator or admin can publish this plan"
            )
        
        # Actualizar estado
        plan.status = PlanStatus.ACTIVE
        plan.published_at = datetime.utcnow()
        plan.updated_at = datetime.utcnow()
        
        session.add(plan)
        await session.commit()
        
        log_success(
            f"Plan semanal publicado: {plan.plan_name} (ID: {plan_id})",
            business_context={
                "action": "plan_publication",
                "plan_id": plan_id,
                "patient_id": plan.patient_id,
                "nutritionist_id": current_user.id
            }
        )
        
        return {"message": "Plan published successfully", "plan_id": plan_id, "status": plan.status}
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error publicando plan {plan_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish plan"
        )

@router.get("/meal-times", response_model=List[Dict[str, Any]])
async def get_meal_times():
    """
    Obtiene información sobre los tiempos de comida disponibles
    """
    meal_times = []
    for meal_time, info in MEAL_TIME_INFO.items():
        meal_times.append({
            "value": meal_time.value,
            "name": info["name"],
            "suggested_time": info["suggested_time"],
            "default_calories_percentage": info["default_calories_percentage"],
            "color": info["color"]
        })
    
    return meal_times

@router.get("/weekdays", response_model=List[Dict[str, Any]])
async def get_weekdays():
    """
    Obtiene información sobre los días de la semana
    """
    weekdays = []
    for weekday, info in WEEKDAY_INFO.items():
        weekdays.append({
            "value": weekday.value,
            "name": info["name"],
            "order": info["order"]
        })
    
    return weekdays

# Endpoints de feedback
@router.post("/weekly-plans/{plan_id}/feedback")
async def submit_plan_feedback(
    plan_id: int,
    feedback: PlanFeedbackRequest,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Permite a un paciente enviar feedback sobre un plan semanal
    """
    try:
        # Verificar que el plan existe
        plan_statement = select(WeeklyMealPlan).where(WeeklyMealPlan.id == plan_id)
        plan_result = await session.exec(plan_statement)
        plan = plan_result.first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Weekly plan not found"
            )
        
        # Verificar que el usuario es el paciente del plan
        if plan.patient_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only provide feedback for your own plans"
            )
        
        # Crear feedback
        plan_feedback = PlanFeedback(
            weekly_plan_id=plan_id,
            patient_id=current_user.id,
            overall_satisfaction=feedback.overall_satisfaction,
            recipe_variety=feedback.recipe_variety,
            portion_adequacy=feedback.portion_adequacy,
            preparation_difficulty=feedback.preparation_difficulty,
            taste_satisfaction=feedback.taste_satisfaction,
            liked_most=feedback.liked_most,
            disliked_most=feedback.disliked_most,
            suggested_changes=feedback.suggested_changes,
            days_followed_completely=feedback.days_followed_completely,
            missed_meals_count=feedback.missed_meals_count
        )
        
        session.add(plan_feedback)
        await session.commit()
        
        log_success(
            f"Feedback enviado para plan {plan_id} por paciente {current_user.id}",
            business_context={
                "action": "plan_feedback_submission",
                "plan_id": plan_id,
                "patient_id": current_user.id,
                "overall_satisfaction": feedback.overall_satisfaction
            }
        )
        
        return {"message": "Feedback submitted successfully", "feedback_id": plan_feedback.id}
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error enviando feedback para plan {plan_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )