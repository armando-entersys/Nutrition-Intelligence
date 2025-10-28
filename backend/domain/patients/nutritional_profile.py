"""
Modelo de Perfil Nutricional para almacenar cálculos y metas del paciente
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
from sqlalchemy import JSON

from .nutrition_calculator import NutritionalGoal

class ProfileStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_APPROVAL = "pending_approval"
    NEEDS_UPDATE = "needs_update"

class NutritionalProfile(SQLModel, table=True):
    """Perfil nutricional calculado y personalizado para cada paciente"""
    __tablename__ = "nutritional_profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    
    # Objetivo y estado
    nutritional_goal: NutritionalGoal
    status: ProfileStatus = Field(default=ProfileStatus.PENDING_APPROVAL)
    
    # Datos antropométricos usados en el cálculo
    calculation_weight_kg: float
    calculation_height_cm: float
    calculation_age: int
    calculation_bmi: Optional[float] = Field(default=None)
    calculation_body_fat_pct: Optional[float] = Field(default=None)
    
    # Cálculos metabólicos
    bmr_calculated: float  # Tasa Metabólica Basal
    tdee_calculated: float  # Gasto Energético Total Diario
    target_calories: float  # Calorías objetivo
    
    # Distribución de macronutrientes (en gramos)
    target_protein_g: float
    target_carbs_g: float
    target_fat_g: float
    target_fiber_g: Optional[float] = Field(default=None)
    
    # Distribución por equivalentes SMAE (JSON con grupos y cantidades)
    equivalents_distribution: Dict[str, float] = Field(sa_column=Column(JSON))
    
    # Configuración de flexibilidad
    allow_flexibility_pct: float = Field(default=10.0)  # % de variación permitida
    min_equivalents: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    max_equivalents: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    
    # Personalización del nutriólogo
    nutritionist_notes: Optional[str] = Field(default=None, max_length=1000)
    custom_adjustments: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Preferencias y restricciones del paciente
    dietary_preferences: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    food_restrictions: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Validez temporal
    valid_from: date = Field(default_factory=date.today)
    valid_until: Optional[date] = Field(default=None)
    auto_update_anthropometric: bool = Field(default=True)
    
    # Auditoría
    created_by_id: int = Field(foreign_key="users.id")  # Nutriólogo que lo creó
    approved_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    approved_at: Optional[datetime] = Field(default=None)
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: "Patient" = Relationship()
    created_by: "User" = Relationship(foreign_keys="[NutritionalProfile.created_by_id]")
    approved_by: Optional["User"] = Relationship(foreign_keys="[NutritionalProfile.approved_by_id]")
    
    @property
    def is_active(self) -> bool:
        """Verificar si el perfil está activo y vigente"""
        if self.status != ProfileStatus.ACTIVE:
            return False
        
        today = date.today()
        if self.valid_until and today > self.valid_until:
            return False
            
        return True
    
    @property
    def total_equivalents(self) -> float:
        """Calcular total de equivalentes por día"""
        return sum(self.equivalents_distribution.values())
    
    @property
    def calories_from_equivalents(self) -> float:
        """Calcular calorías reales basadas en equivalentes asignados"""
        from ..foods.equivalences import EquivalenceGroup, SMAE_GROUP_STANDARDS
        
        total_calories = 0
        for group_key, equiv_count in self.equivalents_distribution.items():
            try:
                group = EquivalenceGroup(group_key)
                standard_calories = SMAE_GROUP_STANDARDS[group]["calories"]
                total_calories += equiv_count * standard_calories
            except ValueError:
                continue
        
        return round(total_calories, 2)
    
    @property 
    def adherence_tolerance(self) -> Dict[str, float]:
        """Calcular rangos de tolerancia para cada grupo"""
        tolerance = {}
        flexibility_factor = self.allow_flexibility_pct / 100
        
        for group_key, target in self.equivalents_distribution.items():
            min_equiv = max(0, target * (1 - flexibility_factor))
            max_equiv = target * (1 + flexibility_factor)
            
            # Aplicar límites personalizados si existen
            if self.min_equivalents and group_key in self.min_equivalents:
                min_equiv = max(min_equiv, self.min_equivalents[group_key])
            if self.max_equivalents and group_key in self.max_equivalents:
                max_equiv = min(max_equiv, self.max_equivalents[group_key])
            
            tolerance[group_key] = {
                "target": target,
                "min": round(min_equiv, 1),
                "max": round(max_equiv, 1)
            }
        
        return tolerance

class ProfileAuditLog(SQLModel, table=True):
    """Registro de cambios en perfiles nutricionales"""
    __tablename__ = "nutritional_profile_audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="nutritional_profiles.id", index=True)
    
    # Cambio realizado
    action: str = Field(max_length=50)  # created, updated, approved, deactivated
    field_changed: Optional[str] = Field(default=None, max_length=100)
    previous_value: Optional[str] = Field(default=None, max_length=1000)
    new_value: Optional[str] = Field(default=None, max_length=1000)
    
    # Razón del cambio
    reason: Optional[str] = Field(default=None, max_length=500)
    change_notes: Optional[str] = Field(default=None, max_length=1000)
    
    # Quién y cuándo
    changed_by_id: int = Field(foreign_key="users.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    profile: NutritionalProfile = Relationship()
    changed_by: "User" = Relationship()

class ProfileTemplate(SQLModel, table=True):
    """Plantillas de perfiles para reutilización"""
    __tablename__ = "nutritional_profile_templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Información de la plantilla
    template_name: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    
    # Para qué tipo de paciente
    target_goal: NutritionalGoal
    target_bmi_range: Optional[str] = Field(default=None, max_length=20)  # "18.5-24.9"
    target_age_range: Optional[str] = Field(default=None, max_length=20)  # "25-40"
    target_activity_level: Optional[str] = Field(default=None, max_length=50)
    
    # Configuración base de la plantilla
    base_equivalents_distribution: Dict[str, float] = Field(sa_column=Column(JSON))
    macro_distribution: Dict[str, float] = Field(sa_column=Column(JSON))
    
    # Ajustes automáticos
    calorie_adjustment_factor: float = Field(default=1.0)  # Multiplicador de calorías
    flexibility_percentage: float = Field(default=10.0)
    
    # Configuración
    is_active: bool = Field(default=True)
    is_public: bool = Field(default=False)  # Disponible para otros nutriólogos
    
    # Quién la creó
    created_by_id: int = Field(foreign_key="users.id")
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    created_by: "User" = Relationship()

# Funciones utilitarias

def get_active_profile(patient_id: int) -> Optional[NutritionalProfile]:
    """Obtener el perfil nutricional activo de un paciente"""
    # Esta función se implementaría en el servicio
    pass

def create_profile_from_template(
    patient_id: int, 
    template_id: int, 
    anthropometric_data: Dict[str, float],
    created_by_id: int
) -> NutritionalProfile:
    """Crear perfil basado en plantilla con ajustes personalizados"""
    # Esta función se implementaría en el servicio
    pass

def compare_profiles(old_profile: NutritionalProfile, new_profile: NutritionalProfile) -> Dict[str, Any]:
    """Comparar dos perfiles y mostrar diferencias"""
    differences = {
        "calories_change": new_profile.target_calories - old_profile.target_calories,
        "equivalents_changes": {},
        "macro_changes": {},
        "significant_changes": []
    }
    
    # Comparar equivalentes
    for group in set(list(old_profile.equivalents_distribution.keys()) + list(new_profile.equivalents_distribution.keys())):
        old_val = old_profile.equivalents_distribution.get(group, 0)
        new_val = new_profile.equivalents_distribution.get(group, 0)
        change = new_val - old_val
        
        if abs(change) > 0.5:  # Cambio significativo
            differences["equivalents_changes"][group] = {
                "old": old_val,
                "new": new_val,
                "change": round(change, 1)
            }
            differences["significant_changes"].append(f"{group}: {change:+.1f} equivalentes")
    
    # Comparar macros
    macro_changes = {
        "protein": new_profile.target_protein_g - old_profile.target_protein_g,
        "carbs": new_profile.target_carbs_g - old_profile.target_carbs_g,
        "fat": new_profile.target_fat_g - old_profile.target_fat_g
    }
    
    for macro, change in macro_changes.items():
        if abs(change) > 5:  # Cambio significativo en gramos
            differences["macro_changes"][macro] = {
                "old": getattr(old_profile, f"target_{macro}_g"),
                "new": getattr(new_profile, f"target_{macro}_g"),
                "change": round(change, 1)
            }
    
    return differences