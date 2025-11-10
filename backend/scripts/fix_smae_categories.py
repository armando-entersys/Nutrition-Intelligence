"""
Script para corregir las categorías de los alimentos SMAE en la base de datos
"""
import sys
import sqlite3
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Mapeo manual de alimentos a categorías correctas
# Basado en la estructura del archivo alimentosMexicanos.js
FOOD_CATEGORY_MAPPING = {
    # CEREALES_SIN_GRASA -> CEREALS
    'Tortilla de maíz': 'CEREALS',
    'Tortilla de harina integral': 'CEREALS',
    'Tostadas horneadas': 'CEREALS',
    'Amaranto tostado': 'CEREALS',
    'Elote (maíz) hervido': 'CEREALS',
    'Pan integral mexicano': 'CEREALS',
    'Tamal de pollo (sin manteca)': 'CEREALS',
    'Gordita de maíz integral': 'CEREALS',

    # LEGUMINOSAS -> LEGUMES
    'Frijoles negros cocidos': 'LEGUMES',
    'Frijoles pintos cocidos': 'LEGUMES',
    'Lentejas cocidas': 'LEGUMES',
    'Garbanzos cocidos': 'LEGUMES',
    'Habas cocidas': 'LEGUMES',

    # VERDURAS -> VEGETABLES
    'Nopal asado': 'VEGETABLES',
    'Chayote cocido': 'VEGETABLES',
    'Flor de calabaza': 'VEGETABLES',
    'Calabacita italiana': 'VEGETABLES',
    'Jitomate (tomate rojo)': 'VEGETABLES',
    'Chile poblano': 'VEGETABLES',
    'Quelites (quintoniles)': 'VEGETABLES',
    'Verdolagas': 'VEGETABLES',
    'Espinacas': 'VEGETABLES',
    'Huitlacoche': 'VEGETABLES',

    # FRUTAS -> FRUITS
    'Papaya maradol': 'FRUITS',
    'Mango ataulfo': 'FRUITS',
    'Guayaba': 'FRUITS',
    'Tuna (nopal)': 'FRUITS',
    'Mamey': 'FRUITS',
    'Tejocote': 'FRUITS',
    'Plátano macho': 'FRUITS',
    'Zapote negro': 'FRUITS',
    'Chicozapote': 'FRUITS',
    'Ciruela mexicana': 'FRUITS',

    # GRASAS -> FATS
    'Aguacate hass': 'FATS',
    'Pepitas de calabaza tostadas': 'FATS',
    'Aceite de aguacate': 'FATS',
    'Aceite de oliva extra virgen': 'FATS',
    'Cacahuates naturales': 'FATS',
    'Nueces de Castilla': 'FATS',
    'Almendras': 'FATS',

    # BEBIDAS -> BEVERAGES
    'Agua de jamaica sin azúcar': 'BEVERAGES',
    'Agua de horchata light (sin azúcar)': 'BEVERAGES',

    # CARNES -> ANIMAL_PRODUCTS
    'Pechuga de pollo sin piel': 'ANIMAL_PRODUCTS',
    'Pescado blanco (tilapia/mojarra)': 'ANIMAL_PRODUCTS',
    'Atún en agua': 'ANIMAL_PRODUCTS',
    'Chapulines tostados': 'ANIMAL_PRODUCTS',
    'Escamoles': 'ANIMAL_PRODUCTS',
    'Carne de res magra (bistec)': 'ANIMAL_PRODUCTS',
    'Lomo de cerdo': 'ANIMAL_PRODUCTS',

    # LECHE -> DAIRY
    'Leche descremada': 'DAIRY',
    'Leche de almendra sin azúcar': 'DAIRY',

    # AZUCARES -> SUGARS
    'Miel de abeja natural': 'SUGARS',
    'Piloncillo (panela)': 'SUGARS',
}

def fix_categories():
    """Corrige las categorías de los alimentos SMAE"""

    db_path = Path(__file__).parent.parent / 'nutrition_intelligence.db'

    print("Conectando a base de datos...")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        print(f"\n{'='*60}")
        print("CORRIGIENDO CATEGORÍAS DE ALIMENTOS SMAE")
        print(f"{'='*60}\n")

        updated_count = 0
        not_found_count = 0

        for food_name, correct_category in FOOD_CATEGORY_MAPPING.items():
            # Buscar el alimento
            cursor.execute(
                "SELECT id, category FROM foods WHERE name = ? AND source LIKE '%SMAE%'",
                (food_name,)
            )
            result = cursor.fetchone()

            if result:
                food_id, current_category = result

                if current_category != correct_category:
                    # Actualizar la categoría
                    cursor.execute(
                        "UPDATE foods SET category = ? WHERE id = ?",
                        (correct_category, food_id)
                    )
                    print(f"✅ {food_name}")
                    print(f"   {current_category} → {correct_category}")
                    updated_count += 1
                else:
                    print(f"⏭️  {food_name} - Ya tiene la categoría correcta ({correct_category})")
            else:
                print(f"⚠️  No encontrado: {food_name}")
                not_found_count += 1

        # Commit cambios
        conn.commit()

        print(f"\n{'='*60}")
        print(f"RESULTADO")
        print(f"{'='*60}")
        print(f"Alimentos actualizados: {updated_count}")
        print(f"Alimentos no encontrados: {not_found_count}")
        print(f"Total procesados: {len(FOOD_CATEGORY_MAPPING)}")
        print(f"{'='*60}\n")

        # Mostrar distribución actualizada
        print("DISTRIBUCIÓN POR CATEGORÍA DESPUÉS DE LA CORRECCIÓN:")
        print(f"{'-'*60}")
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM foods
            WHERE source LIKE '%SMAE%'
            GROUP BY category
            ORDER BY count DESC
        """)

        for category, count in cursor.fetchall():
            print(f"  {category}: {count} alimentos")

        print(f"\n{'='*60}\n")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    try:
        fix_categories()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
