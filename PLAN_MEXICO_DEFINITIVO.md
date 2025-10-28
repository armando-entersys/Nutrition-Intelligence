# 🇲🇽 NUTRITION INTELLIGENCE MÉXICO
## Plan Definitivo - App Gratuita para Transformar la Nutrición en México

**Misión:** Combatir la epidemia de obesidad y diabetes en México (75% adultos con sobrepeso) preservando nuestra cultura alimentaria ancestral 🌮🥑

**Respaldo:** Consejo Nacional de Nutriólogos de México
**Modelo:** 100% GRATUITO - Impacto Social

---

## 📊 CONTEXTO MÉXICO - CRISIS NUTRICIONAL

### **Datos Alarmantes 2025**
```
🔴 ADULTOS:
- 75.2% con sobrepeso u obesidad
- 35.7% mujeres con obesidad
- 27% hombres con obesidad
- 12.7% mujeres con diabetes
- 11.9% hombres con diabetes
- 118,000 muertes/año por obesidad

🔴 NIÑOS Y ADOLESCENTES:
- 37% niños escolares con sobrepeso/obesidad
- 40% adolescentes con sobrepeso/obesidad
- 13.3% niños <5 años con desnutrición crónica
- 1.6% niños con desnutrición aguda

🔴 OBJETIVOS 2030 NO ALCANZADOS:
- Solo 1 de 6 metas nutricionales será cumplida
- Anemia, bajo peso al nacer, lactancia: críticos
```

### **Cultura Alimentaria Mexicana** 🌽
```
✅ PATRIMONIO UNESCO (2010):
- Maíz, frijol, chile: base ancestral
- Mestizaje culinario (prehispánico + español)
- Comida = identidad cultural
- Ritual comunitario y familiar
- Técnicas milenarias preservadas

⚠️ RETO:
Mejorar salud SIN perder identidad cultural
```

---

## 💎 NUTRITION INTELLIGENCE - NUESTRA PROPUESTA ÚNICA

### **Lo que NO tiene Nutrimind (nuestro competidor mexicano):**
1. ❌ No es multiplataforma (solo desktop)
2. ❌ No tiene app mobile
3. ❌ No tiene gamificación
4. ❌ No tiene comunidad social
5. ❌ No tiene IA avanzada
6. ❌ No tiene seguimiento en tiempo real
7. ❌ No tiene escáner de etiquetas
8. ❌ Cuesta $4,000-8,000 MXN

### **Lo que SÍ tenemos:**
1. ✅ Multiplataforma (Web + iOS + Android)
2. ✅ 100% GRATUITO
3. ✅ IA avanzada en TODOS los procesos
4. ✅ Gamificación adictiva mexicana
5. ✅ Comunidad social viral
6. ✅ Expediente clínico MÁS completo que Nutrimind
7. ✅ Escáner de etiquetas NOM-051
8. ✅ Adaptado a cultura mexicana
9. ✅ WhatsApp integrado
10. ✅ Respaldo del Consejo Nacional

---

## 🏥 EXPEDIENTE CLÍNICO DIGITAL COMPLETO
### (Cumple NOM-004-SSA3-2012 + Supera a Nutrimind)

### **1. DATOS GENERALES DEL PACIENTE**
```typescript
interface DatosGenerales {
  // Identificación
  nombre_completo: string;
  fecha_nacimiento: Date;
  edad: number; // calculada automáticamente
  sexo: 'masculino' | 'femenino' | 'otro';
  curp: string;
  telefono: string;
  email: string;
  whatsapp: string; // ⭐ INTEGRACIÓN DIRECTA

  // Ubicación
  estado: string;
  municipio: string;
  colonia: string;
  direccion_completa: string;
  cp: string;

  // Contacto de emergencia
  contacto_emergencia: {
    nombre: string;
    parentesco: string;
    telefono: string;
  };

  // Datos socioeconómicos
  ocupacion: string;
  escolaridad: string;
  estado_civil: string;
  num_integrantes_familia: number;

  // Seguro médico
  tiene_seguro: boolean;
  tipo_seguro?: 'IMSS' | 'ISSSTE' | 'Privado' | 'Otro';
  numero_afiliacion?: string;

  // Foto de perfil
  foto_perfil_url?: string;

  // ⭐ IA: Análisis de contexto socioeconómico
  analisis_ia_contexto: {
    nivel_socioeconomico_estimado: string;
    riesgo_desercion: number; // 0-100
    recomendaciones_adaptacion: string[];
  };
}
```

### **2. MEDICIONES ANTROPOMÉTRICAS COMPLETAS**
```typescript
interface MedicionesAntropometricas {
  fecha_medicion: Date;

  // Peso y talla
  peso_kg: number;
  talla_cm: number;
  imc: number; // calculado automáticamente
  interpretacion_imc: string; // bajo peso, normal, sobrepeso, obesidad I,II,III

  // Circunferencias
  circunferencia_cintura_cm: number;
  circunferencia_cadera_cm: number;
  circunferencia_brazo_cm: number;
  circunferencia_pantorrilla_cm: number;
  circunferencia_cuello_cm: number;
  indice_cintura_cadera: number; // calculado
  indice_cintura_talla: number; // calculado

  // Pliegues cutáneos (7 sitios)
  pliegue_tricipital_mm: number;
  pliegue_bicipital_mm: number;
  pliegue_subescapular_mm: number;
  pliegue_suprailiaco_mm: number;
  pliegue_abdominal_mm: number;
  pliegue_muslo_mm: number;
  pliegue_pantorrilla_mm: number;

  // Composición corporal
  porcentaje_grasa: number; // ecuación Durnin-Womersley
  masa_grasa_kg: number;
  masa_libre_grasa_kg: number;
  masa_muscular_kg: number;
  agua_corporal_l: number;

  // Somatotipo (Heath-Carter)
  endomorfia: number;
  mesomorfia: number;
  ectomorfia: number;
  somatotipo: string; // "endomorfo", "mesomorfo", etc.

  // Bioimpedancia (si disponible)
  impedancia_ohms?: number;
  angulo_fase?: number;

  // ⭐ IA: Análisis predictivo
  analisis_ia: {
    tendencia_peso: 'subiendo' | 'bajando' | 'estable';
    prediccion_peso_30d: number;
    riesgo_obesidad: number; // 0-100
    distribucion_grasa: 'androide' | 'ginecoide' | 'mixta';
    recomendaciones_ejercicio: string[];
    alertas: string[];
  };

  // Fotos progreso
  fotos: {
    frontal_url?: string;
    lateral_url?: string;
    posterior_url?: string;
    fecha: Date;
  }[];

  // Gráficas automáticas
  graficas_disponibles: string[]; // ["peso", "imc", "grasa", "circunferencias"]
}
```

