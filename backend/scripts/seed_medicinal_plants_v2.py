"""
Seed script for Mexican Medicinal Plants - Version 2
Based on UNAM's Atlas de las Plantas de la Medicina Tradicional Mexicana
Matches the actual database schema
"""
import sys
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from core.database import engine
from domain.medicinal_plants.models import (
    MedicinalPlant,
    PlantCategory,
    EvidenceLevel,
    SafetyLevel,
    PreparationType
)


MEDICINAL_PLANTS = [
    {
        "scientific_name": "Matricaria chamomilla",
        "botanical_family": "Asteraceae",
        "popular_names": ["Manzanilla", "Camomila"],
        "indigenous_names": None,
        "states_found": ["Puebla", "Tlaxcala", "Estado de México", "Hidalgo"],
        "origin_region": "Europa, naturalizada en México",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.CALMING],
        "traditional_uses": [
            "Cólicos estomacales e intestinales",
            "Indigestión y gases",
            "Nerviosismo y ansiedad leve",
            "Inflamación ocular",
            "Dolor menstrual"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de flores secas por taza",
                "preparation": "Agregar agua hirviendo sobre las flores y dejar reposar 5-10 minutos tapado",
                "frequency": "2-3 tazas al día después de las comidas",
                "duration": None
            }
        ],
        "active_compounds": ["Apigenina", "Bisabolol", "Camazuleno", "Flavonoides"],
        "pharmacological_actions": ["Espasmolítica", "Carminativa", "Sedante leve", "Antiinflamatoria"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Evitar en personas alérgicas a plantas de la familia Asteraceae.",
        "contraindications": "Alergia conocida a la manzanilla o plantas relacionadas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=matricaria-recutita",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Una de las plantas medicinales más seguras y efectivas, ampliamente utilizada en México."
    },
    {
        "scientific_name": "Mentha spicata",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Hierbabuena", "Yerba buena"],
        "indigenous_names": None,
        "states_found": ["Todo México"],
        "origin_region": "Europa y Asia, naturalizada globalmente",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": None,
        "traditional_uses": [
            "Dolor de estómago y cólicos",
            "Náuseas y vómito",
            "Gases intestinales",
            "Mal aliento",
            "Dolor de cabeza"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "2-3 hojas frescas o 1 cucharadita de hojas secas por taza",
                "preparation": "Agregar agua hirviendo y reposar 5 minutos",
                "frequency": "2-3 tazas al día",
                "duration": None
            },
            {
                "type": PreparationType.FRESH.value,
                "dosage": "2-3 hojas",
                "preparation": "Masticar hojas frescas directamente",
                "frequency": "Según necesidad para mal aliento",
                "duration": None
            }
        ],
        "active_compounds": ["Mentol", "Mentona", "Carvona", "Limoneno"],
        "pharmacological_actions": ["Carminativa", "Antiespasmódica", "Aromática"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Usar con moderación en niños pequeños. Evitar aceite esencial concentrado en bebés.",
        "contraindications": "Reflujo gastroesofágico severo.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=mentha-spicata",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Muy popular en mercados mexicanos, fresca o seca."
    },
    {
        "scientific_name": "Opuntia ficus-indica",
        "botanical_family": "Cactaceae",
        "popular_names": ["Nopal", "Nopal verdura"],
        "indigenous_names": {"Náhuatl": "Nohpalli"},
        "states_found": ["Todo México"],
        "origin_region": "Nativo de México",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Diabetes (control de glucosa)",
            "Colesterol alto",
            "Sobrepeso",
            "Inflamación",
            "Salud digestiva"
        ],
        "indigenous_uses": {
            "Náhuatl": ["Alimento básico", "Medicina digestiva"],
            "Otomí": ["Control de azúcar"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.FRESH.value,
                "dosage": "1-2 pencas medianas limpias",
                "preparation": "Limpiar espinas, cortar y consumir crudo en ensaladas o cocido",
                "frequency": "Diario, preferentemente en ayunas",
                "duration": "Uso continuo"
            },
            {
                "type": PreparationType.JUICE.value,
                "dosage": "1 penca cruda",
                "preparation": "Licuar con agua, colar inmediatamente",
                "frequency": "1 vaso en ayunas",
                "duration": None
            }
        ],
        "active_compounds": ["Fibra soluble (mucílago)", "Pectina", "Flavonoides", "Betalaínas", "Vitaminas C, A, K"],
        "pharmacological_actions": ["Hipoglucemiante", "Hipolipemiante", "Antiinflamatorio", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar diarrea por alto contenido de fibra. Iniciar con cantidades pequeñas.",
        "contraindications": "Obstrucción intestinal.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "interactions": "Puede potenciar medicamentos para diabetes - monitorear glucosa",
        "mexican_sources": ["Tiendas Bienestar"],
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=opuntia-ficus-indica",
        "bienestar_store_available": True,
        "local_market_price": 5.0,
        "image_url": None,
        "notes": "Símbolo nacional de México, alimento y medicina ancestral de gran valor nutricional."
    },
    {
        "scientific_name": "Amphipterygium adstringens",
        "botanical_family": "Anacardiaceae",
        "popular_names": ["Cuachalalate", "Cuachalala"],
        "indigenous_names": {"Náhuatl": "Cuauchachalatli"},
        "states_found": ["Jalisco", "Michoacán", "Guerrero", "Oaxaca"],
        "origin_region": "Endémica de México",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.WOUND_HEALING],
        "traditional_uses": [
            "Úlceras gástricas",
            "Gastritis",
            "Colitis",
            "Infecciones gastrointestinales",
            "Cicatrización de heridas (tópico)"
        ],
        "indigenous_uses": {
            "Purépecha": ["Problemas estomacales"],
            "Náhuatl": ["Corteza medicinal para estómago"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.DECOCTION.value,
                "dosage": "1 cucharada de corteza por litro de agua",
                "preparation": "Hervir la corteza a fuego lento durante 15-20 minutos",
                "frequency": "1 taza 3 veces al día antes de comidas",
                "duration": "2-4 semanas"
            }
        ],
        "active_compounds": ["Taninos", "Flavonoides", "Triterpenos", "Anacardios"],
        "pharmacological_actions": ["Antiulceroso", "Gastroprotector", "Cicatrizante", "Antibacteriano"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Puede causar estreñimiento con uso prolongado por su contenido de taninos.",
        "contraindications": "Estreñimiento crónico.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 12,
        "interactions": None,
        "mexican_sources": ["Mercados tradicionales"],
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=amphipterygium-adstringens",
        "bienestar_store_available": False,
        "local_market_price": 30.0,
        "image_url": None,
        "notes": "Planta endémica mexicana con evidencia científica sólida para problemas digestivos."
    },
    {
        "scientific_name": "Aloe vera",
        "botanical_family": "Asphodelaceae",
        "popular_names": ["Sábila", "Aloe"],
        "indigenous_names": None,
        "states_found": ["Todo México, especialmente zonas cálidas"],
        "origin_region": "África, ampliamente cultivada en México",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.SKIN_HAIR,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Quemaduras leves y solares",
            "Heridas superficiales",
            "Irritación de piel",
            "Estreñimiento (gel interno)",
            "Gastritis (uso interno con precaución)"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Cantidad necesaria de gel fresco",
                "preparation": "Cortar hoja, extraer gel transparente y aplicar directamente sobre piel limpia",
                "frequency": "2-3 veces al día según necesidad",
                "duration": None
            },
            {
                "type": PreparationType.JUICE.value,
                "dosage": "1/4 taza de gel interno",
                "preparation": "Licuar gel transparente con agua o jugo. NUNCA USAR LA CÁSCARA.",
                "frequency": "1-2 veces al día (uso ocasional)",
                "duration": "Máximo 1-2 semanas"
            }
        ],
        "active_compounds": ["Acemanano", "Aloína", "Polisacáridos", "Vitaminas A, C, E"],
        "pharmacological_actions": ["Cicatrizante", "Antiinflamatorio", "Laxante", "Inmunomodulador"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Uso interno: NUNCA usar la cáscara (látex amarillo), solo gel transparente. No usar internamente por más de 1-2 semanas.",
        "contraindications": "Embarazo y lactancia (uso interno). Problemas renales. Obstrucción intestinal.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 12,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=aloe-vera",
        "bienestar_store_available": False,
        "local_market_price": 15.0,
        "image_url": None,
        "notes": "Muy popular en México para problemas de piel. Uso tópico muy seguro, interno requiere precaución."
    }
]


