/**
 * TIPOS PARA DIETAS DINÁMICAS CON IA
 * Sistema de generación automática de planes de alimentación personalizados
 */

export interface TiempoComida {
  hora_recomendada: string;
  calorias: number;
  alimentos: {
    nombre: string;
    cantidad: string;
    equivalentes_usados: string;
    calorias: number;
  }[];
  opciones_sustitucion: string[];
}

export interface RecetaMexicana {
  nombre: string;
  ingredientes: string[];
  preparacion: string;
  tiempo_prep_min: number;
  porciones: number;
  calorias_porcion: number;
  foto_url?: string;
  es_tradicional: boolean;
  region: string;
  tags: string[];
}

export interface MenuDia {
  dia: number;
  nombre_dia: string;
  desayuno: TiempoComida;
  colacion_1: TiempoComida;
  comida: TiempoComida;
  colacion_2: TiempoComida;
  cena: TiempoComida;
  calorias_total: number;
}

export interface OptimizacionesIA {
  sustitucion_alimentos_culturales: boolean;
  considera_presupuesto: boolean;
  considera_temporada: boolean;
  alergias_evitadas: string[];
  preferencias_respetadas: string[];
}

export interface AjusteAutomatico {
  fecha: Date;
  razon: string;
  cambios: string[];
}

export interface DietaDinamica {
  id: string;
  nombre: string;
  paciente_id: string;
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

  // Sistema de equivalentes mexicano
  equivalentes_por_dia: {
    cereales_sin_grasa: number;
    cereales_con_grasa: number;
    leguminosas: number;
    verduras: number;
    frutas: number;
    leche_descremada: number;
    carnes_muy_bajo_aporte: number;
    carnes_bajo_aporte: number;
    carnes_moderado_aporte: number;
    grasas_sin_proteina: number;
    grasas_con_proteina: number;
  };

  // Menú semanal
  menu_semanal: MenuDia[];

  // IA: Generación y optimización
  generado_por_ia: boolean;
  optimizaciones_ia: OptimizacionesIA;

  // Cumplimiento del paciente
  adherencia_porcentaje: number;
  dias_cumplidos: number;
  dias_totales: number;

  // Modificaciones dinámicas
  ajustes_automaticos: AjusteAutomatico[];

  // Recetas
  recetas_incluidas: RecetaMexicana[];

  // Lista de compras
  lista_compras?: {
    categoria: string;
    items: {
      producto: string;
      cantidad: string;
      costo_estimado_mxn: number;
    }[];
  }[];
}