### **3. DIETAS DINÁMICAS** ⚡
```typescript
interface DietaDinamica {
  id: string;
  nombre: string; // "Plan de Reducción - Semana 1"
  fecha_inicio: Date;
  fecha_fin: Date;
  objetivo: 'reduccion' | 'mantenimiento' | 'aumento' | 'deportivo' | 'terapeutico';

  // Cálculos nutricionales
  calorias_totales: number;
  distribucion_macros: {
    proteina_g: number;
    proteina_porcentaje: number;
    carbohidratos_g: number;
    carbohidratos_porcentaje: number;
    grasas_g: number;
    grasas_porcentaje: number;
    fibra_g: number;
  };

  // Tiempos de comida
  tiempos_comida: {
    desayuno: TiempoComida;
    colacion_1: TiempoComida;
    comida: TiempoComida;
    colacion_2: TiempoComida;
    cena: TiempoComida;
    colacion_3?: TiempoComida;
  };

  // ⭐ SISTEMA DE EQUIVALENTES MEXICANO (NOM)
  equivalentes_por_dia: {
    cereales_sin_grasa: number;
    cereales_con_grasa: number;
    leguminosas: number;
    verduras: number;
    frutas: number;
    leche_descremada: number;
    leche_semidescremada: number;
    leche_entera: number;
    carnes_muy_bajo_aporte: number;
    carnes_bajo_aporte: number;
    carnes_moderado_aporte: number;
    carnes_alto_aporte: number;
    grasas_sin_proteina: number;
    grasas_con_proteina: number;
    azucares_sin_grasa: number;
    azucares_con_grasa: number;
    alcohol?: number;
  };

  // Menú semanal
  menu_semanal: MenuDia[]; // 7 días

  // ⭐ IA: Generación y optimización
  generado_por_ia: boolean;
  optimizaciones_ia: {
    sustitucion_alimentos_culturales: boolean; // usar ingredientes mexicanos
    considera_presupuesto: boolean;
    considera_temporada: boolean;
    alergias_evitadas: string[];
    preferencias_respetadas: string[];
  };

  // Cumplimiento del paciente
  adherencia_porcentaje: number; // 0-100
  dias_cumplidos: number;
  dias_totales: number;

  // Modificaciones dinámicas (IA ajusta en tiempo real)
  ajustes_automaticos: {
    fecha: Date;
    razon: string;
    cambios: string[];
  }[];

  // Recetas personalizadas mexicanas
  recetas_incluidas: RecetaMexicana[];
}

interface TiempoComida {
  hora_recomendada: string; // "08:00"
  calorias: number;
  alimentos: {
    nombre: string;
    cantidad: string;
    equivalentes_usados: string; // "2 cereales, 1 fruta"
    calorias: number;
  }[];
  opciones_sustitucion: string[]; // ⭐ IA sugiere alternativas
}

interface RecetaMexicana {
  nombre: string;
  ingredientes: string[];
  preparacion: string;
  tiempo_prep_min: number;
  porciones: number;
  calorias_porcion: number;
  foto_url?: string;
  es_tradicional: boolean; // ⭐ receta mexicana auténtica
  region: string; // "Oaxaca", "Veracruz", etc.
  tags: string[]; // "sin_gluten", "vegetariana", "economica"
}
```

### **4. SISTEMA DE EQUIVALENTES MEXICANO** 🇲🇽
```typescript
// Base de datos 3000+ alimentos mexicanos
interface AlimentoMexicano {
  id: string;
  nombre: string;
  nombres_regionales: string[]; // "elote" = "choclo" en algunas regiones
  categoria_equivalente: string;
  cantidad_porcion: string;

  // Información nutricional
  calorias: number;
  proteina_g: number;
  carbohidratos_g: number;
  grasa_g: number;
  fibra_g: number;

  // Micronutrientes importantes
  calcio_mg: number;
  hierro_mg: number;
  vitamina_a_mcg: number;
  vitamina_c_mg: number;
  folato_mcg: number;

  // Contexto cultural
  es_tradicional_mexicano: boolean;
  region_origen: string[];
  temporada: string[]; // meses disponibles
  costo_relativo: 'economico' | 'moderado' | 'caro';
  disponibilidad: 'alta' | 'media' | 'baja';

  // ⭐ IA: Análisis de salubridad
  nivel_procesamiento: 'minimo' | 'procesado' | 'ultra_procesado';
  indice_glucemico: number;
  carga_glucemica: number;
  potencial_alergeno: string[];

  // Foto
  imagen_url: string;

  // Intercambios sugeridos (IA)
  sustitutos_similares: string[]; // IDs de otros alimentos
}

// Ejemplos de alimentos mexicanos en la base
const ejemplos_alimentos = [
  {
    nombre: "Tortilla de maíz",
    categoria: "Cereales sin grasa",
    cantidad: "1 pieza (30g)",
    es_tradicional: true,
    region: ["Todo México"],
  },
  {
    nombre: "Frijoles negros cocidos",
    categoria: "Leguminosas",
    cantidad: "1/2 taza (90g)",
    es_tradicional: true,
  },
  {
    nombre: "Nopal asado",
    categoria: "Verduras",
    cantidad: "1 taza (150g)",
    es_tradicional: true,
  },
  {
    nombre: "Aguacate (avocado)",
    categoria: "Grasas con proteína",
    cantidad: "1/3 pieza mediana",
    es_tradicional: true,
  },
  {
    nombre: "Atole de avena",
    categoria: "Cereales sin grasa + Leche",
    cantidad: "1 taza (240ml)",
    es_tradicional: true,
  },
  {
    nombre: "Tamal de pollo (sin manteca)",
    categoria: "Cereales + Carne",
    cantidad: "1 pieza pequeña",
    es_tradicional: true,
  },
  {
    nombre: "Quesadilla de flor de calabaza",
    categoria: "Cereales + Verdura + Grasa",
    cantidad: "1 pieza",
    es_tradicional: true,
  },
  {
    nombre: "Agua de jamaica sin azúcar",
    categoria: "Bebida libre",
    cantidad: "1 vaso",
    es_tradicional: true,
  }
];
```

### **5. RECORDATORIO DE 24 HORAS** 📝
```typescript
interface Recordatorio24H {
  fecha: Date;
  dia_semana: string;

  // Método de recolección
  metodo: 'entrevista' | 'app_paciente' | 'foto' | 'mixto';

  // Comidas del día
  comidas: {
    tiempo: 'desayuno' | 'colacion_1' | 'comida' | 'colacion_2' | 'cena' | 'colacion_3';
    hora: string;
    lugar: string; // "casa", "restaurante", "trabajo"

    alimentos_consumidos: {
      nombre: string;
      cantidad: string;
      modo_preparacion: string;
      calorias: number;
      foto_url?: string; // ⭐ IA analiza foto
    }[];

    calorias_total: number;
  }[];

  // Análisis del día
  calorias_totales: number;
  proteina_total_g: number;
  carbohidratos_total_g: number;
  grasas_total_g: number;
  fibra_total_g: number;
  agua_total_ml: number;

  // Comparación con dieta prescrita
  adherencia_dieta: {
    calorias_objetivo: number;
    calorias_reales: number;
    diferencia_calorias: number;
    porcentaje_cumplimiento: number;
    equivalentes_cumplidos: {
      categoria: string;
      objetivo: number;
      consumido: number;
    }[];
  };

  // ⭐ IA: Análisis inteligente
  analisis_ia: {
    calidad_alimentacion: number; // 0-100
    alimentos_ultra_procesados_porcentaje: number;
    balance_macronutrientes: 'optimo' | 'alto_carbos' | 'alto_grasas' | 'alto_proteina';
    deficiencias_detectadas: string[]; // "bajo consumo de verduras"
    excesos_detectados: string[]; // "alto consumo de azúcar"
    horarios_irregulares: boolean;
    recomendaciones: string[];
    alimentos_culturales_identificados: string[]; // reconoce platillos mexicanos
  };

  // Emociones y contexto
  estado_emocional: string; // "estresado", "feliz", "ansioso"
  hubo_evento_especial: boolean; // fiesta, cumpleaños
  notas_paciente: string;
}
```

### **6. HISTORIA CLÍNICA COMPLETA** 🏥
```typescript
interface HistoriaClinica {
  // Antecedentes heredofamiliares
  antecedentes_familiares: {
    diabetes: { presente: boolean; quien: string[]; };
    hipertension: { presente: boolean; quien: string[]; };
    obesidad: { presente: boolean; quien: string[]; };
    dislipidemias: { presente: boolean; quien: string[]; };
    cancer: { presente: boolean; tipo: string; quien: string[]; };
    enfermedades_cardiacas: { presente: boolean; tipo: string; quien: string[]; };
    enfermedades_renales: { presente: boolean; quien: string[]; };
    enfermedades_gastrointestinales: { presente: boolean; tipo: string; quien: string[]; };
    otros: string;
  };

  // Antecedentes personales patológicos
  antecedentes_patologicos: {
    enfermedades_cronicas: {
      nombre: string;
      fecha_diagnostico: Date;
      tratamiento_actual: string;
      controlada: boolean;
    }[];

    cirugias_previas: {
      tipo: string;
      fecha: Date;
      hospital: string;
    }[];

    hospitalizaciones: {
      razon: string;
      fecha: Date;
      duracion_dias: number;
    }[];

    alergias_medicamentos: string[];
    alergias_alimentos: string[];
    intolerancias_alimentarias: string[];
  };

  // Antecedentes gineco-obstétricos (mujeres)
  antecedentes_gineco?: {
    menarca_edad: number;
    ciclos_regulares: boolean;
    fecha_ultima_menstruacion: Date;
    embarazos_previos: number;
    partos: number;
    cesareas: number;
    abortos: number;
    lactancia_actual: boolean;
    menopausia: boolean;
    edad_menopausia?: number;
    terapia_hormonal: boolean;
  };

  // Medicamentos actuales
  medicamentos_actuales: {
    nombre: string;
    dosis: string;
    frecuencia: string;
    indicacion: string;
    fecha_inicio: Date;
    interacciones_nutricion: string[]; // ⭐ IA detecta interacciones
  }[];

  // Suplementos
  suplementos: {
    nombre: string;
    dosis: string;
    frecuencia: string;
    marca: string;
    necesario: boolean; // evaluado por nutriólogo
  }[];

  // ⭐ IA: Análisis de riesgo
  analisis_riesgo_ia: {
    riesgo_cardiovascular: number; // 0-100
    riesgo_diabetes_tipo2: number;
    riesgo_sindrome_metabolico: number;
    riesgo_osteoporosis: number;
    riesgo_anemia: number;
    factores_riesgo_identificados: string[];
    recomendaciones_preventivas: string[];
  };
}
```