def seed_medicinal_plants():
    """Seed the database with Mexican medicinal plants data"""
    print("[*] Starting medicinal plants seeding...")

    with Session(engine) as session:
        # Check if plants already exist
        existing_count = session.exec(select(MedicinalPlant)).all()
        if existing_count:
            print(f"[!] Database already contains {len(existing_count)} plants.")
            response = input("Do you want to clear and re-seed? (yes/no): ")
            if response.lower() != 'yes':
                print("[X] Seeding cancelled.")
                return

            # Clear existing data
            print("[*] Clearing existing plants...")
            for plant in existing_count:
                session.delete(plant)
            session.commit()

        # Add all plants
        plants_added = 0
        for plant_data in MEDICINAL_PLANTS:
            try:
                plant = MedicinalPlant(**plant_data)
                session.add(plant)
                plants_added += 1
                print(f"[OK] Added: {plant.popular_names[0]} ({plant.scientific_name})")
            except Exception as e:
                print(f"[ERROR] Error adding {plant_data.get('scientific_name', 'Unknown')}: {e}")
                continue

        # Commit all changes
        session.commit()
        print(f"\n[SUCCESS] Successfully seeded {plants_added} medicinal plants!")

        # Show summary by category
        print("\n[INFO] Plants by category:")
        categories = {}
        all_plants = session.exec(select(MedicinalPlant)).all()
        for plant in all_plants:
            cat = plant.primary_category.value
            categories[cat] = categories.get(cat, 0) + 1

        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} plants")


if __name__ == "__main__":
    seed_medicinal_plants()
