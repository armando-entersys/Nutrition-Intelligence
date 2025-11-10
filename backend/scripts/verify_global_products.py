"""
Verify Global Products System
==============================

Script para verificar que el sistema global de productos funciona correctamente.
"""

import asyncio
import httpx
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "nutrition_intelligence.db"
BASE_URL = "http://localhost:8000/api/v1"


def get_db_stats():
    """Get database statistics"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    stats = {}

    # Count tables
    tables = ['productos_nom051', 'user_scan_history', 'product_images', 'product_embeddings']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cursor.fetchone()[0]

    # Get verified products count
    cursor.execute("SELECT COUNT(*) FROM productos_nom051 WHERE verified = 1")
    stats['verified_products'] = cursor.fetchone()[0]

    # Get global products count
    cursor.execute("SELECT COUNT(*) FROM productos_nom051 WHERE is_global = 1")
    stats['global_products'] = cursor.fetchone()[0]

    # Get most scanned products
    cursor.execute("""
        SELECT nombre, marca, scan_count, verified
        FROM productos_nom051
        ORDER BY scan_count DESC
        LIMIT 5
    """)
    stats['top_scanned'] = cursor.fetchall()

    conn.close()
    return stats


async def verify_scanner_health():
    """Verify scanner endpoint is healthy"""
    print("\n[1/4] Verificando endpoint /scanner/health...")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/scanner/health")

            if response.status_code == 200:
                data = response.json()
                print(f"   [OK] Scanner status: {data.get('status')}")
                print(f"   [OK] Database: {data.get('database')}")
                print(f"   [OK] Vision AI: {data.get('vision_ai')}")
                return True
            else:
                print(f"   [ERROR] Status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"   [ERROR] {str(e)}")
            return False


async def verify_rag_health():
    """Verify RAG endpoint is healthy"""
    print("\n[2/4] Verificando endpoint /rag/health...")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/rag/health")

            if response.status_code == 200:
                data = response.json()
                print(f"   [OK] RAG status: {data.get('status')}")
                print(f"   [OK] Search service: {data.get('search_service')}")
                print(f"   [OK] AI service: {data.get('ai_service')}")
                return True
            else:
                print(f"   [ERROR] Status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"   [ERROR] {str(e)}")
            return False


async def verify_database_schema():
    """Verify database schema"""
    print("\n[3/4] Verificando esquema de base de datos...")

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Verify tables exist
        required_tables = [
            'productos_nom051',
            'user_scan_history',
            'product_images',
            'product_embeddings'
        ]

        all_ok = True
        for table in required_tables:
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?
            """, (table,))

            if cursor.fetchone():
                print(f"   [OK] Tabla {table} existe")
            else:
                print(f"   [ERROR] Tabla {table} NO existe")
                all_ok = False

        # Verify productos_nom051 columns
        required_columns = [
            'image_hash',
            'created_by_user_id',
            'scan_count',
            'verified',
            'is_global',
            'confidence_score'
        ]

        cursor.execute("PRAGMA table_info(productos_nom051)")
        columns = [col[1] for col in cursor.fetchall()]

        for col in required_columns:
            if col in columns:
                print(f"   [OK] Columna productos_nom051.{col} existe")
            else:
                print(f"   [ERROR] Columna productos_nom051.{col} NO existe")
                all_ok = False

        conn.close()
        return all_ok

    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        return False


async def show_database_stats():
    """Show database statistics"""
    print("\n[4/4] Estadísticas de la base de datos...")

    try:
        stats = get_db_stats()

        print(f"\n   Totales:")
        print(f"   - Productos NOM-051: {stats['productos_nom051']}")
        print(f"   - Historial de escaneos: {stats['user_scan_history']}")
        print(f"   - Imágenes de productos: {stats['product_images']}")
        print(f"   - Embeddings (RAG): {stats['product_embeddings']}")

        print(f"\n   Productos:")
        print(f"   - Globales: {stats['global_products']}")
        print(f"   - Verificados: {stats['verified_products']}")

        if stats['top_scanned']:
            print(f"\n   Top productos escaneados:")
            for i, (nombre, marca, count, verified) in enumerate(stats['top_scanned'], 1):
                verified_icon = "[V]" if verified else "[ ]"
                marca_str = f" ({marca})" if marca else ""
                print(f"   {i}. {verified_icon} {nombre}{marca_str} - {count} escaneos")
        else:
            print(f"\n   [INFO] No hay productos escaneados aún")
            print(f"   [INFO] Usa el frontend para escanear tu primer producto!")

        return True

    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        return False


async def main():
    """
    Main verification script
    """
    print("=" * 80)
    print("VERIFICACION: Sistema Global de Productos NOM-051")
    print("=" * 80)
    print(f"Backend URL: {BASE_URL}")
    print(f"Database: {DB_PATH}")

    # Run all checks
    checks = [
        await verify_scanner_health(),
        await verify_rag_health(),
        await verify_database_schema(),
        await show_database_stats()
    ]

    # Summary
    print("\n" + "=" * 80)
    if all(checks):
        print("[SUCCESS] Todos los checks pasaron!")
        print("=" * 80)
        print("\nSistema listo para usar:")
        print("1. Backend corriendo en: http://localhost:8000")
        print("2. Docs interactivas: http://localhost:8000/docs")
        print("3. Frontend: Inicia con 'npm start' en el directorio frontend")
        print("\nEndpoints disponibles:")
        print("- POST /api/v1/scanner/label - Escanear etiqueta nutricional")
        print("- GET /api/v1/scanner/barcode/{code} - Buscar por codigo de barras")
        print("- POST /api/v1/rag/chat - Chat con Gemini AI")
        print("=" * 80)
        return 0
    else:
        print("[ERROR] Algunos checks fallaron. Revisa los errores arriba.")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