### **7. DATOS DE LABORATORIO** 🧪
```typescript
interface DatosLaboratorio {
  fecha_estudio: Date;
  tipo_estudio: string; // "Química sanguínea", "Perfil lipídico", etc.
  laboratorio: string;

  // Perfil glucémico
  glucosa_ayuno_mgdl?: number;
  glucosa_postprandial_mgdl?: number;
  hemoglobina_glucosilada_porcentaje?: number;
  insulina_ayuno_uUIml?: number;
  homa_ir?: number; // calculado

  // Perfil lipídico
  colesterol_total_mgdl?: number;
  ldl_mgdl?: number;
  hdl_mgdl?: number;
  trigliceridos_mgdl?: number;
  indice_aterogenico?: number; // calculado

  // Función renal
  creatinina_mgdl?: number;
  urea_mgdl?: number;
  acido_urico_mgdl?: number;
  tasa_filtracion_glomerular?: number;

  // Función hepática
  alt_tgp_Ul?: number;
  ast_tgo_Ul?: number;
  bilirrubina_total_mgdl?: number;
  fosfatasa_alcalina_Ul?: number;
  albumina_gdl?: number;

  // Perfil tiroideo
  tsh_uUIml?: number;
  t3_ngdl?: number;
  t4_libre_ngdl?: number;

  // Electrolitos
  sodio_mEql?: number;
  potasio_mEql?: number;
  calcio_mgdl?: number;
  magnesio_mgdl?: number;

  // Biometría hemática
  hemoglobina_gdl?: number;
  hematocrito_porcentaje?: number;
  leucocitos_mm3?: number;
  plaquetas_mm3?: number;

  // Vitaminas y minerales
  vitamina_d_ngml?: number;
  vitamina_b12_pgml?: number;
  acido_folico_ngml?: number;
  hierro_serico_mcgdl?: number;
  ferritina_ngml?: number;

  // Otros
  proteina_c_reactiva_mgdl?: number;

  // ⭐ IA: Interpretación automática
  interpretacion_ia: {
    valores_fuera_rango: {
      parametro: string;
      valor: number;
      rango_normal: string;
      severidad: 'leve' | 'moderada' | 'severa';
      significado_clinico: string;
    }[];
    diagnosticos_sugeridos: string[];
    ajustes_dieta_recomendados: string[];
    estudios_adicionales_sugeridos: string[];
    alertas_criticas: string[]; // valores peligrosos
  };

  // Archivo PDF del estudio
  archivo_pdf_url: string;

  // Comparación con estudios previos (tendencias)
  tendencias: {
    parametro: string;
    direccion: 'mejorando' | 'empeorando' | 'estable';
    cambio_porcentual: number;
  }[];
}
```

### **8. SIGNOS VITALES** 💓
```typescript
interface SignosVitales {
  fecha_hora: Date;
  lugar_medicion: 'consultorio' | 'casa' | 'hospital';

  // Presión arterial
  presion_sistolica_mmHg: number;
  presion_diastolica_mmHg: number;
  presion_arterial_media?: number; // calculada
  clasificacion_presion: string; // "Normal", "Pre-hipertensión", etc.

  // Frecuencia cardíaca
  frecuencia_cardiaca_lpm: number;
  ritmo_regular: boolean;

  // Frecuencia respiratoria
  frecuencia_respiratoria_rpm: number;

  // Temperatura
  temperatura_celsius: number;

  // Oximetría
  saturacion_oxigeno_porcentaje?: number;

  // Glucometría capilar
  glucosa_capilar_mgdl?: number;
  momento_medicion: 'ayuno' | 'postprandial' | 'aleatorio';

  // ⭐ IA: Detección de anomalías
  alertas_ia: {
    presion_anormal: boolean;
    taquicardia: boolean;
    bradicardia: boolean;
    hipoglucemia: boolean;
    hiperglucemia: boolean;
    recomendacion_urgente: string;
  };

  // Notas
  notas: string;
  medido_por: string; // "Dr. Juan Pérez", "Auto-medición"
}
```

### **9. ARCHIVOS CLÍNICOS** 📄
```typescript
interface ArchivosClinicosInterface ArchivoClinco {
  id: string;
  tipo: 'laboratorio' | 'radiografia' | 'ultrasonido' | 'receta' | 'consentimiento' | 'otro';
  nombre: string;
  descripcion: string;
  fecha_documento: Date;
  fecha_subida: Date;
  archivo_url: string;
  formato: 'pdf' | 'jpg' | 'png' | 'doc';
  tamanio_mb: number;

  // ⭐ IA: OCR y extracción de datos
  extraido_por_ia: boolean;
  datos_extraidos?: {
    tipo_estudio: string;
    valores_clave: { [key: string]: any };
    fecha_estudio: Date;
    laboratorio: string;
  };

  tags: string[]; // para búsqueda rápida
  subido_por: 'nutriologo' | 'paciente';
}
```

### **10. ENTREVISTA MOTIVACIONAL** 💬
```typescript
interface EntrevistaMotiacional {
  fecha: Date;
  sesion_numero: number;

  // Etapa de cambio (Prochaska)
  etapa_cambio: 'precontemplacion' | 'contemplacion' | 'preparacion' | 'accion' | 'mantenimiento' | 'recaida';

  // Motivación para cambio (escala 1-10)
  nivel_motivacion: number;
  nivel_confianza: number;

  // Objetivos del paciente
  objetivos_propios: string[];
  razon_principal_consulta: string;

  // Barreras identificadas
  barreras: {
    tipo: 'economica' | 'tiempo' | 'conocimiento' | 'familiar' | 'emocional' | 'otra';
    descripcion: string;
    severidad: number; // 1-10
  }[];

  // Facilitadores
  recursos_apoyo: string[]; // "familia", "amigos", "trabajo flexible"
  experiencias_previas_exito: string[];

  // Balance decisional
  pros_cambio: string[];
  contras_cambio: string[];

  // Metas específicas (SMART)
  metas: {
    descripcion: string;
    especifica: string;
    medible: string;
    alcanzable: boolean;
    relevante: string;
    tiempo_limite: Date;
    cumplida: boolean;
  }[];

  // Plan de acción
  acciones_comprometidas: string[];
  fecha_seguimiento: Date;

  // ⭐ IA: Análisis predictivo
  analisis_ia: {
    probabilidad_adherencia: number; // 0-100
    factores_riesgo_abandono: string[];
    recomendaciones_motivacionales: string[];
    estrategias_sugeridas: string[];
  };

  // Notas del nutriólogo
  notas_sesion: string;
  audio_sesion_url?: string; // grabación (con consentimiento)
}
```

