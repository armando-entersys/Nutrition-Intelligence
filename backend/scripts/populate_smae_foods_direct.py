"""
Script para poblar la base de datos con alimentos del Sistema Mexicano de Alimentos Equivalentes (SMAE)
Usa SQL directo para evitar problemas de mapeo de ORM
"""
import sys
import os
import json
import re
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

# Mapeo de categorías SMAE a categorías del sistema
# IMPORTANTE: Los valores del enum en PostgreSQL son UPPERCASE
CATEGORY_MAP = {
    'cereales_sin_grasa': 'CEREALS',
    'cereales_con_grasa': 'CEREALS',
    'leguminosas': 'LEGUMES',
    'verduras': 'VEGETABLES',
    'frutas': 'FRUITS',
    'leche_descremada': 'DAIRY',
    'leche_semidescremada': 'DAIRY',
    'leche_entera': 'DAIRY',
    'carnes_muy_bajo_aporte': 'ANIMAL_PRODUCTS',
    'carnes_bajo_aporte': 'ANIMAL_PRODUCTS',
    'carnes_moderado_aporte': 'ANIMAL_PRODUCTS',
    'carnes_alto_aporte': 'ANIMAL_PRODUCTS',
    'grasas_sin_proteina': 'FATS',
    'grasas_con_proteina': 'FATS',
    'azucares_sin_grasa': 'SUGARS',
    'azucares_con_grasa': 'SUGARS',
    'bebida_libre': 'BEVERAGES'
}

def extract_foods_manually(content: str):
    """Extracción manual de alimentos del archivo JS"""
    foods = []
    objects = re.findall(r'\{[^}]+\}', content, re.DOTALL)

    for obj_str in objects:
        if 'id:' in obj_str and 'nombre:' in obj_str:
            try:
                food = {}

                # Extraer campos
                id_match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", obj_str)
                if id_match:
                    food['id'] = id_match.group(1)

                name_match = re.search(r"nombre:\s*['\"]([^'\"]+)['\"]", obj_str)
                if name_match:
                    food['nombre'] = name_match.group(1)

                cat_match = re.search(r"categoria_equivalente:\s*['\"]?([^'\"]+)['\"]?", obj_str)
                if cat_match:
                    food['categoria_equivalente'] = cat_match.group(1)

                # Macronutrientes
                for nutrient in ['calorias', 'proteina_g', 'carbohidratos_g', 'grasa_g', 'fibra_g']:
                    nut_match = re.search(rf"{nutrient}:\s*(\d+\.?\d*)", obj_str)
                    if nut_match:
                        food[nutrient] = float(nut_match.group(1))

                # Micronutrientes
                for micro in ['calcio_mg', 'hierro_mg', 'vitamina_a_mcg', 'vitamina_c_mg', 'folato_mcg']:
                    micro_match = re.search(rf"{micro}:\s*(\d+\.?\d*)", obj_str)
                    if micro_match:
                        food[micro] = float(micro_match.group(1))

                # Índice glucémico
                ig_match = re.search(r"indice_glucemico:\s*(\d+)", obj_str)
                if ig_match:
                    food['indice_glucemico'] = int(ig_match.group(1))

                # Porción
                porcion_match = re.search(r"cantidad_porcion:\s*['\"]([^'\"]+)['\"]", obj_str)
                if porcion_match:
                    food['cantidad_porcion'] = porcion_match.group(1)

                # Descripción
                desc_match = re.search(r"descripcion:\s*['\"]([^'\"]+)['\"]", obj_str)
                if desc_match:
                    food['descripcion'] = desc_match.group(1)

                # Tradicional mexicano
                trad_match = re.search(r"es_tradicional_mexicano:\s*(true|false)", obj_str)
                if trad_match:
                    food['es_tradicional_mexicano'] = trad_match.group(1) == 'true'

                if 'id' in food and 'nombre' in food:
                    foods.append(food)

            except Exception as e:
                print(f"Error extrayendo alimento: {e}")
                continue

    return foods

def extract_serving_size(cantidad_porcion: str):
    """Extrae el tamaño de porción en gramos"""
    match = re.search(r'(\d+\.?\d*)\s*(g|ml)', cantidad_porcion)
    if match:
        return float(match.group(1))
    return 100.0

