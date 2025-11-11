"""
NOM-051 Product Models
======================

SQLModel models for NOM-051 products (Mexican food labeling standard)
and SMAE (Sistema Mexicano de Alimentos Equivalentes) foods.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class ProductoNOM051(SQLModel, table=True):
    """
    Producto NOM-051

    Modelo para productos con etiquetado según la norma mexicana NOM-051.
    Incluye información nutricional y sellos de advertencia.
    """
    __tablename__ = "productos_nom051"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic info
    user_id: Optional[int] = Field(default=None, foreign_key="auth_users.id")
    codigo_barras: Optional[str] = Field(default=None, max_length=50, unique=True, index=True)
    nombre: str = Field(max_length=255, index=True)
    marca: Optional[str] = Field(default=None, max_length=255)

    # Nutritional information (per serving)
    porcion_gramos: float = Field(description="Serving size in grams")
    calorias: float = Field(description="Calories per serving")
    proteinas: float = Field(description="Protein in grams")
    carbohidratos: float = Field(description="Carbohydrates in grams")
    azucares: float = Field(description="Sugars in grams")
    grasas_totales: float = Field(description="Total fat in grams")
    grasas_saturadas: float = Field(description="Saturated fat in grams")
    grasas_trans: float = Field(description="Trans fat in grams")
    fibra: float = Field(description="Fiber in grams")
    sodio: float = Field(description="Sodium in milligrams")

    # NOM-051 warning seals
    exceso_calorias: bool = Field(default=False, description="Excess calories seal")
    exceso_azucares: bool = Field(default=False, description="Excess sugar seal")
    exceso_grasas_saturadas: bool = Field(default=False, description="Excess saturated fat seal")
    exceso_grasas_trans: bool = Field(default=False, description="Excess trans fat seal")
    exceso_sodio: bool = Field(default=False, description="Excess sodium seal")
    contiene_edulcorantes: bool = Field(default=False, description="Contains sweeteners")
    contiene_cafeina: bool = Field(default=False, description="Contains caffeine")

    # Additional information
    imagen_url: Optional[str] = Field(default=None, description="Product image URL")
    ingredientes: Optional[str] = Field(default=None, description="Ingredients list")
    categoria: Optional[str] = Field(default=None, max_length=100)
    fuente: str = Field(max_length=50, description="Data source: openfoodfacts, manual, vision_ai")

    # Global products system fields
    image_hash: Optional[str] = Field(default=None, max_length=64, index=True, description="SHA-256 hash of product image")
    created_by_user_id: Optional[int] = Field(default=None, foreign_key="auth_users.id", index=True)
    scan_count: int = Field(default=1, description="Number of times this product has been scanned")
    verified: bool = Field(default=False, index=True, description="Product data has been verified")
    verified_by_user_id: Optional[int] = Field(default=None, foreign_key="auth_users.id")
    verified_at: Optional[datetime] = Field(default=None)
    is_global: bool = Field(default=True, index=True, description="Product is available globally to all users")
    confidence_score: Optional[float] = Field(default=None, description="AI confidence score (0-1)")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Coca-Cola Original",
                "marca": "Coca-Cola",
                "codigo_barras": "7501055300891",
                "porcion_gramos": 100,
                "calorias": 42,
                "azucares": 10.6,
                "exceso_azucares": True,
                "exceso_calorias": False,
                "fuente": "openfoodfacts"
            }
        }


class FoodSMAE(SQLModel, table=True):
    """
    Alimento SMAE

    Modelo para alimentos del Sistema Mexicano de Alimentos Equivalentes.
    Usado para crear planes de alimentación con equivalencias.
    """
    __tablename__ = "alimentos_smae"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic info
    nombre: str = Field(max_length=255, index=True, description="Food name in Spanish")
    nombre_comun: Optional[str] = Field(default=None, max_length=255, description="Common name")
    grupo_smae: str = Field(max_length=100, index=True, description="SMAE food group")
    subgrupo: Optional[str] = Field(default=None, max_length=100)

    # Portion/serving info
    porcion: float = Field(description="Serving size")
    unidad_porcion: str = Field(max_length=50, description="Serving unit: g, ml, pza, taza, etc.")
    peso_neto_g: Optional[float] = Field(default=None, description="Net weight in grams")

    # Macronutrients (per serving)
    calorias: float = Field(description="Calories per serving")
    proteinas: float = Field(description="Protein in grams")
    carbohidratos: float = Field(description="Carbohydrates in grams")
    grasas: float = Field(description="Total fat in grams")
    fibra: Optional[float] = Field(default=None, description="Fiber in grams")

    # Micronutrients (optional)
    sodio_mg: Optional[float] = Field(default=None, description="Sodium in milligrams")
    calcio_mg: Optional[float] = Field(default=None, description="Calcium in milligrams")
    hierro_mg: Optional[float] = Field(default=None, description="Iron in milligrams")

    # SMAE equivalencies
    equivalente_cereales: Optional[float] = Field(default=None)
    equivalente_leguminosas: Optional[float] = Field(default=None)
    equivalente_verduras: Optional[float] = Field(default=None)
    equivalente_frutas: Optional[float] = Field(default=None)
    equivalente_aoa: Optional[float] = Field(default=None, description="Alimentos de Origen Animal")
    equivalente_leche: Optional[float] = Field(default=None)
    equivalente_grasas: Optional[float] = Field(default=None)
    equivalente_azucares: Optional[float] = Field(default=None)

    # Additional info
    descripcion: Optional[str] = Field(default=None, description="Food description")
    preparacion: Optional[str] = Field(default=None, description="Preparation method")
    es_mexicano: bool = Field(default=True, description="Traditional Mexican food")
    temporada: Optional[str] = Field(default=None, max_length=50, description="Seasonal availability")

    # Source tracking
    fuente: str = Field(default="smae", max_length=50, description="Data source")
    verificado: bool = Field(default=False, description="Data has been verified by nutritionist")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Tortilla de maíz",
                "grupo_smae": "Cereales",
                "porcion": 30,
                "unidad_porcion": "g",
                "calorias": 64,
                "proteinas": 1.7,
                "carbohidratos": 13.4,
                "grasas": 0.9,
                "es_mexicano": True
            }
        }
