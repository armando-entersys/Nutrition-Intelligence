"""
Sistema de Equivalencias Dinámicas
Basado en el Sistema Mexicano de Alimentos Equivalentes (SMAE)
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from sqlalchemy import JSON

class EquivalenceGroup(str, Enum):
    """Grupos de equivalencias según SMAE"""
    CEREALES = "cereales"  # Cereales y tubérculos
    LEGUMINOSAS = "leguminosas"  # Leguminosas
    AOA_BAJO_GRASA = "aoa_bajo_grasa"  # Alimentos de Origen Animal bajo en grasa
    AOA_MODERADA_GRASA = "aoa_moderada_grasa"  # Alimentos de Origen Animal moderado en grasa
    AOA_ALTA_GRASA = "aoa_alta_grasa"  # Alimentos de Origen Animal alto en grasa
    LECHE_DESCREMADA = "leche_descremada"  # Leche descremada
    LECHE_SEMIDESCREMADA = "leche_semidescremada"  # Leche semidescremada
    LECHE_ENTERA = "leche_entera"  # Leche entera
    LECHE_CON_AZUCAR = "leche_con_azucar"  # Leche con azúcar
    VERDURAS = "verduras"  # Verduras
    FRUTAS = "frutas"  # Frutas
    GRASAS_SIN_PROTEINA = "grasas_sin_proteina"  # Grasas sin proteína
    GRASAS_CON_PROTEINA = "grasas_con_proteina"  # Grasas con proteína
    AZUCARES_SIN_GRASA = "azucares_sin_grasa"  # Azúcares sin grasa
    AZUCARES_CON_GRASA = "azucares_con_grasa"  # Azúcares con grasa
    ALIMENTOS_LIBRES = "alimentos_libres"  # Alimentos de consumo libre

class FoodEquivalence(SQLModel, table=True):
    """Definición de equivalencias entre alimentos"""
    __tablename__ = "food_equivalences"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Alimento base
    food_id: int = Field(foreign_key="foods.id", index=True)
    
    # Grupo de equivalencia
    equivalence_group: EquivalenceGroup
    
    # Porción estándar por equivalente (en la unidad del alimento)
    standard_portion: float
    standard_unit: str = Field(max_length=20)  # gramos, tazas, piezas, etc.
    
    # Aporte nutricional estándar por equivalente
    calories_per_equivalent: float
    protein_per_equivalent: float = Field(default=0.0)
    carbs_per_equivalent: float = Field(default=0.0)
    fat_per_equivalent: float = Field(default=0.0)
    fiber_per_equivalent: float = Field(default=0.0)
    
    # Metadatos
    notes: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    food: "Food" = Relationship(back_populates="equivalences")

class EquivalenceGroupStandard(SQLModel, table=True):
    """Estándares nutricionales por grupo de equivalencia"""
    __tablename__ = "equivalence_group_standards"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    group: EquivalenceGroup = Field(unique=True, primary_key=True)
    
    # Aporte nutricional estándar por equivalente
    standard_calories: float
    standard_protein: float = Field(default=0.0)
    standard_carbs: float = Field(default=0.0)
    standard_fat: float = Field(default=0.0)
    standard_fiber: float = Field(default=0.0)
    
    # Información del grupo
    group_name: str = Field(max_length=100)
    group_description: str = Field(max_length=500)
    color_hex: str = Field(max_length=7, default="#808080")  # Color para UI
    
    # Recomendaciones de consumo
    min_daily_equivalents: Optional[int] = Field(default=None)
    max_daily_equivalents: Optional[int] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PatientEquivalenceGoal(SQLModel, table=True):
    """Metas de equivalentes por día para cada paciente"""
    __tablename__ = "patient_equivalence_goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    equivalence_group: EquivalenceGroup
    
    # Metas diarias
    daily_target_equivalents: float
    
    # Flexibilidad
    min_equivalents: Optional[float] = Field(default=None)
    max_equivalents: Optional[float] = Field(default=None)
    
    # Estado
    is_active: bool = Field(default=True)
    created_by_nutritionist: int = Field(foreign_key="nutritionists.id")
    
    # Metadatos
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    patient: "Patient" = Relationship()

class DailyEquivalenceTracking(SQLModel, table=True):
    """Seguimiento diario de equivalentes consumidos"""
    __tablename__ = "daily_equivalence_tracking"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)
    tracking_date: datetime = Field(index=True)
    
    # Equivalentes por grupo consumidos
    equivalences_consumed: Dict[str, float] = Field(sa_column=Column(JSON))
    
    # Progreso vs metas
    goals_met_count: int = Field(default=0)
    total_goals_count: int = Field(default=0)
    completion_percentage: float = Field(default=0.0)
    
    # Análisis nutricional derivado
    total_calories_from_equivalents: float = Field(default=0.0)
    macros_distribution: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    patient: "Patient" = Relationship()

# Constantes del SMAE
SMAE_GROUP_STANDARDS = {
    EquivalenceGroup.CEREALES: {
        "name": "Cereales y Tubérculos",
        "calories": 70,
        "protein": 2.0,
        "carbs": 15.0,
        "fat": 0.0,
        "color": "#D2691E",
        "min_daily": 6,
        "max_daily": 11,
        "description": "Aportan energía principalmente de carbohidratos complejos"
    },
    EquivalenceGroup.LEGUMINOSAS: {
        "name": "Leguminosas",
        "calories": 120,
        "protein": 8.0,
        "carbs": 20.0,
        "fat": 1.0,
        "color": "#8B4513",
        "min_daily": 1,
        "max_daily": 2,
        "description": "Fuente importante de proteína vegetal y fibra"
    },
    EquivalenceGroup.AOA_BAJO_GRASA: {
        "name": "Alimentos de Origen Animal - Bajo en Grasa",
        "calories": 75,
        "protein": 14.0,
        "carbs": 0.0,
        "fat": 2.0,
        "color": "#FF6B6B",
        "min_daily": 1,
        "max_daily": 4,
        "description": "Proteína animal de alta calidad con poca grasa"
    },
    EquivalenceGroup.AOA_MODERADA_GRASA: {
        "name": "Alimentos de Origen Animal - Moderada en Grasa",
        "calories": 100,
        "protein": 14.0,
        "carbs": 0.0,
        "fat": 5.5,
        "color": "#FF8E53",
        "min_daily": 0,
        "max_daily": 3,
        "description": "Proteína animal con grasa moderada"
    },
    EquivalenceGroup.AOA_ALTA_GRASA: {
        "name": "Alimentos de Origen Animal - Alta en Grasa",
        "calories": 150,
        "protein": 14.0,
        "carbs": 0.0,
        "fat": 10.0,
        "color": "#FF4757",
        "min_daily": 0,
        "max_daily": 1,
        "description": "Proteína animal con alto contenido de grasa"
    },
    EquivalenceGroup.LECHE_DESCREMADA: {
        "name": "Leche Descremada",
        "calories": 95,
        "protein": 9.0,
        "carbs": 12.0,
        "fat": 2.0,
        "color": "#74B9FF",
        "min_daily": 2,
        "max_daily": 4,
        "description": "Fuente de calcio y proteína con poca grasa"
    },
    EquivalenceGroup.VERDURAS: {
        "name": "Verduras",
        "calories": 25,
        "protein": 2.0,
        "carbs": 4.0,
        "fat": 0.0,
        "color": "#00B894",
        "min_daily": 5,
        "max_daily": 10,
        "description": "Ricas en vitaminas, minerales y fibra"
    },
    EquivalenceGroup.FRUTAS: {
        "name": "Frutas",
        "calories": 60,
        "protein": 0.0,
        "carbs": 15.0,
        "fat": 0.0,
        "color": "#FDCB6E",
        "min_daily": 2,
        "max_daily": 4,
        "description": "Fuente natural de vitaminas y azúcares"
    },
    EquivalenceGroup.GRASAS_SIN_PROTEINA: {
        "name": "Grasas sin Proteína",
        "calories": 45,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 5.0,
        "color": "#6C5CE7",
        "min_daily": 3,
        "max_daily": 6,
        "description": "Ácidos grasos esenciales y vitaminas liposolubles"
    },
    EquivalenceGroup.AZUCARES_SIN_GRASA: {
        "name": "Azúcares sin Grasa",
        "calories": 40,
        "protein": 0.0,
        "carbs": 10.0,
        "fat": 0.0,
        "color": "#FF7675",
        "min_daily": 0,
        "max_daily": 2,
        "description": "Energía rápida, consumo limitado"
    },
    EquivalenceGroup.ALIMENTOS_LIBRES: {
        "name": "Alimentos Libres",
        "calories": 5,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
        "color": "#DDDDD",
        "min_daily": 0,
        "max_daily": 100,
        "description": "Menos de 20 kcal por porción, consumo libre"
    }
}