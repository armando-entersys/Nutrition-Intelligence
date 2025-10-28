"""
Sistema de Planificación Semanal de Comidas
Permite a los nutriólogos asignar recetas a días específicos y gestionar planes semanales
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from enum import Enum
from sqlalchemy import JSON

from ..recipes.models import MealType
from ..foods.equivalences import EquivalenceGroup

class WeekDay(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class PlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NEEDS_REVISION = "needs_revision"

class WeeklyMealPlan(SQLModel, table=True):
    """Plan semanal de comidas asignado por el nutriólogo"""
    __tablename__ = "weekly_meal_plans"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    nutritionist_id: int = Field(foreign_key="nutritionists.id", index=True)
    
    # Información del plan
    plan_name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    
    # Fechas del plan
    week_start_date: date  # Siempre lunes
    week_end_date: date    # Siempre domingo
    
    # Estado y configuración
    status: PlanStatus = Field(default=PlanStatus.DRAFT)
    is_template: bool = Field(default=False)  # Para reutilizar como plantilla
    
    # Metas nutricionales de referencia (del perfil nutricional)
    target_calories_per_day: float
    target_equivalents: Dict[str, float] = Field(sa_column=Column(JSON))  # Por día
    
    # Configuración de flexibilidad
    allow_substitutions: bool = Field(default=True)
    substitution_notes: Optional[str] = Field(default=None, max_length=500)
    
    # Notas del nutriólogo
    nutritionist_notes: Optional[str] = Field(default=None, max_length=1000)
    patient_instructions: Optional[str] = Field(default=None, max_length=1000)
    
    # Progreso y adherencia
    completion_percentage: float = Field(default=0.0)
    adherence_score: Optional[float] = Field(default=None)  # 0-100
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    published_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: "Patient" = Relationship()
    nutritionist: "Nutritionist" = Relationship()
    daily_plans: List["DailyMealPlan"] = Relationship(back_populates="weekly_plan")
    feedback_entries: List["PlanFeedback"] = Relationship(back_populates="weekly_plan")
    
    @property
    def current_week_number(self) -> int:
        """Obtener número de semana del año"""
        return self.week_start_date.isocalendar()[1]
    
    @property
    def days_in_plan(self) -> int:
        """Número de días en el plan"""
        return (self.week_end_date - self.week_start_date).days + 1
    
    @property
    def is_current_week(self) -> bool:
        """Verificar si es la semana actual"""
        today = date.today()
        return self.week_start_date <= today <= self.week_end_date
    
    def get_day_plan(self, target_date: date) -> Optional["DailyMealPlan"]:
        """Obtener plan de un día específico"""
        for daily_plan in self.daily_plans:
            if daily_plan.plan_date == target_date:
                return daily_plan
        return None

class DailyMealPlan(SQLModel, table=True):
    """Plan de comidas para un día específico"""
    __tablename__ = "daily_meal_plans"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    weekly_plan_id: int = Field(foreign_key="weekly_meal_plans.id", index=True)
    
    # Identificación del día
    plan_date: date = Field(index=True)
    week_day: WeekDay
    
    # Metas del día
    daily_calorie_target: float
    daily_equivalents_target: Dict[str, float] = Field(sa_column=Column(JSON))
    
    # Estado del día
    is_completed: bool = Field(default=False)
    completion_date: Optional[datetime] = Field(default=None)
    
    # Notas específicas del día
    daily_notes: Optional[str] = Field(default=None, max_length=500)
    special_instructions: Optional[str] = Field(default=None, max_length=500)
    
    # Tracking de consumo real
    actual_calories_consumed: Optional[float] = Field(default=None)
    actual_equivalents_consumed: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    weekly_plan: WeeklyMealPlan = Relationship(back_populates="daily_plans")
    meal_assignments: List["MealAssignment"] = Relationship(back_populates="daily_plan")
    
    @property
    def planned_calories(self) -> float:
        """Calcular calorías planificadas del día"""
        total = 0
        for assignment in self.meal_assignments:
            if assignment.recipe and assignment.servings:
                total += assignment.recipe.calories_per_serving * assignment.servings
        return round(total, 2)
    
    @property
    def planned_equivalents(self) -> Dict[str, float]:
        """Calcular equivalentes planificados del día"""
        equivalents = {}
        for assignment in self.meal_assignments:
            if assignment.calculated_equivalents:
                for group, amount in assignment.calculated_equivalents.items():
                    equivalents[group] = equivalents.get(group, 0) + amount
        return equivalents
    
    @property
    def adherence_percentage(self) -> float:
        """Calcular porcentaje de adherencia del día"""
        if not self.actual_equivalents_consumed:
            return 0.0
        
        total_adherence = 0
        count = 0
        
        for group, target in self.daily_equivalents_target.items():
            actual = self.actual_equivalents_consumed.get(group, 0)
            if target > 0:
                adherence = min(actual / target, 1.0) * 100
                total_adherence += adherence
                count += 1
        
        return round(total_adherence / count, 2) if count > 0 else 0.0

class MealAssignment(SQLModel, table=True):
    """Asignación de receta a una comida específica"""
    __tablename__ = "meal_assignments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    daily_plan_id: int = Field(foreign_key="daily_meal_plans.id", index=True)
    recipe_id: int = Field(foreign_key="recipes.id", index=True)
    
    # Detalles de la comida
    meal_type: MealType
    planned_time: Optional[str] = Field(default=None, max_length=10)  # "08:00", "13:30"
    servings: float = Field(default=1.0)
    
    # Equivalentes calculados para esta asignación
    calculated_equivalents: Dict[str, float] = Field(sa_column=Column(JSON))
    calculated_calories: float
    
    # Personalización
    preparation_notes: Optional[str] = Field(default=None, max_length=500)
    substitution_allowed: bool = Field(default=True)
    substitution_groups: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Prioridad (1 = muy importante, 5 = opcional)
    priority: int = Field(default=3, ge=1, le=5)
    
    # Estado de la asignación
    is_consumed: bool = Field(default=False)
    consumed_at: Optional[datetime] = Field(default=None)
    actual_servings: Optional[float] = Field(default=None)
    
    # Feedback del paciente sobre esta comida específica
    patient_rating: Optional[int] = Field(default=None, ge=1, le=5)
    patient_comments: Optional[str] = Field(default=None, max_length=500)
    
    # Metadatos
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    daily_plan: DailyMealPlan = Relationship(back_populates="meal_assignments")
    recipe: "Recipe" = Relationship()
    
    @property
    def meal_time_display(self) -> str:
        """Nombre amigable del tipo de comida"""
        meal_names = {
            MealType.BREAKFAST: "Desayuno",
            MealType.MORNING_SNACK: "Colación Matutina",
            MealType.LUNCH: "Comida",
            MealType.AFTERNOON_SNACK: "Colación Vespertina",
            MealType.DINNER: "Cena",
            MealType.EVENING_SNACK: "Colación Nocturna"
        }
        return meal_names.get(self.meal_type, self.meal_type.value)
    
    @property
    def is_overdue(self) -> bool:
        """Verificar si la comida ya debería haber sido consumida"""
        if not self.planned_time or self.is_consumed:
            return False
        
        now = datetime.now()
        plan_datetime = datetime.combine(
            self.daily_plan.plan_date,
            datetime.strptime(self.planned_time, "%H:%M").time()
        )
        
        return now > plan_datetime + timedelta(hours=2)  # 2 horas de tolerancia

class PlanFeedback(SQLModel, table=True):
    """Feedback del paciente sobre el plan semanal"""
    __tablename__ = "weekly_plan_feedback"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    weekly_plan_id: int = Field(foreign_key="weekly_meal_plans.id", index=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    
    # Calificaciones generales (1-5)
    overall_satisfaction: int = Field(ge=1, le=5)
    recipe_variety: int = Field(ge=1, le=5)
    portion_adequacy: int = Field(ge=1, le=5)
    preparation_difficulty: int = Field(ge=1, le=5)
    taste_satisfaction: int = Field(ge=1, le=5)
    
    # Feedback detallado
    liked_most: Optional[str] = Field(default=None, max_length=500)
    disliked_most: Optional[str] = Field(default=None, max_length=500)
    suggested_changes: Optional[str] = Field(default=None, max_length=1000)
    
    # Adherencia auto-reportada
    days_followed_completely: int = Field(ge=0, le=7)
    missed_meals_count: int = Field(default=0)
    substitutions_made: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    
    # Efectos percibidos
    energy_level_change: Optional[int] = Field(default=None, ge=-5, le=5)  # -5 mucho peor, +5 mucho mejor
    satiety_satisfaction: Optional[int] = Field(default=None, ge=1, le=5)
    digestive_comfort: Optional[int] = Field(default=None, ge=1, le=5)
    
    # Metadatos
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    weekly_plan: WeeklyMealPlan = Relationship(back_populates="feedback_entries")
    patient: "Patient" = Relationship()

class PlanTemplate(SQLModel, table=True):
    """Plantillas de planes semanales reutilizables"""
    __tablename__ = "weekly_plan_templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Información de la plantilla
    template_name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: str = Field(max_length=100)  # "weight_loss", "diabetes", "general"
    
    # Configuración objetivo
    target_calories_range: str = Field(max_length=20)  # "1500-1800"
    target_goals: List[str] = Field(sa_column=Column(JSON))  # Objetivos compatibles
    
    # Estructura de la plantilla (7 días)
    template_structure: Dict[str, Any] = Field(sa_column=Column(JSON))
    # Ejemplo: {"monday": {"breakfast": recipe_id, "lunch": recipe_id}, ...}
    
    # Equivalentes promedio por día
    avg_equivalents_per_day: Dict[str, float] = Field(sa_column=Column(JSON))
    
    # Configuración
    is_active: bool = Field(default=True)
    is_public: bool = Field(default=False)
    difficulty_level: int = Field(default=3, ge=1, le=5)  # 1=fácil, 5=difícil
    preparation_time_avg: int = Field(default=30)  # minutos promedio por comida
    
    # Estadísticas de uso
    times_used: int = Field(default=0)
    avg_satisfaction_rating: Optional[float] = Field(default=None)
    
    # Quién la creó
    created_by_id: int = Field(foreign_key="users.id")
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    created_by: "User" = Relationship()

# Funciones utilitarias

def create_weekly_plan_from_template(
    template_id: int,
    patient_id: int,
    nutritionist_id: int,
    start_date: date,
    customizations: Optional[Dict[str, Any]] = None
) -> WeeklyMealPlan:
    """Crear plan semanal basado en plantilla"""
    pass

def generate_shopping_list(weekly_plan_id: int) -> Dict[str, Any]:
    """Generar lista de compras basada en plan semanal"""
    pass

def calculate_weekly_equivalents_summary(weekly_plan_id: int) -> Dict[str, Any]:
    """Calcular resumen de equivalentes para la semana"""
    pass

def suggest_recipe_alternatives(
    meal_assignment_id: int,
    reason: str = "patient_preference"
) -> List[Dict[str, Any]]:
    """Sugerir recetas alternativas para una asignación"""
    pass

def auto_adjust_plan_for_missed_meals(
    weekly_plan_id: int,
    missed_meals: List[int]
) -> Dict[str, Any]:
    """Ajustar plan automáticamente cuando se pierden comidas"""
    pass

# Information dictionaries for API responses
MEAL_TIME_INFO = {
    MealType.BREAKFAST: {
        "name": "Desayuno",
        "suggested_time": "07:00",
        "default_calories_percentage": 25,
        "color": "#FFA726"
    },
    MealType.MORNING_SNACK: {
        "name": "Colación Matutina",
        "suggested_time": "10:00",
        "default_calories_percentage": 10,
        "color": "#66BB6A"
    },
    MealType.LUNCH: {
        "name": "Almuerzo",
        "suggested_time": "13:00",
        "default_calories_percentage": 35,
        "color": "#42A5F5"
    },
    MealType.AFTERNOON_SNACK: {
        "name": "Colación Vespertina",
        "suggested_time": "16:00",
        "default_calories_percentage": 10,
        "color": "#AB47BC"
    },
    MealType.DINNER: {
        "name": "Cena",
        "suggested_time": "19:00",
        "default_calories_percentage": 20,
        "color": "#FF7043"
    },
    MealType.EVENING_SNACK: {
        "name": "Colación Nocturna",
        "suggested_time": "21:00",
        "default_calories_percentage": 5,
        "color": "#8D6E63"
    }
}

WEEKDAY_INFO = {
    WeekDay.MONDAY: {"name": "Lunes", "order": 1},
    WeekDay.TUESDAY: {"name": "Martes", "order": 2},
    WeekDay.WEDNESDAY: {"name": "Miércoles", "order": 3},
    WeekDay.THURSDAY: {"name": "Jueves", "order": 4},
    WeekDay.FRIDAY: {"name": "Viernes", "order": 5},
    WeekDay.SATURDAY: {"name": "Sábado", "order": 6},
    WeekDay.SUNDAY: {"name": "Domingo", "order": 7}
}