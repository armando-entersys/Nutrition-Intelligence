"""
NOM-051 Scanner API Router
Provides barcode scanning and product lookup with NOM-051 seals
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from decimal import Decimal
import logging
from datetime import datetime

from core.database import get_db
from core.auth import get_current_user
from services.openfoodfacts.client import openfoodfacts_client
from services.nom051.calculator import nom051_calculator

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic models
class ProductResponse(BaseModel):
    """Product information with NOM-051 seals"""
    codigo_barras: str
    nombre: str
    marca: Optional[str] = None

    # Nutritional info
    porcion_gramos: float
    calorias: float
    proteinas: float
    carbohidratos: float
    azucares: float
    grasas_totales: float
    grasas_saturadas: float
    grasas_trans: float
    fibra: float
    sodio: float  # in mg

    # NOM-051 seals
    exceso_calorias: bool
    exceso_azucares: bool
    exceso_grasas_saturadas: bool
    exceso_grasas_trans: bool
    exceso_sodio: bool
    contiene_edulcorantes: bool
    contiene_cafeina: bool

    # Additional info
    imagen_url: Optional[str] = None
    ingredientes: Optional[str] = None
    categoria: Optional[str] = None
    fuente: str  # 'local', 'open_food_facts', 'ai_vision'

    # Health score
    health_score: int
    health_level: str
    health_color: str


class ScanHistoryEntry(BaseModel):
    """Scan history entry"""
    codigo_barras: str
    encontrado: bool
    fuente: Optional[str] = None
    fecha_escaneo: datetime


@router.get("/barcode/{barcode}", response_model=ProductResponse)
async def scan_barcode(
    barcode: str,
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Scan a barcode and get product information with NOM-051 seals

    Search strategy:
    1. Check local database (fastest)
    2. Query Open Food Facts API
    3. Calculate NOM-051 seals
    4. Save to local database for future lookups
    5. Record scan in history

    Args:
        barcode: Product barcode (EAN-13, UPC-A, etc.)
        user: Current authenticated user
        db: Database connection

    Returns:
        ProductResponse with complete product information and NOM-051 seals
    """
    try:
        start_time = datetime.now()

        # Clean barcode
        barcode_clean = barcode.strip().replace(" ", "").replace("-", "")

        logger.info(f"Scanning barcode {barcode_clean} for user {user.get('user_id')}")

        # Step 1: Check local database first
        result = await _search_local_db(barcode_clean, db)
        if result:
            logger.info(f"Product found in local database: {result['nombre']}")
            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Record scan
            await _record_scan(
                user_id=user.get('user_id'),
                barcode=barcode_clean,
                product_id=result.get('id'),
                found=True,
                source='cache_local',
                response_time_ms=int(response_time),
                db=db
            )

            return JSONResponse(content=result, status_code=status.HTTP_200_OK)

        # Step 2: Query Open Food Facts
        logger.info(f"Product not in local DB, querying Open Food Facts...")
        off_product = openfoodfacts_client.get_product_by_barcode(barcode_clean)

        if off_product:
            logger.info(f"Product found in Open Food Facts: {off_product.product_name}")

            # Extract nutrition data
            nutrition = off_product.nutrition

            # Determine if product is liquid
            is_liquid = _is_liquid_product(off_product.categories or "")

            # Calculate NOM-051 seals
            seals = nom051_calculator.calculate_seals(
                calorias=nutrition.calories or 0,
                azucares=nutrition.sugars or 0,
                grasas_saturadas=nutrition.saturated_fat or 0,
                grasas_trans=nutrition.trans_fat or 0,
                sodio=nutrition.sodium or 0,
                is_liquid=is_liquid,
                contiene_edulcorantes=False,  # TODO: detect from ingredients
                contiene_cafeina=_contains_caffeine(off_product.ingredients_text or "")
            )

            # Calculate health score
            health_score, health_level, health_color = nom051_calculator.get_health_score(seals)

            # Build response
            product_data = {
                "codigo_barras": barcode_clean,
                "nombre": off_product.product_name,
                "marca": off_product.brands,
                "porcion_gramos": 100.0,  # OFF normalizes to 100g
                "calorias": nutrition.calories or 0,
                "proteinas": nutrition.proteins or 0,
                "carbohidratos": nutrition.carbohydrates or 0,
                "azucares": nutrition.sugars or 0,
                "grasas_totales": nutrition.fat or 0,
                "grasas_saturadas": nutrition.saturated_fat or 0,
                "grasas_trans": nutrition.trans_fat or 0,
                "fibra": nutrition.fiber or 0,
                "sodio": nutrition.sodium or 0,
                **seals.to_dict(),
                "imagen_url": off_product.image_url,
                "ingredientes": off_product.ingredients_text,
                "categoria": _map_category(off_product.categories or ""),
                "fuente": "open_food_facts",
                "health_score": health_score,
                "health_level": health_level,
                "health_color": health_color
            }

            # Step 3: Save to local database
            product_id = await _save_to_local_db(product_data, user.get('user_id'), db)

            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Record scan
            await _record_scan(
                user_id=user.get('user_id'),
                barcode=barcode_clean,
                product_id=product_id,
                found=True,
                source='open_food_facts',
                response_time_ms=int(response_time),
                db=db
            )

            return JSONResponse(content=product_data, status_code=status.HTTP_200_OK)

        # Product not found anywhere
        logger.warning(f"Product not found: {barcode_clean}")

        response_time = (datetime.now() - start_time).total_seconds() * 1000

        # Record failed scan
        await _record_scan(
            user_id=user.get('user_id'),
            barcode=barcode_clean,
            product_id=None,
            found=False,
            source=None,
            response_time_ms=int(response_time),
            db=db
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con código de barras {barcode_clean} no encontrado"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scanning barcode {barcode}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al escanear código de barras: {str(e)}"
        )


