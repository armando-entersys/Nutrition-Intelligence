# Guía de Usuario - Nutrition Intelligence Platform

Bienvenido a Nutrition Intelligence, tu asistente inteligente para una nutrición saludable con enfoque en el contexto mexicano.

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Primeros Pasos](#primeros-pasos)
3. [Análisis de Fotos con IA](#análisis-de-fotos-con-ia)
4. [Recordatorio de 24 Horas](#recordatorio-de-24-horas)
5. [Calculadora de Requerimientos](#calculadora-de-requerimientos)
6. [Recetas Mexicanas](#recetas-mexicanas)
7. [Planes Alimenticios](#planes-alimenticios)
8. [Portal de Nutriólogo](#portal-de-nutriólogo)
9. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

Nutrition Intelligence es una plataforma diseñada para ayudarte a:

- Analizar el contenido nutricional de tus comidas con solo tomar una foto
- Llevar un registro completo de tu alimentación diaria
- Calcular tus requerimientos nutricionales personalizados
- Descubrir recetas mexicanas saludables
- Crear planes alimenticios semanales
- (Nutriólogos) Gestionar pacientes y consultas

**Características únicas:**
- Basado en el **Sistema Mexicano de Alimentos Equivalentes (SMAE)**
- Análisis con **Inteligencia Artificial** (Gemini Vision + Claude)
- Cumplimiento con **NOM-051** (sellos de advertencia)
- Culturalmente apropiado para México

---

## Primeros Pasos

### 1. Acceder a la Plataforma

Abre tu navegador y ve a: `http://localhost:3005`

(En producción sería: `https://nutrition-intelligence.com`)

### 2. Crear una Cuenta

1. Haz clic en **"Registrarse"**
2. Completa el formulario:
   - Nombre de usuario (único)
   - Email (válido)
   - Contraseña (mínimo 8 caracteres)
   - Nombre completo
3. Acepta los términos y condiciones
4. Haz clic en **"Crear Cuenta"**

### 3. Iniciar Sesión

1. Haz clic en **"Iniciar Sesión"**
2. Ingresa tu usuario y contraseña
3. Haz clic en **"Entrar"**

### 4. Explorar el Dashboard

Una vez dentro, verás las principales funcionalidades:

```
┌─────────────────────────────────────────┐
│         NUTRITION INTELLIGENCE          │
├─────────────────────────────────────────┤
│  📸  Análisis de Fotos IA               │
│  📝  Recordatorio 24 Horas              │
│  🧮  Calculadora de Requerimientos      │
│  🍴  Recetas Mexicanas                  │
│  📅  Plan Semanal                       │
│  👤  Mi Perfil                          │
└─────────────────────────────────────────┘
```

---

## Análisis de Fotos con IA

Esta es la funcionalidad estrella de la plataforma. Con solo tomar una foto de tu comida, obtienes un análisis nutricional completo.

### ¿Cómo funciona?

1. **Capturar o subir foto**
2. **IA analiza la imagen** (Gemini o Claude Vision)
3. **Recibes análisis detallado** en 15-30 segundos

### Paso a Paso

#### Opción 1: Capturar con Cámara

1. Ve a **"Análisis de Fotos IA"**
2. Haz clic en el botón **"📷 Capturar Foto"**
3. Permite el acceso a la cámara (si te lo solicita)
4. Encuadra tu comida:
   - Asegúrate de que haya buena iluminación
   - Toma la foto desde arriba
   - Incluye todo el platillo en el encuadre
5. Haz clic en **"Tomar Foto"**
6. Revisa la vista previa
7. Haz clic en **"Analizar con IA"**

#### Opción 2: Subir Imagen desde Archivo

1. Ve a **"Análisis de Fotos IA"**
2. Haz clic en **"📁 Subir Imagen"**
3. Selecciona una imagen de tu dispositivo
   - Formatos aceptados: JPG, PNG, WEBP
   - Tamaño máximo: 10 MB
4. Revisa la vista previa
5. Haz clic en **"Analizar con IA"**

### Interpretar los Resultados

Después de 15-30 segundos, recibirás un análisis completo:

#### 1. Platillo Identificado

```
╔══════════════════════════════════════╗
║    TACOS AL PASTOR                   ║
║    Confianza: 92%                    ║
╠══════════════════════════════════════╣
║  Región: Ciudad de México            ║
║  Categoría: Antojito mexicano        ║
║  Es tradicional: ✓ Sí                ║
╚══════════════════════════════════════╝
```

- **Nombre**: El platillo que la IA detectó
- **Confianza**: Qué tan segura está la IA (0-100%)
- **Región**: De dónde es típico el platillo
- **Categoría**: Tipo de platillo

#### 2. Ingredientes Detectados

Para cada ingrediente verás:

```
🌮 Tortilla de maíz
   Cantidad: 3 piezas (90g)
   Confianza: 95%
   ────────────────────────
   Calorías:     192 kcal
   Proteína:     4.5 g
   Carbohidratos: 41.4 g
   Grasas:       2.7 g
   Fibra:        3.3 g
   Sodio:        15 mg
   ────────────────────────
   Categoría SMAE: Cereales sin grasa
```

#### 3. Totales Nutricionales

```
TOTALES DEL PLATILLO
━━━━━━━━━━━━━━━━━━━━
Calorías:      650 kcal
Proteína:      35 g
Carbohidratos: 70 g
Grasas:        25 g
Fibra:         8 g
Sodio:         1200 mg
━━━━━━━━━━━━━━━━━━━━
Margen de error: ±15%
```

**Nota**: El margen de error indica la precisión de la estimación

#### 4. Sellos NOM-051 (Advertencias)

Verás octágonos negros si el platillo tiene excesos según la norma oficial mexicana:

```
⬛ EXCESO SODIO
⬛ EXCESO GRASAS SATURADAS
```

Posibles sellos:
- ⬛ Exceso Calorías
- ⬛ Exceso Azúcares
- ⬛ Exceso Grasas Saturadas
- ⬛ Exceso Grasas Trans
- ⬛ Exceso Sodio
- ⬛ Contiene Edulcorantes
- ⬛ Contiene Cafeína

#### 5. Evaluación de Salubridad

```
╔══════════════════════════════════╗
║   SCORE: 68/100                  ║
║   NIVEL: BUENO                   ║
╚══════════════════════════════════╝

Factores Positivos:
✓ Alto en proteína
✓ Fibra adecuada
✓ Ingredientes naturales

Factores Negativos:
✗ Alto en sodio
✗ Grasas saturadas elevadas
```

**Niveles de score**:
- 80-100: 🟢 Excelente
- 60-79:  🟡 Bueno
- 40-59:  🟠 Moderado
- 0-39:   🔴 Pobre

#### 6. Recomendaciones Personalizadas

```
💡 RECOMENDACIONES

1. [REDUCCIÓN] Reducir sal
   Pedir sin sal adicional o usar menos salsa
   Impacto: Reducir sodio en 30%

2. [SUSTITUCIÓN] Cambiar tortilla
   Usar tortilla integral en lugar de regular
   Impacto: Aumentar fibra en 5g

3. [ADICIÓN] Agregar verduras
   Incluir pico de gallo o ensalada
   Impacto: Añadir vitaminas y fibra
```

**Tipos de recomendaciones**:
- 🔻 **Reducción**: Disminuir algo problemático
- 🔄 **Sustitución**: Cambiar por opción más saludable
- ➕ **Adición**: Agregar algo beneficioso
- 📏 **Porción**: Ajustar cantidad

#### 7. Contexto Diario

```
📊 CONTEXTO EN TU DÍA

Este platillo representa:
• 32.5% de tus calorías diarias (basado en 2000 kcal/día)

Momento recomendado:
• Comida principal (12:00 - 15:00 h)

Requiere ajuste: No
✓ Porción adecuada para comida fuerte
```

### Historial de Análisis

Todos tus análisis se guardan en el **Historial**:

1. Ve a la pestaña **"Historial"** en Análisis de Fotos
2. Verás una lista de análisis previos con:
   - Miniatura de la foto
   - Platillo identificado
   - Calorías totales
   - Fecha y hora
3. Haz clic en cualquiera para ver el análisis completo

### Consejos para Mejores Resultados

✅ **Haz esto:**
- Toma fotos con buena iluminación (luz natural es mejor)
- Encuadra todo el platillo
- Toma la foto desde arriba (vista cenital)
- Usa fondo simple (mesa, plato)
- Asegúrate que la foto esté enfocada

❌ **Evita esto:**
- Fotos con sombras fuertes
- Imágenes borrosas o desenfocadas
- Fotos muy oscuras
- Platillos muy mezclados (difícil de identificar ingredientes)

---

## Recordatorio de 24 Horas

El Recordatorio de 24 Horas te permite llevar un diario completo de todo lo que comes en el día.

### ¿Para qué sirve?

- Conocer exactamente qué y cuánto comes
- Identificar patrones alimenticios
- Cumplir con tus metas nutricionales
- Compartir con tu nutriólogo

### Cómo Usar el Recordatorio

#### 1. Iniciar un Nuevo Día

1. Ve a **"Recordatorio 24 Horas"**
2. Haz clic en **"Nuevo Día"**
3. Selecciona la fecha (por defecto: hoy)

#### 2. Registrar Comidas

Para cada tiempo de comida:

**Desayuno (7:00 - 10:00)**

1. Haz clic en **"+ Agregar Alimento"**
2. Busca el alimento:
   - Escribe el nombre (ej: "huevo")
   - Verás resultados de la base SMAE
3. Selecciona el alimento exacto
4. Especifica la cantidad:
   - Por peso: 100g, 50g, etc.
   - Por piezas: 2 piezas, 1 taza, etc.
   - Por equivalentes SMAE: 2 equivalentes
5. Haz clic en **"Agregar"**

Repite para todos los alimentos del desayuno.

**Comida (12:00 - 15:00)**

Igual que el desayuno.

**Cena (19:00 - 22:00)**

Igual que el desayuno.

**Colaciones**

También puedes registrar snacks entre comidas:
- Colación matutina (10:00 - 12:00)
- Colación vespertina (16:00 - 18:00)

#### 3. Ver Resumen del Día

Al final de la página verás tu resumen:

```
╔══════════════════════════════════════════╗
║       RESUMEN NUTRICIONAL DEL DÍA        ║
╠══════════════════════════════════════════╣
║  Total Calorías:        1,850 kcal       ║
║  Meta diaria:           2,000 kcal       ║
║  Restante:              150 kcal         ║
╠══════════════════════════════════════════╣
║  Proteína:    92g  (20%)  [✓ Meta: 100g] ║
║  Carbohidratos: 220g (48%)  [✓ Meta: 250g] ║
║  Grasas:      65g  (32%)  [✓ Meta: 67g]  ║
╚══════════════════════════════════════════╝
```

**Gráficas visuales**:
- Gráfica de dona: Distribución de macronutrientes
- Barra de progreso: Calorías vs meta
- Gráfica de barras: Comparación por tiempo de comida

#### 4. Editar o Eliminar Alimentos

- Haz clic en el ícono de lápiz ✏️ para editar
- Haz clic en el ícono de basura 🗑️ para eliminar

#### 5. Guardar el Recordatorio

1. Revisa que todo esté correcto
2. Haz clic en **"Guardar Recordatorio"**
3. Opcionalmente agrega notas:
   - "Día con mucha actividad física"
   - "Me sentí con poca energía en la tarde"
   - "Comí fuera de casa"

### Base de Datos SMAE

El sistema usa la base oficial del **Sistema Mexicano de Alimentos Equivalentes**:

**Categorías disponibles**:
- 🌾 Cereales (con grasa / sin grasa)
- 🍎 Frutas
- 🥗 Verduras
- 🥛 Lácteos (descremados / semidescremados / enteros)
- 🍖 Carnes (muy bajo / bajo / moderado / alto en grasa)
- 🥜 Leguminosas
- 🧈 Grasas (con / sin proteína)
- 🍬 Azúcares (con / sin grasa)

Cada alimento incluye:
- Porción estándar (gramos, tazas, piezas)
- Equivalentes SMAE
- Información nutricional completa
- Origen (México, importado, etc.)

---

## Calculadora de Requerimientos

Descubre cuántas calorías y macronutrientes necesitas según tu perfil y objetivos.

### ¿Qué Calcula?

1. **TMB** (Tasa Metabólica Basal): Calorías que tu cuerpo necesita en reposo
2. **TDEE** (Total Daily Energy Expenditure): Calorías totales según actividad
3. **Distribución de Macronutrientes**: Proteína, carbohidratos, grasas
4. **Ajuste por Objetivo**: Déficit, superávit o mantenimiento

### Paso a Paso

#### 1. Información Personal

```
╔════════════════════════════════════╗
║    DATOS PERSONALES                ║
╠════════════════════════════════════╣
║  Edad:           28 años           ║
║  Sexo:           Masculino         ║
║  Peso:           75 kg             ║
║  Altura:         175 cm            ║
╚════════════════════════════════════╝
```

#### 2. Nivel de Actividad Física

Selecciona el que mejor te describe:

- **Sedentario**: Trabajo de oficina, sin ejercicio (Factor: 1.2)
- **Ligeramente activo**: Ejercicio ligero 1-3 días/semana (Factor: 1.375)
- **Moderadamente activo**: Ejercicio moderado 3-5 días/semana (Factor: 1.55)
- **Muy activo**: Ejercicio intenso 6-7 días/semana (Factor: 1.725)
- **Extremadamente activo**: Ejercicio muy intenso + trabajo físico (Factor: 1.9)

#### 3. Objetivo

Selecciona tu meta:

- **Perder peso**: Déficit de -500 kcal/día (pierde ~0.5 kg/semana)
- **Mantener peso**: Sin ajuste de calorías
- **Ganar masa muscular**: Superávit de +300 kcal/día (gana ~0.25 kg/semana)

#### 4. Ver Resultados

```
╔════════════════════════════════════════════╗
║         TUS REQUERIMIENTOS DIARIOS         ║
╠════════════════════════════════════════════╣
║  Calorías totales:       2,350 kcal        ║
╠════════════════════════════════════════════╣
║  MACRONUTRIENTES                           ║
║  ────────────────────────────────────      ║
║  Proteína:        150g  (26%)              ║
║                   600 kcal                 ║
║                   2.0 g/kg peso            ║
║                                            ║
║  Carbohidratos:   265g  (45%)              ║
║                   1,060 kcal               ║
║                                            ║
║  Grasas:          76g   (29%)              ║
║                   690 kcal                 ║
╚════════════════════════════════════════════╝
```

**Recomendaciones personalizadas**:

```
📋 RECOMENDACIONES

✓ Distribuye tu proteína en 4-5 comidas (30-40g por comida)
✓ Consume carbohidratos antes y después de entrenar
✓ Incluye grasas saludables (aguacate, nueces, aceite de oliva)
✓ Bebe al menos 2-3 litros de agua al día
✓ Duerme 7-8 horas para mejor recuperación
```

### Guardar tus Requerimientos

1. Haz clic en **"Guardar Requerimientos"**
2. Tu perfil nutricional se guarda
3. El sistema lo usará para:
   - Calcular % de metas en el Recordatorio 24h
   - Generar planes alimenticios personalizados
   - Evaluar tus análisis de fotos

---

## Recetas Mexicanas

Explora un catálogo de recetas tradicionales y saludables.

### Explorar Recetas

#### 1. Filtros Disponibles

```
┌────────────────────────────────────┐
│  FILTROS                           │
├────────────────────────────────────┤
│  Categoría:                        │
│  ☑ Desayunos                       │
│  ☐ Comidas                         │
│  ☐ Cenas                           │
│  ☐ Postres                         │
│                                    │
│  Dificultad:                       │
│  ☑ Fácil                           │
│  ☐ Intermedia                      │
│  ☐ Difícil                         │
│                                    │
│  Tiempo de preparación:            │
│  ☑ Menos de 30 min                 │
│  ☐ 30-60 min                       │
│  ☐ Más de 60 min                   │
│                                    │
│  Calorías por porción:             │
│  [200]───────●──────[800] kcal     │
└────────────────────────────────────┘
```

#### 2. Ver Detalles de Receta

Haz clic en cualquier receta para ver:

**Información General**:
```
╔═══════════════════════════════════════╗
║   CHILAQUILES VERDES SALUDABLES       ║
╠═══════════════════════════════════════╣
║   ⭐⭐⭐⭐⭐ 4.8 (124 calificaciones)   ║
║   Dificultad: Fácil                   ║
║   Tiempo: 25 minutos                  ║
║   Porciones: 4                        ║
╚═══════════════════════════════════════╝
```

**Información Nutricional (por porción)**:
```
Calorías:      320 kcal
Proteína:      18 g
Carbohidratos: 35 g
Grasas:        12 g
Fibra:         6 g
Sodio:         450 mg
```

**Ingredientes**:
```
Para 4 porciones:

Base:
• 12 tortillas de maíz horneadas (no fritas)
• 2 tazas de salsa verde casera
• 1/2 cebolla blanca fileteada
• 200g de pechuga de pollo deshebrada

Toppings:
• 1/2 taza de queso fresco bajo en grasa
• 1/4 taza de crema light
• 1 aguacate en rebanadas
• Cilantro fresco al gusto
```

**Instrucciones paso a paso**:
```
1. Precalienta el horno a 180°C. Corta las tortillas
   en triángulos y hornéalas 10 minutos hasta que
   estén crujientes.

2. En una sartén, calienta la salsa verde. Agrega
   las tortillas y mezcla suavemente.

3. Sirve inmediatamente y agrega el pollo, cebolla,
   queso, crema y aguacate.

4. Decora con cilantro fresco.
```

**Tips del Chef**:
```
💡 Puedes preparar la salsa verde el día anterior
💡 Las tortillas horneadas son más saludables que fritas
💡 Usa pollo asado del día anterior para ahorrar tiempo
```

#### 3. Calificar y Comentar

Después de preparar la receta:

1. Haz clic en las estrellas para calificar (1-5)
2. Escribe un comentario:
   - ¿Qué te gustó?
   - ¿Hiciste modificaciones?
   - ¿Recomendaciones para otros?
3. Opcionalmente sube foto de tu platillo

#### 4. Guardar Favoritas

- Haz clic en el ícono de corazón ❤️ para guardar
- Ve a **"Mis Recetas Favoritas"** para acceder rápido

---

## Planes Alimenticios

Genera planes semanales personalizados basados en tus requerimientos.

### Generar Plan Automático

#### 1. Configurar Plan

```
╔═══════════════════════════════════════════╗
║      NUEVO PLAN ALIMENTICIO               ║
╠═══════════════════════════════════════════╣
║  Nombre: Plan Pérdida de Peso - Enero     ║
║  Duración: 7 días                         ║
║  Basado en: Mis requerimientos guardados  ║
║                                           ║
║  Preferencias:                            ║
║  ☑ Solo recetas mexicanas                 ║
║  ☑ Incluir colaciones                     ║
║  ☐ Vegetariano                            ║
║  ☐ Sin lácteos                            ║
║  ☐ Sin gluten                             ║
╚═══════════════════════════════════════════╝
```

#### 2. Generar Plan

1. Haz clic en **"Generar Plan"**
2. El sistema automáticamente:
   - Selecciona recetas apropiadas
   - Distribuye macronutrientes óptimamente
   - Balancea variedad de alimentos
   - Cumple con tus requerimientos diarios

#### 3. Ver Plan Semanal

```
┌─────────────────────────────────────────┐
│           PLAN SEMANAL                  │
├─────────────────────────────────────────┤
│                                         │
│  LUNES                                  │
│  Desayuno: Chilaquiles verdes          │
│            320 kcal | 18P 35C 12G       │
│  Colación: Manzana + almendras         │
│            180 kcal | 4P 22C 9G         │
│  Comida: Pechuga asada + arroz         │
│          450 kcal | 40P 48C 8G          │
│  Colación: Yogurt griego + granola     │
│            200 kcal | 15P 25C 5G        │
│  Cena: Sopa de verduras + quesadilla   │
│        380 kcal | 18P 42C 15G           │
│  ─────────────────────────────────      │
│  Total día: 1,530 kcal | 95P 172C 49G   │
│                                         │
├─────────────────────────────────────────┤
│  MARTES                                 │
│  ...                                    │
└─────────────────────────────────────────┘
```

#### 4. Personalizar Plan

Puedes modificar cualquier comida:

1. Haz clic en **"Editar"** en una comida
2. Opciones:
   - **Sustituir**: Cambia por otra receta similar
   - **Ajustar porciones**: Aumenta o reduce cantidad
   - **Eliminar**: Quita esa comida
   - **Agregar**: Añade algo nuevo

#### 5. Lista de Compras

1. Haz clic en **"Generar Lista de Compras"**
2. El sistema agrupa ingredientes:

```
╔═══════════════════════════════════════╗
║    LISTA DE COMPRAS - SEMANA 1        ║
╠═══════════════════════════════════════╣
║  VERDURAS Y FRUTAS                    ║
║  ☐ Tomates: 1.5 kg                    ║
║  ☐ Cebolla: 3 piezas                  ║
║  ☐ Aguacate: 4 piezas                 ║
║  ☐ Manzanas: 7 piezas                 ║
║                                       ║
║  PROTEÍNAS                            ║
║  ☐ Pechuga de pollo: 1.2 kg           ║
║  ☐ Huevos: 18 piezas                  ║
║  ☐ Queso fresco: 400g                 ║
║                                       ║
║  CEREALES                             ║
║  ☐ Tortillas de maíz: 50 piezas       ║
║  ☐ Arroz integral: 500g               ║
║                                       ║
║  [IMPRIMIR] [COMPARTIR] [COPIAR]      ║
╚═══════════════════════════════════════╝
```

3. Opciones:
   - Imprimir PDF
   - Compartir por WhatsApp
   - Enviar por email
   - Copiar al portapapeles

---

## Portal de Nutriólogo

Si eres nutriólogo certificado, tienes acceso a funcionalidades profesionales.

### Activar Cuenta de Nutriólogo

1. Ve a **"Mi Perfil"**
2. Haz clic en **"Solicitar Cuenta de Nutriólogo"**
3. Proporciona:
   - Cédula profesional
   - Universidad de egreso
   - Años de experiencia
   - Documento de identidad
4. Espera aprobación (24-48 horas)

### Gestión de Pacientes

#### 1. Agregar Nuevo Paciente

```
╔════════════════════════════════════════╗
║       NUEVO PACIENTE                   ║
╠════════════════════════════════════════╣
║  Datos Personales:                     ║
║  Nombre: María González Pérez          ║
║  Edad: 32 años                         ║
║  Sexo: Femenino                        ║
║  Email: maria@email.com                ║
║  Teléfono: +52 55 1234 5678            ║
║                                        ║
║  Mediciones:                           ║
║  Peso: 68 kg                           ║
║  Altura: 162 cm                        ║
║  IMC: 25.9 (Sobrepeso)                 ║
║                                        ║
║  Estilo de Vida:                       ║
║  Actividad física: Moderada            ║
║  Ocupación: Oficina                    ║
║                                        ║
║  Objetivo:                             ║
║  ☑ Perder peso (-5 kg en 3 meses)      ║
║  ☐ Ganar masa muscular                 ║
║  ☐ Control de diabetes                 ║
║  ☐ Embarazo/lactancia                  ║
║                                        ║
║  Alergias/Restricciones:               ║
║  • Intolerancia a la lactosa           ║
║  • No consume mariscos                 ║
╚════════════════════════════════════════╝
```

#### 2. Historial de Consultas

Para cada paciente puedes ver:

```
HISTORIAL - María González
─────────────────────────────────
📅 15 Ene 2025 - Primera consulta
   Peso: 68 kg | IMC: 25.9
   Plan: Pérdida de peso moderada

📅 29 Ene 2025 - Seguimiento 2 sem
   Peso: 66.5 kg (-1.5 kg) ✓
   Adherencia: 85%
   Ajustes: Aumentar proteína

📅 12 Feb 2025 - Seguimiento 1 mes
   Peso: 65.2 kg (-2.8 kg) ✓
   Adherencia: 90%
   Progreso: Excelente
```

#### 3. Crear Plan para Paciente

1. Selecciona paciente
2. Haz clic en **"Nuevo Plan Alimenticio"**
3. El sistema automáticamente:
   - Calcula requerimientos del paciente
   - Considera restricciones/alergias
   - Propone plan semanal
4. Puedes personalizar completamente
5. Comparte directamente con paciente

#### 4. Reportes y Gráficas

Ver progreso visual del paciente:

- Gráfica de peso vs tiempo
- Adherencia al plan
- Distribución de macronutrientes
- Comparación vs metas

---

## Preguntas Frecuentes

### General

**P: ¿Es gratis la plataforma?**
R: La versión básica es gratuita. Hay planes premium con funcionalidades adicionales.

**P: ¿Funciona en celular?**
R: Sí, la interfaz es responsive y funciona en cualquier dispositivo con navegador.

**P: ¿Mis datos están seguros?**
R: Sí, usamos encriptación y cumplimos con todas las normas de privacidad.

### Análisis con IA

**P: ¿Qué tan preciso es el análisis de IA?**
R: Gemini Vision tiene ~85-90% de precisión. En modo híbrido con Claude alcanza ~92-95%.

**P: ¿Puedo analizar fotos de comida internacional?**
R: Sí, pero la precisión es mayor con platillos mexicanos por el entrenamiento del prompt.

**P: ¿Cuánto tiempo tarda el análisis?**
R: Entre 15-30 segundos dependiendo del modelo y complejidad del platillo.

**P: ¿Por qué me da "Confianza: 0%"?**
R: Significa que las API keys no están configuradas y ves datos mock de ejemplo.

### Recordatorio 24 Horas

**P: ¿Puedo editar días anteriores?**
R: Sí, puedes ver y editar cualquier recordatorio previo en el historial.

**P: ¿Cómo busco un alimento que no encuentro?**
R: Usa sinónimos o nombres generales. Ej: "pan dulce" en lugar de "concha".

**P: ¿Puedo agregar alimentos personalizados?**
R: Sí, en **"Mis Alimentos"** puedes crear alimentos con info nutricional personalizada.

### Planes Alimenticios

**P: ¿Puedo generar planes de más de 7 días?**
R: Sí, puedes crear planes de 1, 7, 14, 21 o 30 días.

**P: ¿Se puede exportar el plan?**
R: Sí, puedes exportar a PDF, Excel o compartir por email.

### Técnico

**P: ¿Necesito instalar algo?**
R: No, es una aplicación web que funciona en el navegador.

**P: ¿Qué navegadores son compatibles?**
R: Chrome, Firefox, Safari, Edge (versiones recientes).

**P: ¿Funciona sin internet?**
R: Algunas funcionalidades básicas sí (modo offline limitado).

---

## Soporte

¿Necesitas ayuda?

- **Email**: soporte@nutrition-intelligence.com
- **Chat en vivo**: Botón en esquina inferior derecha
- **FAQ extendido**: https://docs.nutrition-intelligence.com
- **Video tutoriales**: https://youtube.com/nutrition-intelligence

---

## Consejos Generales

### Para Mejores Resultados

1. **Sé consistente**: Registra todos los días en el recordatorio
2. **Sé honesto**: Registra TODO lo que comes, incluso snacks pequeños
3. **Sé preciso**: Usa báscula de cocina para porciones exactas
4. **Sé paciente**: Los cambios toman tiempo (4-6 semanas)

### Maximiza el Valor de la Plataforma

- ✅ Toma fotos de todas tus comidas importantes
- ✅ Revisa tu resumen nutricional diario
- ✅ Sigue las recomendaciones del análisis IA
- ✅ Prueba nuevas recetas semanalmente
- ✅ Consulta con un nutriólogo si tienes dudas

---

**¡Feliz viaje hacia una mejor nutrición! 🥗🇲🇽**

Última actualización: 2025-10-31
