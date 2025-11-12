"""
Script para importar productos NOM-051 a la base de datos
Ejecutar con: python -m scripts.import_products_batch
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from domain.foods.nom051_models import ProductoNOM051
from core.config import settings

# Lista de productos NOM-051 populares en México
PRODUCTOS_NOM051 = [
    # BEBIDAS AZUCARADAS
    {
        "codigo_barras": "7501055300891",
        "nombre": "Coca-Cola Original",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 42,
        "proteinas": 0.0,
        "carbohidratos": 10.6,
        "azucares": 10.6,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 11,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": True,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055362578",
        "nombre": "Coca-Cola Sin Azúcar",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 0,
        "proteinas": 0.0,
        "carbohidratos": 0.0,
        "azucares": 0.0,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 15,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": True,
        "contiene_edulcorantes": True,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055301294",
        "nombre": "Sprite",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 40,
        "proteinas": 0.0,
        "carbohidratos": 10.0,
        "azucares": 10.0,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 14,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055303274",
        "nombre": "Fanta Naranja",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 47,
        "proteinas": 0.0,
        "carbohidratos": 11.8,
        "azucares": 11.8,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 12,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055308859",
        "nombre": "Del Valle Manzana",
        "marca": "Coca-Cola",
        "porcion_gramos": 100,
        "calorias": 45,
        "proteinas": 0.0,
        "carbohidratos": 11.0,
        "azucares": 10.5,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 8,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # BOTANAS Y SNACKS
    {
        "codigo_barras": "7501055309122",
        "nombre": "Sabritas Clásicas",
        "marca": "Sabritas",
        "porcion_gramos": 100,
        "calorias": 536,
        "proteinas": 6.3,
        "carbohidratos": 52.0,
        "azucares": 2.0,
        "grasas_totales": 33.0,
        "grasas_saturadas": 11.0,
        "grasas_trans": 0.0,
        "fibra": 4.5,
        "sodio_mg": 480,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055309887",
        "nombre": "Cheetos Poffs",
        "marca": "Sabritas",
        "porcion_gramos": 100,
        "calorias": 571,
        "proteinas": 5.7,
        "carbohidratos": 50.0,
        "azucares": 5.7,
        "grasas_totales": 37.1,
        "grasas_saturadas": 10.0,
        "grasas_trans": 0.0,
        "fibra": 2.9,
        "sodio_mg": 857,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055310050",
        "nombre": "Doritos Nacho",
        "marca": "Sabritas",
        "porcion_gramos": 100,
        "calorias": 500,
        "proteinas": 7.1,
        "carbohidratos": 60.7,
        "azucares": 3.6,
        "grasas_totales": 25.0,
        "grasas_saturadas": 3.6,
        "grasas_trans": 0.0,
        "fibra": 3.6,
        "sodio_mg": 536,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055310548",
        "nombre": "Ruffles Queso",
        "marca": "Sabritas",
        "porcion_gramos": 100,
        "calorias": 536,
        "proteinas": 6.3,
        "carbohidratos": 52.0,
        "azucares": 3.0,
        "grasas_totales": 33.0,
        "grasas_saturadas": 11.0,
        "grasas_trans": 0.0,
        "fibra": 4.0,
        "sodio_mg": 520,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # CEREALES Y BARRAS
    {
        "codigo_barras": "7501055311248",
        "nombre": "Zucaritas",
        "marca": "Kellogg's",
        "porcion_gramos": 100,
        "calorias": 380,
        "proteinas": 5.0,
        "carbohidratos": 85.0,
        "azucares": 35.0,
        "grasas_totales": 1.0,
        "grasas_saturadas": 0.5,
        "grasas_trans": 0.0,
        "fibra": 2.0,
        "sodio_mg": 200,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055312245",
        "nombre": "Choco Krispis",
        "marca": "Kellogg's",
        "porcion_gramos": 100,
        "calorias": 387,
        "proteinas": 5.0,
        "carbohidratos": 83.0,
        "azucares": 37.0,
        "grasas_totales": 3.0,
        "grasas_saturadas": 1.5,
        "grasas_trans": 0.0,
        "fibra": 3.0,
        "sodio_mg": 333,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055313242",
        "nombre": "Corn Flakes",
        "marca": "Kellogg's",
        "porcion_gramos": 100,
        "calorias": 357,
        "proteinas": 7.1,
        "carbohidratos": 84.3,
        "azucares": 7.1,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 2.9,
        "sodio_mg": 643,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # LÁCTEOS
    {
        "codigo_barras": "7501055314249",
        "nombre": "Yoghurt Griego Natural Alpura",
        "marca": "Alpura",
        "porcion_gramos": 100,
        "calorias": 97,
        "proteinas": 10.0,
        "carbohidratos": 3.6,
        "azucares": 3.6,
        "grasas_totales": 5.0,
        "grasas_saturadas": 3.2,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 46,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055315246",
        "nombre": "Yoghurt Griego Fresa Danone",
        "marca": "Danone",
        "porcion_gramos": 100,
        "calorias": 124,
        "proteinas": 6.9,
        "carbohidratos": 16.9,
        "azucares": 13.8,
        "grasas_totales": 2.6,
        "grasas_saturadas": 1.7,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 43,
        "exceso_calorias": False,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # GALLETAS Y DULCES
    {
        "codigo_barras": "7501055316243",
        "nombre": "Oreo",
        "marca": "Nabisco",
        "porcion_gramos": 100,
        "calorias": 480,
        "proteinas": 5.0,
        "carbohidratos": 70.0,
        "azucares": 40.0,
        "grasas_totales": 20.0,
        "grasas_saturadas": 6.0,
        "grasas_trans": 0.0,
        "fibra": 3.0,
        "sodio_mg": 380,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055317240",
        "nombre": "Príncipe",
        "marca": "Marinela",
        "porcion_gramos": 100,
        "calorias": 464,
        "proteinas": 5.4,
        "carbohidratos": 67.9,
        "azucares": 33.9,
        "grasas_totales": 17.9,
        "grasas_saturadas": 8.9,
        "grasas_trans": 0.0,
        "fibra": 1.8,
        "sodio_mg": 321,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055318247",
        "nombre": "Gansito",
        "marca": "Marinela",
        "porcion_gramos": 100,
        "calorias": 416,
        "proteinas": 4.9,
        "carbohidratos": 58.4,
        "azucares": 36.8,
        "grasas_totales": 17.9,
        "grasas_saturadas": 8.4,
        "grasas_trans": 0.0,
        "fibra": 1.1,
        "sodio_mg": 158,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055319244",
        "nombre": "Submarinos",
        "marca": "Marinela",
        "porcion_gramos": 100,
        "calorias": 446,
        "proteinas": 6.0,
        "carbohidratos": 64.0,
        "azucares": 32.0,
        "grasas_totales": 18.0,
        "grasas_saturadas": 9.0,
        "grasas_trans": 0.0,
        "fibra": 2.0,
        "sodio_mg": 280,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # CHOCOLATE Y DULCERÍA
    {
        "codigo_barras": "7501055320241",
        "nombre": "Carlos V",
        "marca": "Nestlé",
        "porcion_gramos": 100,
        "calorias": 534,
        "proteinas": 7.7,
        "carbohidratos": 57.7,
        "azucares": 50.0,
        "grasas_totales": 30.8,
        "grasas_saturadas": 15.4,
        "grasas_trans": 0.0,
        "fibra": 3.8,
        "sodio_mg": 115,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": True,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055321248",
        "nombre": "KitKat",
        "marca": "Nestlé",
        "porcion_gramos": 100,
        "calorias": 518,
        "proteinas": 6.5,
        "carbohidratos": 64.5,
        "azucares": 48.4,
        "grasas_totales": 25.8,
        "grasas_saturadas": 16.1,
        "grasas_trans": 0.0,
        "fibra": 1.6,
        "sodio_mg": 97,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": True,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055322245",
        "nombre": "Milky Way",
        "marca": "Mars",
        "porcion_gramos": 100,
        "calorias": 456,
        "proteinas": 4.4,
        "carbohidratos": 70.2,
        "azucares": 56.1,
        "grasas_totales": 17.5,
        "grasas_saturadas": 10.5,
        "grasas_trans": 0.0,
        "fibra": 0.9,
        "sodio_mg": 175,
        "exceso_calorias": True,
        "exceso_azucares": True,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # COMIDA INSTANTÁNEA
    {
        "codigo_barras": "7501055323242",
        "nombre": "Maruchan Pollo",
        "marca": "Maruchan",
        "porcion_gramos": 100,
        "calorias": 448,
        "proteinas": 9.0,
        "carbohidratos": 60.0,
        "azucares": 2.0,
        "grasas_totales": 20.0,
        "grasas_saturadas": 10.0,
        "grasas_trans": 0.0,
        "fibra": 2.0,
        "sodio_mg": 1800,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055324249",
        "nombre": "Nissin Cup Noodles Camarón",
        "marca": "Nissin",
        "porcion_gramos": 100,
        "calorias": 460,
        "proteinas": 9.5,
        "carbohidratos": 58.0,
        "azucares": 2.5,
        "grasas_totales": 21.0,
        "grasas_saturadas": 10.5,
        "grasas_trans": 0.0,
        "fibra": 2.5,
        "sodio_mg": 1950,
        "exceso_calorias": True,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": True,
        "exceso_grasas_trans": False,
        "exceso_sodio": True,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },

    # PRODUCTOS SALUDABLES (SIN SELLOS)
    {
        "codigo_barras": "7501055325246",
        "nombre": "Agua Natural Bonafont",
        "marca": "Bonafont",
        "porcion_gramos": 100,
        "calorias": 0,
        "proteinas": 0.0,
        "carbohidratos": 0.0,
        "azucares": 0.0,
        "grasas_totales": 0.0,
        "grasas_saturadas": 0.0,
        "grasas_trans": 0.0,
        "fibra": 0.0,
        "sodio_mg": 0,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055326243",
        "nombre": "Almendras Natural Sin Sal",
        "marca": "Great Value",
        "porcion_gramos": 100,
        "calorias": 607,
        "proteinas": 21.4,
        "carbohidratos": 21.4,
        "azucares": 3.6,
        "grasas_totales": 50.0,
        "grasas_saturadas": 3.6,
        "grasas_trans": 0.0,
        "fibra": 10.7,
        "sodio_mg": 0,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
    {
        "codigo_barras": "7501055327240",
        "nombre": "Avena Natural Quaker",
        "marca": "Quaker",
        "porcion_gramos": 100,
        "calorias": 379,
        "proteinas": 13.7,
        "carbohidratos": 67.7,
        "azucares": 1.0,
        "grasas_totales": 6.5,
        "grasas_saturadas": 1.1,
        "grasas_trans": 0.0,
        "fibra": 10.1,
        "sodio_mg": 6,
        "exceso_calorias": False,
        "exceso_azucares": False,
        "exceso_grasas_saturadas": False,
        "exceso_grasas_trans": False,
        "exceso_sodio": False,
        "contiene_cafeina": False,
        "contiene_edulcorantes": False,
        "verified": True,
        "is_global": True,
        "scan_count": 1
    },
]


async def import_productos():
    """Importa los productos NOM-051 a la base de datos"""
    # Create async engine
    engine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+asyncpg://"),
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
        for producto_data in PRODUCTOS_NOM051:
            try:
                # Check if already exists by barcode
                result = await session.execute(
                    select(ProductoNOM051).where(
                        ProductoNOM051.codigo_barras == producto_data["codigo_barras"]
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    print(f"⏭️  Skipping {producto_data['nombre']} (already exists)")
                    skipped += 1
                    continue

                # Create new producto
                producto = ProductoNOM051(**producto_data)
                session.add(producto)
                await session.commit()

                # Count warning seals
                sellos = sum([
                    producto_data.get('exceso_calorias', False),
                    producto_data.get('exceso_azucares', False),
                    producto_data.get('exceso_grasas_saturadas', False),
                    producto_data.get('exceso_grasas_trans', False),
                    producto_data.get('exceso_sodio', False),
                ])
                sello_emoji = "⚠️ " * sellos if sellos > 0 else "✅"

                print(f"{sello_emoji} Imported {producto_data['nombre']} ({sellos} sellos)")
                imported += 1

            except Exception as e:
                print(f"❌ Error importing {producto_data['nombre']}: {str(e)}")
                errors += 1
                await session.rollback()

    await engine.dispose()

    print(f"\n{'='*60}")
    print(f"📊 Import Summary")
    print(f"{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {errors}")
    print(f"📦 Total:    {len(PRODUCTOS_NOM051)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("🚀 Starting NOM-051 products import...")
    print(f"📦 Products to import: {len(PRODUCTOS_NOM051)}\n")
    asyncio.run(import_productos())