### **11. ACTIVIDAD FÍSICA** 🏃
```typescript
interface ActividadFisica {
  fecha: Date;

  // Cuestionario IPAQ (International Physical Activity Questionnaire)
  nivel_actividad: 'sedentario' | 'ligero' | 'moderado' | 'vigoroso';

  // Actividad laboral
  trabajo_tipo: 'oficina' | 'pie_estatico' | 'caminando' | 'esfuerzo_fisico';
  horas_sentado_dia: number;

  // Ejercicio estructurado
  realiza_ejercicio: boolean;
  tipo_ejercicio: string[]; // "cardio", "pesas", "yoga", etc.
  frecuencia_semanal: number;
  duracion_promedio_min: number;

  // Deporte específico
  practica_deporte: boolean;
  deporte_nombre?: string;
  nivel: 'recreativo' | 'competitivo' | 'profesional';

  // Actividades diarias
  camina_diario_min: number;
  pasos_promedio_dia?: number; // si usa smartwatch
  escaleras_pisos_dia?: number;

  // Limitaciones
  lesiones_actuales: string[];
  limitaciones_medicas: string[];
  dolor_ejercicio: boolean;

  // Metas de actividad física
  meta_pasos_dia: number;
  meta_ejercicio_semanal_min: number;

  // Integración con dispositivos
  dispositivo_conectado?: 'apple_watch' | 'fitbit' | 'garmin' | 'xiaomi' | 'otro';
  datos_sincronizados: boolean;

  // ⭐ IA: Recomendaciones personalizadas
  plan_ejercicio_ia: {
    tipo_recomendado: string[];
    intensidad: string;
    frecuencia_sugerida: number;
    duracion_sugerida_min: number;
    consideraciones_salud: string[];
    ejercicios_contraindicados: string[];
    progresion_12_semanas: {
      semana: number;
      objetivos: string;
      actividades: string[];
    }[];
  };

  // Historial de ejercicios (tracking)
  sesiones_ejercicio: {
    fecha: Date;
    tipo: string;
    duracion_min: number;
    intensidad: 'baja' | 'media' | 'alta';
    calorias_quemadas?: number;
    notas: string;
  }[];
}
```

### **12. CUESTIONARIOS ESPECIALIZADOS** 📋
```typescript
interface Cuestionarios {
  // Cuestionario de frecuencia de consumo
  frecuencia_consumo: {
    alimento: string;
    frecuencia: 'nunca' | 'rara_vez' | '1-2_mes' | '1_semana' | '2-4_semana' | '5-6_semana' | 'diario';
    porcion_promedio: string;
  }[];

  // Screening nutricional
  malnutrition_screening_tool?: {
    perdida_peso_involuntaria: boolean;
    porcentaje_perdida: number;
    apetito_disminuido: boolean;
    enfermedad_aguda: boolean;
    riesgo: 'bajo' | 'medio' | 'alto';
  };

  // Cuestionario de hambre emocional
  comer_emocional: {
    come_cuando_estresado: number; // 1-5
    come_cuando_triste: number;
    come_cuando_aburrido: number;
    come_por_ansiedad: number;
    come_por_celebracion: number;
    puntuacion_total: number;
    nivel: 'bajo' | 'moderado' | 'alto';
  };

  // Cuestionario de trastornos alimentarios (EAT-26)
  eat26?: {
    puntuacion_total: number;
    riesgo_trastorno: boolean;
    requiere_referencia_psicologia: boolean;
  };

  // Calidad de sueño (Pittsburgh)
  calidad_sueno: {
    horas_sueno_promedio: number;
    latencia_sueno_min: number;
    despertares_nocturnos: number;
    calidad_percibida: number; // 1-5
    puntuacion_global: number;
    tiene_trastorno_sueno: boolean;
  };

  // Estrés percibido (Cohen)
  nivel_estres: {
    puntuacion: number; // 0-40
    nivel: 'bajo' | 'moderado' | 'alto';
  };

  // Satisfacción corporal
  imagen_corporal: {
    satisfaccion_actual: number; // 1-10
    importancia_apariencia: number;
    influencia_redes_sociales: number;
  };

  // ⭐ IA: Análisis psicológico-nutricional
  perfil_psicologico_ia: {
    riesgo_trastorno_alimentario: number; // 0-100
    patron_alimentario_emocional: boolean;
    necesita_apoyo_psicologico: boolean;
    factores_psicologicos_clave: string[];
    recomendaciones_abordaje: string[];
  };
}
```

### **13. HÁBITOS** 🎯
```typescript
interface Habitos {
  fecha_evaluacion: Date;

  // Hábitos alimentarios
  num_comidas_dia: number;
  desayuna_diario: boolean;
  hora_primera_comida: string;
  hora_ultima_comida: string;
  ventana_alimentacion_horas: number;

  // Comportamientos
  come_viendo_tv: boolean;
  come_trabajando: boolean;
  come_rapido: boolean;
  mastica_suficiente: boolean;

  // Preferencias
  alimentos_favoritos: string[];
  alimentos_rechazados: string[];
  comida_mexicana_favorita: string[]; // ⭐ platillos tradicionales

  // Hidratación
  vasos_agua_dia: number;
  consume_refrescos: boolean;
  refrescos_semana: number;
  consume_alcohol: boolean;
  bebidas_alcoholicas_semana: number;

  // Tabaquismo
  fuma: boolean;
  cigarros_dia?: number;
  años_fumando?: number;

  // Compras y cocina
  quien_cocina_hogar: string;
  frecuencia_compra_alimentos: string;
  presupuesto_mensual_alimentos?: number;
  compra_mercado_local: boolean;
  compra_supermercado: boolean;

  // Hábitos culturales mexicanos ⭐
  consume_tortilla_diario: boolean;
  consume_frijol_diario: boolean;
  consume_chile_diario: boolean;
  desayuno_tipico: string; // "tamales", "chilaquiles", etc.
  come_tacos_semana: number;
  asiste_fondas_semana: number;

  // ⭐ IA: Análisis de hábitos
  analisis_habitos_ia: {
    habitos_positivos: string[];
    habitos_negativos: string[];
    habitos_criticos: string[]; // urgente modificar
    facilidad_cambio: { [habito: string]: number }; // 0-100
    plan_modificacion_gradual: {
      semana: number;
      habito_objetivo: string;
      estrategia: string;
    }[];
  };
}
```

### **14. APP DE SEGUIMIENTO PACIENTE** 📱
```typescript
interface SeguimientoPacienteApp {
  // Tracking diario automático
  registro_comidas: {
    fecha_hora: Date;
    comida: string;
    foto_url?: string;
    metodo: 'manual' | 'foto_ia' | 'escaneo_barcode';
    validado_nutriologo: boolean;
  }[];

  // Registro de agua
  vasos_agua_hoy: number;
  objetivo_agua_l: number;

  // Peso diario
  peso_registrado: {
    fecha: Date;
    peso_kg: number;
    hora: string;
    condiciones: string; // "en ayunas", "después de ejercicio"
  }[];

  // Actividad física
  pasos_hoy: number;
  ejercicio_hoy: {
    tipo: string;
    duracion_min: number;
    intensidad: string;
  }[];

  // Estado de ánimo
  animo_hoy: 'excelente' | 'bien' | 'regular' | 'mal' | 'muy_mal';
  nivel_energia: number; // 1-10
  nivel_hambre_promedio: number; // 1-10

  // Cumplimiento de dieta
  comidas_plan_cumplidas: number;
  comidas_plan_total: number;
  porcentaje_adherencia_hoy: number;

  // Racha (streak)
  dias_consecutivos_registro: number;
  racha_actual: number;
  racha_maxima: number;

  // Comunicación con nutriólogo
  mensajes_whatsapp: {
    fecha: Date;
    tipo: 'paciente' | 'nutriologo';
    mensaje: string;
    foto_url?: string;
  }[];

  // Recordatorios configurados
  recordatorios: {
    tipo: 'comida' | 'agua' | 'medicamento' | 'ejercicio';
    hora: string;
    activo: boolean;
    dias_semana: number[]; // 0-6
  }[];

  // ⭐ IA: Coach virtual
  coach_ia: {
    mensaje_motivacional_diario: string;
    sugerencias_personalizadas: string[];
    alertas_patrones: string[]; // "has cenado tarde 3 días seguidos"
    prediccion_adherencia_semanal: number;
  };
}
```

