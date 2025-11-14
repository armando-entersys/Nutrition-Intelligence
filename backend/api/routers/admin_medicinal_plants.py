"""
Admin endpoints for medicinal plants - seed and management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List, Dict, Any

from core.database import get_session
from domain.medicinal_plants.models import (
    MedicinalPlant,
    PlantCategory,
    EvidenceLevel,
    SafetyLevel,
    PreparationType
)

router = APIRouter(
    prefix="/admin/medicinal-plants",
    tags=["admin", "medicinal-plants"]
)


SEED_DATA = [
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
        "general_precautions": "Usar con moderación en niños pequeños.",
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
        "notes": "Muy popular en mercados mexicanos."
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
            }
        ],
        "active_compounds": ["Fibra soluble", "Pectina", "Flavonoides", "Betalaínas"],
        "pharmacological_actions": ["Hipoglucemiante", "Hipolipemiante", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar diarrea por alto contenido de fibra.",
        "contraindications": "Obstrucción intestinal.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "interactions": "Puede potenciar medicamentos para diabetes",
        "mexican_sources": ["Tiendas Bienestar"],
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=opuntia-ficus-indica",
        "bienestar_store_available": True,
        "local_market_price": 5.0,
        "image_url": None,
        "notes": "Símbolo nacional de México, alimento y medicina ancestral."
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
            "Infecciones gastrointestinales"
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
        "active_compounds": ["Taninos", "Flavonoides", "Triterpenos"],
        "pharmacological_actions": ["Antiulceroso", "Gastroprotector", "Cicatrizante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Puede causar estreñimiento con uso prolongado.",
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
        "notes": "Planta endémica mexicana con evidencia científica sólida."
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
            "Estreñimiento"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Cantidad necesaria de gel fresco",
                "preparation": "Cortar hoja, extraer gel transparente y aplicar sobre piel limpia",
                "frequency": "2-3 veces al día según necesidad",
                "duration": None
            }
        ],
        "active_compounds": ["Acemanano", "Aloína", "Polisacáridos"],
        "pharmacological_actions": ["Cicatrizante", "Antiinflamatorio", "Laxante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Uso interno: NUNCA usar la cáscara, solo gel transparente.",
        "contraindications": "Embarazo y lactancia (uso interno).",
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
        "notes": "Muy popular en México para problemas de piel."
    }
]


@router.post("/seed", response_model=Dict[str, Any])
def seed_medicinal_plants(
    clear_existing: bool = False,
    session: Session = Depends(get_session)
):
    """
    Seed the database with initial Mexican medicinal plants data

    Args:
        clear_existing: If True, delete all existing plants before seeding
        session: Database session

    Returns:
        Dictionary with seeding results
    """
    try:
        # Check existing plants
        existing = session.exec(select(MedicinalPlant)).all()

        if existing and not clear_existing:
            return {
                "success": False,
                "message": f"Database already contains {len(existing)} plants. Use clear_existing=true to replace.",
                "plants_added": 0,
                "existing_count": len(existing)
            }

        # Clear if requested
        if clear_existing and existing:
            for plant in existing:
                session.delete(plant)
            session.commit()

        # Add plants
        plants_added = []
        errors = []

        for plant_data in SEED_DATA:
            try:
                plant = MedicinalPlant(**plant_data)
                session.add(plant)
                session.flush()  # Get the ID
                plants_added.append({
                    "id": plant.id,
                    "name": plant.popular_names[0],
                    "scientific_name": plant.scientific_name
                })
            except Exception as e:
                errors.append({
                    "scientific_name": plant_data.get("scientific_name"),
                    "error": str(e)
                })

        session.commit()

        # Count by category
        all_plants = session.exec(select(MedicinalPlant)).all()
        categories = {}
        for plant in all_plants:
            cat = plant.primary_category.value
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "success": True,
            "message": f"Successfully seeded {len(plants_added)} plants",
            "plants_added": plants_added,
            "errors": errors if errors else None,
            "total_in_database": len(all_plants),
            "by_category": categories
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error seeding plants: {str(e)}"
        )


@router.delete("/clear-all")
def clear_all_plants(session: Session = Depends(get_session)):
    """Delete ALL medicinal plants from database - USE WITH CAUTION"""
    try:
        plants = session.exec(select(MedicinalPlant)).all()
        count = len(plants)

        for plant in plants:
            session.delete(plant)

        session.commit()

        return {
            "success": True,
            "message": f"Deleted {count} plants",
            "deleted_count": count
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing plants: {str(e)}"
        )
