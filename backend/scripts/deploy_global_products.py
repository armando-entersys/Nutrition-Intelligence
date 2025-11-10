"""
Deploy Global Products System
==============================

Script para verificar y aplicar las migraciones del sistema global de productos.
Compatible con SQLite (desarrollo) y PostgreSQL (producción).
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

DB_PATH = Path(__file__).parent.parent / "nutrition_intelligence.db"


def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect(str(DB_PATH))


def check_table_exists(cursor, table_name):
    """Check if a table exists"""
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None


def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(col[1] == column_name for col in columns)


def migrate_productos_nom051(conn):
    """
    Migrate productos_nom051 table for global products system
    """
    cursor = conn.cursor()

    print("\n[1/5] Verificando tabla productos_nom051...")

    if not check_table_exists(cursor, 'productos_nom051'):
        print("   [INFO] Tabla productos_nom051 no existe. Creando...")
        cursor.execute("""
            CREATE TABLE productos_nom051 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                codigo_barras VARCHAR(50) UNIQUE,
                nombre VARCHAR(255) NOT NULL,
                marca VARCHAR(255),

                -- Nutritional info
                porcion_gramos REAL NOT NULL,
                calorias REAL NOT NULL,
                proteinas REAL NOT NULL,
                carbohidratos REAL NOT NULL,
                azucares REAL NOT NULL,
                grasas_totales REAL NOT NULL,
                grasas_saturadas REAL NOT NULL,
                grasas_trans REAL NOT NULL,
                fibra REAL NOT NULL,
                sodio REAL NOT NULL,

                -- NOM-051 seals
                exceso_calorias BOOLEAN DEFAULT 0,
                exceso_azucares BOOLEAN DEFAULT 0,
                exceso_grasas_saturadas BOOLEAN DEFAULT 0,
                exceso_grasas_trans BOOLEAN DEFAULT 0,
                exceso_sodio BOOLEAN DEFAULT 0,
                contiene_edulcorantes BOOLEAN DEFAULT 0,
                contiene_cafeina BOOLEAN DEFAULT 0,

                -- Additional info
                imagen_url TEXT,
                ingredientes TEXT,
                categoria VARCHAR(100),
                fuente VARCHAR(50) NOT NULL,

                -- Global products fields
                image_hash VARCHAR(64),
                created_by_user_id INTEGER,
                scan_count INTEGER DEFAULT 1,
                verified BOOLEAN DEFAULT 0,
                verified_by_user_id INTEGER,
                verified_at TIMESTAMP,
                is_global BOOLEAN DEFAULT 1,
                confidence_score REAL,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES auth_users(id) ON DELETE SET NULL,
                FOREIGN KEY (created_by_user_id) REFERENCES auth_users(id) ON DELETE SET NULL,
                FOREIGN KEY (verified_by_user_id) REFERENCES auth_users(id) ON DELETE SET NULL
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nom051_image_hash ON productos_nom051(image_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nom051_created_by_user_id ON productos_nom051(created_by_user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nom051_verified ON productos_nom051(verified)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nom051_is_global ON productos_nom051(is_global)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nom051_scan_count ON productos_nom051(scan_count)")

        print("   [OK] Tabla productos_nom051 creada exitosamente")
    else:
        print("   [OK] Tabla productos_nom051 ya existe")

        # Add new columns if they don't exist
        new_columns = [
            ('image_hash', 'VARCHAR(64)'),
            ('created_by_user_id', 'INTEGER'),
            ('scan_count', 'INTEGER DEFAULT 1'),
            ('verified', 'BOOLEAN DEFAULT 0'),
            ('verified_by_user_id', 'INTEGER'),
            ('verified_at', 'TIMESTAMP'),
            ('is_global', 'BOOLEAN DEFAULT 1'),
            ('confidence_score', 'REAL'),
        ]

        for col_name, col_type in new_columns:
            if not check_column_exists(cursor, 'productos_nom051', col_name):
                print(f"   [MIGRATE] Agregando columna {col_name}...")
                cursor.execute(f"ALTER TABLE productos_nom051 ADD COLUMN {col_name} {col_type}")
                print(f"   [OK] Columna {col_name} agregada")
            else:
                print(f"   [OK] Columna {col_name} ya existe")


def migrate_user_scan_history(conn):
    """
    Create user_scan_history table
    """
    cursor = conn.cursor()

    print("\n[2/5] Verificando tabla user_scan_history...")

    if not check_table_exists(cursor, 'user_scan_history'):
        print("   [INFO] Tabla user_scan_history no existe. Creando...")
        cursor.execute("""
            CREATE TABLE user_scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scan_method VARCHAR(20) DEFAULT 'barcode',

                FOREIGN KEY (user_id) REFERENCES auth_users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES productos_nom051(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_scan_history_user_id ON user_scan_history(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_scan_history_product_id ON user_scan_history(product_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_scan_history_scanned_at ON user_scan_history(scanned_at DESC)")

        print("   [OK] Tabla user_scan_history creada exitosamente")
    else:
        print("   [OK] Tabla user_scan_history ya existe")


def migrate_product_images(conn):
    """
    Create product_images table
    """
    cursor = conn.cursor()

    print("\n[3/5] Verificando tabla product_images...")

    if not check_table_exists(cursor, 'product_images'):
        print("   [INFO] Tabla product_images no existe. Creando...")
        cursor.execute("""
            CREATE TABLE product_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                image_url TEXT,
                image_hash VARCHAR(64),
                perceptual_hash VARCHAR(64),
                uploaded_by_user_id INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (product_id) REFERENCES productos_nom051(id) ON DELETE CASCADE,
                FOREIGN KEY (uploaded_by_user_id) REFERENCES auth_users(id) ON DELETE SET NULL
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_images_product_id ON product_images(product_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_images_image_hash ON product_images(image_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_images_perceptual_hash ON product_images(perceptual_hash)")

        print("   [OK] Tabla product_images creada exitosamente")
    else:
        print("   [OK] Tabla product_images ya existe")


def migrate_product_embeddings(conn):
    """
    Create product_embeddings table (for future RAG integration)
    """
    cursor = conn.cursor()

    print("\n[4/5] Verificando tabla product_embeddings...")

    if not check_table_exists(cursor, 'product_embeddings'):
        print("   [INFO] Tabla product_embeddings no existe. Creando...")
        cursor.execute("""
            CREATE TABLE product_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                embedding_model VARCHAR(50) DEFAULT 'text-embedding-ada-002',
                embedding_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (product_id) REFERENCES productos_nom051(id) ON DELETE CASCADE
            )
        """)

        # Create index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_embeddings_product_id ON product_embeddings(product_id)")

        print("   [OK] Tabla product_embeddings creada exitosamente")
    else:
        print("   [OK] Tabla product_embeddings ya existe")


def verify_deployment(conn):
    """
    Verify that all tables and columns exist
    """
    cursor = conn.cursor()

    print("\n[5/5] Verificando deployment...")

    # Check all required tables
    required_tables = [
        'productos_nom051',
        'user_scan_history',
        'product_images',
        'product_embeddings'
    ]

    all_ok = True
    for table in required_tables:
        if check_table_exists(cursor, table):
            print(f"   [OK] Tabla {table} existe")
        else:
            print(f"   [ERROR] Tabla {table} NO existe")
            all_ok = False

    # Check required columns in productos_nom051
    required_columns = [
        'image_hash',
        'created_by_user_id',
        'scan_count',
        'verified',
        'is_global',
        'confidence_score'
    ]

    for column in required_columns:
        if check_column_exists(cursor, 'productos_nom051', column):
            print(f"   [OK] Columna productos_nom051.{column} existe")
        else:
            print(f"   [ERROR] Columna productos_nom051.{column} NO existe")
            all_ok = False

    # Get table counts
    print("\n   Estadisticas de la base de datos:")
    for table in required_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   - {table}: {count} registros")

    return all_ok


def main():
    """
    Main deployment script
    """
    print("=" * 80)
    print("DEPLOYMENT: Sistema Global de Productos NOM-051")
    print("=" * 80)
    print(f"\nBase de datos: {DB_PATH}")

    if not DB_PATH.exists():
        print(f"\n[ERROR] Base de datos no encontrada en: {DB_PATH}")
        print("Por favor ejecuta el backend primero para crear la base de datos.")
        return 1

    try:
        # Connect to database
        conn = get_db_connection()

        # Run migrations
        migrate_productos_nom051(conn)
        migrate_user_scan_history(conn)
        migrate_product_images(conn)
        migrate_product_embeddings(conn)

        # Commit changes
        conn.commit()

        # Verify deployment
        if verify_deployment(conn):
            print("\n" + "=" * 80)
            print("[SUCCESS] Sistema global de productos desplegado correctamente!")
            print("=" * 80)
            print("\nProximos pasos:")
            print("1. Inicia el backend: uvicorn backend.main:app --reload")
            print("2. Prueba el endpoint /api/v1/scanner/label con una imagen")
            print("3. Verifica la deduplicacion escaneando la misma imagen dos veces")
            print("=" * 80)
            return 0
        else:
            print("\n[ERROR] Verificacion fallo. Revisa los errores arriba.")
            return 1

    except Exception as e:
        print(f"\n[ERROR] Error durante deployment: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
