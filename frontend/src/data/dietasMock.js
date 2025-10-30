/**
 * DATOS MOCK - DIETAS DINÁMICAS GENERADAS POR IA
 * Ejemplos de planes de alimentación personalizados para pacientes mexicanos
 */

export const DIETAS_MOCK = [
  {
    id: 'dieta_001',
    nombre: 'Plan de Reducción - Semana 1',
    paciente_id: 'pac_001', // María Guadalupe
    fecha_inicio: new Date('2024-10-28'),
    fecha_fin: new Date('2024-11-04'),
    objetivo: 'reduccion',

    calorias_totales: 1500,
    distribucion_macros: {
      proteina_g: 90,
      proteina_porcentaje: 24,
      carbohidratos_g: 180,
      carbohidratos_porcentaje: 48,
      grasas_g: 47,
      grasas_porcentaje: 28,
      fibra_g: 30,
    },

    equivalentes_por_dia: {
      cereales_sin_grasa: 4,
      cereales_con_grasa: 1,
      leguminosas: 1,
      verduras: 5,
      frutas: 3,
      leche_descremada: 2,
      carnes_muy_bajo_aporte: 2,
      carnes_bajo_aporte: 2,
      carnes_moderado_aporte: 0,
      grasas_sin_proteina: 2,
      grasas_con_proteina: 1,
    },

    menu_semanal: [
      {
        dia: 1,
        nombre_dia: 'Lunes',
        desayuno: {
          hora_recomendada: '08:00',
          calorias: 380,
          alimentos: [
            { nombre: '2 quesadillas de queso panela con nopales', cantidad: '2 piezas', equivalentes_usados: '2 cereales, 1 verdura, 1 carne bajo aporte', calorias: 280 },
            { nombre: 'Papaya picada', cantidad: '1 taza', equivalentes_usados: '1 fruta', calorias: 60 },
            { nombre: 'Café con leche descremada', cantidad: '1 taza', equivalentes_usados: '1 leche descremada', calorias: 40 },
          ],
          opciones_sustitucion: ['Chilaquiles verdes con pollo', 'Huevos a la mexicana con tortilla', 'Molletes con frijoles'],
        },
        colacion_1: {
          hora_recomendada: '11:00',
          calorias: 150,
          alimentos: [
            { nombre: 'Jícama con limón y chile', cantidad: '1 taza', equivalentes_usados: '2 verduras', calorias: 50 },
            { nombre: 'Almendras', cantidad: '12 piezas', equivalentes_usados: '1 grasa con proteína', calorias: 100 },
          ],
          opciones_sustitucion: ['Zanahoria con limón', 'Pepino con chile', 'Manzana con cacahuates'],
        },
        comida: {
          hora_recomendada: '14:30',
          calorias: 550,
          alimentos: [
            { nombre: 'Sopa de verduras', cantidad: '1 taza', equivalentes_usados: '2 verduras', calorias: 50 },
            { nombre: 'Pechuga de pollo a la plancha', cantidad: '120g', equivalentes_usados: '3 carne muy bajo aporte', calorias: 120 },
            { nombre: 'Ensalada verde con aguacate', cantidad: '1 plato', equivalentes_usados: '2 verduras, 1 grasa con proteína', calorias: 120 },
            { nombre: 'Frijoles de la olla', cantidad: '1/2 taza', equivalentes_usados: '1 leguminosa', calorias: 120 },
            { nombre: 'Tortillas de maíz', cantidad: '2 piezas', equivalentes_usados: '2 cereales', calorias: 140 },
          ],
          opciones_sustitucion: ['Pescado a la veracruzana', 'Bistec ranchero', 'Sopes de frijol con queso'],
        },
        colacion_2: {
          hora_recomendada: '17:30',
          calorias: 120,
          alimentos: [
            { nombre: 'Yogurt griego natural', cantidad: '150ml', equivalentes_usados: '1 leche descremada', calorias: 60 },
            { nombre: 'Fresas picadas', cantidad: '1 taza', equivalentes_usados: '1 fruta', calorias: 60 },
          ],
          opciones_sustitucion: ['Licuado de plátano', 'Gelatina con fruta', 'Pan integral con requesón'],
        },
        cena: {
          hora_recomendada: '20:00',
          calorias: 300,
          alimentos: [
            { nombre: 'Tacos de pollo deshebrado', cantidad: '2 tacos', equivalentes_usados: '2 cereales, 2 carne bajo aporte, 1 verdura', calorias: 250 },
            { nombre: 'Agua de jamaica sin azúcar', cantidad: '1 vaso', equivalentes_usados: 'libre', calorias: 0 },
            { nombre: 'Manzana', cantidad: '1 pieza chica', equivalentes_usados: '1 fruta', calorias: 50 },
          ],
          opciones_sustitucion: ['Quesadillas de huitlacoche', 'Sopa de lentejas', 'Tlacoyos de frijol'],
        },
        calorias_total: 1500,
      },
      // Día 2 (ejemplo más corto)
      {
        dia: 2,
        nombre_dia: 'Martes',
        desayuno: {
          hora_recomendada: '08:00',
          calorias: 370,
          alimentos: [
            { nombre: 'Chilaquiles verdes con pollo', cantidad: '1 porción', equivalentes_usados: '2 cereales, 2 carne bajo aporte, 1 verdura', calorias: 320 },
            { nombre: 'Papaya', cantidad: '1/2 taza', equivalentes_usados: '1 fruta', calorias: 50 },
          ],
          opciones_sustitucion: ['Huevos rancheros', 'Enfrijoladas light'],
        },
        colacion_1: {
          hora_recomendada: '11:00',
          calorias: 140,
          alimentos: [
            { nombre: 'Manzana con cacahuates', cantidad: '1 manzana + 10 cacahuates', equivalentes_usados: '1 fruta, 1 grasa con proteína', calorias: 140 },
          ],
          opciones_sustitucion: ['Pera con nueces', 'Mandarina con almendras'],
        },
        comida: {
          hora_recomendada: '14:30',
          calorias: 560,
          alimentos: [
            { nombre: 'Caldo tlalpeño', cantidad: '1 plato', equivalentes_usados: '2 verduras, 1 carne muy bajo aporte', calorias: 90 },
            { nombre: 'Pescado al mojo de ajo', cantidad: '150g', equivalentes_usados: '3 carne muy bajo aporte', calorias: 120 },
            { nombre: 'Nopales asados', cantidad: '1 taza', equivalentes_usados: '2 verduras', calorias: 50 },
            { nombre: 'Arroz a la mexicana (porción pequeña)', cantidad: '1/2 taza', equivalentes_usados: '2 cereales con grasa', calorias: 230 },
            { nombre: 'Tortillas', cantidad: '1 pieza', equivalentes_usados: '1 cereal', calorias: 70 },
          ],
          opciones_sustitucion: ['Camarones al ajillo', 'Pollo en salsa verde'],
        },
        colacion_2: {
          hora_recomendada: '17:30',
          calorias: 130,
          alimentos: [
            { nombre: 'Leche descremada con café', cantidad: '1 taza', equivalentes_usados: '1 leche descremada', calorias: 95 },
            { nombre: 'Mandarina', cantidad: '2 piezas', equivalentes_usados: '1 fruta', calorias: 35 },
          ],
          opciones_sustitucion: ['Licuado de fresa', 'Atole de avena sin azúcar'],
        },
        cena: {
          hora_recomendada: '20:00',
          calorias: 300,
          alimentos: [
            { nombre: 'Sopes de frijol con queso panela', cantidad: '2 piezas', equivalentes_usados: '2 cereales, 1 leguminosa, 1 carne bajo aporte', calorias: 300 },
          ],
          opciones_sustitucion: ['Tostadas de tinga', 'Peneques de requesón'],
        },
        calorias_total: 1500,
      },
    ],

    generado_por_ia: true,
    optimizaciones_ia: {
      sustitucion_alimentos_culturales: true,
      considera_presupuesto: true,
      considera_temporada: true,
      alergias_evitadas: ['Camarones'],
      preferencias_respetadas: ['Comida mexicana tradicional', 'Tortilla diaria', 'Frijoles'],
    },

    adherencia_porcentaje: 85,
    dias_cumplidos: 6,
    dias_totales: 7,

    ajustes_automaticos: [
      {
        fecha: new Date('2024-10-30'),
        razon: 'Paciente reportó cansancio - se aumentó 100 kcal con carbohidratos complejos',
        cambios: ['Agregada 1 porción extra de fruta en colación', 'Aumentada porción de frijoles en comida'],
      },
    ],

    recetas_incluidas: [
      {
        nombre: 'Chilaquiles Verdes Saludables',
        ingredientes: [
          '8 tortillas de maíz cortadas en triángulos',
          '2 tazas de salsa verde (tomatillos, chile serrano, cebolla, cilantro)',
          '100g pechuga de pollo cocida y deshebrada',
          '2 cucharadas de queso fresco desmoronado',
          '2 cucharadas de crema light',
          '1/4 cebolla morada en rodajas',
          'Aceite en spray para hornear',
        ],
        preparacion: '1. Hornea los triángulos de tortilla a 180°C por 15 min hasta dorar. 2. Licua los ingredientes de la salsa verde. 3. Calienta la salsa en un sartén. 4. Agrega las tortillas horneadas y mezcla. 5. Sirve con pollo, queso, crema y cebolla.',
        tiempo_prep_min: 30,
        porciones: 2,
        calorias_porcion: 320,
        es_tradicional: true,
        region: 'Centro de México',
        tags: ['desayuno', 'tradicional', 'saludable', 'alto_proteina'],
      },
      {
        nombre: 'Sopes de Frijol Light',
        ingredientes: [
          '4 sopes de maíz (hechos en casa o comprados)',
          '1 taza de frijoles negros refritos sin manteca',
          '50g queso panela desmoronado',
          '1 taza de lechuga picada',
          '2 jitomates picados',
          'Salsa verde al gusto',
        ],
        preparacion: '1. Calienta los sopes en comal sin aceite. 2. Unta los frijoles refritos. 3. Agrega queso panela, lechuga y jitomate. 4. Sirve con salsa verde.',
        tiempo_prep_min: 20,
        porciones: 2,
        calorias_porcion: 300,
        es_tradicional: true,
        region: 'Centro de México',
        tags: ['cena', 'vegetariano', 'tradicional', 'economico'],
      },
    ],

    lista_compras: [
      {
        categoria: 'Proteínas',
        items: [
          { producto: 'Pechuga de pollo sin piel', cantidad: '1kg', costo_estimado_mxn: 120 },
          { producto: 'Pescado (tilapia o robalo)', cantidad: '500g', costo_estimado_mxn: 90 },
          { producto: 'Queso panela', cantidad: '250g', costo_estimado_mxn: 45 },
          { producto: 'Huevos', cantidad: '12 piezas', costo_estimado_mxn: 40 },
        ],
      },
      {
        categoria: 'Frutas y Verduras',
        items: [
          { producto: 'Nopales', cantidad: '1kg', costo_estimado_mxn: 25 },
          { producto: 'Jitomates', cantidad: '1kg', costo_estimado_mxn: 30 },
          { producto: 'Aguacate', cantidad: '4 piezas', costo_estimado_mxn: 60 },
          { producto: 'Papaya', cantidad: '1 pieza', costo_estimado_mxn: 35 },
          { producto: 'Manzanas', cantidad: '1kg', costo_estimado_mxn: 40 },
          { producto: 'Lechuga', cantidad: '2 piezas', costo_estimado_mxn: 20 },
        ],
      },
      {
        categoria: 'Cereales y Leguminosas',
        items: [
          { producto: 'Tortillas de maíz', cantidad: '1kg', costo_estimado_mxn: 18 },
          { producto: 'Frijoles negros', cantidad: '500g', costo_estimado_mxn: 22 },
          { producto: 'Arroz', cantidad: '1kg', costo_estimado_mxn: 25 },
        ],
      },
      {
        categoria: 'Lácteos',
        items: [
          { producto: 'Leche descremada', cantidad: '2L', costo_estimado_mxn: 50 },
          { producto: 'Yogurt griego natural', cantidad: '1L', costo_estimado_mxn: 65 },
        ],
      },
    ],
  },
];
