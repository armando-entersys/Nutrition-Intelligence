"""
Script para poblar la base de datos con alimentos del Sistema Mexicano de Alimentos Equivalentes (SMAE)
Importa los 64 alimentos mexicanos desde el frontend
"""
import sys
import os
import json
import re
from pathlib import Path

# Add parent directory to path to import models
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, create_engine, SQLModel
from domain.foods.models import Food, FoodCategory, MeasurementUnit, FoodStatus
from core.config import get_settings

# Mapeo de categorías SMAE a categorías del sistema
CATEGORY_MAP = {
    'cereales_sin_grasa': FoodCategory.CEREALS,
    'cereales_con_grasa': FoodCategory.CEREALS,
    'leguminosas': FoodCategory.LEGUMES,
    'verduras': FoodCategory.VEGETABLES,
    'frutas': FoodCategory.FRUITS,
    'leche_descremada': FoodCategory.DAIRY,
    'leche_semidescremada': FoodCategory.DAIRY,
    'leche_entera': FoodCategory.DAIRY,
    'carnes_muy_bajo_aporte': FoodCategory.ANIMAL_PRODUCTS,
    'carnes_bajo_aporte': FoodCategory.ANIMAL_PRODUCTS,
    'carnes_moderado_aporte': FoodCategory.ANIMAL_PRODUCTS,
    'carnes_alto_aporte': FoodCategory.ANIMAL_PRODUCTS,
    'grasas_sin_proteina': FoodCategory.FATS,
    'grasas_con_proteina': FoodCategory.FATS,
    'azucares_sin_grasa': FoodCategory.SUGARS,
    'azucares_con_grasa': FoodCategory.SUGARS,
    'bebida_libre': FoodCategory.BEVERAGES
}

