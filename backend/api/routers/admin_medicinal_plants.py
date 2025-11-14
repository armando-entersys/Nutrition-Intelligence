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
        "scientific_name": "Gnaphalium spp.",
        "botanical_family": "Asteraceae",
        "popular_names": ["Gordolobo"],
        "indigenous_names": None,
        "states_found": ["Estado de México", "Puebla", "Michoacán"],
        "origin_region": "Nativo de México",
        "growing_season": None,
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": [PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": [
            "Tos y resfriados",
            "Bronquitis",
            "Asma leve",
            "Ronquera",
            "Inflamación de garganta"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharada de flores y hojas secas por taza",
                "preparation": "Hervir 5 minutos y reposar 10 minutos",
                "frequency": "3-4 tazas al día, puede endulzarse con miel",
                "duration": "No más de 2 semanas continuas"
            }
        ],
        "active_compounds": ["Flavonoides", "Taninos", "Aceites esenciales", "Mucílagos"],
        "pharmacological_actions": ["Expectorante", "Antiinflamatorio", "Antitusivo"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "No usar por períodos prolongados (más de 2 semanas continuas).",
        "contraindications": None,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=gnaphalium",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta tradicional mexicana muy efectiva para afecciones respiratorias."
    },
    {
        "scientific_name": "Tilia mexicana",
        "botanical_family": "Malvaceae",
        "popular_names": ["Tila", "Tilo"],
        "indigenous_names": None,
        "states_found": ["Puebla", "Veracruz", "Chiapas", "Oaxaca"],
        "origin_region": "Nativa de México",
        "growing_season": None,
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": None,
        "traditional_uses": [
            "Nerviosismo y ansiedad",
            "Insomnio",
            "Estrés",
            "Palpitaciones nerviosas",
            "Dolor de cabeza tensional"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de flores secas por taza",
                "preparation": "Agua casi hirviendo, reposar 10 minutos tapado",
                "frequency": "1-2 tazas al día, preferentemente antes de dormir",
                "duration": None
            }
        ],
        "active_compounds": ["Flavonoides", "Taninos", "Aceites volátiles", "Mucílagos"],
        "pharmacological_actions": ["Sedante leve", "Ansiolítico", "Espasmolítico"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar somnolencia. No operar maquinaria pesada después de consumir.",
        "contraindications": "Evitar combinar con sedantes fuertes.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": "Puede potenciar efectos de sedantes",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=tilia",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Especie mexicana distinta de la tila europea."
    },
    {
        "scientific_name": "Heterotheca inuloides",
        "botanical_family": "Asteraceae",
        "popular_names": ["Árnica mexicana", "Árnica del país"],
        "indigenous_names": None,
        "states_found": ["Estado de México", "Hidalgo", "Puebla", "Tlaxcala"],
        "origin_region": "Endémica de México",
        "growing_season": None,
        "primary_category": PlantCategory.ANTI_INFLAMMATORY,
        "secondary_categories": [PlantCategory.PAIN_RELIEF],
        "traditional_uses": [
            "Golpes y contusiones",
            "Moretones",
            "Esguinces",
            "Dolores musculares",
            "Inflamación por traumatismos"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Tintura diluida (1:10) o gel",
                "preparation": "Aplicar sobre piel intacta, no en heridas abiertas",
                "frequency": "2-3 veces al día",
                "duration": "Hasta mejora de síntomas"
            }
        ],
        "active_compounds": ["Helenalina", "Flavonoides", "Aceites esenciales", "Lactonas sesquiterpénicas"],
        "pharmacological_actions": ["Antiinflamatorio", "Analgésico", "Antiséptico"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.MODERATE,
        "general_precautions": "SOLO USO EXTERNO. NUNCA INGERIR. No aplicar sobre heridas abiertas. Puede causar dermatitis en personas sensibles.",
        "contraindications": "Alergia a Asteraceae. Heridas abiertas. NUNCA VÍA ORAL.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 3,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=heterotheca-inuloides",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Especie mexicana diferente de Arnica montana europea. USO EXTERNO ÚNICAMENTE."
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
    },
    {
        "scientific_name": "Rosmarinus officinalis",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Romero"],
        "indigenous_names": None,
        "states_found": ["Todo México"],
        "origin_region": "Mediterráneo, naturalizado en México",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.MEMORY_COGNITION,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Mejorar memoria y concentración",
            "Dolor de cabeza",
            "Mala circulación",
            "Dolores musculares",
            "Caída de cabello"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas por taza",
                "preparation": "Agua hirviendo, reposar 10 minutos",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Ácido rosmarínico", "Carnosol", "Cineol", "Alcanfor"],
        "pharmacological_actions": ["Antioxidante", "Neuroprotector", "Estimulante circulatorio"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "No exceder dosis recomendadas. Evitar aceite esencial concentrado durante embarazo.",
        "contraindications": "Epilepsia (en dosis altas). Hipertensión severa.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=rosmarinus-officinalis",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Introducido en época colonial, ampliamente adoptado en medicina tradicional mexicana."
    },
    {
        "scientific_name": "Dysphania ambrosioides",
        "botanical_family": "Amaranthaceae",
        "popular_names": ["Epazote", "Pazote"],
        "indigenous_names": {"Náhuatl": "Epazotl"},
        "states_found": ["Todo México"],
        "origin_region": "Nativo de México",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.ANTIPARASITIC],
        "traditional_uses": [
            "Parásitos intestinales (lombrices)",
            "Gases intestinales",
            "Cólicos menstruales",
            "Dolor de estómago"
        ],
        "indigenous_uses": {"Náhuatl": ["Antiparasitario", "Digestivo", "Condimento medicinal"]},
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 hojas frescas o 1/2 cucharadita seca",
                "preparation": "Hervir 3-5 minutos",
                "frequency": "1 taza al día",
                "duration": "Máximo 3 días para parásitos"
            }
        ],
        "active_compounds": ["Ascaridol", "Terpenos", "Aceites esenciales"],
        "pharmacological_actions": ["Antiparasitario", "Carminativo", "Antiespasmódico"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.MODERATE,
        "general_precautions": "NO USAR EN EMBARAZO. No usar por más de 3 días seguidos. TÓXICO en dosis excesivas.",
        "contraindications": "Embarazo, lactancia, problemas hepáticos o renales.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=dysphania-ambrosioides",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta nativa mexicana, también usada como condimento tradicional."
    },
    {
        "scientific_name": "Equisetum arvense",
        "botanical_family": "Equisetaceae",
        "popular_names": ["Cola de caballo"],
        "indigenous_names": None,
        "states_found": ["Zonas húmedas del centro y sur de México"],
        "origin_region": "Cosmopolita",
        "growing_season": None,
        "primary_category": PlantCategory.URINARY,
        "secondary_categories": [PlantCategory.SKIN_HAIR],
        "traditional_uses": [
            "Retención de líquidos",
            "Infecciones urinarias leves",
            "Cálculos renales (prevención)",
            "Fortalecer uñas y cabello"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de planta seca por taza",
                "preparation": "Hervir 10 minutos y reposar 10 minutos más",
                "frequency": "2-3 tazas al día entre comidas",
                "duration": "Máximo 6 semanas continuas"
            }
        ],
        "active_compounds": ["Silicio", "Flavonoides", "Saponinas", "Minerales"],
        "pharmacological_actions": ["Diurético", "Remineralizante", "Astringente"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "No usar por más de 6 semanas continuas. Asegurar hidratación adecuada.",
        "contraindications": "Embarazo y lactancia. Diabetes. Problemas cardíacos o renales graves.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "interactions": "Puede afectar niveles de azúcar en sangre",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=equisetum-arvense",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta diurética tradicional para problemas urinarios."
    },
    {
        "scientific_name": "Passiflora incarnata",
        "botanical_family": "Passifloraceae",
        "popular_names": ["Pasiflora", "Flor de la pasión"],
        "indigenous_names": None,
        "states_found": ["Veracruz", "Chiapas", "Oaxaca", "Tabasco"],
        "origin_region": "Nativa de América",
        "growing_season": None,
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": None,
        "traditional_uses": [
            "Ansiedad y nerviosismo",
            "Insomnio",
            "Estrés",
            "Palpitaciones nerviosas"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de hojas y flores secas",
                "preparation": "Agua hirviendo, reposar 10-15 minutos",
                "frequency": "1 taza 1-3 veces al día, o 1 hora antes de dormir",
                "duration": None
            }
        ],
        "active_compounds": ["Flavonoides", "Alcaloides harmala", "Maltol"],
        "pharmacological_actions": ["Ansiolítico", "Sedante", "Espasmolítico"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Puede causar somnolencia. No operar maquinaria. No combinar con sedantes sin supervisión.",
        "contraindications": "Embarazo (puede estimular contracciones uterinas).",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": "Puede potenciar efecto de sedantes y ansiolíticos",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=passiflora-incarnata",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta calmante natural muy efectiva para ansiedad e insomnio."
    },
    {
        "scientific_name": "Zingiber officinale",
        "botanical_family": "Zingiberaceae",
        "popular_names": ["Jengibre"],
        "indigenous_names": None,
        "states_found": ["Veracruz", "Nayarit", "zonas tropicales"],
        "origin_region": "Asia, cultivado en México",
        "growing_season": None,
        "primary_category": PlantCategory.ANTI_INFLAMMATORY,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Náuseas y mareos",
            "Dolor artrítico",
            "Inflamación",
            "Resfriados y gripe",
            "Problemas digestivos"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cm de raíz fresca rallada",
                "preparation": "Hervir 10 minutos, puede endulzarse con miel",
                "frequency": "2-3 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Gingerol", "Shogaol", "Zingerona", "Aceites esenciales"],
        "pharmacological_actions": ["Antiinflamatorio", "Antiemético", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede aumentar riesgo de sangrado en dosis muy altas. Evitar antes de cirugías.",
        "contraindications": "Trastornos de coagulación. Cálculos biliares.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": "Anticoagulantes en dosis altas",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=zingiber-officinale",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Excelente para náuseas y propiedades antiinflamatorias."
    },
    {
        "scientific_name": "Curcuma longa",
        "botanical_family": "Zingiberaceae",
        "popular_names": ["Cúrcuma", "Azafrán de la India"],
        "indigenous_names": None,
        "states_found": ["Zonas tropicales de México"],
        "origin_region": "Asia, cultivada en México",
        "growing_season": None,
        "primary_category": PlantCategory.ANTI_INFLAMMATORY,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Artritis y dolor articular",
            "Inflamación crónica",
            "Problemas digestivos",
            "Salud hepática"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de cúrcuma en polvo con pizca de pimienta negra",
                "preparation": "Hervir 10 minutos con leche o agua",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Curcumina", "Demetoxicurcumina", "Bisdemetoxicurcumina"],
        "pharmacological_actions": ["Antiinflamatorio", "Antioxidante", "Hepatoprotector"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Combinar con pimienta negra para mejor absorción.",
        "contraindications": "Obstrucción de vías biliares. Cálculos biliares (dosis altas).",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 4,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=curcuma-longa",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Poderoso antiinflamatorio natural, requiere pimienta negra para absorción."
    },
    {
        "scientific_name": "Valeriana officinalis",
        "botanical_family": "Caprifoliaceae",
        "popular_names": ["Valeriana"],
        "indigenous_names": None,
        "states_found": ["Zonas templadas de México"],
        "origin_region": "Europa, cultivada en México",
        "growing_season": None,
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": None,
        "traditional_uses": [
            "Insomnio severo",
            "Ansiedad intensa",
            "Estrés agudo",
            "Nerviosismo extremo"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de raíz seca",
                "preparation": "Agua hirviendo, reposar 15 minutos tapado",
                "frequency": "1 taza 1-2 horas antes de dormir",
                "duration": None
            }
        ],
        "active_compounds": ["Ácido valerénico", "Valepotriatos", "Alcaloides", "GABA"],
        "pharmacological_actions": ["Sedante potente", "Ansiolítico", "Relajante muscular"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Causa somnolencia intensa. NO operar maquinaria. NO combinar con alcohol o sedantes.",
        "contraindications": "Embarazo y lactancia. Problemas hepáticos. No combinar con sedantes.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 3,
        "interactions": "Potencia efectos de sedantes, ansiolíticos y alcohol",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=valeriana-officinalis",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Sedante natural potente, uno de los más efectivos para insomnio."
    },
    {
        "scientific_name": "Allium sativum",
        "botanical_family": "Amaryllidaceae",
        "popular_names": ["Ajo"],
        "indigenous_names": None,
        "states_found": ["Guanajuato", "Zacatecas", "todo México"],
        "origin_region": "Asia Central, cultivado mundialmente",
        "growing_season": None,
        "primary_category": PlantCategory.IMMUNE_SUPPORT,
        "secondary_categories": [PlantCategory.METABOLIC],
        "traditional_uses": [
            "Prevención de resfriados y gripe",
            "Presión arterial alta",
            "Colesterol elevado",
            "Infecciones",
            "Salud cardiovascular"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.FRESH.value,
                "dosage": "1-2 dientes frescos machacados",
                "preparation": "Machacar, dejar reposar 10 minutos para activar alicina, consumir con alimentos",
                "frequency": "1-2 dientes al día",
                "duration": None
            }
        ],
        "active_compounds": ["Alicina", "Ajoeno", "S-alilcisteína", "Compuestos azufrados"],
        "pharmacological_actions": ["Antibiótico", "Antiviral", "Hipotensor", "Hipolipemiante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar mal aliento y olor corporal. Aumenta riesgo de sangrado. Suspender 1-2 semanas antes de cirugías.",
        "contraindications": "Trastornos de coagulación.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": "Anticoagulantes (aumenta riesgo de sangrado)",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=allium-sativum",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Potente antibiótico natural con beneficios cardiovasculares comprobados."
    },
    {
        "scientific_name": "Coriandrum sativum",
        "botanical_family": "Apiaceae",
        "popular_names": ["Cilantro"],
        "indigenous_names": None,
        "states_found": ["Todo México"],
        "origin_region": "Mediterráneo y Asia, cultivado globalmente",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": None,
        "traditional_uses": [
            "Gases y flatulencias",
            "Indigestión",
            "Desintoxicación de metales pesados",
            "Náuseas leves",
            "Mal aliento"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de semillas machacadas",
                "preparation": "Hervir 10 minutos",
                "frequency": "2-3 tazas al día después de comidas",
                "duration": None
            }
        ],
        "active_compounds": ["Linalol", "Geraniol", "Flavonoides", "Vitaminas A, C, K"],
        "pharmacological_actions": ["Carminativo", "Digestivo", "Quelante de metales"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Generalmente seguro.",
        "contraindications": "Alergia conocida al cilantro.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=coriandrum-sativum",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Hierba aromática digestiva con propiedades desintoxicantes."
    },
    {
        "scientific_name": "Argemone mexicana",
        "botanical_family": "Papaveraceae",
        "popular_names": ["Chicalote", "Cardo santo"],
        "indigenous_names": {"Náhuatl": "Chicalotl"},
        "states_found": ["Todo México"],
        "origin_region": "Nativa de México",
        "growing_season": None,
        "primary_category": PlantCategory.PAIN_RELIEF,
        "secondary_categories": [PlantCategory.SKIN_HAIR],
        "traditional_uses": [
            "Dolor de muelas (látex tópico)",
            "Verrugas (látex)",
            "Problemas de piel"
        ],
        "indigenous_uses": {"Náhuatl": ["Látex para dolor", "Uso medicinal tópico"]},
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Látex amarillo",
                "preparation": "Aplicar directamente sobre dolor de muelas o verrugas. USO EXTERNO ÚNICAMENTE",
                "frequency": "1-2 veces al día",
                "duration": "Hasta desaparición"
            }
        ],
        "active_compounds": ["Berberina", "Protopina", "Sanguinarina", "Alcaloides"],
        "pharmacological_actions": ["Analgésico", "Queratolítico"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.MODERATE,
        "general_precautions": "TÓXICA SI SE INGIERE. Solo uso externo. El látex puede irritar piel sensible. NO USAR EN OJOS.",
        "contraindications": "Embarazo, lactancia. NUNCA INGERIR. NO aplicar en ojos.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=argemone-mexicana",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta tradicional mexicana. TÓXICA SI SE INGIERE. Solo uso externo controlado."
    },
    {
        "scientific_name": "Turnera diffusa",
        "botanical_family": "Passifloraceae",
        "popular_names": ["Damiana"],
        "indigenous_names": None,
        "states_found": ["Baja California", "Sonora", "norte de México"],
        "origin_region": "Nativa del norte de México",
        "growing_season": None,
        "primary_category": PlantCategory.FEMALE_HEALTH,
        "secondary_categories": None,
        "traditional_uses": [
            "Bajo deseo sexual",
            "Fatiga",
            "Depresión leve",
            "Problemas menstruales"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de hojas secas",
                "preparation": "Agua hirviendo, reposar 10-15 minutos",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Arbutina", "Flavonoides", "Aceites esenciales", "Taninos"],
        "pharmacological_actions": ["Afrodisíaco tradicional", "Tónico", "Estimulante leve"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Puede causar insomnio si se toma tarde. No exceder dosis recomendadas.",
        "contraindications": "Diabetes (puede afectar niveles de azúcar).",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "interactions": "Medicamentos para diabetes",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=turnera-diffusa",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta tradicional mexicana conocida como afrodisíaco natural."
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
        "scientific_name": "Bougainvillea spectabilis",
        "botanical_family": "Nyctaginaceae",
        "popular_names": ["Bugambilia", "Buganvilia"],
        "indigenous_names": None,
        "states_found": ["Todo México, climas cálidos"],
        "origin_region": "Sudamérica, naturalizada en México",
        "growing_season": ["Todo el año en clima cálido"],
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": None,
        "traditional_uses": [
            "Tos seca y persistente",
            "Bronquitis",
            "Asma leve",
            "Resfriados"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "5-7 flores (brácteas) por taza",
                "preparation": "Agua hirviendo, reposar 10 minutos, puede endulzarse con miel",
                "frequency": "2-3 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Flavonoides", "Alcaloides", "Taninos", "Betacianinas"],
        "pharmacological_actions": ["Expectorante", "Antitusivo", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "Usar flores limpias sin pesticidas.",
        "contraindications": None,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=bougainvillea",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Flores ornamentales ampliamente usadas en medicina tradicional mexicana para la tos."
    },
    {
        "scientific_name": "Agastache mexicana",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Toronjil morado", "Toronjil mexicano"],
        "indigenous_names": None,
        "states_found": ["Centro de México"],
        "origin_region": "Nativa de México",
        "growing_season": None,
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Nerviosismo y ansiedad leve",
            "Problemas de estómago",
            "Cólicos",
            "Dolor de cabeza",
            "Insomnio leve"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de hojas y flores secas",
                "preparation": "Agua hirviendo, reposar 10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Metil-chavicol", "Timol", "Flavonoides", "Aceites esenciales"],
        "pharmacological_actions": ["Sedante leve", "Digestivo", "Espasmolítico"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar leve somnolencia.",
        "contraindications": None,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=agastache-mexicana",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta aromática mexicana calmante, común en mercados tradicionales."
    },
    {
        "scientific_name": "Artemisia ludoviciana",
        "botanical_family": "Asteraceae",
        "popular_names": ["Estafiate", "Ajenjo del país"],
        "indigenous_names": {"Náhuatl": "Istafiatl"},
        "states_found": ["Centro y norte de México"],
        "origin_region": "Nativa de México",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.FEMALE_HEALTH],
        "traditional_uses": [
            "Parásitos intestinales",
            "Dolor de estómago",
            "Gases",
            "Falta de apetito",
            "Cólicos menstruales"
        ],
        "indigenous_uses": {"Náhuatl": ["Digestivo", "Ceremonial", "Temazcal"]},
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas",
                "preparation": "Agua hirviendo, reposar 10 minutos. Sabor muy amargo",
                "frequency": "1 taza 2-3 veces al día antes de comidas",
                "duration": "Máximo 2 semanas continuas"
            }
        ],
        "active_compounds": ["Absintina", "Tuyona", "Flavonoides", "Lactonas sesquiterpénicas"],
        "pharmacological_actions": ["Digestivo amargo", "Antiparasitario", "Emenagogo"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.MODERATE,
        "general_precautions": "NO USAR EN EMBARAZO. No usar por más de 2 semanas. Contiene tuyona tóxica en dosis altas.",
        "contraindications": "Embarazo, lactancia. Epilepsia. Problemas renales.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=artemisia-ludoviciana",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Planta aromática amarga nativa, usada tradicionalmente en temazcal y limpias."
    },
    {
        "scientific_name": "Psidium guajava",
        "botanical_family": "Myrtaceae",
        "popular_names": ["Guayaba (hojas)", "Hojas de guayabo"],
        "indigenous_names": None,
        "states_found": ["Todo México"],
        "origin_region": "América tropical",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": None,
        "traditional_uses": [
            "Diarrea",
            "Disentería",
            "Dolor de estómago",
            "Infecciones intestinales",
            "Higiene bucal"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "3-5 hojas tiernas por taza",
                "preparation": "Hervir 10 minutos",
                "frequency": "2-3 tazas al día para diarrea",
                "duration": "Máximo 3 días"
            }
        ],
        "active_compounds": ["Taninos", "Flavonoides (quercetina)", "Aceites esenciales", "Vitamina C"],
        "pharmacological_actions": ["Astringente", "Antidiarreico", "Antimicrobiano"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede causar estreñimiento si se usa por más de 3 días.",
        "contraindications": "Estreñimiento.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=psidium-guajava",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Hojas astringentes excelentes para diarrea e infecciones intestinales."
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
        "scientific_name": "Illicium verum",
        "botanical_family": "Schisandraceae",
        "popular_names": ["Anís de estrella", "Anís estrellado"],
        "indigenous_names": None,
        "states_found": ["Importado, disponible en todo México"],
        "origin_region": "Asia, ampliamente comercializado en México",
        "growing_season": None,
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.RESPIRATORY],
        "traditional_uses": [
            "Gases y cólicos en bebés",
            "Indigestión",
            "Tos y bronquitis",
            "Flatulencias",
            "Aumentar leche materna"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 estrellas por taza",
                "preparation": "Agua hirviendo, reposar 10 minutos tapado",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Anetol", "Estragol", "Aceites esenciales"],
        "pharmacological_actions": ["Carminativo", "Expectorante", "Galactagogo"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "general_precautions": "No confundir con anís estrella japonés (tóxico). Comprar solo de fuentes confiables.",
        "contraindications": "Alergias a plantas de la familia Apiaceae.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 0,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": False,
        "unam_reference_url": None,
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Especia aromática muy segura, tradicionalmente usada para cólicos en bebés."
    },
    {
        "scientific_name": "Cinnamomum verum",
        "botanical_family": "Lauraceae",
        "popular_names": ["Canela", "Canela de Ceilán"],
        "indigenous_names": None,
        "states_found": ["Importada, disponible en todo México"],
        "origin_region": "Sri Lanka, comercializada globalmente",
        "growing_season": None,
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Control de glucosa en diabetes",
            "Problemas digestivos",
            "Resfriados",
            "Circulación",
            "Inflamación"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 raja de canela (5 cm) por taza",
                "preparation": "Hervir 10 minutos",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Cinamaldehído", "Eugenol", "Ácido cinámico"],
        "pharmacological_actions": ["Hipoglucemiante", "Antioxidante", "Antimicrobiano"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Preferir canela de Ceilán sobre cassia. No exceder 1 cucharadita diaria.",
        "contraindications": "Problemas hepáticos (dosis altas de cassia). Puede potenciar medicamentos para diabetes.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "interactions": "Medicamentos para diabetes",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=cinnamomum",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Especia con propiedades para controlar azúcar en sangre, ampliamente usada en México."
    },
    {
        "scientific_name": "Moringa oleifera",
        "botanical_family": "Moringaceae",
        "popular_names": ["Moringa", "Árbol milagro"],
        "indigenous_names": None,
        "states_found": ["Zonas tropicales del sur y costa del Pacífico"],
        "origin_region": "India, cultivada en México",
        "growing_season": None,
        "primary_category": PlantCategory.IMMUNE_SUPPORT,
        "secondary_categories": [PlantCategory.METABOLIC],
        "traditional_uses": [
            "Desnutrición",
            "Aumentar energía",
            "Fortalecer sistema inmune",
            "Lactancia (aumentar producción de leche)",
            "Inflamación"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas",
                "preparation": "Agua caliente (no hirviendo), reposar 5 minutos",
                "frequency": "1-2 tazas al día",
                "duration": None
            }
        ],
        "active_compounds": ["Vitaminas A, C, E", "Calcio", "Potasio", "Proteínas", "Isotiocianatos"],
        "pharmacological_actions": ["Nutritivo", "Antioxidante", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede tener efecto laxante leve. Iniciar con dosis pequeñas.",
        "contraindications": "Hipotiroidismo (puede interferir con función tiroidea en dosis muy altas).",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": "Anticoagulantes (monitorear)",
        "mexican_sources": None,
        "unam_documented": False,
        "unam_reference_url": None,
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Árbol tropical altamente nutritivo, cada vez más cultivado en México."
    },
    {
        "scientific_name": "Salvia hispanica",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Chía"],
        "indigenous_names": {"Náhuatl": "Chian"},
        "states_found": ["Sur de México"],
        "origin_region": "Nativa de México y Guatemala",
        "growing_season": None,
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": [
            "Control de peso",
            "Estreñimiento",
            "Control de glucosa",
            "Salud cardiovascular",
            "Hidratación prolongada"
        ],
        "indigenous_uses": {"Náhuatl": ["Alimento básico", "Bebida refrescante"]},
        "preparation_methods": [
            {
                "type": PreparationType.FRESH.value,
                "dosage": "1-2 cucharadas de semillas",
                "preparation": "Remojar en agua o líquido por 15-30 minutos hasta formar gel, NUNCA consumir secas",
                "frequency": "1-2 cucharadas diarias, siempre hidratadas",
                "duration": None
            }
        ],
        "active_compounds": ["Omega-3 (ALA)", "Fibra soluble", "Proteína", "Calcio", "Antioxidantes"],
        "pharmacological_actions": ["Saciante", "Hipoglucemiante", "Hipolipemiante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "NUNCA consumir semillas secas sin hidratar (riesgo de obstrucción). Siempre remojar primero.",
        "contraindications": "Disfagia (dificultad para tragar). Obstrucción intestinal.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 5,
        "interactions": "Puede aumentar efecto de anticoagulantes",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=salvia-hispanica",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Semilla ancestral mexicana supernutritiva, rica en omega-3 y fibra."
    },
    {
        "scientific_name": "Amaranthus hypochondriacus",
        "botanical_family": "Amaranthaceae",
        "popular_names": ["Amaranto", "Alegría"],
        "indigenous_names": {"Náhuatl": "Huauhtli"},
        "states_found": ["Puebla", "Tlaxcala", "Morelos"],
        "origin_region": "Nativo de México",
        "growing_season": None,
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": None,
        "traditional_uses": [
            "Desnutrición",
            "Anemia",
            "Fortalecer huesos",
            "Control de colesterol",
            "Salud cardiovascular"
        ],
        "indigenous_uses": {"Náhuatl": ["Alimento sagrado", "Ceremonias religiosas"]},
        "preparation_methods": [
            {
                "type": PreparationType.FRESH.value,
                "dosage": "1/2 a 1 taza de semillas cocidas",
                "preparation": "Cocinar semillas como cereal, en sopas, o hacer alegrías (dulce con miel)",
                "frequency": "Diariamente",
                "duration": None
            }
        ],
        "active_compounds": ["Proteína completa", "Lisina", "Calcio", "Hierro", "Magnesio", "Escualeno"],
        "pharmacological_actions": ["Nutritivo", "Hipolipemiante", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Generalmente muy seguro. Libre de gluten.",
        "contraindications": None,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "interactions": None,
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=amaranthus",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Pseudocereal ancestral mexicano altamente nutritivo, fue alimento sagrado de los aztecas."
    },
    {
        "scientific_name": "Hibiscus sabdariffa",
        "botanical_family": "Malvaceae",
        "popular_names": ["Jamaica", "Flor de Jamaica"],
        "indigenous_names": None,
        "states_found": ["Guerrero", "Oaxaca", "Veracruz"],
        "origin_region": "África, cultivada en México",
        "growing_season": None,
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": [PlantCategory.URINARY],
        "traditional_uses": [
            "Presión arterial alta",
            "Colesterol elevado",
            "Infecciones urinarias",
            "Sobrepeso",
            "Antioxidante"
        ],
        "indigenous_uses": None,
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "2-3 cucharadas de flores secas por litro",
                "preparation": "Hervir 10 minutos, dejar enfriar. Puede servirse frío",
                "frequency": "2-3 tazas al día, sin azúcar para máximo beneficio",
                "duration": None
            }
        ],
        "active_compounds": ["Antocianinas", "Ácidos orgánicos", "Vitamina C", "Flavonoides"],
        "pharmacological_actions": ["Hipotensor", "Hipolipemiante", "Diurético", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "general_precautions": "Puede potenciar medicamentos para presión arterial. Personas con presión baja deben moderar consumo.",
        "contraindications": "Hipotensión.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "interactions": "Medicamentos para presión arterial (puede potenciar efecto)",
        "mexican_sources": None,
        "unam_documented": True,
        "unam_reference_url": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=hibiscus-sabdariffa",
        "bienestar_store_available": False,
        "local_market_price": None,
        "image_url": None,
        "notes": "Flor tradicional mexicana con excelentes propiedades para presión arterial y antioxidantes."
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