### **15. PAGOS DEL PACIENTE** 💰
```typescript
interface PagosPaciente {
  // Esquema de cobro del nutriólogo
  tipo_plan: 'consulta_individual' | 'plan_mensual' | 'plan_trimestral' | 'plan_semestral';
  costo_consulta_individual?: number;
  costo_plan?: number;

  // Historial de pagos
  pagos: {
    id: string;
    fecha: Date;
    concepto: string;
    monto: number;
    metodo_pago: 'efectivo' | 'tarjeta' | 'transferencia' | 'oxxo' | 'mercadopago' | 'stripe';
    comprobante_url?: string;
    status: 'pendiente' | 'pagado' | 'vencido';
  }[];

  // Balance
  pagos_totales: number;
  saldo_pendiente: number;

  // Próximo pago
  proximo_pago_fecha: Date;
  proximo_pago_monto: number;

  // Descuentos aplicados
  tiene_descuento: boolean;
  porcentaje_descuento?: number;
  razon_descuento?: string;

  // ⭐ Integración de pagos
  integracion_mercadopago: boolean;
  integracion_stripe: boolean;

  // Recordatorios de pago
  enviar_recordatorio_dias_antes: number;
  recordatorio_enviado: boolean;

  // Facturación
  requiere_factura: boolean;
  rfc?: string;
  razon_social?: string;
  facturas_emitidas: {
    fecha: Date;
    folio: string;
    monto: number;
    pdf_url: string;
  }[];
}
```

### **16. WHATSAPP INTEGRADO** 💬
```typescript
interface IntegracionWhatsApp {
  numero_nutriologo: string;
  numero_paciente: string;

  // Configuración
  notificaciones_whatsapp_activas: boolean;
  acepto_whatsapp_business: boolean;

  // Mensajes programados
  mensajes_automaticos: {
    tipo: 'recordatorio_cita' | 'seguimiento_semanal' | 'motivacional' | 'cumpleanos';
    plantilla: string;
    frecuencia: string;
    activo: boolean;
  }[];

  // Historial de conversación (últimos 30 días)
  conversacion: {
    fecha_hora: Date;
    remitente: 'paciente' | 'nutriologo' | 'sistema';
    mensaje: string;
    tipo: 'texto' | 'imagen' | 'documento' | 'audio';
    url_archivo?: string;
    leido: boolean;
  }[];

  // ⭐ IA: Análisis de sentiment
  analisis_conversacion_ia: {
    tono_paciente: 'positivo' | 'neutral' | 'negativo';
    nivel_compromiso: number; // 0-100
    preguntas_frecuentes: string[];
    temas_recurrentes: string[];
    alerta_abandono: boolean;
  };

  // Templates rápidos para nutriólogo
  respuestas_rapidas: {
    nombre: string;
    texto: string;
  }[];

  // Recordatorios de citas por WhatsApp
  recordatorio_24h_antes: boolean;
  recordatorio_1h_antes: boolean;
}
```

### **17. AGENDA DEL NUTRIÓLOGO** 📅
```typescript
interface AgendaNutriologo {
  // Configuración de horarios
  horario_atencion: {
    dia_semana: number; // 0-6 (0=Domingo)
    activo: boolean;
    hora_inicio: string; // "09:00"
    hora_fin: string; // "18:00"
    duracion_consulta_min: number; // típicamente 60
    descanso_entre_consultas_min: number; // 15
  }[];

  // Días no laborables
  dias_bloqueados: {
    fecha: Date;
    razon: string; // "vacaciones", "congreso", etc.
    todo_el_dia: boolean;
    hora_inicio?: string;
    hora_fin?: string;
  }[];

  // Citas agendadas
  citas: {
    id: string;
    paciente_id: string;
    paciente_nombre: string;
    fecha_hora: Date;
    duracion_min: number;
    tipo: 'primera_vez' | 'seguimiento' | 'urgencia' | 'online' | 'presencial';
    status: 'confirmada' | 'pendiente' | 'completada' | 'cancelada' | 'no_asistio';

    // Motivo de la consulta
    motivo: string;

    // Recordatorios enviados
    recordatorio_enviado_24h: boolean;
    recordatorio_enviado_1h: boolean;

    // Notas de la cita
    notas_previas: string;
    notas_consulta: string;

    // Link para consulta online
    link_videollamada?: string;

    // Archivos asociados
    archivos_adjuntos: string[];
  }[];

  // ⭐ IA: Optimización de agenda
  sugerencias_ia: {
    horarios_mas_solicitados: string[];
    dias_menor_demanda: number[];
    sugerencia_bloqueos: string[];
    pacientes_con_cita_pendiente: {
      paciente_id: string;
      dias_sin_cita: number;
      urgencia: 'baja' | 'media' | 'alta';
    }[];
  };

  // Integración con Google Calendar
  sync_google_calendar: boolean;
  google_calendar_id?: string;

  // Estadísticas
  estadisticas_mes: {
    total_citas: number;
    citas_completadas: number;
    citas_canceladas: number;
    tasa_ausencia: number;
    horarios_pico: string[];
  };
}
```

---

## 🤖 INTELIGENCIA ARTIFICIAL - FEATURES AVANZADOS

### **1. ANÁLISIS DE FOTOS DE COMIDA** 📸
```typescript
interface AnalisisFotoComidaIA {
  // Input
  foto_url: string;
  fecha_hora: Date;

  // ⭐ IA: Detección automática
  analisis: {
    // Identificación de alimentos
    alimentos_detectados: {
      nombre: string;
      confianza: number; // 0-1
      cantidad_estimada: string;
      calorias_estimadas: number;
      categoria: string;
    }[];

    // Reconocimiento de platillos mexicanos
    platillo_identificado?: {
      nombre: string; // "tacos al pastor", "mole poblano"
      confianza: number;
      region: string;
      ingredientes_tipicos: string[];
    };

    // Análisis nutricional estimado
    estimacion_nutricional: {
      calorias_total: number;
      proteina_g: number;
      carbohidratos_g: number;
      grasas_g: number;
      rango_error: number; // ±20%
    };

    // Evaluación de calidad
    evaluacion_salubridad: {
      score: number; // 0-100
      alto_en_grasa: boolean;
      alto_en_azucar: boolean;
      alto_en_sodio: boolean;
      ultra_procesado: boolean;
      contiene_verduras: boolean;
      porcion_adecuada: boolean;
    };

    // Sugerencias de mejora
    sugerencias: string[];

    // Etiquetas generadas
    tags: string[]; // "desayuno", "mexicano", "casero", "frito"
  };

  // Validación por nutriólogo
  validado: boolean;
  correcciones_nutriologo?: string;
}
```

### **2. ESCÁNER DE ETIQUETAS NOM-051** 🏷️
```typescript
interface EscanerEtiquetaNOM {
  // Input
  foto_etiqueta_url: string;

  // ⭐ OCR: Extracción de información
  informacion_extraida: {
    nombre_producto: string;
    marca: string;
    tamanio_porcion: string;
    porciones_envase: number;

    // Tabla nutrimental
    por_porcion: {
      calorias: number;
      grasa_total_g: number;
      grasa_saturada_g: number;
      grasa_trans_g: number;
      carbohidratos_g: number;
      azucares_g: number;
      azucares_anadidos_g?: number;
      proteina_g: number;
      fibra_g: number;
      sodio_mg: number;
    };

    // Lista de ingredientes
    ingredientes: string[];

    // Alérgenos
    contiene_alergenos: string[];
    puede_contener_alergenos: string[];
  };

  // ⭐ Análisis NOM-051 (Etiquetado frontal México)
  analisis_nom051: {
    // Sellos de advertencia
    sellos: {
      exceso_calorias: boolean;
      exceso_azucares: boolean;
      exceso_grasas_saturadas: boolean;
      exceso_grasas_trans: boolean;
      exceso_sodio: boolean;
    };

    // Leyendas precautorias
    contiene_cafeina: boolean;
    evitar_ninos: boolean;
    contiene_edulcorantes: boolean;

    // Calificación salubridad
    score_salubridad: number; // 0-100
    recomendado_consumo: 'si' | 'ocasional' | 'no_recomendado';
  };

  // ⭐ Comparación con alternativas más saludables
  alternativas_mejores: {
    nombre: string;
    marca: string;
    porque_es_mejor: string[];
    reduccion_calorias: number;
    reduccion_azucar_g: number;
    reduccion_sodio_mg: number;
    disponible_donde: string[];
  }[];

  // Verificación de claims
  verificacion_claims: {
    claim_etiqueta: string; // "bajo en azúcar", "light", etc.
    cumple_norma: boolean;
    explicacion: string;
  }[];

  // Alertas personalizadas
  alertas_paciente: string[]; // "Alto en azúcar - evitar si diabético"

  // Almacenamiento en historial
  guardado_en_historial: boolean;
  categoria_producto: string;
}
```

