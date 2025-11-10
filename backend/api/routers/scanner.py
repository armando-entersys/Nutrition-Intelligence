"""
NOM-051 Scanner API Router
Provides barcode scanning and product lookup with NOM-051 seals
Also supports label scanning using Vision AI with intelligent deduplication
"""
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
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
from services.ai.vision import extract_nutrition_label
from services.utils.image_utils import (
    calculate_image_hash,
    calculate_perceptual_hash,
    calculate_average_hash,
    images_are_similar,
    extract_image_metadata
)

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


@router.post("/label")
async def scan_label(
    image: UploadFile = File(...),
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Scan product label using Vision AI with intelligent deduplication

    Global Product System:
    1. Calculates image hash for exact duplicate detection
    2. Searches for existing products in global database
    3. If duplicate found: increments scan count, registers in user history
    4. If new product: creates global product entry
    5. Stores image in product_images table for deduplication
    6. Always maintains private user scan history

    Args:
        image: Product label image file (JPG, PNG, WEBP)
        user: Current authenticated user
        db: Database connection

    Returns:
        ProductResponse with extracted data and global metadata
    """
    try:
        start_time = datetime.now()
        user_id = user.get('user_id')
        logger.info(f"Scanning label image for user {user_id}")

        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo inválido. Formatos soportados: JPG, PNG, WEBP"
            )

        # Read image bytes
        image_bytes = await image.read()

        # Validate file size (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Archivo demasiado grande. Tamaño máximo: 10MB"
            )

        logger.info(f"Image received: {image.filename} ({len(image_bytes)} bytes)")

        # STEP 1: Calculate image hashes for deduplication
        logger.info("Calculating image hashes for deduplication...")
        image_hash_sha256 = calculate_image_hash(image_bytes, "sha256")
        perceptual_hash = calculate_perceptual_hash(image_bytes)

        logger.info(f"Image SHA-256: {image_hash_sha256[:16]}...")
        logger.info(f"Perceptual hash: {perceptual_hash}")

        # STEP 2: Check for exact duplicate by image hash
        logger.info("Checking for existing product with same image...")
        existing_product = await _find_product_by_image_hash(image_hash_sha256, db)

        if existing_product:
            logger.info(f"✅ DUPLICATE FOUND! Product ID: {existing_product['id']} - {existing_product['nombre']}")

            # Register scan in user's history
            scan_history_id = await _register_user_scan(
                user_id=user_id,
                product_id=existing_product['id'],
                scan_type='label',
                db=db
            )

            logger.info(f"Registered in user scan history (ID: {scan_history_id})")

            # Return existing product data with updated metadata
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            existing_product['response_time_ms'] = int(response_time)
            existing_product['is_duplicate'] = True
            existing_product['scan_history_id'] = scan_history_id

            return JSONResponse(content=existing_product, status_code=status.HTTP_200_OK)

        # STEP 3: Extract nutrition data from label using Vision AI
        logger.info("NEW PRODUCT - Extracting nutritional data with Vision AI...")
        label_data = await extract_nutrition_label(image_bytes)

        # Parse extracted data
        producto = label_data.get('producto', {})
        nutricion = label_data.get('nutricion', {})
        confidence_score = label_data.get('confidence_score', 0)

        # Validate that we got meaningful data
        if not producto.get('nombre') and not nutricion.get('calorias'):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se pudo extraer información nutricional de la imagen. Asegúrate de que la foto muestre claramente la tabla nutricional."
            )

        product_name = producto.get('nombre') or "Producto escaneado"
        product_brand = producto.get('marca')

        # STEP 4: Check for similar products by name/brand
        logger.info(f"Checking for similar products: '{product_name}' by '{product_brand}'")
        similar_products = await _find_similar_products_by_text(
            nombre=product_name,
            marca=product_brand,
            image_hash=image_hash_sha256,
            db=db
        )

        if similar_products:
            logger.info(f"Found {len(similar_products)} similar products (by text similarity)")
            # TODO: In future, could ask user if this is the same product
            # For now, we create a new product entry

        # Determine if product is liquid (default to solid)
        is_liquid = False

        # STEP 5: Calculate NOM-051 seals
        seals = nom051_calculator.calculate_seals(
            calorias=nutricion.get('calorias') or 0,
            azucares=nutricion.get('azucares') or 0,
            grasas_saturadas=nutricion.get('grasas_saturadas') or 0,
            grasas_trans=nutricion.get('grasas_trans') or 0,
            sodio=nutricion.get('sodio') or 0,
            is_liquid=is_liquid,
            contiene_edulcorantes=label_data.get('contiene_edulcorantes', False),
            contiene_cafeina=label_data.get('contiene_cafeina', False)
        )

        # Calculate health score
        health_score, health_level, health_color = nom051_calculator.get_health_score(seals)

        # STEP 6: Create new global product
        logger.info("Creating new global product...")
        product_id = await _create_global_product(
            nombre=product_name,
            marca=product_brand,
            porcion_gramos=producto.get('porcion_gramos') or 100.0,
            calorias=nutricion.get('calorias') or 0,
            proteinas=nutricion.get('proteinas') or 0,
            carbohidratos=nutricion.get('carbohidratos') or 0,
            azucares=nutricion.get('azucares') or 0,
            grasas_totales=nutricion.get('grasas_totales') or 0,
            grasas_saturadas=nutricion.get('grasas_saturadas') or 0,
            grasas_trans=nutricion.get('grasas_trans') or 0,
            fibra=nutricion.get('fibra') or 0,
            sodio=nutricion.get('sodio') or 0,
            seals=seals,
            ingredientes=label_data.get('ingredientes'),
            image_hash=image_hash_sha256,
            perceptual_hash=perceptual_hash,
            confidence_score=confidence_score,
            created_by_user_id=user_id,
            db=db
        )

        logger.info(f"✨ Created new global product with ID: {product_id}")

        # STEP 7: Store product image
        await _save_product_image(
            product_id=product_id,
            image_bytes=image_bytes,
            image_hash=image_hash_sha256,
            image_type='label',
            uploaded_by_user_id=user_id,
            db=db
        )

        # STEP 8: Register scan in user's history
        scan_history_id = await _register_user_scan(
            user_id=user_id,
            product_id=product_id,
            scan_type='label',
            db=db
        )

        response_time = (datetime.now() - start_time).total_seconds() * 1000

        # Build response with global metadata
        product_data = {
            "id": product_id,
            "codigo_barras": f"AI_{product_id}",  # Virtual barcode for AI-scanned products
            "nombre": product_name,
            "marca": product_brand,
            "porcion_gramos": producto.get('porcion_gramos') or 100.0,
            "calorias": nutricion.get('calorias') or 0,
            "proteinas": nutricion.get('proteinas') or 0,
            "carbohidratos": nutricion.get('carbohidratos') or 0,
            "azucares": nutricion.get('azucares') or 0,
            "grasas_totales": nutricion.get('grasas_totales') or 0,
            "grasas_saturadas": nutricion.get('grasas_saturadas') or 0,
            "grasas_trans": nutricion.get('grasas_trans') or 0,
            "fibra": nutricion.get('fibra') or 0,
            "sodio": nutricion.get('sodio') or 0,
            **seals.to_dict(),
            "imagen_url": None,
            "ingredientes": label_data.get('ingredientes'),
            "categoria": "OTROS",
            "fuente": "ai_vision",
            "health_score": health_score,
            "health_level": health_level,
            "health_color": health_color,
            # Global product metadata
            "is_global": True,
            "scan_count": 1,
            "confidence_score": confidence_score,
            "created_by_user_id": user_id,
            "verified": False,
            "is_duplicate": False,
            "scan_history_id": scan_history_id,
            "response_time_ms": int(response_time)
        }

        logger.info(f"Label scan completed in {response_time:.0f}ms. Confidence: {confidence_score}%")

        return JSONResponse(content=product_data, status_code=status.HTTP_200_OK)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scanning label: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al escanear etiqueta: {str(e)}"
        )


async def _find_product_by_image_hash(image_hash: str, db) -> Optional[Dict[str, Any]]:
    """
    Find existing product by exact image hash

    Returns product data with health score if found, None otherwise
    """
    try:
        query = """
            SELECT
                p.id,
                p.nombre,
                p.marca,
                p.porcion_gramos,
                p.calorias,
                p.proteinas,
                p.carbohidratos,
                p.azucares,
                p.grasas_totales,
                p.grasas_saturadas,
                p.grasas_trans,
                p.fibra,
                p.sodio,
                p.exceso_calorias,
                p.exceso_azucares,
                p.exceso_grasas_saturadas,
                p.exceso_grasas_trans,
                p.exceso_sodio,
                p.contiene_edulcorantes,
                p.contiene_cafeina,
                p.ingredientes,
                p.fuente,
                p.image_hash,
                p.scan_count,
                p.verified,
                p.confidence_score,
                p.created_by_user_id,
                p.is_global
            FROM productos_nom051 p
            WHERE p.image_hash = $1
            LIMIT 1
        """

        row = await db.fetchrow(query, image_hash)

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
            "codigo_barras": f"AI_{row['id']}",
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
            "ingredientes": row['ingredientes'],
            "fuente": row['fuente'],
            "health_score": health_score,
            "health_level": health_level,
            "health_color": health_color,
            # Global metadata
            "is_global": row['is_global'],
            "scan_count": row['scan_count'],
            "verified": row['verified'],
            "confidence_score": row['confidence_score'],
            "created_by_user_id": row['created_by_user_id']
        }

    except Exception as e:
        logger.error(f"Error finding product by image hash: {e}")
        return None


async def _find_similar_products_by_text(
    nombre: str,
    marca: Optional[str],
    image_hash: str,
    db,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Find similar products using the find_similar_products SQL function

    Uses both image hash matching and text similarity (pg_trgm)
    """
    try:
        query = """
            SELECT * FROM find_similar_products($1, $2, $3, $4)
        """

        rows = await db.fetch(
            query,
            nombre,
            marca or '',
            image_hash,
            limit
        )

        return [
            {
                "product_id": row['product_id'],
                "nombre": row['nombre'],
                "marca": row['marca'],
                "similarity_score": float(row['similarity_score']),
                "match_type": row['match_type']
            }
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Error finding similar products: {e}")
        return []


async def _create_global_product(
    nombre: str,
    marca: Optional[str],
    porcion_gramos: float,
    calorias: float,
    proteinas: float,
    carbohidratos: float,
    azucares: float,
    grasas_totales: float,
    grasas_saturadas: float,
    grasas_trans: float,
    fibra: float,
    sodio: float,
    seals: 'NOM051Seals',
    ingredientes: Optional[str],
    image_hash: str,
    perceptual_hash: str,
    confidence_score: float,
    created_by_user_id: int,
    db
) -> int:
    """
    Create new global product with deduplication metadata

    Returns the product ID
    """
    try:
        query = """
            INSERT INTO productos_nom051 (
                nombre, marca, porcion_gramos,
                calorias, proteinas, carbohidratos, azucares,
                grasas_totales, grasas_saturadas, grasas_trans, fibra, sodio,
                exceso_calorias, exceso_azucares, exceso_grasas_saturadas,
                exceso_grasas_trans, exceso_sodio, contiene_edulcorantes, contiene_cafeina,
                ingredientes, categoria, fuente,
                image_hash, created_by_user_id, scan_count, verified,
                confidence_score, is_global, validado
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                $13, $14, $15, $16, $17, $18, $19, $20, $21, $22,
                $23, $24, $25, $26, $27, $28, $29
            )
            RETURNING id
        """

        row = await db.fetchrow(
            query,
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
            seals.exceso_calorias,
            seals.exceso_azucares,
            seals.exceso_grasas_saturadas,
            seals.exceso_grasas_trans,
            seals.exceso_sodio,
            seals.contiene_edulcorantes,
            seals.contiene_cafeina,
            ingredientes,
            "OTROS",  # categoria
            "ai_vision",  # fuente
            image_hash,
            created_by_user_id,
            1,  # scan_count (first scan)
            False,  # verified
            confidence_score,
            True,  # is_global
            False  # validado (not validated yet)
        )

        return row['id']

    except Exception as e:
        logger.error(f"Error creating global product: {e}")
        raise


async def _save_product_image(
    product_id: int,
    image_bytes: bytes,
    image_hash: str,
    image_type: str,
    uploaded_by_user_id: int,
    db
):
    """
    Save product image to product_images table

    Stores image for deduplication and visual reference
    """
    try:
        # Extract image metadata
        metadata = extract_image_metadata(image_bytes)

        query = """
            INSERT INTO product_images (
                product_id,
                image_data,
                image_hash,
                image_type,
                uploaded_by_user_id,
                is_primary
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (image_hash) DO NOTHING
        """

        await db.execute(
            query,
            product_id,
            image_bytes,  # Store actual image bytes
            image_hash,
            image_type,
            uploaded_by_user_id,
            True  # First image is primary
        )

        logger.info(f"Saved product image: {image_type}, {metadata.get('width')}x{metadata.get('height')}, {len(image_bytes)} bytes")

    except Exception as e:
        logger.error(f"Error saving product image: {e}")
        # Don't raise - image storage is not critical


async def _register_user_scan(
    user_id: int,
    product_id: int,
    scan_type: str,
    db
) -> Optional[int]:
    """
    Register scan in user's private history using register_product_scan SQL function

    Also increments global scan_count for the product

    Returns scan history ID
    """
    try:
        query = """
            SELECT register_product_scan($1, $2, $3, $4, $5) as scan_history_id
        """

        # Device info (could be passed from frontend in future)
        device_info = {
            "platform": "web",
            "timestamp": datetime.now().isoformat()
        }

        row = await db.fetchrow(
            query,
            user_id,
            product_id,
            scan_type,
            device_info,  # JSONB
            None  # location_context
        )

        return row['scan_history_id'] if row else None

    except Exception as e:
        logger.error(f"Error registering user scan: {e}")
        return None


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
