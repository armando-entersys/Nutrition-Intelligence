"""
Seed script for Mexican Medicinal Plants
Based on UNAM's Atlas de las Plantas de la Medicina Tradicional Mexicana
"""
import asyncio
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
        "common_name": "Manzanilla",
        "scientific_name": "Matricaria chamomilla",
        "category": PlantCategory.DIGESTIVE,
        "description": "Planta herbácea ampliamente utilizada en México para problemas digestivos, nerviosismo y como antiinflamatorio.",
        "traditional_uses": [
            "Cólicos estomacales e intestinales",
            "Indigestión y gases",
            "Nerviosismo y ansiedad leve",
            "Inflamación ocular (lavados)",
            "Dolor menstrual"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de flores secas por taza de agua hirviendo. Dejar reposar 5-10 minutos tapado.",
                "dosage": "2-3 tazas al día después de las comidas"
            }
        ],
        "active_compounds": ["Apigenina", "Bisabolol", "Camazuleno", "Flavonoides"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Evitar en personas alérgicas a plantas de la familia Asteraceae (margaritas, girasoles).",
        "contraindications": "Alergia conocida a la manzanilla o plantas relacionadas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Cultivada ampliamente en todo México, especialmente en Puebla, Tlaxcala y Estado de México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=matricaria-recutita"
    },
    {
        "common_name": "Hierbabuena",
        "scientific_name": "Mentha spicata",
        "category": PlantCategory.DIGESTIVE,
        "description": "Planta aromática refrescante muy popular en la medicina tradicional mexicana para aliviar problemas digestivos.",
        "traditional_uses": [
            "Dolor de estómago y cólicos",
            "Náuseas y vómito",
            "Gases intestinales",
            "Mal aliento",
            "Dolor de cabeza"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "2-3 hojas frescas o 1 cucharadita de hojas secas por taza de agua hirviendo. Reposar 5 minutos.",
                "dosage": "2-3 tazas al día"
            },
            {
                "type": PreparationType.FRESH,
                "instructions": "Masticar hojas frescas para mal aliento.",
                "dosage": "Según necesidad"
            }
        ],
        "active_compounds": ["Mentol", "Mentona", "Carvona", "Limoneno"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Usar con moderación en niños pequeños. Evitar aceite esencial concentrado en bebés.",
        "contraindications": "Reflujo gastroesofágico severo (puede empeorar los síntomas).",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivada en todo México, especialmente en climas templados y húmedos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=mentha-spicata"
    },
    {
        "common_name": "Gordolobo",
        "scientific_name": "Gnaphalium spp.",
        "category": PlantCategory.RESPIRATORY,
        "description": "Planta tradicional mexicana muy efectiva para afecciones respiratorias, especialmente tos y bronquitis.",
        "traditional_uses": [
            "Tos y resfriados",
            "Bronquitis",
            "Asma leve",
            "Ronquera",
            "Inflamación de garganta"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharada de flores y hojas secas por taza de agua. Hervir 5 minutos y reposar 10 minutos.",
                "dosage": "3-4 tazas al día, puede endulzarse con miel"
            },
            {
                "type": PreparationType.SYRUP,
                "instructions": "Cocinar con miel y limón para jarabe contra la tos.",
                "dosage": "1-2 cucharadas cada 4-6 horas"
            }
        ],
        "active_compounds": ["Flavonoides", "Taninos", "Aceites esenciales", "Mucílagos"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "No usar por períodos prolongados (más de 2 semanas continuas).",
        "contraindications": "No se conocen contraindicaciones específicas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Zonas montañosas del centro de México, especialmente Estado de México, Puebla y Michoacán.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=gnaphalium"
    },
    {
        "common_name": "Tila",
        "scientific_name": "Tilia mexicana",
        "category": PlantCategory.CALMING,
        "description": "Flores calmantes utilizadas tradicionalmente para nervios, ansiedad e insomnio.",
        "traditional_uses": [
            "Nerviosismo y ansiedad",
            "Insomnio",
            "Estrés",
            "Palpitaciones nerviosas",
            "Dolor de cabeza tensional"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de flores secas por taza. Agua casi hirviendo, reposar 10 minutos tapado.",
                "dosage": "1-2 tazas al día, preferentemente antes de dormir"
            }
        ],
        "active_compounds": ["Flavonoides", "Taninos", "Aceites volátiles", "Mucílagos"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede causar somnolencia. No operar maquinaria pesada después de consumir.",
        "contraindications": "Evitar combinar con sedantes fuertes.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Bosques templados del centro de México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=tilia"
    },
    {
        "common_name": "Árnica",
        "scientific_name": "Heterotheca inuloides",
        "category": PlantCategory.ANTI_INFLAMMATORY,
        "description": "Planta mexicana muy apreciada para golpes, moretones y dolores musculares. USO EXTERNO ÚNICAMENTE.",
        "traditional_uses": [
            "Golpes y contusiones",
            "Moretones",
            "Esguinces",
            "Dolores musculares",
            "Inflamación por traumatismos"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TINCTURE,
                "instructions": "Aplicar tintura diluida (1:10 con agua) en compresas sobre la zona afectada.",
                "dosage": "2-3 veces al día"
            },
            {
                "type": PreparationType.COMPRESS,
                "instructions": "Infusión de flores aplicada en compresas frías sobre golpes.",
                "dosage": "Según necesidad"
            }
        ],
        "active_compounds": ["Helenalina", "Flavonoides", "Aceites esenciales", "Lactonas sesquiterpénicas"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": "SOLO USO EXTERNO. NUNCA INGERIR. No aplicar sobre heridas abiertas o piel lastimada. Puede causar dermatitis en personas sensibles.",
        "contraindications": "Alergia a plantas de la familia Asteraceae. Heridas abiertas. NUNCA VÍA ORAL.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 3,
        "mexican_distribution": "Altiplano mexicano, especialmente Estado de México, Hidalgo y Puebla.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=heterotheca-inuloides"
    },
    {
        "common_name": "Sábila (Aloe)",
        "scientific_name": "Aloe vera",
        "category": PlantCategory.SKIN_HAIR,
        "description": "Planta suculenta ampliamente cultivada en México, excelente para problemas de piel y digestivos.",
        "traditional_uses": [
            "Quemaduras leves y solares",
            "Heridas superficiales",
            "Irritación de piel",
            "Estreñimiento (gel interno)",
            "Gastritis (uso interno con precaución)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL,
                "instructions": "Aplicar gel fresco directamente sobre la piel limpia.",
                "dosage": "2-3 veces al día según necesidad"
            },
            {
                "type": PreparationType.JUICE,
                "instructions": "Licuar gel interno con agua o jugo. NUNCA USAR LA CÁSCARA.",
                "dosage": "1/4 taza 1-2 veces al día (uso ocasional)"
            }
        ],
        "active_compounds": ["Acemanano", "Aloína", "Polisacáridos", "Vitaminas A, C, E"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Uso interno: NUNCA usar la cáscara (látex amarillo), solo el gel transparente. Puede causar diarrea. No usar internamente por más de 1-2 semanas.",
        "contraindications": "Embarazo y lactancia (uso interno). Problemas renales. Obstrucción intestinal.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 12,
        "mexican_distribution": "Cultivada en todo México, especialmente en climas cálidos y secos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=aloe-vera"
    },
    {
        "common_name": "Romero",
        "scientific_name": "Rosmarinus officinalis",
        "category": PlantCategory.MEMORY_COGNITION,
        "description": "Hierba aromática con propiedades estimulantes, mejora la concentración y circulación.",
        "traditional_uses": [
            "Mejorar memoria y concentración",
            "Dolor de cabeza",
            "Mala circulación",
            "Dolores musculares",
            "Caída de cabello (uso tópico)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de hojas secas por taza. Agua hirviendo, reposar 10 minutos.",
                "dosage": "1-2 tazas al día"
            },
            {
                "type": PreparationType.TOPICAL,
                "instructions": "Infusión fuerte como enjuague para el cabello.",
                "dosage": "Después del lavado regular"
            }
        ],
        "active_compounds": ["Ácido rosmarínico", "Carnosol", "Cineol", "Alcanfor"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "No exceder dosis recomendadas. Evitar aceite esencial concentrado durante embarazo.",
        "contraindications": "Epilepsia (en dosis altas). Hipertensión severa.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Cultivado en todo México, especialmente en climas templados.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=rosmarinus-officinalis"
    },
    {
        "common_name": "Epazote",
        "scientific_name": "Dysphania ambrosioides",
        "category": PlantCategory.DIGESTIVE,
        "description": "Planta aromática mexicana tradicional, excelente para parásitos intestinales y gases.",
        "traditional_uses": [
            "Parásitos intestinales (lombrices)",
            "Gases intestinales",
            "Cólicos menstruales",
            "Dolor de estómago",
            "Antiparasitario"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 hojas frescas o 1/2 cucharadita seca por taza. Hervir 3-5 minutos.",
                "dosage": "1 taza al día por máximo 3 días para parásitos"
            },
            {
                "type": PreparationType.FRESH,
                "instructions": "Agregar hojas frescas a frijoles y otros alimentos (previene gases).",
                "dosage": "Al cocinar"
            }
        ],
        "active_compounds": ["Ascaridol", "Terpenos", "Aceites esenciales"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": "NO USAR EN EMBARAZO (puede causar aborto). No usar por más de 3 días seguidos. TÓXICO en dosis excesivas. No dar aceite esencial.",
        "contraindications": "Embarazo, lactancia, problemas hepáticos o renales. Niños menores de 2 años.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Nativo de México, crece en todo el país especialmente en zonas cálidas.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=dysphania-ambrosioides"
    },
    {
        "common_name": "Cola de Caballo",
        "scientific_name": "Equisetum arvense",
        "category": PlantCategory.URINARY,
        "description": "Planta diurética tradicional, excelente para problemas urinarios y fortalecimiento de huesos.",
        "traditional_uses": [
            "Retención de líquidos",
            "Infecciones urinarias leves",
            "Cálculos renales (prevención)",
            "Fortalecer uñas y cabello",
            "Cicatrización de heridas"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de planta seca por taza. Hervir 10 minutos y reposar 10 minutos más.",
                "dosage": "2-3 tazas al día entre comidas"
            }
        ],
        "active_compounds": ["Silicio", "Flavonoides", "Saponinas", "Minerales (potasio)"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "No usar por más de 6 semanas continuas. Puede causar deficiencia de tiamina (vitamina B1) con uso prolongado. Asegurar hidratación adecuada.",
        "contraindications": "Embarazo y lactancia. Diabetes (puede afectar niveles de azúcar). Problemas cardíacos o renales graves.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "mexican_distribution": "Zonas húmedas y templadas del centro y sur de México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=equisetum-arvense"
    },
    {
        "common_name": "Pasiflora (Flor de Pasión)",
        "scientific_name": "Passiflora incarnata",
        "category": PlantCategory.CALMING,
        "description": "Planta calmante y sedante natural, excelente para ansiedad e insomnio.",
        "traditional_uses": [
            "Ansiedad y nerviosismo",
            "Insomnio",
            "Estrés",
            "Palpitaciones nerviosas",
            "Síndrome de abstinencia (apoyo)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de hojas y flores secas por taza. Agua hirviendo, reposar 10-15 minutos.",
                "dosage": "1 taza 1-3 veces al día, o 1 hora antes de dormir"
            }
        ],
        "active_compounds": ["Flavonoides", "Alcaloides harmala", "Maltol", "Glucósidos"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Puede causar somnolencia. No operar maquinaria. No combinar con sedantes o ansiolíticos sin supervisión médica.",
        "contraindications": "Embarazo (puede estimular contracciones uterinas). Niños menores de 6 años.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Cultivada en México, especialmente en climas cálidos y húmedos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=passiflora-incarnata"
    },
    {
        "common_name": "Jengibre",
        "scientific_name": "Zingiber officinale",
        "category": PlantCategory.ANTI_INFLAMMATORY,
        "description": "Raíz con potentes propiedades antiinflamatorias, digestivas y contra náuseas.",
        "traditional_uses": [
            "Náuseas y mareos",
            "Dolor artrítico",
            "Inflamación",
            "Resfriados y gripe",
            "Problemas digestivos"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cm de raíz fresca rallada o 1 cucharadita de jengibre en polvo por taza. Hervir 10 minutos.",
                "dosage": "2-3 tazas al día, puede endulzarse con miel"
            },
            {
                "type": PreparationType.FRESH,
                "instructions": "Masticar jengibre fresco o cristalizado para náuseas.",
                "dosage": "Según necesidad"
            }
        ],
        "active_compounds": ["Gingerol", "Shogaol", "Zingerona", "Aceites esenciales"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede aumentar riesgo de sangrado en dosis muy altas. Evitar antes de cirugías.",
        "contraindications": "Trastornos de coagulación. Cálculos biliares (consultar médico).",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivado ampliamente en zonas tropicales de México, especialmente Veracruz y Nayarit.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=zingiber-officinale"
    },
    {
        "common_name": "Cúrcuma",
        "scientific_name": "Curcuma longa",
        "category": PlantCategory.ANTI_INFLAMMATORY,
        "description": "Raíz dorada con poderosas propiedades antiinflamatorias y antioxidantes.",
        "traditional_uses": [
            "Artritis y dolor articular",
            "Inflamación crónica",
            "Problemas digestivos",
            "Salud hepática",
            "Prevención de enfermedades crónicas"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de cúrcuma en polvo con pizca de pimienta negra (mejora absorción). Hervir 10 minutos con leche o agua.",
                "dosage": "1-2 tazas al día"
            },
            {
                "type": PreparationType.CAPSULE,
                "instructions": "Suplementos estandarizados de curcumina.",
                "dosage": "Según indicaciones del producto"
            }
        ],
        "active_compounds": ["Curcumina", "Demetoxicurcumina", "Bisdemetoxicurcumina", "Aceites esenciales"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Combinar con pimienta negra para mejor absorción. Puede manchar ropa y utensilios.",
        "contraindications": "Obstrucción de vías biliares. Cálculos biliares (dosis altas).",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 4,
        "mexican_distribution": "Cultivada en zonas tropicales de México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=curcuma-longa"
    },
    {
        "common_name": "Valeriana",
        "scientific_name": "Valeriana officinalis",
        "category": PlantCategory.CALMING,
        "description": "Sedante natural potente, excelente para ansiedad severa e insomnio.",
        "traditional_uses": [
            "Insomnio severo",
            "Ansiedad intensa",
            "Estrés agudo",
            "Nerviosismo extremo",
            "Taquicardia nerviosa"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de raíz seca por taza. Agua hirviendo, reposar 15 minutos tapado.",
                "dosage": "1 taza 1-2 horas antes de dormir"
            },
            {
                "type": PreparationType.TINCTURE,
                "instructions": "20-30 gotas en agua.",
                "dosage": "1-3 veces al día o antes de dormir"
            }
        ],
        "active_compounds": ["Ácido valerénico", "Valepotriatos", "Alcaloides", "GABA"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Puede causar somnolencia intensa. NO operar maquinaria. NO combinar con alcohol o sedantes. Puede tener efecto paradójico (estimulante) en algunas personas.",
        "contraindications": "Embarazo y lactancia. Problemas hepáticos. Niños menores de 3 años. No combinar con medicamentos sedantes.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 3,
        "mexican_distribution": "Cultivada en zonas templadas de México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=valeriana-officinalis"
    },
    {
        "common_name": "Ajo",
        "scientific_name": "Allium sativum",
        "category": PlantCategory.IMMUNE_SUPPORT,
        "description": "Bulbo medicinal con potentes propiedades antibióticas, antivirales y cardiovasculares.",
        "traditional_uses": [
            "Prevención de resfriados y gripe",
            "Presión arterial alta",
            "Colesterol elevado",
            "Infecciones",
            "Salud cardiovascular"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.FRESH,
                "instructions": "Machacar 1-2 dientes frescos, dejar reposar 10 minutos (activa alicina) y consumir.",
                "dosage": "1-2 dientes al día con alimentos"
            },
            {
                "type": PreparationType.CAPSULE,
                "instructions": "Suplementos estandarizados de extracto de ajo.",
                "dosage": "Según indicaciones del producto"
            }
        ],
        "active_compounds": ["Alicina", "Ajoeno", "S-alilcisteína", "Compuestos azufrados"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede causar mal aliento y olor corporal. Aumenta riesgo de sangrado. Suspender 1-2 semanas antes de cirugías.",
        "contraindications": "Trastornos de coagulación. Uso con anticoagulantes (consultar médico).",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivado ampliamente en todo México, especialmente en Guanajuato y Zacatecas.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=allium-sativum"
    },
    {
        "common_name": "Cilantro",
        "scientific_name": "Coriandrum sativum",
        "category": PlantCategory.DIGESTIVE,
        "description": "Hierba aromática digestiva con propiedades desintoxicantes de metales pesados.",
        "traditional_uses": [
            "Gases y flatulencias",
            "Indigestión",
            "Desintoxicación de metales pesados",
            "Náuseas leves",
            "Mal aliento"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de semillas machacadas por taza. Hervir 10 minutos.",
                "dosage": "2-3 tazas al día después de comidas"
            },
            {
                "type": PreparationType.FRESH,
                "instructions": "Consumir hojas frescas en ensaladas y alimentos.",
                "dosage": "Al gusto, diariamente"
            }
        ],
        "active_compounds": ["Linalol", "Geraniol", "Flavonoides", "Vitaminas A, C, K"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Generalmente seguro. Algunas personas tienen aversión genética al sabor.",
        "contraindications": "Alergia conocida al cilantro.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "mexican_distribution": "Cultivado en todo México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=coriandrum-sativum"
    },
    {
        "common_name": "Chicalote",
        "scientific_name": "Argemone mexicana",
        "category": PlantCategory.PAIN_RELIEF,
        "description": "Planta mexicana tradicional con propiedades analgésicas. USO CONTROLADO por alcaloides tóxicos.",
        "traditional_uses": [
            "Dolor de muelas (látex tópico)",
            "Cataratas (uso tradicional - NO RECOMENDADO)",
            "Verrugas (látex)",
            "Problemas de piel",
            "Ictericia (uso tradicional)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TOPICAL,
                "instructions": "Látex amarillo aplicado directamente sobre dolor de muelas o verrugas. USO EXTERNO ÚNICAMENTE.",
                "dosage": "Aplicación puntual, 1-2 veces al día"
            }
        ],
        "active_compounds": ["Berberina", "Protopina", "Sanguinarina", "Alcaloides"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": "TÓXICA SI SE INGIERE. Solo uso externo. El látex puede irritar piel sensible. NO USAR EN OJOS. Las semillas son altamente tóxicas.",
        "contraindications": "Embarazo, lactancia. Niños. NUNCA INGERIR. NO aplicar en ojos.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "mexican_distribution": "Nativa de México, común en terrenos baldíos de todo el país.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=argemone-mexicana"
    },
    {
        "common_name": "Damiana",
        "scientific_name": "Turnera diffusa",
        "category": PlantCategory.FEMALE_HEALTH,
        "description": "Planta mexicana tradicional afrodisíaca, tónica y estimulante del sistema nervioso.",
        "traditional_uses": [
            "Bajo deseo sexual",
            "Fatiga",
            "Depresión leve",
            "Problemas menstruales",
            "Ansiedad leve"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de hojas secas por taza. Agua hirviendo, reposar 10-15 minutos.",
                "dosage": "1-2 tazas al día"
            },
            {
                "type": PreparationType.TINCTURE,
                "instructions": "20-30 gotas en agua.",
                "dosage": "2-3 veces al día"
            }
        ],
        "active_compounds": ["Arbutina", "Flavonoides", "Aceites esenciales", "Taninos"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Puede causar insomnio si se toma tarde. No exceder dosis recomendadas.",
        "contraindications": "Diabetes (puede afectar niveles de azúcar). Evitar con medicamentos para diabetes.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": False,
        "min_age_children": None,
        "mexican_distribution": "Nativa del norte de México, especialmente Baja California y Sonora.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=turnera-diffusa"
    },
    {
        "common_name": "Cuachalalate",
        "scientific_name": "Amphipterygium adstringens",
        "category": PlantCategory.DIGESTIVE,
        "description": "Corteza medicinal mexicana excepcional para úlceras gástricas y problemas digestivos.",
        "traditional_uses": [
            "Úlceras gástricas",
            "Gastritis",
            "Colitis",
            "Infecciones gastrointestinales",
            "Cicatrización de heridas (tópico)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.DECOCTION,
                "instructions": "1 cucharada de corteza por litro de agua. Hervir 15-20 minutos a fuego lento.",
                "dosage": "1 taza 3 veces al día antes de comidas"
            }
        ],
        "active_compounds": ["Taninos", "Flavonoides", "Triterpenos", "Anacardios"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Puede causar estreñimiento con uso prolongado por su contenido de taninos.",
        "contraindications": "Estreñimiento crónico.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 12,
        "mexican_distribution": "Endémica de México, principalmente en estados del Pacífico: Jalisco, Michoacán, Guerrero y Oaxaca.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=amphipterygium-adstringens"
    },
    {
        "common_name": "Bugambilia",
        "scientific_name": "Bougainvillea spectabilis",
        "category": PlantCategory.RESPIRATORY,
        "description": "Flores ornamentales mexicanas con propiedades expectorantes y contra la tos.",
        "traditional_uses": [
            "Tos seca y persistente",
            "Bronquitis",
            "Asma leve",
            "Resfriados",
            "Inflamación respiratoria"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "5-7 flores (brácteas) por taza de agua hirviendo. Reposar 10 minutos.",
                "dosage": "2-3 tazas al día, puede endulzarse con miel"
            },
            {
                "type": PreparationType.SYRUP,
                "instructions": "Cocinar flores con agua y miel para jarabe contra la tos.",
                "dosage": "1-2 cucharadas 3-4 veces al día"
            }
        ],
        "active_compounds": ["Flavonoides", "Alcaloides", "Taninos", "Betacianinas"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "Generalmente segura. Usar flores limpias sin pesticidas.",
        "contraindications": "No se conocen contraindicaciones específicas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivada ornamentalmente en todo México, especialmente en climas cálidos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=bougainvillea"
    },
    {
        "common_name": "Toronjil Morado",
        "scientific_name": "Agastache mexicana",
        "category": PlantCategory.CALMING,
        "description": "Planta aromática mexicana calmante, excelente para nervios y problemas digestivos.",
        "traditional_uses": [
            "Nerviosismo y ansiedad leve",
            "Problemas de estómago",
            "Cólicos",
            "Dolor de cabeza",
            "Insomnio leve"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 cucharaditas de hojas y flores secas por taza. Agua hirviendo, reposar 10 minutos.",
                "dosage": "2-3 tazas al día"
            }
        ],
        "active_compounds": ["Metil-chavicol", "Timol", "Flavonoides", "Aceites esenciales"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Generalmente muy segura. Puede causar leve somnolencia.",
        "contraindications": "No se conocen contraindicaciones específicas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Nativa del centro de México, común en mercados tradicionales.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=agastache-mexicana"
    },
    {
        "common_name": "Estafiate",
        "scientific_name": "Artemisia ludoviciana",
        "category": PlantCategory.DIGESTIVE,
        "description": "Planta aromática amarga mexicana, excelente para problemas digestivos y parásitos.",
        "traditional_uses": [
            "Parásitos intestinales",
            "Dolor de estómago",
            "Gases",
            "Falta de apetito",
            "Cólicos menstruales"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de hojas secas por taza. Agua hirviendo, reposar 10 minutos. Sabor muy amargo.",
                "dosage": "1 taza 2-3 veces al día antes de comidas"
            }
        ],
        "active_compounds": ["Absintina", "Tuyona", "Flavonoides", "Lactonas sesquiterpénicas"],
        "evidence_level": EvidenceLevel.TRADITIONAL_ONLY,
        "safety_level": SafetyLevel.MODERATE,
        "precautions": "NO USAR EN EMBARAZO (puede causar aborto). No usar por más de 2 semanas continuas. Contiene tuyona que es tóxica en dosis altas.",
        "contraindications": "Embarazo, lactancia. Epilepsia. Problemas renales. No exceder dosis.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": False,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Nativa de México, común en zonas áridas del centro y norte del país.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=artemisia-ludoviciana"
    },
    {
        "common_name": "Guayaba (Hojas)",
        "scientific_name": "Psidium guajava",
        "category": PlantCategory.DIGESTIVE,
        "description": "Hojas astringentes del árbol de guayaba, excelentes para diarrea y problemas digestivos.",
        "traditional_uses": [
            "Diarrea",
            "Disentería",
            "Dolor de estómago",
            "Infecciones intestinales",
            "Higiene bucal (enjuagues)"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "3-5 hojas tiernas por taza. Hervir 10 minutos.",
                "dosage": "2-3 tazas al día para diarrea"
            },
            {
                "type": PreparationType.DECOCTION,
                "instructions": "Decocción concentrada para enjuagues bucales.",
                "dosage": "2-3 veces al día"
            }
        ],
        "active_compounds": ["Taninos", "Flavonoides (quercetina)", "Aceites esenciales", "Vitamina C"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede causar estreñimiento si se usa por más de 3 días para diarrea.",
        "contraindications": "Estreñimiento.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "mexican_distribution": "Cultivada en todo México, especialmente en climas cálidos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=psidium-guajava"
    },
    {
        "common_name": "Nopal",
        "scientific_name": "Opuntia ficus-indica",
        "category": PlantCategory.METABOLIC,
        "description": "Cactus mexicano icónico con excelentes propiedades para controlar azúcar y colesterol.",
        "traditional_uses": [
            "Diabetes (control de glucosa)",
            "Colesterol alto",
            "Sobrepeso",
            "Inflamación",
            "Salud digestiva"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.FRESH,
                "instructions": "Consumir pencas limpias, sin espinas, crudas o cocidas en ensaladas, licuados o guisados.",
                "dosage": "1-2 pencas medianas al día, preferentemente en ayunas"
            },
            {
                "type": PreparationType.JUICE,
                "instructions": "Licuar penca cruda con agua, colar y beber inmediatamente.",
                "dosage": "1 vaso en ayunas"
            }
        ],
        "active_compounds": ["Fibra soluble (mucílago)", "Pectina", "Flavonoides", "Betalaínas", "Vitaminas C, A, K"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede causar diarrea o heces sueltas por su alto contenido de fibra. Iniciar con cantidades pequeñas. Puede interferir con absorción de algunos medicamentos.",
        "contraindications": "Personas con diabetes deben monitorear glucosa (potencia efecto de medicamentos). Obstrucción intestinal.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "mexican_distribution": "Nativo de México, crece en todo el país especialmente en zonas áridas y semiáridas.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=opuntia-ficus-indica"
    },
    {
        "common_name": "Anís de Estrella",
        "scientific_name": "Illicium verum",
        "category": PlantCategory.DIGESTIVE,
        "description": "Especia aromática con propiedades carminativas y expectorantes.",
        "traditional_uses": [
            "Gases y cólicos en bebés",
            "Indigestión",
            "Tos y bronquitis",
            "Flatulencias",
            "Aumentar leche materna"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1-2 estrellas por taza de agua hirviendo. Reposar 10 minutos tapado.",
                "dosage": "1-2 tazas al día"
            }
        ],
        "active_compounds": ["Anetol", "Estragol", "Aceites esenciales"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.SAFE,
        "precautions": "No confundir con anís estrella japonés (tóxico). Comprar solo de fuentes confiables. Dosis moderadas en niños.",
        "contraindications": "Alergias a plantas de la familia Apiaceae. Evitar aceite esencial concentrado en embarazo.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 0,
        "mexican_distribution": "Importado y ampliamente disponible en México.",
        "image_url": None,
        "unam_reference": None
    },
    {
        "common_name": "Canela",
        "scientific_name": "Cinnamomum verum",
        "category": PlantCategory.METABOLIC,
        "description": "Especia aromática con propiedades para controlar azúcar en sangre y mejorar digestión.",
        "traditional_uses": [
            "Control de glucosa en diabetes",
            "Problemas digestivos",
            "Resfriados",
            "Circulación",
            "Inflamación"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 raja de canela (5 cm) por taza. Hervir 10 minutos.",
                "dosage": "1-2 tazas al día"
            },
            {
                "type": PreparationType.POWDER,
                "instructions": "1/2 a 1 cucharadita de canela en polvo en alimentos o bebidas.",
                "dosage": "Diariamente con alimentos"
            }
        ],
        "active_compounds": ["Cinamaldehído", "Eugenol", "Cumarina (en cassia)", "Ácido cinámico"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "La canela cassia (más común) contiene cumarina que puede afectar hígado en dosis muy altas. Preferir canela de Ceilán. No exceder 1 cucharadita diaria de canela cassia.",
        "contraindications": "Problemas hepáticos (dosis altas de cassia). Puede potenciar medicamentos para diabetes.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 1,
        "mexican_distribution": "Importada, ampliamente disponible en todo México.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=cinnamomum"
    },
    {
        "common_name": "Moringa",
        "scientific_name": "Moringa oleifera",
        "category": PlantCategory.IMMUNE_SUPPORT,
        "description": "Árbol tropical nutritivo conocido como 'árbol milagro', rico en vitaminas y minerales.",
        "traditional_uses": [
            "Desnutrición",
            "Aumentar energía",
            "Fortalecer sistema inmune",
            "Lactancia (aumentar producción de leche)",
            "Inflamación"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "1 cucharadita de hojas secas por taza. Agua caliente (no hirviendo), reposar 5 minutos.",
                "dosage": "1-2 tazas al día"
            },
            {
                "type": PreparationType.POWDER,
                "instructions": "1/2 a 1 cucharadita de polvo de hojas en batidos, jugos o alimentos.",
                "dosage": "Diariamente"
            }
        ],
        "active_compounds": ["Vitaminas A, C, E", "Calcio", "Potasio", "Proteínas", "Isotiocianatos", "Quercetina"],
        "evidence_level": EvidenceLevel.MODERATE_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede tener efecto laxante leve. Iniciar con dosis pequeñas. Puede afectar absorción de algunos medicamentos.",
        "contraindications": "Hipotiroidismo (puede interferir con función tiroidea en dosis muy altas). Anticoagulantes (monitorear).",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivada en zonas tropicales de México, especialmente sur y costa del Pacífico.",
        "image_url": None,
        "unam_reference": None
    },
    {
        "common_name": "Chía",
        "scientific_name": "Salvia hispanica",
        "category": PlantCategory.METABOLIC,
        "description": "Semilla ancestral mexicana supernutritiva, rica en omega-3 y fibra.",
        "traditional_uses": [
            "Control de peso",
            "Estreñimiento",
            "Control de glucosa",
            "Salud cardiovascular",
            "Hidratación prolongada"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.FRESH,
                "instructions": "Remojar 1-2 cucharadas de semillas en agua o líquido por 15-30 minutos hasta formar gel.",
                "dosage": "1-2 cucharadas diarias, siempre hidratadas"
            }
        ],
        "active_compounds": ["Omega-3 (ALA)", "Fibra soluble", "Proteína", "Calcio", "Antioxidantes"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "NUNCA consumir semillas secas sin hidratar (riesgo de obstrucción esofágica). Siempre remojar primero. Beber abundante agua.",
        "contraindications": "Disfagia (dificultad para tragar). Obstrucción intestinal. Puede aumentar efecto de anticoagulantes.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 5,
        "mexican_distribution": "Nativa de México y Guatemala, cultivada principalmente en estados del sur.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=salvia-hispanica"
    },
    {
        "common_name": "Amaranto",
        "scientific_name": "Amaranthus hypochondriacus",
        "category": PlantCategory.METABOLIC,
        "description": "Pseudocereal ancestral mexicano altamente nutritivo, rico en proteína y minerales.",
        "traditional_uses": [
            "Desnutrición",
            "Anemia",
            "Fortalecer huesos",
            "Control de colesterol",
            "Salud cardiovascular"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.FRESH,
                "instructions": "Cocinar semillas como cereal, en sopas, o hacer alegrías (dulce tradicional con miel).",
                "dosage": "1/2 a 1 taza de semillas cocidas al día"
            },
            {
                "type": PreparationType.POWDER,
                "instructions": "Harina de amaranto en panes, tortillas o batidos.",
                "dosage": "Incorporar en dieta regular"
            }
        ],
        "active_compounds": ["Proteína completa", "Lisina", "Calcio", "Hierro", "Magnesio", "Escualeno"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Generalmente muy seguro. Libre de gluten (apto para celíacos).",
        "contraindications": "No se conocen contraindicaciones específicas.",
        "safe_in_pregnancy": True,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 6,
        "mexican_distribution": "Nativo de México, cultivado principalmente en Puebla, Tlaxcala y Morelos.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=amaranthus"
    },
    {
        "common_name": "Jamaica (Flor de)",
        "scientific_name": "Hibiscus sabdariffa",
        "category": PlantCategory.METABOLIC,
        "description": "Flor roja mexicana con excelentes propiedades para presión arterial y antioxidantes.",
        "traditional_uses": [
            "Presión arterial alta",
            "Colesterol elevado",
            "Infecciones urinarias",
            "Sobrepeso",
            "Antioxidante"
        ],
        "preparation_methods": [
            {
                "type": PreparationType.TEA,
                "instructions": "2-3 cucharadas de flores secas por litro de agua. Hervir 10 minutos, dejar enfriar. Puede servirse frío.",
                "dosage": "2-3 tazas al día, sin azúcar para máximo beneficio"
            }
        ],
        "active_compounds": ["Antocianinas", "Ácidos orgánicos", "Vitamina C", "Flavonoides"],
        "evidence_level": EvidenceLevel.STRONG_EVIDENCE,
        "safety_level": SafetyLevel.VERY_SAFE,
        "precautions": "Puede potenciar efecto de medicamentos para presión arterial. Personas con presión baja deben moderar consumo. Puede manchar dientes con uso frecuente.",
        "contraindications": "Hipotensión. Puede afectar fertilidad en dosis muy altas (estudios en animales). Evitar con medicamentos para presión.",
        "safe_in_pregnancy": False,
        "safe_in_lactation": True,
        "safe_for_children": True,
        "min_age_children": 2,
        "mexican_distribution": "Cultivada en zonas tropicales de México, especialmente Guerrero, Oaxaca y Veracruz.",
        "image_url": None,
        "unam_reference": "https://www.medicinatradicionalmexicana.unam.mx/apmtm/termino.php?l=3&t=hibiscus-sabdariffa"
    }
]


def seed_medicinal_plants():
    """Seed the database with Mexican medicinal plants data"""
    print("🌿 Starting medicinal plants seeding...")

    with Session(engine) as session:
        # Check if plants already exist
        existing_count = session.exec(select(MedicinalPlant)).all()
        if existing_count:
            print(f"⚠️  Database already contains {len(existing_count)} plants.")
            response = input("Do you want to clear and re-seed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return

            # Clear existing data
            print("🗑️  Clearing existing plants...")
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
                print(f"✅ Added: {plant.common_name} ({plant.scientific_name})")
            except Exception as e:
                print(f"❌ Error adding {plant_data.get('common_name', 'Unknown')}: {e}")
                continue

        # Commit all changes
        session.commit()
        print(f"\n✨ Successfully seeded {plants_added} medicinal plants!")

        # Show summary by category
        print("\n📊 Plants by category:")
        categories = {}
        all_plants = session.exec(select(MedicinalPlant)).all()
        for plant in all_plants:
            cat = plant.category.value
            categories[cat] = categories.get(cat, 0) + 1

        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} plants")


if __name__ == "__main__":
    seed_medicinal_plants()