### **3. CHAT con NUTRIÓLOGO VIRTUAL (IA)** 🤖
```typescript
interface ChatNutriologoIA {
  // Asistente IA 24/7 para pacientes
  conversacion: {
    mensaje: string;
    remitente: 'paciente' | 'ia';
    fecha_hora: Date;

    // Contexto de la pregunta
    contexto_detectado: string; // "receta", "sustitucion", "duda_nutrimental"
  }[];

  // ⭐ Capacidades del asistente IA
  funcionalidades: {
    // Responder dudas nutricionales
    responde_dudas_generales: true;
    explica_conceptos: true; // "¿Qué son los macros?"

    // Sugerir recetas
    sugiere_recetas_mexicanas: true;
    considera_ingredientes_disponibles: true;
    adapta_presupuesto: true;

    // Ayuda con sustituciones
    sugiere_sustitutos_alimentos: true;
    mantiene_equivalentes: true;

    // Motivación
    mensajes_motivacionales: true;
    celebra_logros: true;
    ayuda_superar_obstaculos: true;

    // Recordatorios inteligentes
    recuerda_objetivos: true;
    sugiere_hidratacion: true;

    // NO hace diagnósticos ni sustituye al nutriólogo
    derivar_a_nutriologo: true; // cuando la pregunta es médica
  };

  // Entrenamiento con base de conocimiento mexicana
  base_conocimiento: {
    alimentos_mexicanos: 3000;
    recetas_tradicionales: 500;
    guias_nom: true;
    estudios_cientificos: true;
  };

  // Personalización
  aprende_preferencias_paciente: boolean;
  tono_conversacion: 'formal' | 'amigable' | 'motivacional';
}
```

### **4. PREDICCIÓN DE RESULTADOS** 📈
```typescript
interface PrediccionResultados {
  paciente_id: string;
  fecha_prediccion: Date;

  // ⭐ Machine Learning: Predicción a 30, 60, 90 días
  predicciones: {
    // Peso proyectado
    peso_actual_kg: number;
    peso_30dias_kg: number;
    peso_60dias_kg: number;
    peso_90dias_kg: number;
    confianza_prediccion: number; // 0-100

    // Composición corporal proyectada
    grasa_corporal_30dias: number;
    masa_muscular_30dias: number;

    // Marcadores de salud
    glucosa_proyectada?: number;
    presion_arterial_proyectada?: {
      sistolica: number;
      diastolica: number;
    };
    colesterol_proyectado?: number;
  };

  // Factores que influyen en la predicción
  factores_clave: {
    adherencia_actual: number;
    deficit_calorico_promedio: number;
    ejercicio_frecuencia: number;
    historial_peso: number[]; // últimos 12 registros
  };

  // Escenarios "qué pasaría si..."
  escenarios: {
    nombre: string; // "Si aumentas ejercicio a 5x semana"
    impacto_peso_kg: number;
    impacto_tiempo_objetivo_dias: number;
  }[];

  // Probabilidad de alcanzar objetivo
  probabilidad_exito: {
    objetivo_peso_kg: number;
    fecha_objetivo: Date;
    probabilidad: number; // 0-100
    requiere_ajustes: boolean;
    ajustes_sugeridos: string[];
  };

  // Alertas predictivas
  alertas: string[]; // "Patrón indica posible abandono en 2 semanas"
}
```

### **5. GENERADOR DE DIETAS CON IA** 🍽️
```typescript
interface GeneradorDietasIA {
  // Input del nutriólogo
  parametros: {
    paciente_id: string;
    objetivo_calorias: number;
    distribucion_macros: { proteina: number; carbos: number; grasas: number; };
    num_tiempos_comida: number;
    presupuesto_diario_mxn?: number;

    // Restricciones
    alergias: string[];
    intolerancias: string[];
    alimentos_no_gustan: string[];
    preferencias_culturales: string[]; // "comida mexicana tradicional"

    // Contexto
    vegetariano: boolean;
    vegano: boolean;
    considera_temporada: boolean;
    evitar_ultra_procesados: boolean;
  };

  // ⭐ IA genera plan completo
  plan_generado: {
    // Menú semanal (7 días)
    menu_semanal: {
      dia: number;
      desayuno: MealIA;
      colacion_1: MealIA;
      comida: MealIA;
      colacion_2: MealIA;
      cena: MealIA;
    }[];

    // Variaciones inteligentes
    considera_variedad: boolean; // no repite alimentos
    rota_proteinas: boolean;
    incluye_platillos_mexicanos: boolean;

    // Lista de compras generada
    lista_compras: {
      categoria: string; // "Frutas y verduras", "Abarrotes"
      items: {
        producto: string;
        cantidad: string;
        costo_estimado_mxn: number;
        donde_comprar: string; // "mercado local", "tienda"
      }[];
    }[];

    // Recetas detalladas
    recetas: RecetaDetallada[];

    // Análisis nutricional del plan
    promedio_diario: {
      calorias: number;
      proteina_g: number;
      carbohidratos_g: number;
      grasas_g: number;
      fibra_g: number;
      cumple_objetivo: boolean;
    };
  };

  // El nutriólogo puede modificar
  permite_edicion: boolean;
  versiones_guardadas: number;

  // Aprendizaje continuo
  mejora_con_feedback: boolean;
  aprende_preferencias_paciente: boolean;
}

interface MealIA {
  nombre: string;
  hora_sugerida: string;
  calorias: number;
  alimentos: {
    nombre: string;
    cantidad: string;
    equivalentes: string;
    preparacion: string;
  }[];
  receta_completa?: RecetaDetallada;
  tiempo_preparacion_min: number;
  dificultad: 'facil' | 'media' | 'dificil';
  costo_estimado_mxn: number;
}

interface RecetaDetallada {
  nombre: string;
  ingredientes: { nombre: string; cantidad: string; }[];
  instrucciones: string[];
  tiempo_prep: number;
  tiempo_coccion: number;
  porciones: number;
  foto_url: string;
  tips_chef: string[];
  info_nutricional_porcion: any;
  es_receta_mexicana: boolean;
  region_origen: string;
  historia_platillo?: string;
}
```

### **6. DETECCIÓN DE ABANDONO TEMPRANO** 🚨
```typescript
interface DeteccionAbandonoIA {
  // Análisis continuo de señales
  paciente_id: string;
  fecha_analisis: Date;

  // ⭐ Machine Learning: Señales de abandono
  señales_detectadas: {
    // Comportamiento en app
    dias_sin_abrir_app: number;
    reduccion_registros: boolean; // registraba 3x día, ahora 1x
    mensajes_sin_responder: number;
    citas_canceladas_recientes: number;

    // Adherencia
    adherencia_dieta_ultimos_7d: number;
    adherencia_dieta_ultimos_30d: number;
    tendencia_adherencia: 'mejorando' | 'empeorando' | 'estable';

    // Engagement
    interaccion_comunidad: boolean;
    responde_notificaciones: boolean;
    completa_cuestionarios: boolean;

    // Emocional
    mensajes_negativos_detectados: number;
    expresa_frustracion: boolean;
    menciona_dificultades: string[];
  };

  // Score de riesgo de abandono
  riesgo_abandono: {
    score: number; // 0-100
    nivel: 'bajo' | 'medio' | 'alto' | 'critico';
    probabilidad_abandono_30d: number; // 0-100%
  };

  // ⭐ Recomendaciones de intervención
  acciones_sugeridas: {
    prioridad: 'urgente' | 'alta' | 'media';
    tipo: string; // "llamada_telefonica", "mensaje_motivacional", "ajuste_plan"
    mensaje_sugerido: string;
    cuando_ejecutar: Date;
  }[];

  // Notificación automática al nutriólogo
  alerta_enviada_nutriologo: boolean;
  canal_notificacion: 'app' | 'email' | 'whatsapp';
}
```

