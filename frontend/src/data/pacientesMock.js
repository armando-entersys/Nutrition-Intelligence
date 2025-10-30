/**
 * DATOS MOCK DE PACIENTES - EXPEDIENTE CLÍNICO
 * Base de datos de ejemplo con pacientes mexicanos
 */

export const PACIENTES_MOCK = [
  {
    datos_generales: {
      id: 'pac_001',
      nombre_completo: 'María Guadalupe Hernández López',
      fecha_nacimiento: new Date('1985-03-15'),
      edad: 39,
      sexo: 'femenino',
      curp: 'HELM850315MDFRZR08',
      telefono: '5512345678',
      email: 'maria.hernandez@gmail.com',
      whatsapp: '5512345678',

      // Ubicación
      estado: 'Ciudad de México',
      municipio: 'Iztapalapa',
      colonia: 'Santa María Aztahuacán',
      direccion_completa: 'Calle Atzacoalco #123, Col. Santa María Aztahuacán',
      cp: '09500',

      // Contacto de emergencia
      contacto_emergencia: {
        nombre: 'Juan Hernández Pérez',
        parentesco: 'Esposo',
        telefono: '5587654321'
      },

      // Datos socioeconómicos
      ocupacion: 'Secretaria',
      escolaridad: 'Licenciatura',
      estado_civil: 'Casada',
      num_integrantes_familia: 4,

      // Seguro médico
      tiene_seguro: true,
      tipo_seguro: 'IMSS',
      numero_afiliacion: '12345678901',

      // IA: Análisis de contexto
      analisis_ia_contexto: {
        nivel_socioeconomico_estimado: 'Medio-bajo',
        riesgo_desercion: 35,
        recomendaciones_adaptacion: [
          'Sugerir alimentos accesibles en mercados locales',
          'Recetas económicas con ingredientes de temporada',
          'Opciones de comida casera vs restaurante'
        ]
      }
    },

    mediciones_antropometricas: [
      {
        id: 'med_001',
        paciente_id: 'pac_001',
        fecha_medicion: new Date('2024-10-20'),

        // Peso y talla
        peso_kg: 78.5,
        talla_cm: 158,
        imc: 31.4,
        interpretacion_imc: 'Obesidad grado I',

        // Circunferencias
        circunferencia_cintura_cm: 95,
        circunferencia_cadera_cm: 110,
        circunferencia_brazo_cm: 32,
        circunferencia_pantorrilla_cm: 38,
        circunferencia_cuello_cm: 35,
        indice_cintura_cadera: 0.86,
        indice_cintura_talla: 0.60,

        // Composición corporal
        porcentaje_grasa: 38,
        masa_grasa_kg: 29.8,
        masa_libre_grasa_kg: 48.7,
        masa_muscular_kg: 45.2,

        // IA: Análisis predictivo
        analisis_ia: {
          tendencia_peso: 'subiendo',
          prediccion_peso_30d: 77.2,
          riesgo_obesidad: 75,
          distribucion_grasa: 'ginecoide',
          recomendaciones_ejercicio: [
            'Caminar 30 minutos diarios',
            'Ejercicios de fuerza 2 veces por semana',
            'Baile folclórico mexicano 1 vez por semana'
          ],
          alertas: [
            'Circunferencia de cintura elevada - riesgo cardiovascular',
            'Índice cintura-talla >0.5 - riesgo metabólico'
          ]
        }
      }
    ],

    historia_clinica: {
      paciente_id: 'pac_001',
      fecha_elaboracion: new Date('2024-10-20'),

      // Antecedentes familiares
      antecedentes_familiares: {
        diabetes: {
          presente: true,
          quien: ['Madre', 'Abuela materna']
        },
        hipertension: {
          presente: true,
          quien: ['Padre']
        },
        obesidad: {
          presente: true,
          quien: ['Madre', 'Hermana']
        },
        dislipidemias: {
          presente: false
        },
        cancer: {
          presente: false
        },
        enfermedades_cardiacas: {
          presente: false
        },
        enfermedades_renales: {
          presente: false
        },
        enfermedades_gastrointestinales: {
          presente: false
        }
      },

      // Antecedentes patológicos
      antecedentes_patologicos: {
        enfermedades_cronicas: [],
        cirugias_previas: [],
        hospitalizaciones: [],
        alergias_medicamentos: [],
        alergias_alimentos: ['Camarones'],
        intolerancias_alimentarias: ['Lactosa (leve)']
      },

      // Antecedentes gineco-obstétricos
      antecedentes_gineco: {
        menarca_edad: 12,
        ciclos_regulares: true,
        fecha_ultima_menstruacion: new Date('2024-10-05'),
        embarazos_previos: 2,
        partos: 2,
        cesareas: 0,
        abortos: 0,
        lactancia_actual: false,
        menopausia: false,
        terapia_hormonal: false
      },

      // Medicamentos actuales
      medicamentos_actuales: [],

      // Suplementos
      suplementos: [
        {
          nombre: 'Multivitamínico',
          dosis: '1 tableta',
          frecuencia: 'Diaria',
          marca: 'Centrum',
          necesario: true
        }
      ],

      // IA: Análisis de riesgo
      analisis_riesgo_ia: {
        riesgo_cardiovascular: 45,
        riesgo_diabetes_tipo2: 60,
        riesgo_sindrome_metabolico: 55,
        riesgo_osteoporosis: 20,
        riesgo_anemia: 15,
        factores_riesgo_identificados: [
          'Antecedentes familiares de diabetes',
          'Obesidad grado I',
          'Circunferencia de cintura elevada',
          'Sedentarismo'
        ],
        recomendaciones_preventivas: [
          'Reducir peso corporal 5-10%',
          'Aumentar actividad física gradualmente',
          'Monitorear glucosa cada 6 meses',
          'Consumir alimentos de bajo índice glucémico'
        ]
      }
    },

    signos_vitales: [
      {
        id: 'sv_001',
        paciente_id: 'pac_001',
        fecha_hora: new Date('2024-10-20T10:30:00'),
        lugar_medicion: 'consultorio',

        // Presión arterial
        presion_sistolica_mmHg: 128,
        presion_diastolica_mmHg: 82,
        presion_arterial_media: 97.3,
        clasificacion_presion: 'Pre-hipertensión',

        // Frecuencia cardíaca
        frecuencia_cardiaca_lpm: 78,
        ritmo_regular: true,

        // Frecuencia respiratoria
        frecuencia_respiratoria_rpm: 16,

        // Temperatura
        temperatura_celsius: 36.5,

        // Oximetría
        saturacion_oxigeno_porcentaje: 98,

        // Glucometría
        glucosa_capilar_mgdl: 102,
        momento_medicion: 'ayuno',

        // IA: Alertas
        alertas_ia: {
          presion_anormal: true,
          taquicardia: false,
          bradicardia: false,
          hipoglucemia: false,
          hiperglucemia: false,
          recomendacion_urgente: 'Monitorear presión arterial. Considerar reducción de sodio en dieta.'
        },

        medido_por: 'Dra. Ana Pérez Lizaur',
        notas: 'Paciente reporta estrés laboral reciente'
      }
    ],

    habitos: {
      paciente_id: 'pac_001',
      fecha_evaluacion: new Date('2024-10-20'),

      // Hábitos alimentarios
      num_comidas_dia: 3,
      desayuna_diario: true,
      hora_primera_comida: '07:00',
      hora_ultima_comida: '21:00',
      ventana_alimentacion_horas: 14,

      // Comportamientos
      come_viendo_tv: true,
      come_trabajando: false,
      come_rapido: true,
      mastica_suficiente: false,

      // Preferencias
      alimentos_favoritos: ['Tacos', 'Quesadillas', 'Mole', 'Pan dulce'],
      alimentos_rechazados: ['Brócoli', 'Coliflor'],
      comida_mexicana_favorita: ['Tacos al pastor', 'Chilaquiles', 'Pozole'],

      // Hidratación
      vasos_agua_dia: 4,
      consume_refrescos: true,
      refrescos_semana: 5,
      consume_alcohol: false,
      bebidas_alcoholicas_semana: 0,

      // Tabaquismo
      fuma: false,

      // Compras y cocina
      quien_cocina_hogar: 'Ella misma',
      frecuencia_compra_alimentos: 'Semanal',
      presupuesto_mensual_alimentos: 6000,
      compra_mercado_local: true,
      compra_supermercado: true,

      // Hábitos culturales mexicanos
      consume_tortilla_diario: true,
      consume_frijol_diario: true,
      consume_chile_diario: true,
      desayuno_tipico: 'Chilaquiles o quesadillas',
      come_tacos_semana: 3,
      asiste_fondas_semana: 2,

      // IA: Análisis de hábitos
      analisis_habitos_ia: {
        habitos_positivos: [
          'Desayuna diariamente',
          'Cocina en casa la mayoría de veces',
          'Compra en mercado local (alimentos frescos)'
        ],
        habitos_negativos: [
          'Come viendo TV (alimentación no consciente)',
          'Come rápido y mastica poco',
          'Bajo consumo de agua',
          'Alto consumo de refrescos'
        ],
        habitos_criticos: [
          'Refrescos 5 veces por semana - azúcares añadidos',
          'Solo 4 vasos de agua al día - deshidratación crónica'
        ],
        facilidad_cambio: {
          'aumentar_agua': 70,
          'reducir_refrescos': 50,
          'comer_despacio': 60,
          'comer_sin_tv': 40
        },
        plan_modificacion_gradual: [
          {
            semana: 1,
            habito_objetivo: 'Aumentar consumo de agua',
            estrategia: 'Agregar 2 vasos más al día (6 total). Usar botella reutilizable.'
          },
          {
            semana: 2,
            habito_objetivo: 'Reducir refrescos',
            estrategia: 'Sustituir 2 refrescos por agua de jamaica sin azúcar.'
          },
          {
            semana: 3,
            habito_objetivo: 'Comer más despacio',
            estrategia: 'Masticar cada bocado 20 veces. Dejar cubiertos entre bocados.'
          },
          {
            semana: 4,
            habito_objetivo: 'Comer sin TV',
            estrategia: 'Comer en la mesa sin distracciones al menos en 1 comida al día.'
          }
        ]
      }
    },

    actividad_fisica: {
      paciente_id: 'pac_001',
      fecha: new Date('2024-10-20'),

      // IPAQ
      nivel_actividad: 'ligero',

      // Actividad laboral
      trabajo_tipo: 'oficina',
      horas_sentado_dia: 8,

      // Ejercicio
      realiza_ejercicio: false,
      tipo_ejercicio: [],
      frecuencia_semanal: 0,
      duracion_promedio_min: 0,

      // Deporte
      practica_deporte: false,

      // Actividades diarias
      camina_diario_min: 15,
      pasos_promedio_dia: 3500,

      // Limitaciones
      lesiones_actuales: [],
      limitaciones_medicas: [],
      dolor_ejercicio: false,

      // Metas
      meta_pasos_dia: 8000,
      meta_ejercicio_semanal_min: 150,

      // Integración
      dispositivo_conectado: 'xiaomi',
      datos_sincronizados: true,

      // IA: Plan personalizado
      plan_ejercicio_ia: {
        tipo_recomendado: ['Caminata', 'Baile', 'Yoga'],
        intensidad: 'Moderada',
        frecuencia_sugerida: 5,
        duracion_sugerida_min: 30,
        consideraciones_salud: [
          'Iniciar gradualmente por sedentarismo prolongado',
          'Evitar impacto alto por sobrepeso'
        ],
        ejercicios_contraindicados: ['Correr', 'Saltos de alta intensidad'],
        progresion_12_semanas: [
          {
            semana: 1,
            objetivos: 'Adaptación cardiovascular básica',
            actividades: ['Caminar 15 min/día', 'Estiramientos 5 min']
          },
          {
            semana: 2,
            objetivos: 'Aumentar duración',
            actividades: ['Caminar 20 min/día', 'Estiramientos 5 min']
          },
          {
            semana: 3,
            objetivos: 'Introducir variedad',
            actividades: ['Caminar 25 min/día', 'Baile folclórico 1x/semana']
          },
          {
            semana: 4,
            objetivos: 'Consolidar hábito',
            actividades: ['Caminar 30 min/día', 'Baile folclórico 1x/semana']
          }
        ]
      },

      sesiones_ejercicio: []
    },

    // Metadata
    fecha_creacion: new Date('2024-10-20'),
    fecha_ultima_modificacion: new Date('2024-10-20'),
    nutriologo_responsable: 'Dra. Ana Bertha Pérez Lizaur',
    nutriologo_id: 'nut_001'
  },

  // SEGUNDO PACIENTE
  {
    datos_generales: {
      id: 'pac_002',
      nombre_completo: 'Carlos Alberto Ramírez Sánchez',
      fecha_nacimiento: new Date('1992-08-22'),
      edad: 32,
      sexo: 'masculino',
      curp: 'RASC920822HDFRNN03',
      telefono: '5523456789',
      email: 'carlos.ramirez@outlook.com',
      whatsapp: '5523456789',

      estado: 'Estado de México',
      municipio: 'Nezahualcóyotl',
      colonia: 'Ciudad Jardín',
      direccion_completa: 'Av. Chimalhuacán #456',
      cp: '57139',

      contacto_emergencia: {
        nombre: 'Rosa María Sánchez',
        parentesco: 'Madre',
        telefono: '5534567890'
      },

      ocupacion: 'Chofer de transporte público',
      escolaridad: 'Preparatoria',
      estado_civil: 'Soltero',
      num_integrantes_familia: 5,

      tiene_seguro: true,
      tipo_seguro: 'IMSS',
      numero_afiliacion: '98765432101',

      analisis_ia_contexto: {
        nivel_socioeconomico_estimado: 'Bajo',
        riesgo_desercion: 55,
        recomendaciones_adaptacion: [
          'Alimentos económicos y accesibles en puestos callejeros',
          'Comidas rápidas saludables para horario irregular',
          'Opciones de refrigerios no perecederos'
        ]
      }
    },

    mediciones_antropometricas: [
      {
        id: 'med_002',
        paciente_id: 'pac_002',
        fecha_medicion: new Date('2024-10-25'),

        peso_kg: 95.2,
        talla_cm: 172,
        imc: 32.2,
        interpretacion_imc: 'Obesidad grado I',

        circunferencia_cintura_cm: 105,
        circunferencia_cadera_cm: 102,
        circunferencia_brazo_cm: 35,
        circunferencia_pantorrilla_cm: 40,
        circunferencia_cuello_cm: 40,
        indice_cintura_cadera: 1.03,
        indice_cintura_talla: 0.61,

        porcentaje_grasa: 32,
        masa_grasa_kg: 30.5,
        masa_libre_grasa_kg: 64.7,
        masa_muscular_kg: 60.2,

        analisis_ia: {
          tendencia_peso: 'subiendo',
          prediccion_peso_30d: 96.8,
          riesgo_obesidad: 80,
          distribucion_grasa: 'androide',
          recomendaciones_ejercicio: [
            'Actividades de bajo impacto: natación, bicicleta estática',
            'Ejercicios de fuerza con peso corporal',
            'Fútbol recreativo los fines de semana'
          ],
          alertas: [
            'Distribución androide - ALTO riesgo cardiovascular',
            'Índice cintura-cadera >1.0 - Síndrome metabólico probable',
            'Perímetro de cuello elevado - posible apnea del sueño'
          ]
        }
      }
    ],

    historia_clinica: {
      paciente_id: 'pac_002',
      fecha_elaboracion: new Date('2024-10-25'),

      antecedentes_familiares: {
        diabetes: {
          presente: true,
          quien: ['Padre', 'Abuelo paterno', 'Tío']
        },
        hipertension: {
          presente: true,
          quien: ['Padre', 'Madre']
        },
        obesidad: {
          presente: true,
          quien: ['Padre', 'Hermano']
        },
        dislipidemias: {
          presente: true,
          quien: ['Padre']
        },
        cancer: {
          presente: false
        },
        enfermedades_cardiacas: {
          presente: true,
          tipo: 'Infarto',
          quien: ['Abuelo paterno (†55 años)']
        },
        enfermedades_renales: {
          presente: false
        },
        enfermedades_gastrointestinales: {
          presente: false
        }
      },

      antecedentes_patologicos: {
        enfermedades_cronicas: [
          {
            nombre: 'Pre-diabetes',
            fecha_diagnostico: new Date('2024-06-15'),
            tratamiento_actual: 'Cambios en estilo de vida',
            controlada: false
          }
        ],
        cirugias_previas: [],
        hospitalizaciones: [],
        alergias_medicamentos: [],
        alergias_alimentos: [],
        intolerancias_alimentarias: []
      },

      medicamentos_actuales: [],

      suplementos: [],

      analisis_riesgo_ia: {
        riesgo_cardiovascular: 75,
        riesgo_diabetes_tipo2: 85,
        riesgo_sindrome_metabolico: 80,
        riesgo_osteoporosis: 10,
        riesgo_anemia: 15,
        factores_riesgo_identificados: [
          'CRÍTICO: Antecedentes familiares múltiples de diabetes',
          'CRÍTICO: Pre-diabetes diagnosticada',
          'Obesidad abdominal (distribución androide)',
          'Sedentarismo laboral prolongado',
          'Alimentación irregular por horarios de trabajo',
          'Probable apnea del sueño no diagnosticada'
        ],
        recomendaciones_preventivas: [
          'URGENTE: Monitoreo glucémico cada 3 meses',
          'Reducción de peso 10% en 6 meses',
          'Estudio de sueño para descartar apnea',
          'Perfil lipídico completo',
          'Dieta baja en carbohidratos refinados',
          'Actividad física mínimo 150 min/semana'
        ]
      }
    },

    signos_vitales: [
      {
        id: 'sv_002',
        paciente_id: 'pac_002',
        fecha_hora: new Date('2024-10-25T14:00:00'),
        lugar_medicion: 'consultorio',

        presion_sistolica_mmHg: 138,
        presion_diastolica_mmHg: 88,
        presion_arterial_media: 104.7,
        clasificacion_presion: 'Hipertensión Etapa 1',

        frecuencia_cardiaca_lpm: 82,
        ritmo_regular: true,

        frecuencia_respiratoria_rpm: 18,

        temperatura_celsius: 36.7,

        saturacion_oxigeno_porcentaje: 96,

        glucosa_capilar_mgdl: 118,
        momento_medicion: 'postprandial',

        alertas_ia: {
          presion_anormal: true,
          taquicardia: false,
          bradicardia: false,
          hipoglucemia: false,
          hiperglucemia: true,
          recomendacion_urgente: 'ALERTA: Hipertensión Etapa 1 + Glucosa postprandial elevada. Requiere seguimiento médico urgente. Considerar referencia a medicina interna.'
        },

        medido_por: 'Dra. Berenice Palacios',
        notas: 'Paciente refiere ronquidos nocturnos y cansancio diurno. Se sugiere estudio de sueño.'
      }
    ],

    habitos: {
      paciente_id: 'pac_002',
      fecha_evaluacion: new Date('2024-10-25'),

      num_comidas_dia: 2,
      desayuna_diario: false,
      hora_primera_comida: '13:00',
      hora_ultima_comida: '23:00',
      ventana_alimentacion_horas: 10,

      come_viendo_tv: true,
      come_trabajando: true,
      come_rapido: true,
      mastica_suficiente: false,

      alimentos_favoritos: ['Tacos', 'Tortas', 'Refresco', 'Chicharrón'],
      alimentos_rechazados: ['Ensaladas', 'Verduras cocidas'],
      comida_mexicana_favorita: ['Tacos de carnitas', 'Torta de chilaquiles', 'Quesadillas de chicharrón'],

      vasos_agua_dia: 2,
      consume_refrescos: true,
      refrescos_semana: 10,
      consume_alcohol: true,
      bebidas_alcoholicas_semana: 6,

      fuma: true,
      cigarros_dia: 5,
      años_fumando: 10,

      quien_cocina_hogar: 'Madre',
      frecuencia_compra_alimentos: 'Diaria (come en la calle)',
      presupuesto_mensual_alimentos: 3000,
      compra_mercado_local: false,
      compra_supermercado: false,

      consume_tortilla_diario: true,
      consume_frijol_diario: false,
      consume_chile_diario: true,
      desayuno_tipico: 'No desayuna (solo café)',
      come_tacos_semana: 7,
      asiste_fondas_semana: 7,

      analisis_habitos_ia: {
        habitos_positivos: [
          'Ninguno identificado - Patrón alimentario de alto riesgo'
        ],
        habitos_negativos: [
          'No desayuna',
          'Solo 2 comidas al día (ayuno prolongado)',
          'Come exclusivamente en la calle (alta densidad calórica)',
          'Consume 10 refrescos semanales',
          'Come trabajando (conduciendo)',
          'Bajo consumo de agua'
        ],
        habitos_criticos: [
          'CRÍTICO: Tabaquismo activo (5 cigarros/día)',
          'CRÍTICO: Alto consumo de alcohol (6 bebidas/semana)',
          'CRÍTICO: Alimentación 100% en puestos callejeros',
          'CRÍTICO: Cero consumo de verduras y frutas'
        ],
        facilidad_cambio: {
          'iniciar_desayuno': 40,
          'reducir_refrescos': 30,
          'aumentar_agua': 60,
          'dejar_fumar': 20,
          'reducir_alcohol': 35,
          'incorporar_verduras': 25
        },
        plan_modificacion_gradual: [
          {
            semana: 1,
            habito_objetivo: 'Iniciar desayuno simple',
            estrategia: 'Desayuno portátil: 1 pieza de fruta + 1 huevo cocido antes de salir. Preparar la noche anterior.'
          },
          {
            semana: 2,
            habito_objetivo: 'Aumentar agua',
            estrategia: 'Llevar 1 botella de agua en el auto. Objetivo: 4 vasos diarios.'
          },
          {
            semana: 3,
            habito_objetivo: 'Reducir refrescos',
            estrategia: 'Sustituir 3 refrescos por agua natural o agua de limón sin azúcar.'
          },
          {
            semana: 4,
            habito_objetivo: 'Mejorar elecciones en puestos',
            estrategia: 'Elegir tacos de pollo o pescado. Agregar verduras (pico de gallo, nopales).'
          }
        ]
      }
    },

    actividad_fisica: {
      paciente_id: 'pac_002',
      fecha: new Date('2024-10-25'),

      nivel_actividad: 'sedentario',

      trabajo_tipo: 'caminando',
      horas_sentado_dia: 12,

      realiza_ejercicio: false,
      tipo_ejercicio: [],
      frecuencia_semanal: 0,
      duracion_promedio_min: 0,

      practica_deporte: false,

      camina_diario_min: 5,
      pasos_promedio_dia: 2000,

      lesiones_actuales: ['Dolor lumbar crónico'],
      limitaciones_medicas: [],
      dolor_ejercicio: true,

      meta_pasos_dia: 6000,
      meta_ejercicio_semanal_min: 90,

      dispositivo_conectado: undefined,
      datos_sincronizados: false,

      plan_ejercicio_ia: {
        tipo_recomendado: ['Caminata ligera', 'Natación', 'Ejercicios en casa'],
        intensidad: 'Leve a moderada',
        frecuencia_sugerida: 3,
        duracion_sugerida_min: 20,
        consideraciones_salud: [
          'IMPORTANTE: Dolor lumbar crónico - evitar impacto',
          'Sedentarismo severo - iniciar MUY gradualmente',
          'Sobrepeso significativo - preferir actividades sin carga articular',
          'Considerar fisioterapia para dolor lumbar antes de ejercicio intenso'
        ],
        ejercicios_contraindicados: [
          'Correr',
          'Saltos',
          'Levantamiento de peso pesado',
          'Ejercicios de alto impacto'
        ],
        progresion_12_semanas: [
          {
            semana: 1,
            objetivos: 'Evaluación médica + movilidad básica',
            actividades: ['Consulta con traumatólogo', 'Caminar 10 min/día', 'Estiramientos suaves']
          },
          {
            semana: 2,
            objetivos: 'Adaptación cardiovascular mínima',
            actividades: ['Caminar 12 min/día', 'Estiramientos 5 min']
          },
          {
            semana: 3,
            objetivos: 'Incremento gradual',
            actividades: ['Caminar 15 min/día', 'Natación 1x/semana (si es posible)']
          },
          {
            semana: 4,
            objetivos: 'Establecer rutina',
            actividades: ['Caminar 20 min/día', 'Ejercicios en casa (bajo impacto) 2x/semana']
          }
        ]
      },

      sesiones_ejercicio: []
    },

    fecha_creacion: new Date('2024-10-25'),
    fecha_ultima_modificacion: new Date('2024-10-25'),
    nutriologo_responsable: 'Dra. Berenice Palacios González',
    nutriologo_id: 'nut_002'
  }
];
