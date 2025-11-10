"""Script para verificar los alimentos SMAE en la base de datos"""
import sqlite3
from pathlib import Path

# Conectar a la base de datos
db_path = Path(__file__).parent.parent / 'nutrition_intelligence.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Contar total de alimentos SMAE
cursor.execute("SELECT COUNT(*) FROM foods WHERE source LIKE '%SMAE%'")
total = cursor.fetchone()[0]

print(f"\n{'='*60}")
print(f"ALIMENTOS SMAE EN LA BASE DE DATOS")
print(f"{'='*60}")
print(f"Total de alimentos SMAE: {total}")

# Mostrar primeros 15 alimentos
print(f"\nPrimeros 15 alimentos:")
print(f"{'-'*60}")
cursor.execute("""
    SELECT name, category, calories_per_serving, protein_g, carbs_g, fat_g
    FROM foods
    WHERE source LIKE '%SMAE%'
    LIMIT 15
""")

for row in cursor.fetchall():
    name, category, calories, protein, carbs, fat = row
    print(f"• {name}")
    print(f"  Categoría: {category}")
    print(f"  Macros: {calories} kcal | Proteína: {protein}g | Carbs: {carbs}g | Grasa: {fat}g")
    print()

# Contar por categoría
print(f"\n{'='*60}")
print(f"DISTRIBUCIÓN POR CATEGORÍA")
print(f"{'='*60}")
cursor.execute("""
    SELECT category, COUNT(*) as count
    FROM foods
    WHERE source LIKE '%SMAE%'
    GROUP BY category
    ORDER BY count DESC
""")

for category, count in cursor.fetchall():
    print(f"  {category}: {count} alimentos")

print(f"\n{'='*60}")

conn.close()
