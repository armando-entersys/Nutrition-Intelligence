"""
Seed data for Trophology (Food Categories and Compatibility Rules)
Based on Manuel Lezaeta Acharán's "La Medicina Natural al Alcance de Todos" (1927)
Capítulo XXV "Trofología" (Páginas 112-121)
"""
import sys
from pathlib import Path

# Add parent directory to path to import from domain
sys.path.append(str(Path(__file__).parent.parent))

from sqlmodel import Session, create_engine, select
from core.config import get_settings
from domain.trophology.models import FoodCategory, FoodCompatibility, CompatibilitySeverity

def seed_food_categories(session: Session) -> dict[str, FoodCategory]:
    """
    Seed the 9 food categories according to Lezaeta's Trophology

    Categories are based on page references from the book
    """
    categories_data = [
        {
            "name": "Frutas Ácidas",
            "description": "Frutas con alto contenido de ácidos. Combinan bien con frutas aceitosas.",
            "examples": "naranjas, limones, piñas, fresas, toronjas, mandarinas"
        },
        {
            "name": "Frutas Dulces",
            "description": "Frutas con alto contenido de azúcares naturales. Combinan bien con almidones harináceos.",
            "examples": "pasas, higos, dátiles, plátanos maduros, ciruelas secas"
        },
        {
            "name": "Frutas Aceitosas",
            "description": "Frutas ricas en aceites y grasas saludables. Combinan bien con frutas ácidas.",
            "examples": "nueces, avellanas, almendras, aceitunas, aguacate"
        },
        {
            "name": "Frutas Harináceas",
            "description": "Frutas con alto contenido de almidón. Combinan bien con frutas dulces jugosas.",
            "examples": "castañas, plátanos verdes, bellotas"
        },
        {
            "name": "Almidones",
            "description": "Alimentos ricos en almidón y fécula. NO mezclar papas con cereales o pan.",
            "examples": "papas, trigo, maíz, arroz, quaker, avena, cebada, pan"
        },
        {
            "name": "Hortalizas/Verduras",
            "description": "Vegetales ricos en sales minerales. Combinan bien con cereales y papas, pero NO con frutas.",
            "examples": "lechuga, zanahoria, apio, espinaca, brócoli, col, pepino, tomate"
        },
        {
            "name": "Proteínas",
            "description": "Alimentos ricos en proteínas. Huevos combinan con toda clase de vegetales.",
            "examples": "huevos, queso, leche, frejoles, lentejas, garbanzos, arvejas"
        },
        {
            "name": "Azúcares",
            "description": "Azúcares simples y miel. NO mezclar con hortalizas ni con aceitunas.",
            "examples": "miel, azúcar, panela, piloncillo"
        },
        {
            "name": "Grasas",
            "description": "Aceites y grasas. NO mezclar con frutas dulces o azúcares.",
            "examples": "aceite de oliva, aceite vegetal, mantequilla, aceitunas"
        }
    ]

    categories = {}

    for cat_data in categories_data:
        # Check if category already exists
        statement = select(FoodCategory).where(FoodCategory.name == cat_data["name"])
        existing = session.exec(statement).first()

        if existing:
            print(f"✓ Categoría '{cat_data['name']}' ya existe (ID: {existing.id})")
            categories[cat_data["name"]] = existing
        else:
            category = FoodCategory(**cat_data)
            session.add(category)
            session.commit()
            session.refresh(category)
            categories[cat_data["name"]] = category
            print(f"✓ Categoría '{cat_data['name']}' creada (ID: {category.id})")

    return categories


