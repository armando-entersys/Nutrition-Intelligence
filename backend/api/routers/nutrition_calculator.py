"""
API Router para Calculadora de Nutrición
Endpoints para nutricionistas para calcular requerimientos y generar planes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from domain.nutritionists.kilocalorie_calculator import (
    KilocalorieCalculator, PatientProfile, MacroDistribution,
    ActivityLevel, Gender, NutritionalGoal
)
from core.logging import log_success, log_error

router = APIRouter()

# Schemas de entrada
class PatientProfileRequest(BaseModel):
    """Esquema para perfil del paciente"""
    age: int = Field(..., ge=1, le=120, description="Edad en años")
    weight: float = Field(..., gt=0, le=500, description="Peso en kilogramos")
    height: float = Field(..., gt=0, le=300, description="Altura en centímetros")
    gender: Gender = Field(..., description="Género")
    activity_level: ActivityLevel = Field(..., description="Nivel de actividad física")
    goal: NutritionalGoal = Field(..., description="Objetivo nutricional")
    
    # Condiciones especiales
    is_pregnant: bool = Field(default=False, description="¿Está embarazada?")
    is_lactating: bool = Field(default=False, description="¿Está lactando?")
    has_diabetes: bool = Field(default=False, description="¿Tiene diabetes?")
    has_hypertension: bool = Field(default=False, description="¿Tiene hipertensión?")

class MacroDistributionRequest(BaseModel):
    """Esquema para distribución de macronutrientes"""
    protein_percentage: float = Field(default=15.0, ge=10, le=25, description="% de proteínas")
    carbs_percentage: float = Field(default=60.0, ge=45, le=70, description="% de carbohidratos")
    fat_percentage: float = Field(default=25.0, ge=15, le=35, description="% de grasas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "protein_percentage": 15.0,
                "carbs_percentage": 60.0,
                "fat_percentage": 25.0
            }
        }

class NutritionPlanRequest(BaseModel):
    """Esquema completo para generar plan nutricional"""
    patient_profile: PatientProfileRequest
    macro_distribution: Optional[MacroDistributionRequest] = None
    nutritionist_id: Optional[int] = Field(None, description="ID del nutricionista")
    notes: Optional[str] = Field(None, description="Notas adicionales")

# Endpoints
@router.post("/calculate-bmr", response_model=Dict)
async def calculate_bmr(profile: PatientProfileRequest):
    """
    Calcula la Tasa Metabólica Basal (TMB) del paciente
    """
    try:
        calculator = KilocalorieCalculator()
        
        # Convertir a objeto de dominio
        patient_profile = PatientProfile(
            age=profile.age,
            weight=profile.weight,
            height=profile.height,
            gender=profile.gender,
            activity_level=profile.activity_level,
            goal=profile.goal,
            is_pregnant=profile.is_pregnant,
            is_lactating=profile.is_lactating,
            has_diabetes=profile.has_diabetes,
            has_hypertension=profile.has_hypertension
        )
        
        bmr = calculator.calculate_bmr(patient_profile)
        
        result = {
            "bmr": bmr,
            "formula": "Mifflin-St Jeor",
            "adjustments": []
        }
        
        if profile.is_pregnant:
            result["adjustments"].append("Embarazo: +300 kcal")
        if profile.is_lactating:
            result["adjustments"].append("Lactancia: +500 kcal")
            
        log_success(
            f"TMB calculada: {bmr} kcal para paciente {profile.gender.value}, {profile.age} años",
            business_context={
                "action": "bmr_calculation",
                "bmr": bmr,
                "patient_age": profile.age,
                "patient_gender": profile.gender.value
            }
        )
        
        return result
        
    except Exception as e:
        log_error(f"Error calculando TMB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en cálculo de TMB: {str(e)}")

@router.post("/calculate-tdee", response_model=Dict)
async def calculate_tdee(profile: PatientProfileRequest):
    """
    Calcula el Gasto Energético Total Diario (TDEE)
    """
    try:
        calculator = KilocalorieCalculator()
        
        patient_profile = PatientProfile(
            age=profile.age,
            weight=profile.weight,
            height=profile.height,
            gender=profile.gender,
            activity_level=profile.activity_level,
            goal=profile.goal,
            is_pregnant=profile.is_pregnant,
            is_lactating=profile.is_lactating,
            has_diabetes=profile.has_diabetes,
            has_hypertension=profile.has_hypertension
        )
        
        bmr = calculator.calculate_bmr(patient_profile)
        tdee = calculator.calculate_tdee(patient_profile)
        activity_factor = calculator.ACTIVITY_FACTORS[profile.activity_level]
        goal_adjustment = calculator.GOAL_ADJUSTMENTS[profile.goal]
        
        result = {
            "bmr": bmr,
            "tdee": tdee,
            "activity_factor": activity_factor,
            "activity_level": profile.activity_level.value,
            "goal": profile.goal.value,
            "goal_adjustment_percentage": round(goal_adjustment * 100, 1),
            "calories_difference": round(tdee - (bmr * activity_factor), 0)
        }
        
        log_success(
            f"TDEE calculado: {tdee} kcal (TMB: {bmr}, Factor: {activity_factor}, Objetivo: {profile.goal.value})",
            business_context={
                "action": "tdee_calculation",
                "tdee": tdee,
                "bmr": bmr,
                "activity_level": profile.activity_level.value,
                "goal": profile.goal.value
            }
        )
        
        return result
        
    except Exception as e:
        log_error(f"Error calculando TDEE: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en cálculo de TDEE: {str(e)}")

class CaloriesRequest(BaseModel):
    """Esquema para calorías"""
    calories: float = Field(..., gt=0, description="Calorías totales")

@router.post("/calculate-macros", response_model=Dict)
async def calculate_macros(request: CaloriesRequest, macro_distribution: MacroDistributionRequest = MacroDistributionRequest()):
    """
    Calcula distribución de macronutrientes en gramos
    """
    try:
        # Validar que los porcentajes suman 100%
        total_percentage = (
            macro_distribution.protein_percentage + 
            macro_distribution.carbs_percentage + 
            macro_distribution.fat_percentage
        )
        
        if abs(total_percentage - 100.0) > 0.1:
            raise HTTPException(
                status_code=400, 
                detail=f"Los porcentajes deben sumar 100%. Actual: {total_percentage}%"
            )
        
        calculator = KilocalorieCalculator()
        macros_distribution = MacroDistribution(
            protein_percentage=macro_distribution.protein_percentage,
            carbs_percentage=macro_distribution.carbs_percentage,
            fat_percentage=macro_distribution.fat_percentage
        )
        
        macros = calculator.calculate_macros(request.calories, macros_distribution)
        
        result = {
            "total_calories": request.calories,
            "protein": {
                "grams": macros["protein_grams"],
                "calories": macros["protein_calories"],
                "percentage": macro_distribution.protein_percentage
            },
            "carbohydrates": {
                "grams": macros["carbs_grams"],
                "calories": macros["carbs_calories"],
                "percentage": macro_distribution.carbs_percentage
            },
            "fats": {
                "grams": macros["fat_grams"],
                "calories": macros["fat_calories"],
                "percentage": macro_distribution.fat_percentage
            }
        }
        
        log_success(
            f"Macros calculados para {request.calories} kcal: P:{macros['protein_grams']}g, C:{macros['carbs_grams']}g, G:{macros['fat_grams']}g",
            business_context={
                "action": "macros_calculation",
                "calories": request.calories,
                "protein_g": macros["protein_grams"],
                "carbs_g": macros["carbs_grams"],
                "fat_g": macros["fat_grams"]
            }
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error calculando macronutrientes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en cálculo de macros: {str(e)}")

@router.post("/create-nutrition-plan", response_model=Dict)
async def create_nutrition_plan(request: NutritionPlanRequest):
    """
    Crea un plan nutricional completo con distribución de equivalentes SMAE
    """
    try:
        calculator = KilocalorieCalculator()
        
        # Convertir perfil del paciente
        patient_profile = PatientProfile(
            age=request.patient_profile.age,
            weight=request.patient_profile.weight,
            height=request.patient_profile.height,
            gender=request.patient_profile.gender,
            activity_level=request.patient_profile.activity_level,
            goal=request.patient_profile.goal,
            is_pregnant=request.patient_profile.is_pregnant,
            is_lactating=request.patient_profile.is_lactating,
            has_diabetes=request.patient_profile.has_diabetes,
            has_hypertension=request.patient_profile.has_hypertension
        )
        
        # Distribución de macros (usar default si no se proporciona)
        macro_distribution = MacroDistribution()
        if request.macro_distribution:
            macro_distribution = MacroDistribution(
                protein_percentage=request.macro_distribution.protein_percentage,
                carbs_percentage=request.macro_distribution.carbs_percentage,
                fat_percentage=request.macro_distribution.fat_percentage
            )
        
        # Generar plan completo
        nutrition_plan = calculator.create_nutrition_plan(patient_profile, macro_distribution)
        
        # Agregar metadatos adicionales
        nutrition_plan["nutritionist_id"] = request.nutritionist_id
        nutrition_plan["additional_notes"] = request.notes
        
        log_success(
            f"Plan nutricional creado: {nutrition_plan['calculations']['tdee']} kcal, {len(nutrition_plan['equivalents_prescription'])} grupos de equivalentes",
            business_context={
                "action": "nutrition_plan_creation",
                "tdee": nutrition_plan['calculations']['tdee'],
                "equivalents_groups": len(nutrition_plan['equivalents_prescription']),
                "nutritionist_id": request.nutritionist_id,
                "patient_age": request.patient_profile.age,
                "patient_goal": request.patient_profile.goal.value
            }
        )
        
        return nutrition_plan
        
    except Exception as e:
        log_error(f"Error creando plan nutricional: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creando plan nutricional: {str(e)}")

@router.get("/activity-levels", response_model=List[Dict])
async def get_activity_levels():
    """
    Obtiene los niveles de actividad física disponibles
    """
    return [
        {
            "value": ActivityLevel.SEDENTARIO.value,
            "name": "Sedentario",
            "description": "Poco o ningún ejercicio",
            "factor": 1.2
        },
        {
            "value": ActivityLevel.LIGERO.value,
            "name": "Actividad Ligera",
            "description": "Ejercicio ligero 1-3 días por semana",
            "factor": 1.375
        },
        {
            "value": ActivityLevel.MODERADO.value,
            "name": "Actividad Moderada",
            "description": "Ejercicio moderado 3-5 días por semana",
            "factor": 1.55
        },
        {
            "value": ActivityLevel.ACTIVO.value,
            "name": "Actividad Alta",
            "description": "Ejercicio intenso 6-7 días por semana",
            "factor": 1.725
        },
        {
            "value": ActivityLevel.MUY_ACTIVO.value,
            "name": "Muy Activo",
            "description": "Ejercicio muy intenso, trabajo físico",
            "factor": 1.9
        }
    ]

@router.get("/nutritional-goals", response_model=List[Dict])
async def get_nutritional_goals():
    """
    Obtiene los objetivos nutricionales disponibles
    """
    return [
        {
            "value": NutritionalGoal.MANTENER.value,
            "name": "Mantener Peso",
            "description": "Mantener peso actual",
            "adjustment": "0%"
        },
        {
            "value": NutritionalGoal.PERDER_LENTO.value,
            "name": "Pérdida Lenta",
            "description": "Perder peso gradualmente",
            "adjustment": "-10%"
        },
        {
            "value": NutritionalGoal.PERDER_MODERADO.value,
            "name": "Pérdida Moderada",
            "description": "Pérdida de peso más acelerada",
            "adjustment": "-20%"
        },
        {
            "value": NutritionalGoal.GANAR_LENTO.value,
            "name": "Ganancia Lenta",
            "description": "Ganancia gradual de peso",
            "adjustment": "+10%"
        },
        {
            "value": NutritionalGoal.GANAR_MODERADO.value,
            "name": "Ganancia Moderada",
            "description": "Ganancia más rápida de peso",
            "adjustment": "+15%"
        }
    ]