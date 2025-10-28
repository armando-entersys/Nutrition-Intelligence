"""
Calculadora Nutricional para Conversión de Kilocalorías a Equivalentes
Basado en fórmulas científicas y patrones alimentarios mexicanos
"""
from typing import Dict, Optional
from enum import Enum
from datetime import datetime, date
import math

from .models import Patient, Gender, ActivityLevel, AnthropometricRecord
from ..foods.equivalences import EquivalenceGroup, SMAE_GROUP_STANDARDS

class NutritionalGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_MAINTENANCE = "weight_maintenance"
    WEIGHT_GAIN = "weight_gain"
    MUSCLE_GAIN = "muscle_gain"
    FAT_LOSS = "fat_loss"
    HEALTH_IMPROVEMENT = "health_improvement"

class BMRFormula(str, Enum):
    HARRIS_BENEDICT = "harris_benedict"
    MIFFLIN_ST_JEOR = "mifflin_st_jeor"
    KATCH_MCARDLE = "katch_mcardle"  # Requiere % grasa corporal

class NutritionalCalculator:
    """Calculadora principal para requerimientos nutricionales"""
    
    # Factores de actividad física
    ACTIVITY_FACTORS = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHTLY_ACTIVE: 1.375,
        ActivityLevel.MODERATELY_ACTIVE: 1.55,
        ActivityLevel.VERY_ACTIVE: 1.725,
        ActivityLevel.EXTREMELY_ACTIVE: 1.9
    }
    
    # Ajustes calóricos por objetivo
    GOAL_ADJUSTMENTS = {
        NutritionalGoal.WEIGHT_LOSS: -0.20,  # -20% de calorías
        NutritionalGoal.WEIGHT_MAINTENANCE: 0.0,
        NutritionalGoal.WEIGHT_GAIN: 0.15,  # +15% de calorías
        NutritionalGoal.MUSCLE_GAIN: 0.10,  # +10% de calorías
        NutritionalGoal.FAT_LOSS: -0.15,  # -15% de calorías
        NutritionalGoal.HEALTH_IMPROVEMENT: 0.0
    }
    
    # Distribución de macronutrientes por objetivo (% de calorías totales)
    MACRO_DISTRIBUTIONS = {
        NutritionalGoal.WEIGHT_LOSS: {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
        NutritionalGoal.WEIGHT_MAINTENANCE: {"protein": 0.20, "carbs": 0.50, "fat": 0.30},
        NutritionalGoal.WEIGHT_GAIN: {"protein": 0.20, "carbs": 0.55, "fat": 0.25},
        NutritionalGoal.MUSCLE_GAIN: {"protein": 0.25, "carbs": 0.45, "fat": 0.30},
        NutritionalGoal.FAT_LOSS: {"protein": 0.35, "carbs": 0.35, "fat": 0.30},
        NutritionalGoal.HEALTH_IMPROVEMENT: {"protein": 0.20, "carbs": 0.50, "fat": 0.30}
    }
    
    def __init__(self, patient: Patient, latest_anthropometric: AnthropometricRecord):
        self.patient = patient
        self.anthropometric = latest_anthropometric
        
    def calculate_bmr(self, formula: BMRFormula = BMRFormula.MIFFLIN_ST_JEOR) -> float:
        """Calcular Tasa Metabólica Basal"""
        age = self.patient.current_age
        weight = self.anthropometric.weight_kg
        height = self.anthropometric.height_cm
        gender = self.patient.gender
        
        if not height:
            raise ValueError("Altura requerida para calcular BMR")
            
        if formula == BMRFormula.HARRIS_BENEDICT:
            if gender == Gender.MALE:
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
                
        elif formula == BMRFormula.MIFFLIN_ST_JEOR:
            if gender == Gender.MALE:
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
                
        elif formula == BMRFormula.KATCH_MCARDLE:
            if not self.anthropometric.body_fat_pct:
                raise ValueError("% de grasa corporal requerido para fórmula Katch-McArdle")
            lean_mass = weight * (1 - self.anthropometric.body_fat_pct / 100)
            bmr = 370 + (21.6 * lean_mass)
            
        return round(bmr, 2)
    
    def calculate_tdee(self, bmr: Optional[float] = None) -> float:
        """Calcular Gasto Energético Total Diario"""
        if bmr is None:
            bmr = self.calculate_bmr()
            
        activity_factor = self.ACTIVITY_FACTORS.get(
            self.patient.activity_level, 
            self.ACTIVITY_FACTORS[ActivityLevel.SEDENTARY]
        )
        
        tdee = bmr * activity_factor
        return round(tdee, 2)
    
    def calculate_target_calories(self, goal: NutritionalGoal, tdee: Optional[float] = None) -> float:
        """Calcular calorías objetivo según meta del paciente"""
        if tdee is None:
            tdee = self.calculate_tdee()
            
        adjustment = self.GOAL_ADJUSTMENTS.get(goal, 0.0)
        target_calories = tdee * (1 + adjustment)
        
        # Límites de seguridad
        min_calories = max(1200 if self.patient.gender == Gender.FEMALE else 1500, tdee * 0.7)
        max_calories = tdee * 1.3
        
        target_calories = max(min_calories, min(target_calories, max_calories))
        
        return round(target_calories, 2)
    
    def calculate_macronutrients(self, target_calories: float, goal: NutritionalGoal) -> Dict[str, float]:
        """Calcular distribución de macronutrientes"""
        distribution = self.MACRO_DISTRIBUTIONS.get(
            goal, 
            self.MACRO_DISTRIBUTIONS[NutritionalGoal.WEIGHT_MAINTENANCE]
        )
        
        # Calcular gramos de cada macronutriente
        protein_calories = target_calories * distribution["protein"]
        carbs_calories = target_calories * distribution["carbs"]
        fat_calories = target_calories * distribution["fat"]
        
        # Convertir a gramos (4 kcal/g para proteína y carbos, 9 kcal/g para grasa)
        protein_grams = protein_calories / 4
        carbs_grams = carbs_calories / 4
        fat_grams = fat_calories / 9
        
        return {
            "protein_g": round(protein_grams, 1),
            "carbs_g": round(carbs_grams, 1),
            "fat_g": round(fat_grams, 1),
            "protein_calories": round(protein_calories, 1),
            "carbs_calories": round(carbs_calories, 1),
            "fat_calories": round(fat_calories, 1)
        }

class EquivalenceDistributor:
    """Distribuidor de calorías en equivalentes por grupo SMAE"""
    
    # Patrones de distribución típicos mexicanos por objetivo
    DISTRIBUTION_PATTERNS = {
        NutritionalGoal.WEIGHT_LOSS: {
            EquivalenceGroup.CEREALES: 0.25,           # 25% de calorías
            EquivalenceGroup.LEGUMINOSAS: 0.05,        # 5% de calorías
            EquivalenceGroup.AOA_BAJO_GRASA: 0.20,     # 20% de calorías
            EquivalenceGroup.AOA_MODERADA_GRASA: 0.10, # 10% de calorías
            EquivalenceGroup.LECHE_DESCREMADA: 0.08,   # 8% de calorías
            EquivalenceGroup.VERDURAS: 0.10,           # 10% de calorías
            EquivalenceGroup.FRUTAS: 0.12,             # 12% de calorías
            EquivalenceGroup.GRASAS_SIN_PROTEINA: 0.10 # 10% de calorías
        },
        NutritionalGoal.WEIGHT_MAINTENANCE: {
            EquivalenceGroup.CEREALES: 0.35,
            EquivalenceGroup.LEGUMINOSAS: 0.08,
            EquivalenceGroup.AOA_BAJO_GRASA: 0.15,
            EquivalenceGroup.AOA_MODERADA_GRASA: 0.08,
            EquivalenceGroup.LECHE_DESCREMADA: 0.10,
            EquivalenceGroup.VERDURAS: 0.08,
            EquivalenceGroup.FRUTAS: 0.10,
            EquivalenceGroup.GRASAS_SIN_PROTEINA: 0.06
        },
        NutritionalGoal.WEIGHT_GAIN: {
            EquivalenceGroup.CEREALES: 0.40,
            EquivalenceGroup.LEGUMINOSAS: 0.10,
            EquivalenceGroup.AOA_MODERADA_GRASA: 0.15,
            EquivalenceGroup.AOA_BAJO_GRASA: 0.10,
            EquivalenceGroup.LECHE_SEMIDESCREMADA: 0.10,
            EquivalenceGroup.VERDURAS: 0.05,
            EquivalenceGroup.FRUTAS: 0.08,
            EquivalenceGroup.GRASAS_SIN_PROTEINA: 0.02
        },
        NutritionalGoal.MUSCLE_GAIN: {
            EquivalenceGroup.CEREALES: 0.30,
            EquivalenceGroup.LEGUMINOSAS: 0.12,
            EquivalenceGroup.AOA_BAJO_GRASA: 0.20,
            EquivalenceGroup.AOA_MODERADA_GRASA: 0.08,
            EquivalenceGroup.LECHE_DESCREMADA: 0.12,
            EquivalenceGroup.VERDURAS: 0.08,
            EquivalenceGroup.FRUTAS: 0.08,
            EquivalenceGroup.GRASAS_SIN_PROTEINA: 0.02
        }
    }
    
    def __init__(self, target_calories: float, goal: NutritionalGoal):
        self.target_calories = target_calories
        self.goal = goal
        
    def distribute_to_equivalents(self) -> Dict[str, float]:
        """Convertir calorías objetivo a equivalentes por grupo"""
        pattern = self.DISTRIBUTION_PATTERNS.get(
            self.goal,
            self.DISTRIBUTION_PATTERNS[NutritionalGoal.WEIGHT_MAINTENANCE]
        )
        
        equivalents_by_group = {}
        
        for group, percentage in pattern.items():
            calories_for_group = self.target_calories * percentage
            standard_calories = SMAE_GROUP_STANDARDS[group]["calories"]
            equivalents = calories_for_group / standard_calories
            
            # Redondear a medios equivalentes (0.5, 1.0, 1.5, etc.)
            equivalents = round(equivalents * 2) / 2
            
            # Mínimos y máximos de seguridad
            min_equiv = SMAE_GROUP_STANDARDS[group].get("min_daily", 0)
            max_equiv = SMAE_GROUP_STANDARDS[group].get("max_daily", 20)
            
            equivalents = max(min_equiv, min(equivalents, max_equiv))
            
            if equivalents > 0:
                equivalents_by_group[group.value] = equivalents
        
        return equivalents_by_group
    
    def calculate_actual_calories(self, equivalents: Dict[str, float]) -> float:
        """Calcular calorías reales basadas en los equivalentes asignados"""
        total_calories = 0
        
        for group_key, equiv_count in equivalents.items():
            try:
                group = EquivalenceGroup(group_key)
                standard_calories = SMAE_GROUP_STANDARDS[group]["calories"]
                total_calories += equiv_count * standard_calories
            except ValueError:
                continue  # Skip invalid groups
                
        return round(total_calories, 2)
    
    def get_distribution_summary(self, equivalents: Dict[str, float]) -> Dict[str, any]:
        """Obtener resumen completo de la distribución"""
        actual_calories = self.calculate_actual_calories(equivalents)
        
        summary = {
            "target_calories": self.target_calories,
            "actual_calories": actual_calories,
            "difference": round(actual_calories - self.target_calories, 2),
            "equivalents_by_group": equivalents,
            "daily_distribution": []
        }
        
        # Detalles por grupo
        for group_key, equiv_count in equivalents.items():
            try:
                group = EquivalenceGroup(group_key)
                standards = SMAE_GROUP_STANDARDS[group]
                group_calories = equiv_count * standards["calories"]
                
                summary["daily_distribution"].append({
                    "group": group_key,
                    "group_name": standards["name"],
                    "equivalents": equiv_count,
                    "calories": round(group_calories, 2),
                    "percentage": round((group_calories / actual_calories) * 100, 1) if actual_calories > 0 else 0,
                    "color": standards["color"]
                })
            except ValueError:
                continue
                
        return summary

def create_nutritional_profile(patient: Patient, goal: NutritionalGoal) -> Dict[str, any]:
    """Función principal para crear perfil nutricional completo"""
    # Obtener último registro antropométrico
    # En producción, esto vendría de la base de datos
    latest_anthropometric = AnthropometricRecord(
        patient_id=patient.id,
        weight_kg=70.0,  # Ejemplo
        height_cm=165.0,  # Ejemplo
        measurement_date=date.today()
    )
    
    # Calcular requerimientos
    calculator = NutritionalCalculator(patient, latest_anthropometric)
    
    bmr = calculator.calculate_bmr()
    tdee = calculator.calculate_tdee(bmr)
    target_calories = calculator.calculate_target_calories(goal, tdee)
    macros = calculator.calculate_macronutrients(target_calories, goal)
    
    # Distribuir en equivalentes
    distributor = EquivalenceDistributor(target_calories, goal)
    equivalents = distributor.distribute_to_equivalents()
    distribution_summary = distributor.get_distribution_summary(equivalents)
    
    # Perfil completo
    profile = {
        "patient_id": patient.id,
        "goal": goal.value,
        "calculations": {
            "bmr": bmr,
            "tdee": tdee,
            "target_calories": target_calories
        },
        "macronutrients": macros,
        "equivalents_distribution": distribution_summary,
        "anthropometric_data": {
            "weight_kg": latest_anthropometric.weight_kg,
            "height_cm": latest_anthropometric.height_cm,
            "bmi": round(latest_anthropometric.weight_kg / (latest_anthropometric.height_cm/100)**2, 2) if latest_anthropometric.height_cm else None
        },
        "created_at": datetime.utcnow()
    }
    
    return profile