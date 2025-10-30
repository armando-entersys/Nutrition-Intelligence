/**
 * EXPEDIENTE CLÍNICO DIGITAL - NUTRITION INTELLIGENCE MÉXICO
 * Sistema completo de expediente clínico que cumple NOM-004-SSA3-2012
 * y supera las funcionalidades de Nutrimind
 */

// ============================================================================
// 1. DATOS GENERALES DEL PACIENTE
// ============================================================================

export interface ContactoEmergencia {
  nombre: string;
  parentesco: string;
  telefono: string;
}

export interface AnalisisContextoIA {
  nivel_socioeconomico_estimado: string;
  riesgo_desercion: number; // 0-100
  recomendaciones_adaptacion: string[];
}

export interface DatosGenerales {
  // Identificación
  id: string;
  nombre_completo: string;
  fecha_nacimiento: Date;
  edad: number; // calculada automáticamente
  sexo: 'masculino' | 'femenino' | 'otro';
  curp: string;
  telefono: string;
  email: string;
  whatsapp: string;

  // Ubicación
  estado: string;
  municipio: string;
  colonia: string;
  direccion_completa: string;
  cp: string;

  // Contacto de emergencia
  contacto_emergencia: ContactoEmergencia;

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

  // IA: Análisis de contexto socioeconómico
  analisis_ia_contexto?: AnalisisContextoIA;
}

// ============================================================================
// 2. MEDICIONES ANTROPOMÉTRICAS
// ============================================================================

export interface FotoProgreso {
  frontal_url?: string;
  lateral_url?: string;
  posterior_url?: string;
  fecha: Date;
}

export interface AnalisisAntropometricoIA {
  tendencia_peso: 'subiendo' | 'bajando' | 'estable';
  prediccion_peso_30d: number;
  riesgo_obesidad: number; // 0-100
  distribucion_grasa: 'androide' | 'ginecoide' | 'mixta';
  recomendaciones_ejercicio: string[];
  alertas: string[];
}

export interface MedicionesAntropometricas {
  id: string;
  paciente_id: string;
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
  pliegue_tricipital_mm?: number;
  pliegue_bicipital_mm?: number;
  pliegue_subescapular_mm?: number;
  pliegue_suprailiaco_mm?: number;
  pliegue_abdominal_mm?: number;
  pliegue_muslo_mm?: number;
  pliegue_pantorrilla_mm?: number;

  // Composición corporal
  porcentaje_grasa?: number; // ecuación Durnin-Womersley
  masa_grasa_kg?: number;
  masa_libre_grasa_kg?: number;
  masa_muscular_kg?: number;
  agua_corporal_l?: number;

  // Somatotipo (Heath-Carter)
  endomorfia?: number;
  mesomorfia?: number;
  ectomorfia?: number;
  somatotipo?: string; // "endomorfo", "mesomorfo", etc.

  // Bioimpedancia (si disponible)
  impedancia_ohms?: number;
  angulo_fase?: number;

  // IA: Análisis predictivo
  analisis_ia?: AnalisisAntropometricoIA;

  // Fotos progreso
  fotos?: FotoProgreso[];

  // Gráficas disponibles
  graficas_disponibles?: string[]; // ["peso", "imc", "grasa", "circunferencias"]
}

// ============================================================================
// 3. HISTORIA CLÍNICA
// ============================================================================

export interface AntecedenteFamiliar {
  presente: boolean;
  quien?: string[];
  tipo?: string;
}

export interface AntecedentesFamiliares {
  diabetes: AntecedenteFamiliar;
  hipertension: AntecedenteFamiliar;
  obesidad: AntecedenteFamiliar;
  dislipidemias: AntecedenteFamiliar;
  cancer: AntecedenteFamiliar;
  enfermedades_cardiacas: AntecedenteFamiliar;
  enfermedades_renales: AntecedenteFamiliar;
  enfermedades_gastrointestinales: AntecedenteFamiliar;
  otros?: string;
}

export interface EnfermedadCronica {
  nombre: string;
  fecha_diagnostico: Date;
  tratamiento_actual: string;
  controlada: boolean;
}

export interface Cirugia {
  tipo: string;
  fecha: Date;
  hospital: string;
}

export interface Hospitalizacion {
  razon: string;
  fecha: Date;
  duracion_dias: number;
}

export interface AntecedentesPatologicos {
  enfermedades_cronicas: EnfermedadCronica[];
  cirugias_previas: Cirugia[];
  hospitalizaciones: Hospitalizacion[];
  alergias_medicamentos: string[];
  alergias_alimentos: string[];
  intolerancias_alimentarias: string[];
}

export interface AntecedentesGineco {
  menarca_edad: number;
  ciclos_regulares: boolean;
  fecha_ultima_menstruacion?: Date;
  embarazos_previos: number;
  partos: number;
  cesareas: number;
  abortos: number;
  lactancia_actual: boolean;
  menopausia: boolean;
  edad_menopausia?: number;
  terapia_hormonal: boolean;
}

export interface Medicamento {
  nombre: string;
  dosis: string;
  frecuencia: string;
  indicacion: string;
  fecha_inicio: Date;
  interacciones_nutricion?: string[]; // IA detecta interacciones
}

export interface Suplemento {
  nombre: string;
  dosis: string;
  frecuencia: string;
  marca: string;
  necesario: boolean; // evaluado por nutriólogo
}

