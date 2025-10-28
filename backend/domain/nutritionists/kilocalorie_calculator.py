"""
Calculadora de Kilocalorías y Distribución de Equivalentes
Sistema para nutricionistas para calcular requerimientos energéticos y convertirlos a equivalentes SMAE
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from ..foods.equivalences import EquivalenceGroup, SMAE_GROUP_STANDARDS

class ActivityLevel(str, Enum):
    """Niveles de actividad física"""
    SEDENTARIO = "sedentario"          # 1.2
    LIGERO = "ligero"                  # 1.375
    MODERADO = "moderado"              # 1.55
    ACTIVO = "activo"                  # 1.725
    MUY_ACTIVO = "muy_activo"          # 1.9

class Gender(str, Enum):
    """Género para cálculo de TMB"""
    MASCULINO = "masculino"
    FEMENINO = "femenino"

class NutritionalGoal(str, Enum):
    """Objetivos nutricionales"""
    MANTENER = "mantener"              # 0%
    PERDER_LENTO = "perder_lento"      # -10%
    PERDER_MODERADO = "perder_moderado" # -20%
    GANAR_LENTO = "ganar_lento"        # +10%
    GANAR_MODERADO = "ganar_moderado"  # +15%

@dataclass
class PatientProfile:
    """Perfil del paciente para cálculo"""
    age: int                    # años
    weight: float              # kg
    height: float              # cm
    gender: Gender
    activity_level: ActivityLevel
    goal: NutritionalGoal
    
    # Factores adicionales
    is_pregnant: bool = False
    is_lactating: bool = False
    has_diabetes: bool = False
    has_hypertension: bool = False

@dataclass
class MacroDistribution:
    """Distribución de macronutrientes"""
    protein_percentage: float = 15.0    # 10-15%
    carbs_percentage: float = 60.0      # 55-65%
    fat_percentage: float = 25.0        # 20-30%

@dataclass
class EquivalentsPrescription:
    """Prescripción de equivalentes por grupo"""
    group: EquivalenceGroup
    daily_equivalents: float
    calories_contribution: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    notes: Optional[str] = None

class KilocalorieCalculator:
    """Calculadora principal de kilocalorías y equivalentes"""
    
    # Factores de actividad física
    ACTIVITY_FACTORS = {
        ActivityLevel.SEDENTARIO: 1.2,
        ActivityLevel.LIGERO: 1.375,
        ActivityLevel.MODERADO: 1.55,
        ActivityLevel.ACTIVO: 1.725,
        ActivityLevel.MUY_ACTIVO: 1.9
    }
    
    # Ajustes por objetivo
    GOAL_ADJUSTMENTS = {
        NutritionalGoal.MANTENER: 0.0,
        NutritionalGoal.PERDER_LENTO: -0.10,
        NutritionalGoal.PERDER_MODERADO: -0.20,
        NutritionalGoal.GANAR_LENTO: 0.10,
        NutritionalGoal.GANAR_MODERADO: 0.15
    }
    
    def calculate_bmr(self, profile: PatientProfile) -> float:
        """
        Calcula la Tasa Metabólica Basal usando ecuación de Mifflin-St Jeor
        """
        if profile.gender == Gender.MASCULINO:
            bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * profile.age) + 5
        else:
            bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * profile.age) - 161
            
        # Ajustes por condiciones especiales
        if profile.is_pregnant:
            bmr += 300  # Segundo y tercer trimestre
        elif profile.is_lactating:
            bmr += 500  # Lactancia exclusiva
            
        return round(bmr, 1)
    
    def calculate_tdee(self, profile: PatientProfile) -> float:
        """
        Calcula el Gasto Energético Total Diario
        """
        bmr = self.calculate_bmr(profile)
        activity_factor = self.ACTIVITY_FACTORS[profile.activity_level]
        tdee = bmr * activity_factor
        
        # Ajuste por objetivo nutricional
        goal_adjustment = self.GOAL_ADJUSTMENTS[profile.goal]
        adjusted_tdee = tdee * (1 + goal_adjustment)
        
        return round(adjusted_tdee, 0)
    
    def calculate_macros(self, total_calories: float, distribution: MacroDistribution) -> Dict[str, float]:
        """
        Calcula gramos de macronutrientes basado en calorías totales
        """
        protein_calories = total_calories * (distribution.protein_percentage / 100)
        carbs_calories = total_calories * (distribution.carbs_percentage / 100)
        fat_calories = total_calories * (distribution.fat_percentage / 100)
        
        return {
            "protein_grams": round(protein_calories / 4, 1),  # 4 kcal/g
            "carbs_grams": round(carbs_calories / 4, 1),      # 4 kcal/g
            "fat_grams": round(fat_calories / 9, 1),          # 9 kcal/g
            "protein_calories": protein_calories,
            "carbs_calories": carbs_calories,
            "fat_calories": fat_calories
        }
    
    def distribute_to_equivalents(
        self, 
        total_calories: float, 
        macro_targets: Dict[str, float],
        custom_priorities: Optional[Dict[EquivalenceGroup, float]] = None
    ) -> List[EquivalentsPrescription]:
        """
        Distribuye calorías totales en equivalentes SMAE
        """
        prescriptions = []
        remaining_calories = total_calories
        remaining_protein = macro_targets["protein_grams"]
        remaining_carbs = macro_targets["carbs_grams"]
        remaining_fat = macro_targets["fat_grams"]
        
        # Orden de prioridad (básicos primero)
        priority_order = [
            EquivalenceGroup.VERDURAS,           # Base de vitaminas/minerales
            EquivalenceGroup.FRUTAS,             # Vitaminas y fibra
            EquivalenceGroup.CEREALES,           # Carbohidratos base
            EquivalenceGroup.AOA_BAJO_GRASA,     # Proteína principal
            EquivalenceGroup.LECHE_DESCREMADA,   # Calcio y proteína
            EquivalenceGroup.LEGUMINOSAS,        # Proteína vegetal y fibra
            EquivalenceGroup.GRASAS_SIN_PROTEINA, # Ácidos grasos esenciales
            EquivalenceGroup.AOA_MODERADA_GRASA, # Proteína adicional
            EquivalenceGroup.AZUCARES_SIN_GRASA  # Energía adicional si necesaria
        ]
        
        for group in priority_order:
            if group not in SMAE_GROUP_STANDARDS:
                continue
                
            standard = SMAE_GROUP_STANDARDS[group]
            
            # Calcular equivalentes necesarios basado en recomendaciones mínimas
            min_equivalents = standard.get("min_daily", 0)
            max_equivalents = standard.get("max_daily", 10)
            
            # Ajustar según necesidades nutricionales restantes
            if group == EquivalenceGroup.VERDURAS:
                target_equivalents = max(min_equivalents, min(8, max_equivalents))
            elif group == EquivalenceGroup.FRUTAS:
                target_equivalents = max(min_equivalents, min(3, max_equivalents))
            elif group == EquivalenceGroup.CEREALES:
                # Basado en carbohidratos restantes
                carbs_needed = remaining_carbs
                carbs_per_equiv = standard["carbs"]
                cereales_needed = carbs_needed * 0.6 / carbs_per_equiv  # 60% de carbs de cereales
                target_equivalents = max(min_equivalents, min(cereales_needed, max_equivalents))
            elif group == EquivalenceGroup.AOA_BAJO_GRASA:
                # Basado en proteína restante
                protein_needed = remaining_protein
                protein_per_equiv = standard["protein"]
                protein_needed_equiv = protein_needed * 0.5 / protein_per_equiv  # 50% de proteína animal
                target_equivalents = max(min_equivalents, min(protein_needed_equiv, max_equivalents))
            else:
                # Para otros grupos, usar el mínimo recomendado
                target_equivalents = min_equivalents
            
            target_equivalents = round(target_equivalents, 1)
            
            if target_equivalents > 0:
                calories_contrib = target_equivalents * standard["calories"]
                protein_contrib = target_equivalents * standard["protein"]
                carbs_contrib = target_equivalents * standard["carbs"]
                fat_contrib = target_equivalents * standard["fat"]
                
                # Verificar que no excedamos los límites
                if calories_contrib <= remaining_calories:
                    prescription = EquivalentsPrescription(
                        group=group,
                        daily_equivalents=target_equivalents,
                        calories_contribution=calories_contrib,
                        protein_grams=protein_contrib,
                        carbs_grams=carbs_contrib,
                        fat_grams=fat_contrib,
                        notes=f"Aporta {standard['description']}"
                    )
                    prescriptions.append(prescription)
                    
                    remaining_calories -= calories_contrib
                    remaining_protein -= protein_contrib
                    remaining_carbs -= carbs_contrib
                    remaining_fat -= fat_contrib
        
        return prescriptions
    
    def create_nutrition_plan(
        self, 
        profile: PatientProfile, 
        macro_distribution: MacroDistribution = MacroDistribution()
    ) -> Dict:
        """
        Crea un plan nutricional completo
        """
        # Cálculos base
        bmr = self.calculate_bmr(profile)
        tdee = self.calculate_tdee(profile)
        macros = self.calculate_macros(tdee, macro_distribution)
        
        # Distribución en equivalentes
        equivalents = self.distribute_to_equivalents(tdee, macros)
        
        # Resumen nutricional
        total_equiv_calories = sum(eq.calories_contribution for eq in equivalents)
        total_equiv_protein = sum(eq.protein_grams for eq in equivalents)
        total_equiv_carbs = sum(eq.carbs_grams for eq in equivalents)
        total_equiv_fat = sum(eq.fat_grams for eq in equivalents)
        
        return {
            "patient_profile": profile,
            "calculations": {
                "bmr": bmr,
                "tdee": tdee,
                "target_calories": tdee,
                "macro_targets": macros
            },
            "equivalents_prescription": [
                {
                    "group": eq.group.value,
                    "group_name": SMAE_GROUP_STANDARDS[eq.group]["name"],
                    "daily_equivalents": eq.daily_equivalents,
                    "calories": eq.calories_contribution,
                    "protein_g": eq.protein_grams,
                    "carbs_g": eq.carbs_grams,
                    "fat_g": eq.fat_grams,
                    "notes": eq.notes
                }
                for eq in equivalents
            ],
            "plan_summary": {
                "total_calories_from_equivalents": total_equiv_calories,
                "total_protein_from_equivalents": total_equiv_protein,
                "total_carbs_from_equivalents": total_equiv_carbs,
                "total_fat_from_equivalents": total_equiv_fat,
                "calories_accuracy": round((total_equiv_calories / tdee) * 100, 1),
                "protein_accuracy": round((total_equiv_protein / macros["protein_grams"]) * 100, 1)
            },
            "created_at": datetime.utcnow().isoformat(),
            "nutritionist_notes": {
                "activity_level": f"Nivel de actividad: {profile.activity_level.value}",
                "goal": f"Objetivo: {profile.goal.value}",
                "special_conditions": self._get_special_conditions_notes(profile)
            }
        }
    
    def _get_special_conditions_notes(self, profile: PatientProfile) -> List[str]:
        """Genera notas sobre condiciones especiales"""
        notes = []
        
        if profile.is_pregnant:
            notes.append("Embarazo: +300 kcal adicionales (2do/3er trimestre)")
        if profile.is_lactating:
            notes.append("Lactancia: +500 kcal adicionales")
        if profile.has_diabetes:
            notes.append("Diabetes: Control de carbohidratos, preferir complejos")
        if profile.has_hypertension:
            notes.append("Hipertensión: Reducir sodio, aumentar potasio")
            
        return notes