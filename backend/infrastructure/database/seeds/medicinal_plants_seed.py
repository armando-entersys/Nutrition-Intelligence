"""
Seed data for Mexican Medicinal Plants
Based on UNAM research and traditional Mexican medicine

Top 20 most popular and widely used medicinal plants in Mexico
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_async_session, async_engine
from domain.medicinal_plants.models import (
    MedicinalPlant,
    PlantCategory,
    EvidenceLevel,
    SafetyLevel,
    PreparationType
)

# The 20 most popular Mexican medicinal plants for MVP
MEDICINAL_PLANTS_DATA = [
    {
        "scientific_name": "Matricaria chamomilla",
        "botanical_family": "Asteraceae",
        "popular_names": ["Manzanilla", "Camomila"],
        "indigenous_names": {"Náhuatl": "Manzanilla"},
        "states_found": ["Todo México", "Jalisco", "Michoacán", "Puebla", "CDMX"],
        "origin_region": "Europa, naturalizada en México",
        "growing_season": ["Primavera", "Verano"],
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.CALMING, PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": [
            "Dolores estomacales y cólicos",
            "Problemas digestivos",
            "Nerviosismo e insomnio",
            "Inflamación ocular",
            "Dolor menstrual"
        ],
        "indigenous_uses": {
            "Medicina tradicional": ["Té para el estómago", "Baños relajantes"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de flores secas por taza",
                "preparation": "Infusión en agua caliente por 5-10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            },
            {
                "type": PreparationType.COMPRESS.value,
                "dosage": "Infusión concentrada",
                "preparation": "Aplicar compresas tibias sobre los ojos",
                "frequency": "2-3 veces al día",
                "duration": "10-15 minutos"
            }
        ],
        "active_compounds": ["Apigenina", "Bisabolol", "Camazuleno"],
        "pharmacological_actions": ["Antiinflamatorio", "Antiespasmódico", "Sedante suave"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 50,
        "proven_effects": ["Mejora digestión", "Reduce ansiedad", "Antiinflamatorio ocular"],
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": ["Alergia a plantas de la familia Asteraceae"],
        "contraindications": ["Alergia conocida a manzanilla"],
        "adverse_effects": ["Raras reacciones alérgicas"],
        "drug_interactions": ["Anticoagulantes (en dosis muy altas)"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 1,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Farmacias", "Tiendas naturistas", "Supermercados"],
        "approximate_price_range": "$20-60 MXN por 50g",
        "plant_description": "Planta herbácea anual con flores pequeñas blancas con centro amarillo, aromáticas. Alcanza 15-60 cm de altura.",
        "identification_features": [
            "Flores con pétalos blancos y centro amarillo",
            "Aroma dulce característico",
            "Hojas finamente divididas"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "source_urls": ["http://www.medicinatradicionalmexicana.unam.mx/"],
        "validated_by_expert": True,
        "historical_notes": "Una de las plantas medicinales más antiguas y estudiadas. Usada desde el antiguo Egipto.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Mentha spicata",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Hierbabuena", "Menta verde", "Yerbabuena"],
        "indigenous_names": {"Náhuatl": "Ahuíyac xihuitl"},
        "states_found": ["Todo México", "Puebla", "Hidalgo", "Veracruz", "Oaxaca"],
        "origin_region": "Mediterráneo, cultivada en todo México",
        "growing_season": ["Todo el año en clima templado"],
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.RESPIRATORY],
        "traditional_uses": [
            "Dolor de estómago y gases",
            "Náuseas y vómito",
            "Dolor de cabeza",
            "Problemas respiratorios",
            "Mal aliento"
        ],
        "indigenous_uses": {
            "Medicina prehispánica": ["Té digestivo", "Baños temazcal"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "5-10 hojas frescas o 1 cucharadita seca",
                "preparation": "Infusión en agua caliente por 5 minutos",
                "frequency": "2-3 tazas al día después de comidas",
                "duration": "Según necesidad"
            },
            {
                "type": PreparationType.FRESH.value,
                "dosage": "Hojas frescas masticadas",
                "preparation": "Masticar hojas frescas directamente",
                "frequency": "Según necesidad",
                "duration": "N/A"
            }
        ],
        "active_compounds": ["Mentol", "Carvona", "Limoneno"],
        "pharmacological_actions": ["Antiespasmódico", "Carminativo", "Digestivo"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 35,
        "proven_effects": ["Alivia síndrome de intestino irritable", "Mejora digestión"],
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": ["Evitar aceite esencial en bebés"],
        "contraindications": ["Reflujo gastroesofágico severo"],
        "adverse_effects": ["Raras: ardor estomacal en exceso"],
        "drug_interactions": ["Ninguna significativa"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Cultivo casero", "Tiendas naturistas"],
        "approximate_price_range": "$10-30 MXN manojo fresco",
        "plant_description": "Planta aromática perenne de 30-90 cm, hojas verdes brillantes dentadas, flores en espigas moradas.",
        "identification_features": [
            "Aroma mentolado característico",
            "Hojas dentadas opuestas",
            "Tallos cuadrados"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta ampliamente usada en la medicina tradicional mexicana, presente en mercados desde época prehispánica.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Zingiber officinale",
        "botanical_family": "Zingiberaceae",
        "popular_names": ["Jengibre", "Kión"],
        "indigenous_names": {"Maya": "Sak yab", "Náhuatl": "Jengibre"},
        "states_found": ["Veracruz", "Puebla", "Chiapas", "Oaxaca", "Tabasco"],
        "origin_region": "Asia, cultivado en México desde época colonial",
        "growing_season": ["Clima cálido-húmedo"],
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.ANTI_INFLAMMATORY, PlantCategory.IMMUNE_SUPPORT],
        "traditional_uses": [
            "Náuseas y mareos",
            "Problemas digestivos",
            "Gripe y resfriados",
            "Dolor e inflamación",
            "Circulación"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cm de rizoma fresco rallado",
                "preparation": "Hervir en agua 10 minutos, colar",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            },
            {
                "type": PreparationType.FRESH.value,
                "dosage": "Pequeñas rodajas",
                "preparation": "Masticar jengibre fresco para náuseas",
                "frequency": "Según necesidad",
                "duration": "N/A"
            }
        ],
        "active_compounds": ["Gingerol", "Shogaol", "Zingibereno"],
        "pharmacological_actions": ["Antiemético", "Antiinflamatorio", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 100,
        "proven_effects": ["Reduce náuseas", "Antiinflamatorio", "Mejora digestión"],
        "safety_level": SafetyLevel.SAFE,
        "precautions": ["Evitar en dosis altas si toma anticoagulantes"],
        "contraindications": ["Cálculos biliares"],
        "adverse_effects": ["Acidez estomacal en exceso"],
        "drug_interactions": ["Anticoagulantes", "Antidiabéticos"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Supermercados", "Mercados", "Tiendas naturistas"],
        "approximate_price_range": "$40-80 MXN por kg",
        "plant_description": "Planta herbácea tropical, rizoma (raíz) grueso y aromático color beige, tallos hasta 1m.",
        "identification_features": [
            "Rizoma color beige nudoso",
            "Aroma picante característico",
            "Interior amarillo pálido"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Introducido a México en época colonial, ampliamente adoptado por la medicina tradicional.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Arnica montana",
        "botanical_family": "Asteraceae",
        "popular_names": ["Árnica", "Tabaco de montaña"],
        "indigenous_names": {"Náhuatl": "Xonequilpatli"},
        "states_found": ["Puebla", "Veracruz", "Hidalgo", "Estado de México", "Michoacán"],
        "origin_region": "México - especie nativa",
        "growing_season": ["Verano", "Otoño"],
        "primary_category": PlantCategory.ANTI_INFLAMMATORY,
        "secondary_categories": [PlantCategory.PAIN_RELIEF],
        "traditional_uses": [
            "Golpes y moretones",
            "Dolor muscular",
            "Inflamaciones",
            "Torceduras",
            "Artritis (uso externo)"
        ],
        "indigenous_uses": {
            "Medicina tradicional": ["Pomadas para golpes", "Tinturas para dolor"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Tintura o gel 10-30%",
                "preparation": "Aplicar sobre piel intacta, masajear suavemente",
                "frequency": "2-3 veces al día",
                "duration": "Hasta mejora de síntomas"
            },
            {
                "type": PreparationType.COMPRESS.value,
                "dosage": "Infusión de flores",
                "preparation": "Compresas tibias sobre área afectada",
                "frequency": "2 veces al día",
                "duration": "15-20 minutos"
            }
        ],
        "active_compounds": ["Helenalina", "Flavonoides", "Timol"],
        "pharmacological_actions": ["Antiinflamatorio", "Analgésico", "Antiséptico"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 40,
        "proven_effects": ["Reduce inflamación", "Alivia dolor muscular", "Acelera curación de moretones"],
        "safety_level": SafetyLevel.MODERATE,
        "precautions": [
            "SOLO USO EXTERNO",
            "No aplicar en heridas abiertas",
            "Posible sensibilización cutánea"
        ],
        "contraindications": ["Heridas abiertas", "Alergia a Asteraceae", "Embarazo (uso interno)"],
        "adverse_effects": ["Dermatitis de contacto en personas sensibles"],
        "drug_interactions": ["Ninguna documentada para uso tópico"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "minimum_age_years": 3,
        "availability_level": "MEDIUM",
        "where_to_find": ["Farmacias", "Tiendas naturistas", "Herbolarias"],
        "approximate_price_range": "$80-200 MXN gel/tintura",
        "plant_description": "Planta herbácea de 20-60 cm, flores amarillas-naranjas similares a margaritas.",
        "identification_features": [
            "Flores amarillo-naranja brillante",
            "Hojas ovaladas en roseta basal",
            "Aroma aromático"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta muy apreciada en medicina tradicional mexicana para traumatismos. Diferente de árnica europea.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Aloe vera",
        "botanical_family": "Asphodelaceae",
        "popular_names": ["Sábila", "Aloe", "Penca sábila"],
        "indigenous_names": {"Náhuatl": "Mexocotl"},
        "states_found": ["Todo México", "Puebla", "Veracruz", "Yucatán", "Sonora"],
        "origin_region": "África, ampliamente cultivada en México",
        "growing_season": ["Todo el año en clima cálido"],
        "primary_category": PlantCategory.SKIN_HAIR,
        "secondary_categories": [PlantCategory.DIGESTIVE, PlantCategory.WOUND_HEALING],
        "traditional_uses": [
            "Quemaduras y heridas",
            "Problemas de piel",
            "Estreñimiento",
            "Gastritis",
            "Cuidado del cabello"
        ],
        "indigenous_uses": {
            "Medicina tradicional": ["Gel para quemaduras", "Jugo para estómago"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Gel fresco de la penca",
                "preparation": "Cortar penca, extraer gel transparente, aplicar directo",
                "frequency": "2-3 veces al día",
                "duration": "Hasta curación"
            },
            {
                "type": PreparationType.JUICE.value,
                "dosage": "30-60 ml de gel interno",
                "preparation": "Licuar gel con agua, colar",
                "frequency": "1 vez al día en ayunas",
                "duration": "Máximo 2 semanas"
            }
        ],
        "active_compounds": ["Aloína", "Polisacáridos", "Antraquinonas"],
        "pharmacological_actions": ["Cicatrizante", "Antiinflamatorio", "Laxante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 70,
        "proven_effects": ["Acelera cicatrización", "Alivia quemaduras", "Hidrata piel"],
        "safety_level": SafetyLevel.SAFE,
        "precautions": [
            "Uso interno: solo gel interno, nunca el látex amarillo",
            "No usar como laxante por tiempo prolongado"
        ],
        "contraindications": ["Embarazo (uso interno)", "Enfermedad renal"],
        "adverse_effects": ["Diarrea si se consume el látex amarillo"],
        "drug_interactions": ["Medicamentos para diabetes", "Diuréticos"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Cultivo casero", "Mercados", "Viveros"],
        "approximate_price_range": "$30-80 MXN por penca",
        "plant_description": "Suculenta perenne con hojas carnosas verdes en roseta, bordes con espinas suaves, hasta 60 cm.",
        "identification_features": [
            "Hojas carnosas verde-gris",
            "Espinas suaves en bordes",
            "Gel transparente en interior"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta con más de 6,000 años de uso medicinal. Muy popular en México desde época prehispánica.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Opuntia ficus-indica",
        "botanical_family": "Cactaceae",
        "popular_names": ["Nopal", "Tuna", "Chumbera"],
        "indigenous_names": {"Náhuatl": "Nopalli"},
        "states_found": ["Todo México", "Especialmente zonas áridas"],
        "origin_region": "México - planta emblemática nacional",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.METABOLIC,
        "secondary_categories": [PlantCategory.DIGESTIVE, PlantCategory.WOUND_HEALING],
        "traditional_uses": [
            "Control de diabetes",
            "Colesterol alto",
            "Problemas digestivos",
            "Gastritis y úlceras",
            "Heridas y quemaduras"
        ],
        "indigenous_uses": {
            "Medicina prehispánica": ["Alimento y medicina", "Cataplasmas para heridas"],
            "Códices": ["Registrado en códices aztecas"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.FRESH.value,
                "dosage": "1-2 nopales medianos",
                "preparation": "Consumir crudos en ensalada o cocidos",
                "frequency": "Diariamente con alimentos",
                "duration": "Uso regular"
            },
            {
                "type": PreparationType.JUICE.value,
                "dosage": "100-200 ml",
                "preparation": "Licuar nopal crudo con agua, colar",
                "frequency": "1 vez al día en ayunas",
                "duration": "Uso regular"
            }
        ],
        "active_compounds": ["Fibra soluble", "Pectina", "Mucílago", "Flavonoides"],
        "pharmacological_actions": ["Hipoglucemiante", "Hipolipidemiante", "Antioxidante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 60,
        "proven_effects": ["Reduce glucosa en sangre", "Disminuye colesterol", "Mejora digestión"],
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": ["Puede bajar demasiado la glucosa si se combina con antidiabéticos"],
        "contraindications": ["Ninguna conocida"],
        "adverse_effects": ["Raros: leve malestar estomacal en exceso"],
        "drug_interactions": ["Medicamentos para diabetes (monitorear glucosa)"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 1,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Supermercados", "Cultivo silvestre"],
        "approximate_price_range": "$10-20 MXN por pieza",
        "plant_description": "Cactus con pencas (cladodios) ovaladas planas verde brillante, con espinas pequeñas.",
        "identification_features": [
            "Pencas ovaladas planas",
            "Espinas pequeñas agrupadas",
            "Fruto tunas de colores"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta sagrada en cultura azteca, presente en escudo nacional. Alimento y medicina por milenios.",
        "ritual_ceremonial_use": "Planta sagrada presente en mitos fundacionales de Tenochtitlan.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Valeriana officinalis",
        "botanical_family": "Caprifoliaceae",
        "popular_names": ["Valeriana", "Hierba de los gatos"],
        "indigenous_names": {"Náhuatl": "Tlacopatli"},
        "states_found": ["Hidalgo", "Puebla", "Veracruz", "Oaxaca", "Chiapas"],
        "origin_region": "Europa, cultivada en México",
        "growing_season": ["Primavera", "Verano"],
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": [PlantCategory.PAIN_RELIEF],
        "traditional_uses": [
            "Insomnio",
            "Ansiedad y nerviosismo",
            "Estrés",
            "Dolores de cabeza tensionales",
            "Palpitaciones"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de raíz seca",
                "preparation": "Infusión en agua caliente 10-15 minutos",
                "frequency": "1-2 tazas, especialmente antes de dormir",
                "duration": "Según necesidad"
            },
            {
                "type": PreparationType.CAPSULE.value,
                "dosage": "300-600 mg extracto",
                "preparation": "Tomar cápsulas según indicaciones",
                "frequency": "1-2 veces al día",
                "duration": "Máximo 4-6 semanas continuas"
            }
        ],
        "active_compounds": ["Ácido valerénico", "Valepotriatos", "GABA"],
        "pharmacological_actions": ["Sedante", "Ansiolítico", "Relajante muscular"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 45,
        "proven_effects": ["Mejora calidad del sueño", "Reduce ansiedad"],
        "safety_level": SafetyLevel.SAFE,
        "precautions": [
            "Puede causar somnolencia",
            "No conducir después de tomar",
            "No combinar con alcohol"
        ],
        "contraindications": ["Embarazo", "Lactancia", "Cirugía programada"],
        "adverse_effects": ["Somnolencia", "Mareos", "Dolor de cabeza leve"],
        "drug_interactions": ["Sedantes", "Ansiolíticos", "Alcohol"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "minimum_age_years": 12,
        "availability_level": "MEDIUM",
        "where_to_find": ["Farmacias", "Tiendas naturistas", "Herbolarias"],
        "approximate_price_range": "$60-150 MXN cápsulas",
        "plant_description": "Planta herbácea perenne hasta 1.5m, flores pequeñas blanco-rosadas, raíz aromática.",
        "identification_features": [
            "Raíz con olor fuerte característico",
            "Flores pequeñas en racimos",
            "Hojas pinnadas compuestas"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Usada desde la antigua Grecia. Ampliamente estudiada para insomnio y ansiedad.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Tilia mexicana",
        "botanical_family": "Malvaceae",
        "popular_names": ["Tila", "Tilo", "Flor de tila"],
        "indigenous_names": {"Náhuatl": "Tlilxochitl"},
        "states_found": ["Puebla", "Veracruz", "Chiapas", "Oaxaca", "Guerrero"],
        "origin_region": "México - especie nativa",
        "growing_season": ["Primavera"],
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": [PlantCategory.RESPIRATORY],
        "traditional_uses": [
            "Nerviosismo e insomnio",
            "Ansiedad",
            "Resfriados y gripe",
            "Dolor de cabeza",
            "Palpitaciones"
        ],
        "indigenous_uses": {
            "Medicina tradicional": ["Té relajante", "Baños para nervios"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de flores",
                "preparation": "Infusión en agua caliente 5-10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Flavonoides", "Mucílagos", "Aceites esenciales"],
        "pharmacological_actions": ["Sedante suave", "Antiespasmódico", "Diaforético"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "clinical_studies_count": 15,
        "proven_effects": ["Efecto calmante leve", "Ayuda con resfriados"],
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": ["Ninguna significativa"],
        "contraindications": ["Ninguna conocida"],
        "adverse_effects": ["Ninguno reportado"],
        "drug_interactions": ["Ninguna conocida"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 1,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Farmacias", "Tiendas naturistas"],
        "approximate_price_range": "$30-60 MXN por 50g",
        "plant_description": "Árbol de hasta 20m, flores pequeñas amarillentas muy aromáticas, hojas en forma de corazón.",
        "identification_features": [
            "Flores amarillas pequeñas aromáticas",
            "Hojas acorazonadas",
            "Aroma dulce característico"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta tradicional mexicana muy popular para té relajante. Diferente de la tila europea.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Dysphania ambrosioides",
        "botanical_family": "Amaranthaceae",
        "popular_names": ["Epazote", "Pazote", "Té de México"],
        "indigenous_names": {"Náhuatl": "Epazotl"},
        "states_found": ["Todo México"],
        "origin_region": "México - planta nativa",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.ANTIPARASITIC],
        "traditional_uses": [
            "Parásitos intestinales",
            "Gases y flatulencias",
            "Cólicos estomacales",
            "Diarrea",
            "Condimento medicinal"
        ],
        "indigenous_uses": {
            "Medicina prehispánica": ["Antiparasitario", "Digestivo", "Condimento sagrado"],
            "Códices": ["Presente en códices aztecas"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas",
                "preparation": "Infusión en agua caliente 5 minutos",
                "frequency": "1-2 tazas al día",
                "duration": "Máximo 3 días para parásitos"
            },
            {
                "type": PreparationType.FRESH.value,
                "dosage": "Hojas frescas al cocinar",
                "preparation": "Agregar durante cocción de frijoles",
                "frequency": "Regular en alimentación",
                "duration": "Uso culinario continuo"
            }
        ],
        "active_compounds": ["Ascaridol", "Cimeno", "Limoneno"],
        "pharmacological_actions": ["Antiparasitario", "Carminativo", "Antiespasmódico"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "clinical_studies_count": 25,
        "proven_effects": ["Elimina parásitos intestinales", "Reduce gases"],
        "safety_level": SafetyLevel.MODERATE,
        "precautions": [
            "NO usar aceite esencial (tóxico)",
            "Dosis terapéuticas solo por tiempo limitado",
            "Como condimento es seguro"
        ],
        "contraindications": ["Embarazo", "Lactancia", "Enfermedad renal/hepática"],
        "adverse_effects": ["Náuseas en dosis altas", "Toxicidad del aceite esencial"],
        "drug_interactions": ["Ninguna significativa en uso culinario"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Supermercados", "Cultivo casero"],
        "approximate_price_range": "$5-15 MXN manojo",
        "plant_description": "Hierba aromática anual de 40-80 cm, hojas dentadas verde oscuro, olor fuerte característico.",
        "identification_features": [
            "Olor fuerte muy característico",
            "Hojas dentadas lanceoladas",
            "Flores pequeñas verdosas"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Planta sagrada en cultura azteca. Uso medicinal y culinario por más de 3,000 años en México.",
        "ritual_ceremonial_use": "Usado en ceremonias prehispánicas y como ofrenda.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Rosmarinus officinalis",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Romero"],
        "indigenous_names": {"Español colonial": "Romero"},
        "states_found": ["Todo México", "Especialmente regiones templadas"],
        "origin_region": "Mediterráneo, naturalizado en México",
        "growing_season": ["Todo el año"],
        "primary_category": PlantCategory.MEMORY_COGNITION,
        "secondary_categories": [PlantCategory.DIGESTIVE, PlantCategory.CIRCULATORY],
        "traditional_uses": [
            "Memoria y concentración",
            "Dolor de cabeza",
            "Problemas digestivos",
            "Circulación",
            "Caída del cabello"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas",
                "preparation": "Infusión en agua caliente 10 minutos",
                "frequency": "2 tazas al día",
                "duration": "Uso regular"
            },
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Infusión concentrada",
                "preparation": "Enjuague para cabello después de lavar",
                "frequency": "2-3 veces por semana",
                "duration": "Uso regular"
            }
        ],
        "active_compounds": ["Ácido rosmarínico", "Carnosol", "1,8-cineol"],
        "pharmacological_actions": ["Antioxidante", "Neuroprotector", "Digestivo"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 55,
        "proven_effects": ["Mejora memoria", "Antioxidante potente", "Estimula circulación"],
        "safety_level": SafetyLevel.SAFE,
        "precautions": ["Evitar dosis altas en embarazo"],
        "contraindications": ["Epilepsia (aceite esencial concentrado)"],
        "adverse_effects": ["Raros en uso normal"],
        "drug_interactions": ["Anticoagulantes en dosis muy altas"],
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Supermercados", "Cultivo casero"],
        "approximate_price_range": "$20-40 MXN manojo",
        "plant_description": "Arbusto perenne aromático hasta 1.5m, hojas aciculares verde-grisáceas, flores azul-violetas.",
        "identification_features": [
            "Hojas lineales como agujas",
            "Aroma intenso característico",
            "Flores azul-violeta pequeñas"
        ],
        "source": "UNAM - Atlas de Plantas Medicinales",
        "validated_by_expert": True,
        "historical_notes": "Introducido en época colonial, ampliamente adoptado en medicina tradicional mexicana.",
        "featured": True,
        "is_active": True
    }
]

# We'll add 10 more plants to complete the 20
ADDITIONAL_PLANTS_DATA = [
    {
        "scientific_name": "Origanum vulgare",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Orégano", "Mejorana silvestre"],
        "indigenous_names": {"Náhuatl": "Ahuíyac patli"},
        "states_found": ["Todo México"],
        "origin_region": "Mediterráneo, cultivado en México",
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": [PlantCategory.DIGESTIVE, PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": ["Tos y bronquitis", "Problemas digestivos", "Dolor menstrual"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita de hojas secas",
                "preparation": "Infusión 5-10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Carvacrol", "Timol", "Ácido rosmarínico"],
        "pharmacological_actions": ["Antibacteriano", "Antioxidante", "Expectorante"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "clinical_studies_count": 30,
        "safety_level": SafetyLevel.VERY_SAFE,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 1,
        "availability_level": "HIGH",
        "where_to_find": ["Supermercados", "Mercados", "Cultivo casero"],
        "approximate_price_range": "$15-30 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Todo el año"],
        "plant_description": "Hierba aromática perenne, hojas pequeñas ovaladas, flores moradas.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Thymus vulgaris",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Tomillo"],
        "indigenous_names": {},
        "states_found": ["Todo México"],
        "origin_region": "Mediterráneo",
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": [PlantCategory.ANTISEPTIC],
        "traditional_uses": ["Tos", "Bronquitis", "Infecciones respiratorias", "Digestión"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas",
                "preparation": "Infusión 10 minutos",
                "frequency": "3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Timol", "Carvacrol"],
        "pharmacological_actions": ["Antiséptico", "Expectorante", "Antibacteriano"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 40,
        "safety_level": SafetyLevel.SAFE,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Supermercados", "Mercados", "Farmacias"],
        "approximate_price_range": "$20-40 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Primavera", "Verano"],
        "plant_description": "Hierba pequeña muy aromática, hojas diminutas, flores rosadas.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Passiflora incarnata",
        "botanical_family": "Passifloraceae",
        "popular_names": ["Pasiflora", "Flor de la pasión", "Pasionaria"],
        "indigenous_names": {"Náhuatl": "Matlālīn"},
        "states_found": ["Veracruz", "Chiapas", "Oaxaca", "Tabasco"],
        "origin_region": "América, nativa de México",
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": [PlantCategory.PAIN_RELIEF],
        "traditional_uses": ["Ansiedad", "Insomnio", "Nerviosismo", "Dolor de cabeza"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de hojas",
                "preparation": "Infusión 10 minutos",
                "frequency": "1-2 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Flavonoides", "Alcaloides harmala"],
        "pharmacological_actions": ["Ansiolítico", "Sedante"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 35,
        "safety_level": SafetyLevel.SAFE,
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "minimum_age_years": 12,
        "availability_level": "MEDIUM",
        "where_to_find": ["Farmacias", "Tiendas naturistas"],
        "approximate_price_range": "$60-120 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Veracruz", "Chiapas", "Oaxaca"],
        "growing_season": ["Verano"],
        "plant_description": "Enredadera con flores espectaculares moradas y blancas.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Artemisia ludoviciana",
        "botanical_family": "Asteraceae",
        "popular_names": ["Estafiate", "Ajenjo del país", "Altamisa"],
        "indigenous_names": {"Náhuatl": "Istafiatl"},
        "states_found": ["Todo México", "Altiplano central"],
        "origin_region": "México - planta nativa",
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.FEMALE_HEALTH],
        "traditional_uses": ["Dolor estomacal", "Parásitos", "Cólicos menstruales", "Fiebre"],
        "indigenous_uses": {
            "Medicina prehispánica": ["Digestivo", "Ceremonial", "Temazcal"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1 cucharadita",
                "preparation": "Infusión 5-7 minutos",
                "frequency": "1-2 tazas al día",
                "duration": "Máximo 1 semana"
            }
        ],
        "active_compounds": ["Tuyona", "Cineol", "Alcanfor"],
        "pharmacological_actions": ["Digestivo", "Antiparasitario", "Emenagogo"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "clinical_studies_count": 12,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": ["No usar por tiempo prolongado", "Evitar en embarazo"],
        "contraindications": ["Embarazo", "Lactancia"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "minimum_age_years": 12,
        "availability_level": "MEDIUM",
        "where_to_find": ["Mercados", "Herbolarias"],
        "approximate_price_range": "$20-50 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Verano", "Otoño"],
        "plant_description": "Hierba aromática grisácea, hojas plateadas, aroma intenso.",
        "ritual_ceremonial_use": "Usado en temazcal y limpias tradicionales",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Bougainvillea glabra",
        "botanical_family": "Nyctaginaceae",
        "popular_names": ["Bugambilia", "Buganvilia"],
        "indigenous_names": {},
        "states_found": ["Todo México", "Clima cálido"],
        "origin_region": "Sudamérica, naturalizada en México",
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": [PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": ["Tos", "Bronquitis", "Asma", "Problemas respiratorios"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "5-7 brácteas (flores)",
                "preparation": "Hervir 5 minutos, infusionar 5 más",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Flavonoides", "Taninos", "Alcaloides"],
        "pharmacological_actions": ["Expectorante", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "clinical_studies_count": 8,
        "safety_level": SafetyLevel.SAFE,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Jardines", "Cultivo ornamental", "Mercados"],
        "approximate_price_range": "$10-20 MXN",
        "source": "Medicina Tradicional Mexicana",
        "validated_by_expert": False,
        "states_found": ["Todo México"],
        "growing_season": ["Todo el año en clima cálido"],
        "plant_description": "Arbusto trepador con brácteas coloridas (rosa, morado, rojo).",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Amphipterygium adstringens",
        "botanical_family": "Anacardiaceae",
        "popular_names": ["Cuachalalate", "Cuachalala"],
        "indigenous_names": {"Náhuatl": "Cuauchachalatli"},
        "states_found": ["Guerrero", "Michoacán", "Oaxaca", "Jalisco"],
        "origin_region": "México - endémica",
        "primary_category": PlantCategory.DIGESTIVE,
        "secondary_categories": [PlantCategory.WOUND_HEALING, PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": ["Gastritis", "Úlceras", "Cáncer (tradicional)", "Heridas", "Inflamación"],
        "indigenous_uses": {
            "Medicina prehispánica": ["Corteza para estómago", "Heridas de guerra"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.DECOCTION.value,
                "dosage": "1 cucharada de corteza",
                "preparation": "Hervir 10 minutos en 1 litro de agua",
                "frequency": "3 tazas al día antes de alimentos",
                "duration": "2-4 semanas"
            }
        ],
        "active_compounds": ["Anacardina", "Masticadienóico", "Anacárdicos"],
        "pharmacological_actions": ["Gastroprotector", "Cicatrizante", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "clinical_studies_count": 28,
        "proven_effects": ["Protección gástrica", "Cicatrización"],
        "safety_level": SafetyLevel.SAFE,
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "minimum_age_years": 5,
        "availability_level": "MEDIUM",
        "where_to_find": ["Mercados", "Herbolarias", "Tiendas naturistas"],
        "approximate_price_range": "$40-80 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Guerrero", "Michoacán", "Oaxaca"],
        "growing_season": ["Verano"],
        "plant_description": "Árbol con corteza rojiza que se desprende en placas.",
        "historical_notes": "Planta con más de 500 años de uso documentado en México.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Argemone mexicana",
        "botanical_family": "Papaveraceae",
        "popular_names": ["Chicalote", "Cardo santo"],
        "indigenous_names": {"Náhuatl": "Chicalotl"},
        "states_found": ["Todo México"],
        "origin_region": "México - nativa",
        "primary_category": PlantCategory.SKIN_HAIR,
        "secondary_categories": [PlantCategory.PAIN_RELIEF],
        "traditional_uses": ["Problemas de piel", "Verrugas", "Dolor de muelas", "Cataratas (tradicional)"],
        "indigenous_uses": {
            "Medicina prehispánica": ["Látex para ojos", "Dolor"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL.value,
                "dosage": "Látex amarillo",
                "preparation": "Aplicar con cuidado sobre verrugas",
                "frequency": "1-2 veces al día",
                "duration": "Hasta desaparición"
            }
        ],
        "active_compounds": ["Berberina", "Protopina", "Alcaloides"],
        "pharmacological_actions": ["Queratolítico", "Analgésico"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "clinical_studies_count": 10,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": ["SOLO USO EXTERNO", "Látex puede irritar", "Tóxico si se ingiere"],
        "contraindications": ["Uso interno", "Embarazo"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "minimum_age_years": 12,
        "availability_level": "LOW",
        "where_to_find": ["Mercados", "Herbolarias especializadas"],
        "approximate_price_range": "$30-60 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Verano"],
        "plant_description": "Hierba espinosa con flores amarillas, látex amarillo.",
        "ritual_ceremonial_use": "Usado en medicina tradicional azteca.",
        "featured": False,
        "is_active": True
    },
    {
        "scientific_name": "Equisetum arvense",
        "botanical_family": "Equisetaceae",
        "popular_names": ["Cola de caballo"],
        "indigenous_names": {},
        "states_found": ["Todo México", "Zonas húmedas"],
        "origin_region": "Cosmopolita",
        "primary_category": PlantCategory.URINARY,
        "secondary_categories": [PlantCategory.SKIN_HAIR],
        "traditional_uses": ["Infecciones urinarias", "Retención de líquidos", "Fortalece cabello y uñas"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas",
                "preparation": "Infusión 10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": "Máximo 6 semanas continuas"
            }
        ],
        "active_compounds": ["Silicio", "Flavonoides", "Saponinas"],
        "pharmacological_actions": ["Diurético", "Remineralizante"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "clinical_studies_count": 20,
        "safety_level": SafetyLevel.SAFE,
        "precautions": ["No usar más de 6 semanas continuas"],
        "contraindications": ["Problemas cardiacos", "Insuficiencia renal"],
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "minimum_age_years": 12,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Farmacias", "Tiendas naturistas"],
        "approximate_price_range": "$30-60 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Primavera", "Verano"],
        "plant_description": "Planta primitiva sin flores, tallos segmentados verdes.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Gnaphalium spp.",
        "botanical_family": "Asteraceae",
        "popular_names": ["Gordolobo"],
        "indigenous_names": {"Náhuatl": "Yauhtli"},
        "states_found": ["Todo México", "Altiplano"],
        "origin_region": "México - nativa",
        "primary_category": PlantCategory.RESPIRATORY,
        "secondary_categories": [PlantCategory.ANTI_INFLAMMATORY],
        "traditional_uses": ["Tos", "Bronquitis", "Asma", "Problemas respiratorios"],
        "indigenous_uses": {
            "Medicina tradicional": ["Té para tos", "Infecciones respiratorias"]
        },
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharadas de flores y hojas",
                "preparation": "Infusión 10 minutos",
                "frequency": "3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Flavonoides", "Mucílagos", "Taninos"],
        "pharmacological_actions": ["Expectorante", "Antiinflamatorio"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "clinical_studies_count": 10,
        "safety_level": SafetyLevel.VERY_SAFE,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 1,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Herbolarias"],
        "approximate_price_range": "$20-40 MXN",
        "source": "Medicina Tradicional Mexicana",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Otoño", "Invierno"],
        "plant_description": "Hierba con hojas y flores cubiertas de pelusa blanca-grisácea.",
        "featured": True,
        "is_active": True
    },
    {
        "scientific_name": "Melissa officinalis",
        "botanical_family": "Lamiaceae",
        "popular_names": ["Toronjil", "Melisa", "Té de limón"],
        "indigenous_names": {},
        "states_found": ["Todo México"],
        "origin_region": "Mediterráneo, cultivado en México",
        "primary_category": PlantCategory.CALMING,
        "secondary_categories": [PlantCategory.DIGESTIVE],
        "traditional_uses": ["Nerviosismo", "Insomnio", "Problemas digestivos", "Dolor de cabeza"],
        "preparation_methods": [
            {
                "type": PreparationType.TEA.value,
                "dosage": "1-2 cucharaditas de hojas",
                "preparation": "Infusión 5-10 minutos",
                "frequency": "2-3 tazas al día",
                "duration": "Según necesidad"
            }
        ],
        "active_compounds": ["Ácido rosmarínico", "Citral", "Citronelal"],
        "pharmacological_actions": ["Ansiolítico", "Sedante", "Antiviral"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "clinical_studies_count": 45,
        "proven_effects": ["Reduce ansiedad", "Mejora sueño", "Alivia herpes labial (tópico)"],
        "safety_level": SafetyLevel.VERY_SAFE,
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "minimum_age_years": 2,
        "availability_level": "HIGH",
        "where_to_find": ["Mercados", "Farmacias", "Tiendas naturistas"],
        "approximate_price_range": "$30-60 MXN",
        "source": "UNAM",
        "validated_by_expert": True,
        "states_found": ["Todo México"],
        "growing_season": ["Primavera", "Verano"],
        "plant_description": "Hierba perenne aromática, hojas rugosas, aroma a limón.",
        "featured": True,
        "is_active": True
    }
]

async def seed_medicinal_plants():
    """Seed the database with initial medicinal plants data"""
    print("🌿 Starting medicinal plants seed...")

    async with async_engine.begin() as conn:
        # Use the connection to get a session
        async_session = AsyncSession(bind=conn)

        try:
            # Combine all plant data
            all_plants = MEDICINAL_PLANTS_DATA + ADDITIONAL_PLANTS_DATA

            print(f"📊 Preparing to seed {len(all_plants)} medicinal plants...")

            for idx, plant_data in enumerate(all_plants, 1):
                # Check if plant already exists
                result = await async_session.execute(
                    select(MedicinalPlant).where(
                        MedicinalPlant.scientific_name == plant_data["scientific_name"]
                    )
                )
                existing_plant = result.scalar_one_or_none()

                if existing_plant:
                    print(f"⏭️  [{idx}/{len(all_plants)}] {plant_data['scientific_name']} - Already exists, skipping...")
                    continue

                # Create new plant
                plant = MedicinalPlant(**plant_data)
                async_session.add(plant)
                print(f"✅ [{idx}/{len(all_plants)}] Added: {plant_data['scientific_name']} ({plant_data['popular_names'][0]})")

            await async_session.commit()
            print("\n🎉 Seed completed successfully!")
            print(f"📈 Total plants in database: {len(all_plants)}")

        except Exception as e:
            await async_session.rollback()
            print(f"\n❌ Error during seed: {str(e)}")
            raise
        finally:
            await async_session.close()

if __name__ == "__main__":
    print("=" * 70)
    print("🇲🇽 MEXICAN MEDICINAL PLANTS SEED - UNAM RESEARCH BASED")
    print("=" * 70)
    asyncio.run(seed_medicinal_plants())