def seed_food_compatibilities(session: Session, categories: dict[str, FoodCategory]):
    """
    Seed compatibility rules between food categories
    Based on Lezaeta's combination rules (Páginas 118-119)
    """

    # MALAS COMBINACIONES (Incompatible combinations)
    incompatibilities = [
        {
            "cat1": "Frutas Aceitosas",
            "cat2": "Frutas Dulces",
            "reason": "Los aceites al mezclarse con los azúcares producen fermentaciones alcohólicas, recargando la sangre de productos nocivos.",
            "severity": CompatibilitySeverity.HIGH,
            "page": "Página 118"
        },
        {
            "cat1": "Frutas Ácidas",
            "cat2": "Almidones",
            "reason": "Los ácidos impiden el desdoblamiento normal de los almidones en maltosa y glucosa, originando fermentación por detenerse en los intestinos mayor tiempo del debido.",
            "severity": CompatibilitySeverity.HIGH,
            "page": "Página 118"
        },
        {
            "cat1": "Frutas Dulces",
            "cat2": "Frutas Ácidas",
            "reason": "Producen fermentaciones intestinales tóxicas.",
            "severity": CompatibilitySeverity.HIGH,
            "page": "Página 118"
        },
        {
            "cat1": "Almidones",
            "cat2": "Almidones",  # Specifically: potatoes with cereals/bread
            "reason": "La fécula de las papas con el almidón de los cereales generalmente no se digieren simultáneamente, entrando en fermentación malsana. NO MEZCLAR PAPAS CON PAN O CEREALES.",
            "severity": CompatibilitySeverity.HIGH,
            "note": "Regla crítica de Lezaeta: Papas y pan/cereales deben consumirse en comidas separadas",
            "page": "Página 118-119"
        },
        {
            "cat1": "Proteínas",
            "cat2": "Proteínas",  # Specifically: milk with eggs, eggs with cheese
            "reason": "Una de estas sustancias puede ser digerida con preferencia a la otra que entrará en descomposición. Aplicable a: leche con huevos, huevos con queso.",
            "severity": CompatibilitySeverity.MEDIUM,
            "page": "Página 119"
        },
        {
            "cat1": "Hortalizas/Verduras",
            "cat2": "Frutas Dulces",
            "reason": "Las verduras contienen en gran proporción sales minerales y las frutas contienen ácidos y azúcares. Alimentos de naturaleza opuesta producen fácilmente fermentaciones.",
            "severity": CompatibilitySeverity.HIGH,
            "page": "Página 119"
        },
        {
            "cat1": "Hortalizas/Verduras",
            "cat2": "Frutas Ácidas",
            "reason": "Sales minerales con ácidos y azúcares (alimentos de naturaleza opuesta) producen fermentaciones.",
            "severity": CompatibilitySeverity.HIGH,
            "page": "Página 119"
        },
        {
            "cat1": "Azúcares",
            "cat2": "Hortalizas/Verduras",
            "reason": "Sales minerales con ácidos y azúcares no deben comerse juntos.",
            "severity": CompatibilitySeverity.MEDIUM,
            "page": "Página 119"
        },
        {
            "cat1": "Azúcares",
            "cat2": "Frutas Aceitosas",
            "reason": "Azúcares con aceitunas o aceites producen fermentaciones alcohólicas.",
            "severity": CompatibilitySeverity.MEDIUM,
            "page": "Página 118-119"
        },
        {
            "cat1": "Grasas",
            "cat2": "Frutas Dulces",
            "reason": "Aceitunas o aceites con frutas dulces o secas (azúcares) producen fermentaciones alcohólicas.",
            "severity": CompatibilitySeverity.MEDIUM,
            "page": "Página 118-119"
        },
        {
            "cat1": "Proteínas",
            "cat2": "Hortalizas/Verduras",  # Specifically: milk with vegetables
            "reason": "Leche con hortaliza produce mala combinación.",
            "severity": CompatibilitySeverity.MEDIUM,
            "note": "Aplicable específicamente a leche con verduras. Huevos SÍ combinan bien con vegetales.",
            "page": "Página 119"
        }
    ]

    # BUENAS COMBINACIONES (Compatible combinations)
    compatibilities = [
        {
            "cat1": "Frutas Ácidas",
            "cat2": "Frutas Aceitosas",
            "reason": "Las frutas ácidas combinan bien con las aceitosas.",
            "note": "Importante: comer primero las ácidas (naranjas con nueces o avellanas)",
            "page": "Página 118"
        },
        {
            "cat1": "Frutas Dulces",
            "cat2": "Frutas Harináceas",
            "reason": "Las frutas dulces jugosas combinan bien con los almidones que contienen las castañas o plátanos.",
            "page": "Página 118"
        },
        {
            "cat1": "Frutas Harináceas",
            "cat2": "Almidones",
            "reason": "Frutas harináceas con cereales o pan combinan bien.",
            "page": "Página 119"
        },
        {
            "cat1": "Hortalizas/Verduras",
            "cat2": "Almidones",
            "reason": "Hortaliza con cereales, papas, o ensaladas con cereales/papas y aceite combinan bien.",
            "page": "Página 119"
        },
        {
            "cat1": "Frutas Aceitosas",
            "cat2": "Almidones",
            "reason": "Nueces con cereales u hortaliza combinan bien.",
            "page": "Página 119"
        },
        {
            "cat1": "Proteínas",
            "cat2": "Almidones",
            "reason": "Queso con cereales, pan o papas combina bien. Legumbres secas con hortaliza también.",
            "note": "NO aplicable a leche con huevos, huevos con queso",
            "page": "Página 119"
        },
        {
            "cat1": "Almidones",
            "cat2": "Frutas Dulces",
            "reason": "Cereales con frutas secas combinan bien.",
            "page": "Página 119"
        },
        {
            "cat1": "Proteínas",
            "cat2": "Hortalizas/Verduras",
            "reason": "Huevos con toda clase de vegetales combinan bien. Pan con frutas, dulces, hortalizas, leche, miel, huevos, aceite.",
            "note": "Huevos son muy versátiles. Leche con hortalizas NO es recomendable.",
            "page": "Página 119"
        }
    ]

    print("\n--- CREANDO INCOMPATIBILIDADES ---")
    for incomp in incompatibilities:
        cat1 = categories[incomp["cat1"]]
        cat2 = categories[incomp["cat2"]]

        # Check if already exists
        statement = select(FoodCompatibility).where(
            (
                (FoodCompatibility.category1_id == cat1.id) &
                (FoodCompatibility.category2_id == cat2.id)
            ) | (
                (FoodCompatibility.category1_id == cat2.id) &
                (FoodCompatibility.category2_id == cat1.id)
            )
        )
        existing = session.exec(statement).first()

        if existing:
            print(f"✓ Incompatibilidad '{incomp['cat1']} + {incomp['cat2']}' ya existe")
            continue

        compatibility = FoodCompatibility(
            category1_id=cat1.id,
            category2_id=cat2.id,
            compatible=False,
            reason=incomp["reason"],
            severity=incomp["severity"],
            note=incomp.get("note"),
            page_reference=incomp["page"]
        )
        session.add(compatibility)
        print(f"✗ Incompatibilidad: {incomp['cat1']} + {incomp['cat2']} [{incomp['severity'].value}]")

    print("\n--- CREANDO COMPATIBILIDADES ---")
    for comp in compatibilities:
        cat1 = categories[comp["cat1"]]
        cat2 = categories[comp["cat2"]]

        # Check if already exists
        statement = select(FoodCompatibility).where(
            (
                (FoodCompatibility.category1_id == cat1.id) &
                (FoodCompatibility.category2_id == cat2.id)
            ) | (
                (FoodCompatibility.category1_id == cat2.id) &
                (FoodCompatibility.category2_id == cat1.id)
            )
        )
        existing = session.exec(statement).first()

        if existing:
            print(f"✓ Compatibilidad '{comp['cat1']} + {comp['cat2']}' ya existe")
            continue

        compatibility = FoodCompatibility(
            category1_id=cat1.id,
            category2_id=cat2.id,
            compatible=True,
            reason=comp["reason"],
            severity=None,  # No severity for compatible combinations
            note=comp.get("note"),
            page_reference=comp["page"]
        )
        session.add(compatibility)
        print(f"✓ Compatibilidad: {comp['cat1']} + {comp['cat2']}")

    session.commit()
    print("\n✅ Todas las compatibilidades/incompatibilidades creadas")