@router.get("/history", response_model=List[ScanHistoryEntry])
async def get_scan_history(
    limit: int = 20,
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get user's scan history

    Args:
        limit: Maximum number of results (default 20)
        user: Current authenticated user
        db: Database connection

    Returns:
        List of recent scans
    """
    try:
        user_id = user.get('user_id')

        query = """
            SELECT
                codigo_barras,
                encontrado,
                fuente,
                fecha_escaneo
            FROM escaneos_historia
            WHERE usuario_id = $1
            ORDER BY fecha_escaneo DESC
            LIMIT $2
        """

        rows = await db.fetch(query, user_id, limit)

        history = [
            {
                "codigo_barras": row['codigo_barras'],
                "encontrado": row['encontrado'],
                "fuente": row['fuente'],
                "fecha_escaneo": row['fecha_escaneo'].isoformat()
            }
            for row in rows
        ]

        return JSONResponse(content=history, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fetching scan history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial de escaneos: {str(e)}"
        )


@router.get("/stats")
async def get_scan_stats(
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get scanning statistics for current user

    Returns:
        Statistics about scans (total, found rate, etc.)
    """
    try:
        user_id = user.get('user_id')

        query = """
            SELECT
                COUNT(*) as total_scans,
                SUM(CASE WHEN encontrado THEN 1 ELSE 0 END) as found_count,
                AVG(tiempo_respuesta_ms) as avg_response_time,
                COUNT(DISTINCT codigo_barras) as unique_products
            FROM escaneos_historia
            WHERE usuario_id = $1
        """

        row = await db.fetchrow(query, user_id)

        total = row['total_scans'] or 0
        found = row['found_count'] or 0

        stats = {
            "total_scans": total,
            "found_count": found,
            "not_found_count": total - found,
            "found_rate": round((found / total * 100) if total > 0 else 0, 1),
            "avg_response_time_ms": round(row['avg_response_time'] or 0, 0),
            "unique_products": row['unique_products'] or 0
        }

        return JSONResponse(content=stats, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fetching scan stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


# Helper functions

async def _search_local_db(barcode: str, db) -> Optional[Dict[str, Any]]:
    """Search product in local database"""
    try:
        query = """
            SELECT
                id,
                codigo_barras,
                nombre,
                marca,
                porcion_gramos,
                calorias,
                proteinas,
                carbohidratos,
                azucares,
                grasas_totales,
                grasas_saturadas,
                grasas_trans,
                fibra,
                sodio,
                exceso_calorias,
                exceso_azucares,
                exceso_grasas_saturadas,
                exceso_grasas_trans,
                exceso_sodio,
                contiene_edulcorantes,
                contiene_cafeina,
                imagen_url,
                ingredientes,
                categoria,
                fuente
            FROM productos_nom051
            WHERE codigo_barras = $1
            LIMIT 1
        """

        row = await db.fetchrow(query, barcode)

        if not row:
            return None

        # Calculate health score
        from services.nom051.calculator import NOM051Seals
        seals = NOM051Seals(
            exceso_calorias=row['exceso_calorias'],
            exceso_azucares=row['exceso_azucares'],
            exceso_grasas_saturadas=row['exceso_grasas_saturadas'],
            exceso_grasas_trans=row['exceso_grasas_trans'],
            exceso_sodio=row['exceso_sodio'],
            contiene_edulcorantes=row['contiene_edulcorantes'],
            contiene_cafeina=row['contiene_cafeina']
        )
        health_score, health_level, health_color = nom051_calculator.get_health_score(seals)

        return {
            "id": row['id'],
            "codigo_barras": row['codigo_barras'],
            "nombre": row['nombre'],
            "marca": row['marca'],
            "porcion_gramos": float(row['porcion_gramos']) if row['porcion_gramos'] else 100.0,
            "calorias": float(row['calorias']) if row['calorias'] else 0,
            "proteinas": float(row['proteinas']) if row['proteinas'] else 0,
            "carbohidratos": float(row['carbohidratos']) if row['carbohidratos'] else 0,
            "azucares": float(row['azucares']) if row['azucares'] else 0,
            "grasas_totales": float(row['grasas_totales']) if row['grasas_totales'] else 0,
            "grasas_saturadas": float(row['grasas_saturadas']) if row['grasas_saturadas'] else 0,
            "grasas_trans": float(row['grasas_trans']) if row['grasas_trans'] else 0,
            "fibra": float(row['fibra']) if row['fibra'] else 0,
            "sodio": float(row['sodio']) if row['sodio'] else 0,
            "exceso_calorias": row['exceso_calorias'],
            "exceso_azucares": row['exceso_azucares'],
            "exceso_grasas_saturadas": row['exceso_grasas_saturadas'],
            "exceso_grasas_trans": row['exceso_grasas_trans'],
            "exceso_sodio": row['exceso_sodio'],
            "contiene_edulcorantes": row['contiene_edulcorantes'],
            "contiene_cafeina": row['contiene_cafeina'],
            "imagen_url": row['imagen_url'],
            "ingredientes": row['ingredientes'],
            "categoria": row['categoria'],
            "fuente": row['fuente'],
            "health_score": health_score,
            "health_level": health_level,
            "health_color": health_color
        }

    except Exception as e:
        logger.error(f"Error searching local DB: {e}")
        return None


async def _save_to_local_db(product_data: Dict[str, Any], user_id: int, db) -> Optional[int]:
    """Save product to local database"""
    try:
        query = """
            INSERT INTO productos_nom051 (
                codigo_barras, nombre, marca, porcion_gramos,
                calorias, proteinas, carbohidratos, azucares,
                grasas_totales, grasas_saturadas, grasas_trans, fibra, sodio,
                exceso_calorias, exceso_azucares, exceso_grasas_saturadas,
                exceso_grasas_trans, exceso_sodio, contiene_edulcorantes, contiene_cafeina,
                imagen_url, ingredientes, categoria, fuente, usuario_id, validado
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
                $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26
            )
            ON CONFLICT (codigo_barras) DO UPDATE SET
                fecha_actualizacion = CURRENT_TIMESTAMP
            RETURNING id
        """

        row = await db.fetchrow(
            query,
            product_data['codigo_barras'],
            product_data['nombre'],
            product_data.get('marca'),
            product_data['porcion_gramos'],
            product_data['calorias'],
            product_data['proteinas'],
            product_data['carbohidratos'],
            product_data['azucares'],
            product_data['grasas_totales'],
            product_data['grasas_saturadas'],
            product_data['grasas_trans'],
            product_data['fibra'],
            product_data['sodio'],
            product_data['exceso_calorias'],
            product_data['exceso_azucares'],
            product_data['exceso_grasas_saturadas'],
            product_data['exceso_grasas_trans'],
            product_data['exceso_sodio'],
            product_data['contiene_edulcorantes'],
            product_data['contiene_cafeina'],
            product_data.get('imagen_url'),
            product_data.get('ingredientes'),
            product_data.get('categoria'),
            product_data['fuente'],
            user_id,
            False  # Not validated yet
        )

        return row['id'] if row else None

    except Exception as e:
        logger.error(f"Error saving to local DB: {e}")
        return None


async def _record_scan(
    user_id: int,
    barcode: str,
    product_id: Optional[int],
    found: bool,
    source: Optional[str],
    response_time_ms: int,
    db
):
    """Record scan in history"""
    try:
        query = """
            INSERT INTO escaneos_historia (
                usuario_id, producto_id, codigo_barras, encontrado,
                fuente, tiempo_respuesta_ms
            )
            VALUES ($1, $2, $3, $4, $5, $6)
        """

        await db.execute(
            query,
            user_id,
            product_id,
            barcode,
            found,
            source,
            response_time_ms
        )

    except Exception as e:
        logger.error(f"Error recording scan: {e}")


def _is_liquid_product(categories: str) -> bool:
    """Determine if product is liquid based on categories"""
    liquid_keywords = ['bebida', 'drink', 'juice', 'agua', 'water', 'refresco', 'soda']
    categories_lower = categories.lower()
    return any(keyword in categories_lower for keyword in liquid_keywords)


def _contains_caffeine(ingredients: str) -> bool:
    """Check if product contains caffeine"""
    caffeine_keywords = ['cafeína', 'caffeine', 'café', 'coffee', 'té', 'tea', 'guaraná', 'guarana']
    ingredients_lower = ingredients.lower()
    return any(keyword in ingredients_lower for keyword in caffeine_keywords)


def _map_category(categories: str) -> str:
    """Map Open Food Facts categories to SMAE categories"""
    categories_lower = categories.lower()

    if any(word in categories_lower for word in ['bebida', 'drink', 'juice', 'agua', 'refresco']):
        return 'BEVERAGES'
    elif any(word in categories_lower for word in ['snack', 'galleta', 'cookie', 'chip']):
        return 'CEREALS'
    elif any(word in categories_lower for word in ['dairy', 'leche', 'yogur', 'queso']):
        return 'DAIRY'
    elif any(word in categories_lower for word in ['carne', 'meat', 'pollo', 'chicken']):
        return 'ANIMAL_PRODUCTS'
    elif any(word in categories_lower for word in ['fruta', 'fruit']):
        return 'FRUITS'
    elif any(word in categories_lower for word in ['verdura', 'vegetable']):
        return 'VEGETABLES'
    else:
        return 'OTROS'


@router.get("/health")
async def scanner_health():
    """Health check for scanner service"""
    # Check Open Food Facts availability
    off_available = await openfoodfacts_client.health_check() if hasattr(openfoodfacts_client, 'health_check') else True

    return {
        "status": "healthy",
        "service": "nom051-scanner",
        "openfoodfacts_available": off_available
    }