export interface AnalisisRiesgoIA {
  riesgo_cardiovascular: number; // 0-100
  riesgo_diabetes_tipo2: number;
  riesgo_sindrome_metabolico: number;
  riesgo_osteoporosis: number;
  riesgo_anemia: number;
  factores_riesgo_identificados: string[];
  recomendaciones_preventivas: string[];
}

export interface HistoriaClinica {
  paciente_id: string;
  fecha_elaboracion: Date;

  // Antecedentes heredofamiliares
  antecedentes_familiares: AntecedentesFamiliares;

  // Antecedentes personales patológicos
  antecedentes_patologicos: AntecedentesPatologicos;

  // Antecedentes gineco-obstétricos (mujeres)
  antecedentes_gineco?: AntecedentesGineco;

  // Medicamentos actuales
  medicamentos_actuales: Medicamento[];

  // Suplementos
  suplementos: Suplemento[];

  // IA: Análisis de riesgo
  analisis_riesgo_ia?: AnalisisRiesgoIA;
}

// ============================================================================
// 4. SIGNOS VITALES
// ============================================================================

export interface AlertasSignosVitalesIA {
  presion_anormal: boolean;
  taquicardia: boolean;
  bradicardia: boolean;
  hipoglucemia: boolean;
  hiperglucemia: boolean;
  recomendacion_urgente?: string;
}

export interface SignosVitales {
  id: string;
  paciente_id: string;
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
  momento_medicion?: 'ayuno' | 'postprandial' | 'aleatorio';

  // IA: Detección de anomalías
  alertas_ia?: AlertasSignosVitalesIA;

  // Notas
  notas?: string;
  medido_por: string; // "Dr. Juan Pérez", "Auto-medición"
}

// ============================================================================
// 5. DATOS DE LABORATORIO
// ============================================================================

export interface ValorFueraRango {
  parametro: string;
  valor: number;
  rango_normal: string;
  severidad: 'leve' | 'moderada' | 'severa';
  significado_clinico: string;
}

export interface InterpretacionLaboratorioIA {
  valores_fuera_rango: ValorFueraRango[];
  diagnosticos_sugeridos: string[];
  ajustes_dieta_recomendados: string[];
  estudios_adicionales_sugeridos: string[];
  alertas_criticas: string[]; // valores peligrosos
}

export interface TendenciaLaboratorio {
  parametro: string;
  direccion: 'mejorando' | 'empeorando' | 'estable';
  cambio_porcentual: number;
}

export interface DatosLaboratorio {
  id: string;
  paciente_id: string;
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

  // IA: Interpretación automática
  interpretacion_ia?: InterpretacionLaboratorioIA;

  // Archivo PDF del estudio
  archivo_pdf_url?: string;

  // Comparación con estudios previos (tendencias)
  tendencias?: TendenciaLaboratorio[];
}

// ============================================================================
// 6. HÁBITOS
// ============================================================================

export interface AnalisisHabitosIA {
  habitos_positivos: string[];
  habitos_negativos: string[];
  habitos_criticos: string[]; // urgente modificar
  facilidad_cambio: { [habito: string]: number }; // 0-100
  plan_modificacion_gradual: {
    semana: number;
    habito_objetivo: string;
    estrategia: string;
  }[];
}

export interface Habitos {
  paciente_id: string;
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
  comida_mexicana_favorita: string[]; // platillos tradicionales

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

  // Hábitos culturales mexicanos
  consume_tortilla_diario: boolean;
  consume_frijol_diario: boolean;
  consume_chile_diario: boolean;
  desayuno_tipico: string; // "tamales", "chilaquiles", etc.
  come_tacos_semana: number;
  asiste_fondas_semana: number;

  // IA: Análisis de hábitos
  analisis_habitos_ia?: AnalisisHabitosIA;
}

// ============================================================================
// 7. ACTIVIDAD FÍSICA
// ============================================================================

export interface PlanEjercicioIA {
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
}

export interface SesionEjercicio {
  fecha: Date;
  tipo: string;
  duracion_min: number;
  intensidad: 'baja' | 'media' | 'alta';
  calorias_quemadas?: number;
  notas: string;
}

export interface ActividadFisica {
  paciente_id: string;
  fecha: Date;

  // Cuestionario IPAQ
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
  nivel?: 'recreativo' | 'competitivo' | 'profesional';

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

  // IA: Recomendaciones personalizadas
  plan_ejercicio_ia?: PlanEjercicioIA;

  // Historial de ejercicios (tracking)
  sesiones_ejercicio: SesionEjercicio[];
}

// ============================================================================
// EXPEDIENTE CLÍNICO COMPLETO
// ============================================================================

export interface ExpedienteClinico {
  // Datos básicos
  datos_generales: DatosGenerales;

  // Mediciones
  mediciones_antropometricas: MedicionesAntropometricas[];

  // Historia
  historia_clinica: HistoriaClinica;

  // Monitoreo
  signos_vitales: SignosVitales[];
  datos_laboratorio: DatosLaboratorio[];

  // Evaluación
  habitos: Habitos;
  actividad_fisica: ActividadFisica;

  // Metadata
  fecha_creacion: Date;
  fecha_ultima_modificacion: Date;
  nutriologo_responsable: string;
  nutriologo_id: string;
}
