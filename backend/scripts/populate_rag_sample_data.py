"""
Populate RAG System with Sample Data
====================================

Agrega datos de ejemplo para probar el sistema RAG:
- Productos NOM-051
- Alimentos SMAE
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from domain.foods.nom051_models import ProductoNOM051, FoodSMAE
from core.config import get_settings


# Datos de ejemplo de alimentos SMAE
SAMPLE_FOODS_SMAE = [
    {
        "nombre": "Tortilla de maíz",
        "nombre_comun": "Tortilla",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": 30,
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 64,
        "proteinas": 1.7,
        "carbohidratos": 13.4,
        "grasas": 0.9,
        "fibra": 1.5,
        "sodio_mg": 3,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Frijoles negros cocidos",
        "nombre_comun": "Frijoles",
        "grupo_smae": "Leguminosas",
        "porcion": 120,
        "unidad_porcion": "g",
        "peso_neto_g": 120,
        "calorias": 120,
        "proteinas": 8,
        "carbohidratos": 20,
        "grasas": 0.5,
        "fibra": 7.5,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Aguacate Hass",
        "nombre_comun": "Aguacate",
        "grupo_smae": "Grasas",
        "subgrupo": "Sin proteína",
        "porcion": 30,
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 45,
        "proteinas": 0.6,
        "carbohidratos": 2.4,
        "grasas": 4.5,
        "fibra": 2,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Pollo pechuga sin piel",
        "nombre_comun": "Pechuga de pollo",
        "grupo_smae": "Alimentos de Origen Animal",
        "subgrupo": "Muy bajo aporte de grasa",
        "porcion": 30,
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 42,
        "proteinas": 7.5,
        "carbohidratos": 0,
        "grasas": 1.5,
        "sodio_mg": 25,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Leche descremada",
        "grupo_smae": "Leche",
        "subgrupo": "Descremada",
        "porcion": 240,
        "unidad_porcion": "ml",
        "peso_neto_g": 240,
        "calorias": 95,
        "proteinas": 9,
        "carbohidratos": 12,
        "grasas": 2,
        "calcio_mg": 300,
        "sodio_mg": 130,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Nopal cocido",
        "grupo_smae": "Verduras",
        "porcion": 150,
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 23,
        "proteinas": 1.5,
        "carbohidratos": 4,
        "grasas": 0.1,
        "fibra": 2.5,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Mango manila",
        "nombre_comun": "Mango",
        "grupo_smae": "Frutas",
        "porcion": 120,
        "unidad_porcion": "g",
        "peso_neto_g": 120,
        "calorias": 60,
        "proteinas": 0.5,
        "carbohidratos": 15,
        "grasas": 0.2,
        "fibra": 1.6,
        "sodio_mg": 1,
        "es_mexicano": True,
        "temporada": "Marzo-Julio",
        "fuente": "smae",
        "verificado": True,
    },
    {
        "nombre": "Chícharos cocidos",
        "nombre_comun": "Chícharos",
        "grupo_smae": "Leguminosas",
        "porcion": 90,
        "unidad_porcion": "g",
        "peso_neto_g": 90,
        "calorias": 120,
        "proteinas": 8,
        "carbohidratos": 20,
        "grasas": 0.5,
        "fibra": 6,
        "sodio_mg": 4,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True,
    },
]

# Datos de ejemplo de productos NOM-051
SAMPLE_PRODUCTS_NOM051 = [
    {
        "codigo_barras": "7501055300891",
        "nombre": "Coca-Cola Original",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 42,
        "proteinas": 0,
        "carbohidratos": 10.6,
        "azucares": 10.6,
        "grasas_totales": 0,
        "grasas_saturadas": 0,
        "grasas_trans": 0,
        "fibra": 0,
        "sodio": 11,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "categoria": "Bebidas",
        "fuente": "manual",
        "scan_count": 1,
        "verified": True,
        "is_global": True,
    },
    {
        "codigo_barras": "7501000111111",
        "nombre": "Sabritas Original",
        "marca": "Sabritas",
        "porcion_gramos": 30,
        "calorias": 150,
        "proteinas": 2,
        "carbohidratos": 15,
        "azucares": 1,
        "grasas_totales": 10,
        "grasas_saturadas": 1.5,
        "grasas_trans": 0,
        "fibra": 1,
        "sodio": 180,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "categoria": "Botanas",
        "fuente": "manual",
        "scan_count": 1,
        "verified": True,
        "is_global": True,
    },
    {
        "codigo_barras": "7501234567890",
        "nombre": "Yogurt Griego Natural",
        "marca": "Alpura",
        "porcion_gramos": 100,
        "calorias": 97,
        "proteinas": 10,
        "carbohidratos": 3.6,
        "azucares": 3.6,
        "grasas_totales": 5,
        "grasas_saturadas": 3,
        "grasas_trans": 0,
        "fibra": 0,
        "sodio": 44,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "categoria": "Lácteos",
        "fuente": "manual",
        "scan_count": 1,
        "verified": True,
        "is_global": True,
    },
]


async def populate_foods_smae(session: AsyncSession):
    """Poblar tabla alimentos_smae"""
    print("\n📦 Poblando alimentos SMAE...")

    for food_data in SAMPLE_FOODS_SMAE:
        food = FoodSMAE(**food_data)
        session.add(food)

    await session.commit()
    print(f"✅ {len(SAMPLE_FOODS_SMAE)} alimentos SMAE agregados")


async def populate_products_nom051(session: AsyncSession):
    """Poblar tabla productos_nom051"""
    print("\n📦 Poblando productos NOM-051...")

    for product_data in SAMPLE_PRODUCTS_NOM051:
        product = ProductoNOM051(**product_data)
        session.add(product)

    await session.commit()
    print(f"✅ {len(SAMPLE_PRODUCTS_NOM051)} productos NOM-051 agregados")


async def main():
    """Main function"""
    settings = get_settings()

    print("=" * 60)
    print("🚀 Población de Datos del Sistema RAG")
    print("=" * 60)
    print(f"\n📍 Database: {settings.database_url}")

    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=False,
    )

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Poblar alimentos SMAE
        await populate_foods_smae(session)

        # Poblar productos NOM-051
        await populate_products_nom051(session)

    # Close engine
    await engine.dispose()

    print("\n" + "=" * 60)
    print("✨ Población completada!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
