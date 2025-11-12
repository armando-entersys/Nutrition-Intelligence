"""
Script para importar alimentos SMAE completos a la base de datos
Ejecutar con: python -m scripts.import_smae_complete
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from domain.foods.nom051_models import FoodSMAE
from core.config import get_settings

settings = get_settings()

# Lista completa de alimentos SMAE por grupo
ALIMENTOS_SMAE = [
    # CEREALES SIN GRASA
    {
        "nombre": "Tortilla de maíz",
        "nombre_comun": "Tortilla",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": "30",
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
        "verificado": True
    },
    {
        "nombre": "Arroz cocido",
        "nombre_comun": "Arroz blanco",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": "90",
        "unidad_porcion": "g",
        "peso_neto_g": 90,
        "calorias": 70,
        "proteinas": 2.0,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 0.2,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Pasta cocida",
        "nombre_comun": "Pasta",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": "70",
        "unidad_porcion": "g",
        "peso_neto_g": 70,
        "calorias": 70,
        "proteinas": 2.5,
        "carbohidratos": 15.0,
        "grasas": 0.2,
        "fibra": 0.8,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Pan de caja integral",
        "nombre_comun": "Pan integral",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 69,
        "proteinas": 2.6,
        "carbohidratos": 13.0,
        "grasas": 1.0,
        "fibra": 2.0,
        "sodio_mg": 150,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Avena cruda",
        "nombre_comun": "Avena",
        "grupo_smae": "Cereales",
        "subgrupo": "Sin grasa",
        "porcion": "20",
        "unidad_porcion": "g",
        "peso_neto_g": 20,
        "calorias": 70,
        "proteinas": 2.6,
        "carbohidratos": 12.0,
        "grasas": 1.4,
        "fibra": 2.0,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # CEREALES CON GRASA
    {
        "nombre": "Totopos",
        "nombre_comun": "Totopos/Nachos",
        "grupo_smae": "Cereales",
        "subgrupo": "Con grasa",
        "porcion": "20",
        "unidad_porcion": "g",
        "peso_neto_g": 20,
        "calorias": 115,
        "proteinas": 2.0,
        "carbohidratos": 15.0,
        "grasas": 5.0,
        "fibra": 1.5,
        "sodio_mg": 150,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Pan dulce",
        "nombre_comun": "Concha o pan dulce",
        "grupo_smae": "Cereales",
        "subgrupo": "Con grasa",
        "porcion": "40",
        "unidad_porcion": "g",
        "peso_neto_g": 40,
        "calorias": 115,
        "proteinas": 2.0,
        "carbohidratos": 15.0,
        "grasas": 5.0,
        "fibra": 0.5,
        "sodio_mg": 100,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },

    # FRUTAS
    {
        "nombre": "Manzana con cáscara",
        "nombre_comun": "Manzana",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "120",
        "unidad_porcion": "g",
        "peso_neto_g": 120,
        "calorias": 60,
        "proteinas": 0.0,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 2.4,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Plátano",
        "nombre_comun": "Plátano Tabasco",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "80",
        "unidad_porcion": "g",
        "peso_neto_g": 80,
        "calorias": 60,
        "proteinas": 0.5,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 1.6,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Papaya",
        "nombre_comun": "Papaya",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 60,
        "proteinas": 0.5,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 1.8,
        "sodio_mg": 3,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Sandía",
        "nombre_comun": "Sandía",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "250",
        "unidad_porcion": "g",
        "peso_neto_g": 250,
        "calorias": 60,
        "proteinas": 0.5,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 1.0,
        "sodio_mg": 3,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Mango",
        "nombre_comun": "Mango manila",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "120",
        "unidad_porcion": "g",
        "peso_neto_g": 120,
        "calorias": 60,
        "proteinas": 0.5,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 1.8,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Naranja",
        "nombre_comun": "Naranja",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 60,
        "proteinas": 1.0,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 2.4,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Guayaba",
        "nombre_comun": "Guayaba",
        "grupo_smae": "Frutas",
        "subgrupo": "General",
        "porcion": "110",
        "unidad_porcion": "g",
        "peso_neto_g": 110,
        "calorias": 60,
        "proteinas": 1.0,
        "carbohidratos": 15.0,
        "grasas": 0.0,
        "fibra": 5.5,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },

    # VERDURAS
    {
        "nombre": "Jitomate",
        "nombre_comun": "Jitomate/Tomate rojo",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 25,
        "proteinas": 1.0,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 1.5,
        "sodio_mg": 7,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Cebolla",
        "nombre_comun": "Cebolla blanca",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "70",
        "unidad_porcion": "g",
        "peso_neto_g": 70,
        "calorias": 25,
        "proteinas": 0.7,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 1.4,
        "sodio_mg": 3,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Calabacita",
        "nombre_comun": "Calabacita italiana",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 25,
        "proteinas": 1.5,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 1.5,
        "sodio_mg": 3,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Chayote",
        "nombre_comun": "Chayote",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 25,
        "proteinas": 0.8,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 2.0,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Nopales",
        "nombre_comun": "Nopal",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 25,
        "proteinas": 1.5,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 3.0,
        "sodio_mg": 30,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Espinaca",
        "nombre_comun": "Espinaca",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "150",
        "unidad_porcion": "g",
        "peso_neto_g": 150,
        "calorias": 25,
        "proteinas": 2.5,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 2.5,
        "sodio_mg": 80,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Brócoli",
        "nombre_comun": "Brócoli",
        "grupo_smae": "Verduras",
        "subgrupo": "General",
        "porcion": "100",
        "unidad_porcion": "g",
        "peso_neto_g": 100,
        "calorias": 25,
        "proteinas": 2.5,
        "carbohidratos": 5.0,
        "grasas": 0.0,
        "fibra": 2.4,
        "sodio_mg": 33,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # LEGUMINOSAS
    {
        "nombre": "Frijol negro cocido",
        "nombre_comun": "Frijoles negros",
        "grupo_smae": "Leguminosas",
        "subgrupo": "General",
        "porcion": "80",
        "unidad_porcion": "g",
        "peso_neto_g": 80,
        "calorias": 120,
        "proteinas": 8.0,
        "carbohidratos": 20.0,
        "grasas": 1.0,
        "fibra": 7.5,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Frijol pinto cocido",
        "nombre_comun": "Frijoles pintos",
        "grupo_smae": "Leguminosas",
        "subgrupo": "General",
        "porcion": "80",
        "unidad_porcion": "g",
        "peso_neto_g": 80,
        "calorias": 120,
        "proteinas": 8.0,
        "carbohidratos": 20.0,
        "grasas": 1.0,
        "fibra": 7.0,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Lentejas cocidas",
        "nombre_comun": "Lentejas",
        "grupo_smae": "Leguminosas",
        "subgrupo": "General",
        "porcion": "80",
        "unidad_porcion": "g",
        "peso_neto_g": 80,
        "calorias": 120,
        "proteinas": 9.0,
        "carbohidratos": 20.0,
        "grasas": 0.5,
        "fibra": 8.0,
        "sodio_mg": 2,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Garbanzo cocido",
        "nombre_comun": "Garbanzos",
        "grupo_smae": "Leguminosas",
        "subgrupo": "General",
        "porcion": "80",
        "unidad_porcion": "g",
        "peso_neto_g": 80,
        "calorias": 120,
        "proteinas": 8.0,
        "carbohidratos": 20.0,
        "grasas": 2.0,
        "fibra": 6.0,
        "sodio_mg": 7,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # ALIMENTOS DE ORIGEN ANIMAL - MUY BAJO APORTE DE GRASA
    {
        "nombre": "Pechuga de pollo sin piel",
        "nombre_comun": "Pechuga de pollo",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Muy bajo aporte de grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 40,
        "proteinas": 7.0,
        "carbohidratos": 0.0,
        "grasas": 1.0,
        "fibra": 0.0,
        "sodio_mg": 20,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Pescado blanco",
        "nombre_comun": "Pescado (tilapia, huachinango)",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Muy bajo aporte de grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 40,
        "proteinas": 7.0,
        "carbohidratos": 0.0,
        "grasas": 1.0,
        "fibra": 0.0,
        "sodio_mg": 30,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Clara de huevo",
        "nombre_comun": "Clara de huevo",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Muy bajo aporte de grasa",
        "porcion": "66",
        "unidad_porcion": "g",
        "peso_neto_g": 66,
        "calorias": 40,
        "proteinas": 7.0,
        "carbohidratos": 1.0,
        "grasas": 0.0,
        "fibra": 0.0,
        "sodio_mg": 55,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # ALIMENTOS DE ORIGEN ANIMAL - BAJO APORTE DE GRASA
    {
        "nombre": "Carne de res magra",
        "nombre_comun": "Bistec de res",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Bajo aporte de grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 55,
        "proteinas": 7.0,
        "carbohidratos": 0.0,
        "grasas": 3.0,
        "fibra": 0.0,
        "sodio_mg": 20,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Huevo entero",
        "nombre_comun": "Huevo",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Bajo aporte de grasa",
        "porcion": "50",
        "unidad_porcion": "g",
        "peso_neto_g": 50,
        "calorias": 75,
        "proteinas": 7.0,
        "carbohidratos": 0.5,
        "grasas": 5.0,
        "fibra": 0.0,
        "sodio_mg": 70,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Atún en agua",
        "nombre_comun": "Atún en lata",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Bajo aporte de grasa",
        "porcion": "40",
        "unidad_porcion": "g",
        "peso_neto_g": 40,
        "calorias": 55,
        "proteinas": 7.0,
        "carbohidratos": 0.0,
        "grasas": 3.0,
        "fibra": 0.0,
        "sodio_mg": 200,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # ALIMENTOS DE ORIGEN ANIMAL - MODERADO APORTE DE GRASA
    {
        "nombre": "Carne molida de res",
        "nombre_comun": "Carne molida",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Moderado aporte de grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 75,
        "proteinas": 7.0,
        "carbohidratos": 0.0,
        "grasas": 5.0,
        "fibra": 0.0,
        "sodio_mg": 20,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Queso panela",
        "nombre_comun": "Queso panela",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Moderado aporte de grasa",
        "porcion": "40",
        "unidad_porcion": "g",
        "peso_neto_g": 40,
        "calorias": 75,
        "proteinas": 7.0,
        "carbohidratos": 1.0,
        "grasas": 5.0,
        "fibra": 0.0,
        "sodio_mg": 180,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },

    # ALIMENTOS DE ORIGEN ANIMAL - ALTO APORTE DE GRASA
    {
        "nombre": "Chorizo",
        "nombre_comun": "Chorizo",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Alto aporte de grasa",
        "porcion": "25",
        "unidad_porcion": "g",
        "peso_neto_g": 25,
        "calorias": 100,
        "proteinas": 7.0,
        "carbohidratos": 1.0,
        "grasas": 8.0,
        "fibra": 0.0,
        "sodio_mg": 300,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Queso Oaxaca",
        "nombre_comun": "Quesillo",
        "grupo_smae": "Alimentos de origen animal",
        "subgrupo": "Alto aporte de grasa",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 100,
        "proteinas": 7.0,
        "carbohidratos": 1.0,
        "grasas": 8.0,
        "fibra": 0.0,
        "sodio_mg": 180,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },

    # LECHE - DESCREMADA
    {
        "nombre": "Leche descremada",
        "nombre_comun": "Leche Light",
        "grupo_smae": "Leche",
        "subgrupo": "Descremada",
        "porcion": "240",
        "unidad_porcion": "ml",
        "peso_neto_g": 240,
        "calorias": 95,
        "proteinas": 9.0,
        "carbohidratos": 12.0,
        "grasas": 2.0,
        "fibra": 0.0,
        "sodio_mg": 125,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Yogurt natural light",
        "nombre_comun": "Yogurt bajo en grasa",
        "grupo_smae": "Leche",
        "subgrupo": "Descremada",
        "porcion": "240",
        "unidad_porcion": "ml",
        "peso_neto_g": 240,
        "calorias": 95,
        "proteinas": 9.0,
        "carbohidratos": 12.0,
        "grasas": 2.0,
        "fibra": 0.0,
        "sodio_mg": 150,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # LECHE - SEMIDESCREMADA
    {
        "nombre": "Leche semidescremada",
        "nombre_comun": "Leche reducida en grasa",
        "grupo_smae": "Leche",
        "subgrupo": "Semidescremada",
        "porcion": "240",
        "unidad_porcion": "ml",
        "peso_neto_g": 240,
        "calorias": 110,
        "proteinas": 9.0,
        "carbohidratos": 12.0,
        "grasas": 4.0,
        "fibra": 0.0,
        "sodio_mg": 125,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # LECHE - ENTERA
    {
        "nombre": "Leche entera",
        "nombre_comun": "Leche completa",
        "grupo_smae": "Leche",
        "subgrupo": "Entera",
        "porcion": "240",
        "unidad_porcion": "ml",
        "peso_neto_g": 240,
        "calorias": 150,
        "proteinas": 9.0,
        "carbohidratos": 12.0,
        "grasas": 8.0,
        "fibra": 0.0,
        "sodio_mg": 120,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # ACEITES Y GRASAS - SIN PROTEÍNA
    {
        "nombre": "Aceite vegetal",
        "nombre_comun": "Aceite",
        "grupo_smae": "Aceites y grasas",
        "subgrupo": "Sin proteína",
        "porcion": "5",
        "unidad_porcion": "ml",
        "peso_neto_g": 5,
        "calorias": 45,
        "proteinas": 0.0,
        "carbohidratos": 0.0,
        "grasas": 5.0,
        "fibra": 0.0,
        "sodio_mg": 0,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Aguacate",
        "nombre_comun": "Aguacate",
        "grupo_smae": "Aceites y grasas",
        "subgrupo": "Con proteína",
        "porcion": "30",
        "unidad_porcion": "g",
        "peso_neto_g": 30,
        "calorias": 45,
        "proteinas": 0.5,
        "carbohidratos": 2.5,
        "grasas": 4.5,
        "fibra": 2.0,
        "sodio_mg": 2,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Nuez",
        "nombre_comun": "Nuez",
        "grupo_smae": "Aceites y grasas",
        "subgrupo": "Con proteína",
        "porcion": "10",
        "unidad_porcion": "g",
        "peso_neto_g": 10,
        "calorias": 70,
        "proteinas": 1.5,
        "carbohidratos": 1.5,
        "grasas": 7.0,
        "fibra": 0.7,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Cacahuate",
        "nombre_comun": "Cacahuate/Maní",
        "grupo_smae": "Aceites y grasas",
        "subgrupo": "Con proteína",
        "porcion": "10",
        "unidad_porcion": "g",
        "peso_neto_g": 10,
        "calorias": 60,
        "proteinas": 2.5,
        "carbohidratos": 2.0,
        "grasas": 5.0,
        "fibra": 1.0,
        "sodio_mg": 2,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # AZÚCARES - SIN GRASA
    {
        "nombre": "Azúcar blanca",
        "nombre_comun": "Azúcar",
        "grupo_smae": "Azúcares",
        "subgrupo": "Sin grasa",
        "porcion": "10",
        "unidad_porcion": "g",
        "peso_neto_g": 10,
        "calorias": 40,
        "proteinas": 0.0,
        "carbohidratos": 10.0,
        "grasas": 0.0,
        "fibra": 0.0,
        "sodio_mg": 0,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Miel de abeja",
        "nombre_comun": "Miel",
        "grupo_smae": "Azúcares",
        "subgrupo": "Sin grasa",
        "porcion": "10",
        "unidad_porcion": "g",
        "peso_neto_g": 10,
        "calorias": 40,
        "proteinas": 0.0,
        "carbohidratos": 10.0,
        "grasas": 0.0,
        "fibra": 0.0,
        "sodio_mg": 1,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Mermelada",
        "nombre_comun": "Mermelada",
        "grupo_smae": "Azúcares",
        "subgrupo": "Sin grasa",
        "porcion": "15",
        "unidad_porcion": "g",
        "peso_neto_g": 15,
        "calorias": 40,
        "proteinas": 0.0,
        "carbohidratos": 10.0,
        "grasas": 0.0,
        "fibra": 0.2,
        "sodio_mg": 5,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },

    # AZÚCARES - CON GRASA
    {
        "nombre": "Chocolate",
        "nombre_comun": "Chocolate con leche",
        "grupo_smae": "Azúcares",
        "subgrupo": "Con grasa",
        "porcion": "10",
        "unidad_porcion": "g",
        "peso_neto_g": 10,
        "calorias": 60,
        "proteinas": 1.0,
        "carbohidratos": 6.0,
        "grasas": 3.5,
        "fibra": 0.5,
        "sodio_mg": 15,
        "es_mexicano": False,
        "fuente": "smae",
        "verificado": True
    },
    {
        "nombre": "Cajeta",
        "nombre_comun": "Cajeta",
        "grupo_smae": "Azúcares",
        "subgrupo": "Con grasa",
        "porcion": "15",
        "unidad_porcion": "g",
        "peso_neto_g": 15,
        "calorias": 60,
        "proteinas": 1.0,
        "carbohidratos": 11.0,
        "grasas": 1.5,
        "fibra": 0.0,
        "sodio_mg": 35,
        "es_mexicano": True,
        "fuente": "smae",
        "verificado": True
    },
]


async def import_alimentos():
    """Importa los alimentos SMAE a la base de datos"""
    # Create async engine
    engine = create_async_engine(
        settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False
    )

    # Create session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    imported = 0
    skipped = 0
    errors = 0

    async with async_session() as session:
        for alimento_data in ALIMENTOS_SMAE:
            try:
                # Check if already exists
                result = await session.execute(
                    select(FoodSMAE).where(
                        FoodSMAE.nombre == alimento_data["nombre"]
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    print(f"⏭️  Skipping {alimento_data['nombre']} (already exists)")
                    skipped += 1
                    continue

                # Create new alimento
                alimento = FoodSMAE(**alimento_data)
                session.add(alimento)
                await session.commit()

                print(f"✅ Imported {alimento_data['nombre']}")
                imported += 1

            except Exception as e:
                print(f"❌ Error importing {alimento_data['nombre']}: {str(e)}")
                errors += 1
                await session.rollback()

    await engine.dispose()

    print(f"\n{'='*60}")
    print(f"📊 Import Summary")
    print(f"{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {errors}")
    print(f"📦 Total:    {len(ALIMENTOS_SMAE)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("🚀 Starting SMAE foods import...")
    print(f"📦 Foods to import: {len(ALIMENTOS_SMAE)}\n")
    asyncio.run(import_alimentos())