def populate_database():
    """Pobla la base de datos usando SQL directo"""

    # Leer archivo de alimentos
    data_path = Path(__file__).parent.parent / 'data' / 'alimentosMexicanos.js'

    print(f"Leyendo alimentos desde: {data_path}")

    if not data_path.exists():
        print(f"ERROR: No se encontró el archivo {data_path}")
        return

    # Parsear archivo
    print("Parseando archivo JS...")
    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()
    foods_data = extract_foods_manually(content)

    print(f"Se encontraron {len(foods_data)} alimentos")

    # Conectar a base de datos
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL no está configurada")
        return

    # Convertir async driver a sync driver
    database_url = database_url.replace('postgresql+asyncpg', 'postgresql')

    print("Conectando a base de datos...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    try:
        foods_added = 0
        foods_skipped = 0

        for food_data in foods_data:
            try:
                name = food_data.get('nombre', '')

                # Verificar si ya existe
                cursor.execute("SELECT id FROM foods WHERE name = %s", (name,))
                if cursor.fetchone():
                    print(f"[SKIP] Omitiendo (ya existe): {name}")
                    foods_skipped += 1
                    continue

                # Mapear categoría
                categoria_smae = food_data.get('categoria_equivalente', '').replace('CATEGORIAS_EQUIVALENTES.', '')
                categoria = CATEGORY_MAP.get(categoria_smae, 'CEREALS')  # Default to CEREALS (uppercase)

                # Extraer tamaño de porción
                cantidad_porcion = food_data.get('cantidad_porcion', '100g')
                serving_size = extract_serving_size(cantidad_porcion)

                # Preparar datos
                vitamins_json = json.dumps({
                    'vitamin_a_mcg': food_data.get('vitamina_a_mcg', 0),
                    'vitamin_c_mg': food_data.get('vitamina_c_mg', 0),
                    'folate_mcg': food_data.get('folato_mcg', 0)
                })

                minerals_json = json.dumps({
                    'calcium_mg': food_data.get('calcio_mg', 0),
                    'iron_mg': food_data.get('hierro_mg', 0)
                })

                dietary_flags = json.dumps(['traditional_mexican'] if food_data.get('es_tradicional_mexicano', False) else [])

                # Insertar en la base de datos
                insert_query = """
                INSERT INTO foods (
                    name, category, subcategory, base_unit, serving_size,
                    calories_per_serving, protein_g, carbs_g, fat_g, fiber_g, sugar_g, sodium_mg,
                    vitamins, minerals, glycemic_index, allergens, dietary_flags,
                    description, source, status, search_keywords, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s::jsonb, %s::jsonb, %s, %s, %s::jsonb,
                    %s, %s, %s, %s, NOW()
                )
                """

                cursor.execute(insert_query, (
                    name, categoria, categoria_smae, 'grams', serving_size,
                    food_data.get('calorias', 0),
                    food_data.get('proteina_g', 0),
                    food_data.get('carbohidratos_g', 0),
                    food_data.get('grasa_g', 0),
                    food_data.get('fibra_g', 0),
                    0.0,  # sugar_g
                    0.0,  # sodium_mg
                    vitamins_json,
                    minerals_json,
                    food_data.get('indice_glucemico'),
                    json.dumps([]),  # allergens
                    dietary_flags,
                    food_data.get('descripcion', ''),
                    'SMAE (Sistema Mexicano de Alimentos Equivalentes)',
                    'approved',
                    json.dumps([name]),
                ))

                foods_added += 1
                print(f"[OK] Agregado: {name} ({categoria})")

            except Exception as e:
                print(f"[ERROR] Error procesando {food_data.get('nombre', 'unknown')}: {str(e)}")
                continue

        # Commit
        conn.commit()

        print(f"\n{'='*60}")
        print(f"Proceso completado!")
        print(f"   Alimentos agregados: {foods_added}")
        print(f"   Alimentos omitidos: {foods_skipped}")
        print(f"   Total en archivo: {len(foods_data)}")
        print(f"{'='*60}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    try:
        populate_database()
    except Exception as e:
        print(f"ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