### **7. ASISTENTE DE CONSULTA PARA NUTRIÓLOGO** 👨‍⚕️
```typescript
interface AsistenteConsultaIA {
  // Durante la consulta, IA asiste al nutriólogo
  paciente_id: string;

  // ⭐ Información preparada automáticamente
  resumen_preparado: {
    // Cambios desde última consulta
    cambio_peso_kg: number;
    cambio_imc: number;
    cambio_grasa: number;

    // Adherencia periodo
    adherencia_promedio: number;
    dias_cumplimiento: number;
    principales_desviaciones: string[];

    // Laboratorios recientes
    valores_preocupantes: {
      parametro: string;
      valor_actual: number;
      valor_anterior: number;
      cambio: string;
      interpretacion: string;
    }[];

    // Patrones identificados
    patrones_alimentarios: string[]; // "desayuno inconsistente"
    patrones_ejercicio: string[];
    patrones_emocionales: string[];

    // Metas del paciente (de entrevista motivacional)
    metas_periodo: {
      meta: string;
      cumplida: boolean;
      progreso: number;
    }[];
  };

  // ⭐ Sugerencias inteligentes
  sugerencias_consulta: {
    // Ajustes recomendados
    ajuste_calorias?: { nuevo_valor: number; razon: string; };
    ajuste_macros?: { nuevo_porcentaje: any; razon: string; };
    ajuste_equivalentes?: string;

    // Temas a abordar
    temas_prioritarios: string[]; // "abordar comer emocional"
    preguntas_sugeridas: string[]; // "¿Has tenido antojos nocturnos?"

    // Estudios complementarios
    estudios_sugeridos: string[]; // "Solicitar perfil tiroideo"

    // Referencias
    requiere_referencia: {
      especialidad: string; // "psicologia", "endocrinologia"
      razon: string;
      urgencia: 'baja' | 'media' | 'alta';
    }[];
  };

  // Transcripción automática (si se activa audio)
  transcripcion_consulta?: string;

  // Notas generadas automáticamente (borrador)
  notas_soap_generadas: {
    subjetivo: string;
    objetivo: string;
    evaluacion: string;
    plan: string;
  };

  // Nutriólogo revisa y aprueba
  notas_aprobadas: boolean;
  notas_editadas_por_nutriologo: string;
}
```

---

## 🎮 GAMIFICACIÓN ADAPTADA A MÉXICO

### **Sistema de Niveles Mexicano**
```
Nivel 1: Novato 🌱 (0-100 XP)
Nivel 2: Guerrero Azteca 🗿 (101-300 XP)
Nivel 3: Águila Mexicana 🦅 (301-600 XP)
Nivel 4: Luchador 🤼 (601-1000 XP)
Nivel 5: Leyenda Nacional 🇲🇽 (1001-2000 XP)
Nivel 6: Patrimonio UNESCO 🏆 (2000+ XP)
```

### **Badges Culturales Mexicanos** 🏅
```
🌮 "Taquero de Corazón" - 30 días comiendo tacos saludables
🌽 "Guardián del Maíz" - consumir tortilla de maíz 90% del tiempo
🌶️ "Amante del Chile" - incorporar chile en comidas saludables
🫔 "Maestro del Frijol" - 50 días consumiendo frijoles
🥑 "Rey del Aguacate" - usar aguacate como grasa saludable
🍫 "Cacao Sagrado" - elegir chocolate >70% cacao
🌻 "Flor de Calabaza" - consumir 20 platillos con flores comestibles
📚 "Heredero Prehispánico" - dominar 15 ingredientes ancestrales
🏔️ "Montañas de México" - cumplir objetivo 30 días consecutivos
🎭 "Lucha contra la Obesidad" - perder 10% peso corporal
```

### **Desafíos Comunitarios Nacionales** 🏆
```
"Septiembre Saludable" (mes patrio):
- Comer pozole bajo en grasa
- Hacer tostadas light
- Agua de fruta sin azúcar

"Noviembre sin Azúcar":
- 30 días reduciendo azúcares añadidos
- Premios: Badges especiales + aparición nacional

"Reto Milpa" (Enero):
- Consumir maíz, frijol, calabaza juntos 21 días
- Reconexión con tradiciones

"Semana del Nopal":
- Incorporar nopal en 7 recetas diferentes
```

### **Leaderboard Nacional por Estado** 🗺️
```
Ranking general México
Ranking por Estado (32 estados)
Ranking por ciudad
Ranking por consultorio de nutriólogo

Categorías:
- Mayor pérdida de peso saludable
- Más días de racha
- Comunidad más activa
- Nutriólogo más valorado
```

---

## 🔬 FUNCIONALIDADES VIRALES

### **1. RETO MÉXICO SALUDABLE** 🇲🇽
```
Challenge nacional que aparece en portada:
"10,000 mexicanos comprometidos a perder 50,000 kg en 6 meses"

Progreso en vivo:
[██████░░░░] 45,234 kg / 50,000 kg

Tracking público:
- Total de mexicanos participando
- Kg totales perdidos
- Estados más activos
- Historias de éxito destacadas

Premio final:
- Top 100: Consultas gratis por 1 año
- Top 10: Entrevista en medios nacionales
- Top 3: Embajadores de la app
```

### **2. COMPARACIÓN ETIQUETAS EN TIENDA** 🏪
```
Escenario:
Usuario en el supermercado frente a 3 yogures

Acción:
1. Escanea código de barras de los 3
2. IA compara instantáneamente
3. Muestra comparación visual

Resultado:
┌────────────────────────────────┐
│ Yogurt A: ❌❌❌ (3 sellos)    │
│ Yogurt B: ❌❌ (2 sellos)      │
│ Yogurt C: ✅ (0 sellos)        │
│                                │
│ ⭐ RECOMENDADO: Yogurt C       │
│ Ahorro: 50 cal, 8g azúcar     │
└────────────────────────────────┘

Compartir:
[Botón: Compartir comparación en redes]
"Escogí el yogurt más saludable con Nutrition Intelligence 🇲🇽"
```

### **3. TRANSFORMACIONES DESTACADAS** 📸
```
Sección "Historias de Éxito"

Features:
- Foto antes/después con slider interactivo
- Estadísticas: -20kg en 4 meses
- Testimonio en video
- Plan alimenticio seguido
- Nutriólogo que lo asesoró

Compartir en redes:
Template automático con:
- Fotos
- Datos
- Logo de la app
- "Respaldado por Consejo Nacional de Nutriólogos"

Viralidad:
- Cada historia puede llegar a miles
- Hashtag #MéxicoSaludable
- Menciones a nutriólogos
```

### **4. RECETA DE LA SEMANA** 👨‍🍳
```
Cada lunes:
Nueva receta mexicana saludable votada por comunidad

Ejemplo:
"🌮 Tacos de Pescado a la Parrilla"
- 350 cal por porción
- Alto en proteína (30g)
- Bajo en grasa
- Ingredientes locales
- Video de preparación
- Variaciones por región

Engagement:
- Usuarios cocinan y suben foto
- Votan mejor presentación
- Ganador aparece en portada
- Nutriólogo valida nutrición
```

### **5. ALERTAS DE SALUD PÚBLICA** 🚨
```
Integración con Secretaría de Salud:

Ejemplo alerta:
┌───────────────────────────────┐
│ ⚠️ ALERTA DIABETES            │
│                               │
│ Nuevo estudio: 1 de cada 3   │
│ mexicanos desarrollará        │
│ diabetes tipo 2               │
│                               │
│ [Test de Riesgo (2 min)]     │
│ [Ver prevención]              │
└───────────────────────────────┘

Impacto:
- Educación masiva
- Prevención
- Vinculación institucional
```

---