def parse_js_foods_file(file_path: str):
    """Parse el archivo JS de alimentos mexicanos"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar el array ALIMENTOS_MEXICANOS
    match = re.search(r'export const ALIMENTOS_MEXICANOS = \[(.*?)\];', content, re.DOTALL)
    if not match:
        raise ValueError("No se encontró ALIMENTOS_MEXICANOS en el archivo")

    array_content = match.group(1)

    # Reemplazar las comillas simples con dobles para JSON
    # Primero proteger las comillas dentro de strings
    array_content = array_content.replace("'", '"')

    # Arreglar referencias a CATEGORIAS_EQUIVALENTES
    array_content = re.sub(
        r'categoria_equivalente:\s*"([^"]+)"',
        lambda m: f'categoria_equivalente: "{m.group(1)}"',
        array_content
    )

    # Convertir a formato JSON válido
    array_content = re.sub(r'(\w+):', r'"\1":', array_content)
    array_content = re.sub(r',\s*}', '}', array_content)
    array_content = re.sub(r',\s*\]', ']', array_content)

    # Parsear como JSON
    try:
        foods_data = json.loads(f'[{array_content}]')
        return foods_data
    except json.JSONDecodeError as e:
        print(f"Error parseando JSON: {e}")
        # Plan B: extraer manualmente los objetos
        return extract_foods_manually(content)

def extract_foods_manually(content: str):
    """Extracción manual de alimentos si falla el parsing JSON"""
    foods = []

    # Pattern para encontrar cada objeto alimento
    pattern = r'\{[^}]+id:\s*["\']([^"\']+)["\'][^}]*nombre:\s*["\']([^"\']+)["\'][^}]*\}'

    # Buscar todos los bloques que empiezan con { y terminan con },
    objects = re.findall(r'\{[^}]+\}', content, re.DOTALL)

    for obj_str in objects:
        if 'id:' in obj_str and 'nombre:' in obj_str:
            try:
                # Extraer campos clave manualmente
                food = {}

                # ID
                id_match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", obj_str)
                if id_match:
                    food['id'] = id_match.group(1)

                # Nombre
                name_match = re.search(r"nombre:\s*['\"]([^'\"]+)['\"]", obj_str)
                if name_match:
                    food['nombre'] = name_match.group(1)

                # Categoría
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

                # Nombres regionales
                nombres_match = re.search(r"nombres_regionales:\s*\[([^\]]+)\]", obj_str)
                if nombres_match:
                    nombres = re.findall(r"['\"]([^'\"]+)['\"]", nombres_match.group(1))
                    food['nombres_regionales'] = nombres

                # Región origen
                region_match = re.search(r"region_origen:\s*\[([^\]]+)\]", obj_str)
                if region_match:
                    regiones = re.findall(r"['\"]([^'\"]+)['\"]", region_match.group(1))
                    food['region_origen'] = regiones

                # Alérgenos
                alergenos_match = re.search(r"potencial_alergeno:\s*\[([^\]]*)\]", obj_str)
                if alergenos_match:
                    alergenos_str = alergenos_match.group(1)
                    if alergenos_str.strip():
                        alergenos = re.findall(r"['\"]([^'\"]+)['\"]", alergenos_str)
                        food['potencial_alergeno'] = alergenos
                    else:
                        food['potencial_alergeno'] = []

                if 'id' in food and 'nombre' in food:
                    foods.append(food)

            except Exception as e:
                print(f"Error extrayendo alimento: {e}")
                continue

    return foods

def extract_serving_size(cantidad_porcion: str):
    """Extrae el tamaño de porción en gramos de la string"""
    # Buscar números seguidos de 'g' o 'ml'
    match = re.search(r'(\d+\.?\d*)\s*(g|ml)', cantidad_porcion)
    if match:
        return float(match.group(1))

    # Si no hay unidad explícita, asumir 100g
    return 100.0

def create_food_from_data(food_data: dict) -> Food:
    """Crea un objeto Food desde los datos parseados"""

    # Mapear categoría
    categoria_smae = food_data.get('categoria_equivalente', '').replace('CATEGORIAS_EQUIVALENTES.', '')
    categoria = CATEGORY_MAP.get(categoria_smae, FoodCategory.CEREALS)

    # Extraer tamaño de porción
    cantidad_porcion = food_data.get('cantidad_porcion', '100g')
    serving_size = extract_serving_size(cantidad_porcion)

    # Crear objeto Food
    food = Food(
        name=food_data.get('nombre', ''),
        common_names=food_data.get('nombres_regionales', []),
        category=categoria,
        subcategory=categoria_smae,
        base_unit=MeasurementUnit.GRAMS,
        serving_size=serving_size,

        # Macronutrientes
        calories_per_serving=food_data.get('calorias', 0),
        protein_g=food_data.get('proteina_g', 0),
        carbs_g=food_data.get('carbohidratos_g', 0),
        fat_g=food_data.get('grasa_g', 0),
        fiber_g=food_data.get('fibra_g', 0),
        sugar_g=0.0,  # No está en los datos SMAE
        sodium_mg=0.0,  # No está en los datos SMAE

        # Micronutrientes
        vitamins={
            'vitamin_a_mcg': food_data.get('vitamina_a_mcg', 0),
            'vitamin_c_mg': food_data.get('vitamina_c_mg', 0),
            'folate_mcg': food_data.get('folato_mcg', 0)
        },
        minerals={
            'calcium_mg': food_data.get('calcio_mg', 0),
            'iron_mg': food_data.get('hierro_mg', 0)
        },

        # Índice glucémico
        glycemic_index=food_data.get('indice_glucemico'),

        # Alérgenos
        allergens=food_data.get('potencial_alergeno', []),

        # Banderas dietéticas
        dietary_flags=['traditional_mexican'] if food_data.get('es_tradicional_mexicano', False) else [],

        # Metadata
        description=food_data.get('descripcion', ''),
        source='SMAE (Sistema Mexicano de Alimentos Equivalentes)',
        image_url=food_data.get('imagen_url'),

        # Información regional
        region=', '.join(food_data.get('region_origen', [])),
        seasonal_availability=food_data.get('temporada', []),

        # Keywords para búsqueda
        search_keywords=food_data.get('nombres_regionales', []) + [food_data.get('nombre', '')],

        # Estado aprobado (es data oficial SMAE)
        status=FoodStatus.APPROVED,
        approved_at=None
    )

    return food

def populate_database():
    """Pobla la base de datos con los alimentos SMAE"""

    # Leer archivo de alimentos
    frontend_path = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'data' / 'alimentosMexicanos.js'

    print(f"Leyendo alimentos desde: {frontend_path}")
    print(f"Path absoluto: {frontend_path.absolute()}")
    print(f"Existe: {frontend_path.exists()}")

    if not frontend_path.exists():
        print(f"ERROR: No se encontró el archivo {frontend_path}")
        print(f"Buscando en path alternativo...")
        # Try alternative path for Docker environment
        alt_path = Path('/app') / 'frontend' / 'src' / 'data' / 'alimentosMexicanos.js'
        print(f"Intentando: {alt_path}")
        if alt_path.exists():
            frontend_path = alt_path
            print(f"✓ Encontrado en: {frontend_path}")
        else:
            print(f"ERROR: No se encontró el archivo en ninguna ubicación")
            return

    # Parsear archivo
    print("Parseando archivo JS...")
    foods_data = extract_foods_manually(open(frontend_path, 'r', encoding='utf-8').read())

    print(f"Se encontraron {len(foods_data)} alimentos")

    # Conectar a base de datos (usar settings para obtener DATABASE_URL de producción)
    settings = get_settings()

    # Convertir async driver (asyncpg) a sync driver (psycopg2) para create_all
    db_url = settings.database_url.replace('postgresql+asyncpg', 'postgresql+psycopg2')

    print(f"Conectando a base de datos...")
    print(f"Driver: psycopg2 (sync)")

    engine = create_engine(db_url, echo=False)

    # Crear tablas si no existen
    SQLModel.metadata.create_all(engine)

    # Insertar alimentos
    with Session(engine) as session:
        foods_added = 0
        foods_skipped = 0

        for food_data in foods_data:
            try:
                # Verificar si ya existe
                existing = session.query(Food).filter(
                    Food.name == food_data.get('nombre', '')
                ).first()

                if existing:
                    print(f"[SKIP] Omitiendo (ya existe): {food_data.get('nombre', '')}")
                    foods_skipped += 1
                    continue

                # Crear y agregar
                food = create_food_from_data(food_data)
                session.add(food)
                foods_added += 1

                print(f"[OK] Agregado: {food.name} ({food.category})")

            except Exception as e:
                print(f"[ERROR] Error procesando {food_data.get('nombre', 'unknown')}: {str(e)}")
                continue

        # Commit
        session.commit()

        print(f"\n{'='*60}")
        print(f"Proceso completado!")
        print(f"   Alimentos agregados: {foods_added}")
        print(f"   Alimentos omitidos: {foods_skipped}")
        print(f"   Total en archivo: {len(foods_data)}")
        print(f"{'='*60}")

if __name__ == "__main__":
    try:
        populate_database()
    except Exception as e:
        print(f"ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
