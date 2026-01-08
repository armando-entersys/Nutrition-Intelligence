"""
Script para importar alimentos del SMAE 2025 desde archivos CSV
Corrige problemas de acentos y carga los datos a la base de datos
"""

import os
import csv
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nutrition_user:nutrition_password_dev@localhost:5432/nutrition_intelligence"
)

# Mapping of file names to food groups
FILE_TO_GROUP = {
    "Grupo_Alimentos_de_Origen_Animal.csv": "Alimentos de Origen Animal",
    "Grupo_Azúcares.csv": "Azucares",
    "Grupo_Cereal.csv": "Cereales",
    "Grupo_Etanol.csv": "Etanol",
    "Grupo_Frutas.csv": "Frutas",
    "Grupo_grasas.csv": "Grasas",
    "Grupo_Leche.csv": "Leche",
    "Grupo_Leguminosas.csv": "Leguminosas",
    "Grupo_Libre.csv": "Alimentos Libres",
    "Grupo_Verduras.csv": "Verduras",
}

# Common encoding fixes for Spanish text
ENCODING_FIXES = {
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ã­': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã±': 'ñ',
    'Ã': 'Á',
    'Ã‰': 'É',
    'Ã': 'Í',
    'Ã"': 'Ó',
    'Ãš': 'Ú',
    'Ã'': 'Ñ',
    'Ã¼': 'ü',
    'Ãœ': 'Ü',
    'â€™': "'",
    'â€"': '-',
    'â€œ': '"',
    'â€': '"',
    'Â°': '°',
    'Â®': '®',
    'â„¢': '™',
}

def fix_encoding(text):
    """Fix common encoding issues in Spanish text"""
    if not text:
        return text

    result = text
    for wrong, correct in ENCODING_FIXES.items():
        result = result.replace(wrong, correct)

    return result.strip()

def parse_float(value):
    """Parse a float value, handling different formats"""
    if not value or value.strip() == '':
        return None
    try:
        # Replace comma with dot for decimal
        return float(value.replace(',', '.'))
    except (ValueError, AttributeError):
        return None

def read_csv_file(filepath, group_name):
    """Read a CSV file and return list of food records"""
    foods = []

    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f, delimiter='|')
                for row in reader:
                    food = {
                        'nombre': fix_encoding(row.get('Alimento', '')),
                        'nombre_comun': None,
                        'grupo_smae': group_name,
                        'subgrupo': fix_encoding(row.get('Subgrupo', '')),
                        'porcion': parse_float(row.get('Cant.', '1')),
                        'unidad_porcion': fix_encoding(row.get('Unidad', 'porción')),
                        'peso_neto_g': None,
                        'calorias': parse_float(row.get('Energía', '0')),
                        'proteinas': parse_float(row.get('Proteína', '0')),
                        'carbohidratos': parse_float(row.get('H de C', '0')),
                        'grasas': parse_float(row.get('Lípidos', '0')),
                        'fibra': None,
                        'sodio_mg': None,
                        'calcio_mg': None,
                        'hierro_mg': None,
                        'equivalente_cereales': parse_float(row.get('Equivalentes', '0')) if group_name == 'Cereales' else None,
                        'equivalente_leguminosas': parse_float(row.get('Equivalentes', '0')) if group_name == 'Leguminosas' else None,
                        'equivalente_verduras': parse_float(row.get('Equivalentes', '0')) if group_name == 'Verduras' else None,
                        'equivalente_frutas': parse_float(row.get('Equivalentes', '0')) if group_name == 'Frutas' else None,
                        'equivalente_aoa': parse_float(row.get('Equivalentes', '0')) if group_name == 'Alimentos de Origen Animal' else None,
                        'equivalente_leche': parse_float(row.get('Equivalentes', '0')) if group_name == 'Leche' else None,
                        'equivalente_grasas': parse_float(row.get('Equivalentes', '0')) if group_name == 'Grasas' else None,
                        'equivalente_azucares': parse_float(row.get('Equivalentes', '0')) if group_name == 'Azucares' else None,
                        'descripcion': None,
                        'preparacion': None,
                        'es_mexicano': True,
                        'temporada': None,
                        'fuente': 'SMAE 2025',
                        'verificado': True,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow(),
                    }

                    # Skip if no name
                    if food['nombre']:
                        foods.append(food)

                print(f"  ✓ Read {len(foods)} foods from {filepath.name} using {encoding} encoding")
                return foods

        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"  ✗ Error reading {filepath.name}: {e}")
            continue

    print(f"  ✗ Could not read {filepath.name} with any encoding")
    return []

def import_foods(foods, engine):
    """Import foods into the database"""
    Session = sessionmaker(bind=engine)
    session = Session()

    inserted = 0
    skipped = 0

    try:
        for food in foods:
            # Check if food already exists
            result = session.execute(
                text("SELECT id FROM alimentos_smae WHERE nombre = :nombre AND grupo_smae = :grupo"),
                {'nombre': food['nombre'], 'grupo': food['grupo_smae']}
            )
            existing = result.fetchone()

            if existing:
                skipped += 1
                continue

            # Insert new food
            columns = ', '.join(food.keys())
            placeholders = ', '.join([f':{k}' for k in food.keys()])

            session.execute(
                text(f"INSERT INTO alimentos_smae ({columns}) VALUES ({placeholders})"),
                food
            )
            inserted += 1

        session.commit()
        print(f"  → Inserted: {inserted}, Skipped (duplicates): {skipped}")
        return inserted, skipped

    except Exception as e:
        session.rollback()
        print(f"  ✗ Error inserting foods: {e}")
        raise
    finally:
        session.close()

def main():
    """Main function to import all SMAE foods"""
    print("=" * 60)
    print("IMPORTADOR DE ALIMENTOS SMAE 2025")
    print("=" * 60)

    # Get the CSV folder path
    script_dir = Path(__file__).parent
    csv_folder = script_dir.parent.parent / "Grupos de alimentos"

    if not csv_folder.exists():
        print(f"✗ Folder not found: {csv_folder}")
        return

    print(f"\n📁 Reading from: {csv_folder}\n")

    # Create database connection
    print(f"🔌 Connecting to database...")
    engine = create_engine(DATABASE_URL)

    # Test connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM alimentos_smae"))
            current_count = result.scalar()
            print(f"  ✓ Connected. Current records: {current_count}\n")
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        return

    total_inserted = 0
    total_skipped = 0

    # Process each CSV file
    for filename, group_name in FILE_TO_GROUP.items():
        filepath = csv_folder / filename

        if not filepath.exists():
            print(f"⚠️  File not found: {filename}")
            continue

        print(f"\n📄 Processing: {filename}")
        print(f"   Group: {group_name}")

        # Read foods from CSV
        foods = read_csv_file(filepath, group_name)

        if foods:
            # Import to database
            inserted, skipped = import_foods(foods, engine)
            total_inserted += inserted
            total_skipped += skipped

    # Final count
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Total insertados: {total_inserted}")
    print(f"Total omitidos (duplicados): {total_skipped}")

    # Get new count
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM alimentos_smae"))
        new_count = result.scalar()
        print(f"Total en base de datos: {new_count}")

    print("\n✅ Importación completada")

if __name__ == "__main__":
    main()