## 🚀 ROADMAP DE LANZAMIENTO

### **Fase 0: Preparación (2 semanas)**
- [ ] Firma convenio con Consejo Nacional
- [ ] Registro de marca
- [ ] Diseño de identidad visual mexicana
- [ ] Plan de comunicación

### **Fase 1: MVP Básico (4 semanas)**
- [ ] Backend auth completo
- [ ] Expediente clínico básico (datos generales + antropometría)
- [ ] Sistema de equivalentes mexicanos
- [ ] Dietas dinámicas
- [ ] App mobile iOS + Android

### **Fase 2: Funcionalidades Core (4 semanas)**
- [ ] Recordatorio 24H con IA
- [ ] Historia clínica completa
- [ ] Laboratorios
- [ ] Signos vitales
- [ ] WhatsApp integration

### **Fase 3: IA Avanzada (4 semanas)**
- [ ] Análisis de fotos de comida
- [ ] Escáner de etiquetas NOM-051
- [ ] Predicción de resultados
- [ ] Generador de dietas IA
- [ ] Chat nutriólogo virtual

### **Fase 4: Gamificación (3 semanas)**
- [ ] Sistema XP y niveles mexicanos
- [ ] Badges culturales
- [ ] Rachas (streaks)
- [ ] Desafíos comunitarios
- [ ] Leaderboards por estado

### **Fase 5: Social (3 semanas)**
- [ ] Feed comunitario
- [ ] Compartir en redes
- [ ] Historias de éxito
- [ ] Receta de la semana
- [ ] Grupos por objetivo

### **Fase 6: Lanzamiento Nacional (2 semanas)**
- [ ] Beta testing con 100 nutriólogos
- [ ] Campaña de PR
- [ ] Launch event
- [ ] Conferencia de prensa
- [ ] Activación en redes

**TOTAL: 20 semanas (5 meses)**

---

## 💰 MODELO DE NEGOCIO - GRATUITO

### **¿Cómo nos sostenemos siendo gratis?**

#### **1. Alianzas Institucionales** 🏛️
```
- Consejo Nacional de Nutriólogos (respaldo)
- Secretaría de Salud (campañas)
- ISSSTE / IMSS (programas prevención)
- Universidades (investigación)
```

#### **2. Grants y Fondos** 💵
```
- Fondos gubernamentales para salud
- OMS / OPS (Organización Panamericana Salud)
- Fundaciones internacionales
- Conacyt (investigación + desarrollo)
```

#### **3. Features Premium Opcional** ✨
```
Para pacientes (100% opcional):
- Consultas con nutriólogo por videollamada ($150-300 MXN)
- Planes de comida personalizados extra ($99 MXN/mes)
- Análisis genético nutricional ($500 MXN one-time)

Para nutriólogos (100% opcional):
- Templates avanzados de reportes ($199 MXN/mes)
- IA para análisis predictivo avanzado ($299 MXN/mes)
- White-label (tu marca) ($999 MXN/mes)
```

#### **4. Marketplace de Productos Saludables** 🛒
```
- Comisión 10% en venta de suplementos verificados
- Comisión 5% en ingredientes saludables
- Partnership con marcas mexicanas sanas
- Descuentos exclusivos para usuarios

Ejemplo:
Usuario escanea suplemento → App verifica autenticidad →
Ofrece mejor precio → Comisión si compra
```

#### **5. Data Anónima para Investigación** 🔬
```
(Previa autorización y anonimizada)
- Patrones alimentarios México
- Efectividad de intervenciones
- Publicaciones científicas
- Mejora políticas públicas
```

#### **6. Publicidad NO INVASIVA** 📢
```
Solo de marcas verificadas:
- Productos orgánicos mexicanos
- Gimnasios locales
- Apps de meditación
- Agua embotellada

Límites:
- Máximo 1 anuncio por sesión
- Solo en secciones no críticas
- Nunca en expediente clínico
- Usuario puede ocultarlos (free)
```

---

## 🎯 MÉTRICAS DE ÉXITO

### **Año 1 (12 meses)**
```
👨‍⚕️ Nutriólogos:
- 5,000 nutriólogos registrados
- 3,000 activos mensualmente
- 80% satisfacción

👥 Pacientes:
- 100,000 pacientes registrados
- 50,000 activos mensualmente
- 70% adherencia >30 días

📊 Impacto:
- 500 toneladas perdidas colectivamente
- 10,000 personas saliendo de obesidad
- 5,000 pre-diabéticos prevenidos

🇲🇽 Nacional:
- Presencia en 32 estados
- 500 historias de éxito documentadas
- 1M visitas al mes en blog educativo
```

### **Indicadores Clave**
```
DAU (Daily Active Users): 15,000
MAU (Monthly Active Users): 50,000
Retention D30: 70%
NPS (Net Promoter Score): >80
App Store Rating: >4.8⭐
Tiempo promedio sesión: 12 min
```

---

## 🌟 ESLOGAN Y MISIÓN

### **Eslogan:**
```
"Nutrition Intelligence: Tu salud, tu cultura, tu México 🇲🇽"

Alternativas:
- "Nutrición inteligente con sabor a México"
- "Transforma tu salud sin perder tus raíces"
- "Porque comer rico y saludable es posible"
```

### **Misión:**
```
Combatir la epidemia de obesidad y diabetes en México
mediante tecnología de vanguardia, inteligencia artificial
y respeto profundo a nuestra identidad cultural alimentaria,
haciendo accesible la nutrición profesional para todos los mexicanos.
```

### **Visión:**
```
Ser la plataforma líder en salud nutricional de México,
reconocida internacionalmente por integrar tradición,
tecnología e impacto social, reduciendo en 50% los índices
de obesidad infantil y diabetes tipo 2 en México para 2035.
```

---

## 📱 MOCKUPS Y DISEÑO

### **Paleta de Colores Mexicana**
```
Primario: Verde México #006847 (bandera)
Secundario: Rojo México #CE1126 (bandera)
Acento: Amarillo Maíz #FFD700
Neutro Cálido: Terracota #E07B39
Texto: Negro Obsidiana #2C2C2C
Backgrounds: Blanco Hueso #FAF8F3

Gradientes:
- Verde → Amarillo (amanecer mexicano)
- Rojo → Naranja (atardecer)
```

### **Tipografía**
```
Títulos: Montserrat Bold (moderno, limpio)
Cuerpo: Open Sans Regular (legible)
Acentos: Pacifico (cálido, mexicano para celebraciones)
```

### **Iconografía**
```
- Iconos line-art modernos
- Ilustraciones flat con toque mexicano
- Emojis nativos para familiaridad
- Fotos reales de mexicanos (no stock gringo)
```

---

## 🎉 ¿SIGUIENTE PASO?

Propongo comenzar INMEDIATAMENTE con:

### **OPCIÓN A: Backend Completo (Recomendado)** ⚡
```
Semanas 1-4:
✅ Sistema de autenticación robusto
✅ Base de datos expediente clínico completo
✅ API REST documentada
✅ Integración WhatsApp
✅ Sistema de equivalentes mexicanos (3000 alimentos)
✅ Generador de dietas con IA básica
```

### **OPCIÓN B: App Mobile Nativa (React Native)** 📱
```
Semanas 1-4:
✅ Setup React Native + Expo
✅ Pantallas de onboarding mexicano
✅ Sistema de login/registro
✅ Dashboard paciente
✅ Registro de comidas
✅ Escáner de código de barras
```

### **OPCIÓN C: Ambos en Paralelo** 🚀
```
Trabajo simultáneo:
Backend + Mobile al mismo tiempo
Tiempo total: 4 semanas
Resultado: MVP funcional end-to-end
```

---

## 📞 CONTACTO Y COORDINACIÓN

**Para arrancar necesitamos:**
1. ✅ Confirmar inicio
2. ✅ Definir prioridad (Backend, Mobile o Ambos)
3. ✅ Acceso a servidores/hosting (si ya tienen)
4. ✅ Logo en alta resolución
5. ✅ Colores corporativos finales

**¿Arrancamos? 💪🇲🇽**

Dime y comenzamos DE INMEDIATO con el desarrollo!