def main():
    """Main seeding function"""
    print("=" * 80)
    print("SEED DATA: TROFOLOGÍA DE MANUEL LEZAETA ACHARÁN (1927)")
    print("=" * 80)
    print("\nBasado en: 'La Medicina Natural al Alcance de Todos'")
    print("Capítulo XXV 'Trofología' (Páginas 112-121)\n")

    # Get database URL from settings
    settings = get_settings()
    engine = create_engine(str(settings.database_url))

    with Session(engine) as session:
        print("--- PASO 1: CATEGORÍAS DE ALIMENTOS ---")
        categories = seed_food_categories(session)

        print(f"\n✅ {len(categories)} categorías creadas/verificadas\n")

        print("--- PASO 2: REGLAS DE COMPATIBILIDAD ---")
        seed_food_compatibilities(session, categories)

    print("\n" + "=" * 80)
    print("✅ SEED DATA COMPLETADO")
    print("=" * 80)
    print("\nPrincipio fundamental de Lezaeta:")
    print('  "No hay enfermo con buena digestión, ni persona sana con mala digestión"')
    print("  (Página 113)")
    print("\nRegla de oro:")
    print('  "Simplificar cada comida a uno o dos productos"')
    print("  (Página 119)")
    print("\nSeñal de buena digestión:")
    print('  "Excrementos inodoros, color bronce y no duros ni diarreicos"')
    print("  (Página 115)")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
