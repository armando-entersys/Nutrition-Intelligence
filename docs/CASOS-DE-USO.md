# Documentación de Casos de Uso

## Nutrition Intelligence Platform - Especificación Funcional

**Versión:** 1.0.0
**Fecha:** Enero 2025
**Autor:** Equipo de Arquitectura de Software
**Estado:** Producción

---

## 📋 Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Actores del Sistema](#2-actores-del-sistema)
3. [Diagrama General de Casos de Uso](#3-diagrama-general-de-casos-de-uso)
4. [Casos de Uso por Módulo](#4-casos-de-uso-por-módulo)
5. [Flujos Detallados](#5-flujos-detallados)
6. [Matriz de Trazabilidad](#6-matriz-de-trazabilidad)

---

## 1. Introducción

### 1.1 Propósito del Documento

Este documento describe los casos de uso del sistema **Nutrition Intelligence Platform**, especificando las interacciones entre los usuarios y el sistema para lograr objetivos específicos en el contexto de la gestión nutricional profesional.

### 1.2 Alcance

Este documento cubre todos los casos de uso implementados en la Fase 2 del proyecto:

- ✅ Gestión de Expediente Clínico
- ✅ Gestión de Datos de Laboratorio con IA
- ✅ Archivos Clínicos con OCR
- ✅ Mensajería WhatsApp
- ✅ Generación de Dietas
- ✅ Análisis de Fotos con IA
- ✅ Gamificación Mexicana
- ✅ Chat con Nutriólogo IA

### 1.3 Definiciones

- **Actor:** Usuario o sistema externo que interactúa con la plataforma
- **Caso de Uso:** Secuencia de acciones que el sistema ejecuta para proveer valor a un actor
- **Precondición:** Estado del sistema antes de ejecutar el caso de uso
- **Postcondición:** Estado del sistema después de ejecutar el caso de uso
- **Flujo Principal:** Secuencia normal de eventos
- **Flujo Alterno:** Variaciones del flujo principal
- **Flujo de Excepción:** Manejo de errores

---

## 2. Actores del Sistema

### 2.1 Actores Primarios

#### 👨‍⚕️ Nutriólogo (Nutritionist)
**Descripción:** Profesional de la salud que gestiona planes nutricionales para pacientes.

**Responsabilidades:**
- Gestionar expedientes clínicos completos
- Analizar datos de laboratorio
- Crear y ajustar planes de alimentación
- Enviar mensajes y recordatorios a pacientes
- Interpretar análisis de fotos de alimentos
- Consultar sistema SMAE y equivalencias mexicanas

**Nivel de Acceso:** Alto (todas las funcionalidades excepto administración)

#### 😊 Paciente (Patient)
**Descripción:** Persona que recibe atención nutricional.

**Responsabilidades:**
- Consultar su propio expediente clínico
- Ver su plan de alimentación
- Subir fotos de alimentos para análisis
- Interactuar con gamificación (logros, puntos)
- Usar recordatorio de 24 horas
- Chatear con IA nutriológica

**Nivel de Acceso:** Limitado (solo información propia)

#### 🔧 Administrador (Admin)
**Descripción:** Personal técnico que gestiona el sistema.

**Responsabilidades:**
- Gestionar usuarios y roles
- Monitorear sistema y logs
- Configurar parámetros del sistema
- Gestionar base de datos
- Acceder a dashboard de pruebas

**Nivel de Acceso:** Total (incluye funciones administrativas)

### 2.2 Actores Secundarios

#### 🤖 IA de Google Gemini
**Descripción:** Servicio de inteligencia artificial para análisis de imágenes.

**Rol:** Analizar fotos de alimentos y proporcionar información nutricional.

#### 🤖 Anthropic Claude
**Descripción:** Servicio de IA avanzada para análisis nutricional profundo.

**Rol:** Analizar fotos de alimentos con mayor precisión cuando se requiere.

#### 📱 Twilio WhatsApp API
**Descripción:** Servicio de mensajería para comunicación con pacientes.

**Rol:** Enviar recordatorios, notificaciones y mensajes motivacionales.

#### 📊 Sistema SMAE
**Descripción:** Base de datos del Sistema Mexicano de Alimentos Equivalentes.

**Rol:** Proveer información de equivalencias de alimentos mexicanos.

---

## 3. Diagrama General de Casos de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│                 NUTRITION INTELLIGENCE PLATFORM                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│  Nutriólogo  │────────┐
└──────────────┘        │
                        ├──► [CU-001] Gestionar Expediente Clínico
┌──────────────┐        │
│   Paciente   │────────┤    [CU-002] Analizar Datos de Laboratorio
└──────────────┘        │
                        ├──► [CU-003] Subir y Analizar Archivos Clínicos
┌──────────────┐        │
│     Admin    │────────┤    [CU-004] Enviar Mensajes WhatsApp
└──────────────┘        │
                        ├──► [CU-005] Generar Plan de Alimentación
                        │
                        ├──► [CU-006] Analizar Foto de Alimento con IA
                        │
                        ├──► [CU-007] Usar Gamificación Mexicana
                        │
                        ├──► [CU-008] Chatear con Nutriólogo IA
                        │
                        └──► [CU-009] Usar Recordatorio 24 Horas
```

---

## 4. Casos de Uso por Módulo

### 4.1 Módulo: Expediente Clínico

#### CU-001: Gestionar Expediente Clínico

**ID:** CU-001
**Actor Principal:** Nutriólogo
**Actores Secundarios:** Paciente (consulta solamente)

**Descripción:**
Permite crear, consultar, modificar y gestionar el expediente clínico completo de un paciente, incluyendo datos generales, historia clínica, mediciones antropométricas, signos vitales, datos de laboratorio y archivos clínicos.

**Precondiciones:**
- Usuario autenticado como Nutriólogo
- Paciente existe en el sistema (o será creado)

**Postcondiciones:**
- Expediente clínico creado/actualizado
- Datos almacenados en base de datos
- Historial de cambios registrado (auditoría)

**Flujo Principal:**

1. Nutriólogo accede a "Expediente Clínico" desde el menú
2. Sistema muestra lista de pacientes existentes
3. Nutriólogo selecciona un paciente o crea uno nuevo
4. Sistema muestra el expediente con las siguientes secciones:
   - 4.1. **Datos Generales**
   - 4.2. **Historia Clínica**
   - 4.3. **Mediciones Antropométricas**
   - 4.4. **Signos Vitales**
   - 4.5. **Datos de Laboratorio**
   - 4.6. **Archivos Clínicos**
5. Nutriólogo navega entre tabs y actualiza información
6. Nutriólogo guarda cambios
7. Sistema valida datos y guarda en base de datos
8. Sistema muestra confirmación de éxito
9. Sistema registra auditoría (NOM-004-SSA3-2012)

**Flujos Alternos:**

**FA-001:** Crear Nuevo Paciente
- 3a. Nutriólogo selecciona "Nuevo Paciente"
- 3b. Sistema muestra formulario de datos generales
- 3c. Nutriólogo completa información mínima requerida
- 3d. Sistema valida CURP (opcional)
- 3e. Sistema crea paciente y abre expediente
- Retorna a paso 4

**FA-002:** Búsqueda Rápida de Paciente
- 2a. Nutriólogo usa barra de búsqueda
- 2b. Sistema filtra pacientes por nombre, CURP o ID
- 2c. Nutriólogo selecciona paciente
- Retorna a paso 4

**Flujos de Excepción:**

**FE-001:** Error de Validación
- 7a. Sistema detecta datos inválidos (ej: peso negativo)
- 7b. Sistema muestra mensaje de error específico
- 7c. Sistema resalta campos con error
- Retorna a paso 5

**FE-002:** Error de Conexión
- 7a. Falla conexión a base de datos
- 7b. Sistema muestra mensaje de error
- 7c. Sistema guarda datos en cache local (localStorage)
- 7d. Sistema reintenta envío cuando se restaura conexión
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** CURP debe ser válido si se proporciona
- **RN-002:** Edad se calcula automáticamente desde fecha de nacimiento
- **RN-003:** IMC se calcula automáticamente (peso/talla²)
- **RN-004:** Datos modificados deben registrarse en auditoría
- **RN-005:** Pacientes no pueden modificar su propio expediente

**Requerimientos Especiales:**

- **RE-001:** Cumplimiento NOM-004-SSA3-2012 (expediente clínico)
- **RE-002:** Encriptación de datos sensibles en BD
- **RE-003:** Retención de datos: 7 años mínimo
- **RE-004:** Interfaz responsive (móvil/tablet/escritorio)

---

### 4.2 Módulo: Datos de Laboratorio

#### CU-002: Analizar Datos de Laboratorio con IA

**ID:** CU-002
**Actor Principal:** Nutriólogo
**Actores Secundarios:** Google Gemini API

**Descripción:**
Permite ingresar y analizar datos de laboratorio del paciente (40+ parámetros), con interpretación automática mediante IA que genera alertas y diagnósticos preliminares.

**Precondiciones:**
- Expediente del paciente existe
- Usuario autenticado como Nutriólogo

**Postcondiciones:**
- Datos de laboratorio almacenados
- Interpretación IA generada y guardada
- Alertas creadas para valores fuera de rango

**Flujo Principal:**

1. Nutriólogo accede a "Laboratorio" dentro del expediente
2. Sistema muestra lista de estudios de laboratorio previos
3. Nutriólogo selecciona "Nuevo Estudio"
4. Sistema muestra formulario con 40+ parámetros organizados por categorías:
   - Química Sanguínea (glucosa, urea, creatinina, etc.)
   - Perfil de Lípidos (colesterol, triglicéridos, HDL, LDL)
   - Hematología Completa (hemoglobina, leucocitos, plaquetas)
   - Función Hepática (ALT, AST, bilirrubinas)
   - Función Renal (creatinina, urea, TFG)
   - Electrolitos (sodio, potasio, cloro)
   - Otros (HbA1c, proteína C reactiva, etc.)
5. Nutriólogo ingresa valores de laboratorio
6. Sistema valida rangos de referencia en tiempo real
7. Nutriólogo marca estudio como "ayunas" o "postprandial" (si aplica)
8. Nutriólogo guarda estudio
9. Sistema envía datos a IA (Gemini) para interpretación
10. IA analiza valores y genera:
    - Lista de valores fuera de rango
    - Índices calculados (HOMA-IR, índice aterogénico, TFG)
    - Diagnósticos preliminares
    - Recomendaciones nutricionales
11. Sistema muestra interpretación IA al nutriólogo
12. Nutriólogo revisa y puede editar interpretación
13. Sistema guarda interpretación final
14. Sistema genera PDF del estudio con interpretación

**Flujos Alternos:**

**FA-001:** Importar desde PDF/Imagen (OCR)
- 3a. Nutriólogo selecciona "Importar desde archivo"
- 3b. Sistema muestra diálogo de carga
- 3c. Nutriólogo sube PDF o imagen de laboratorio
- 3d. Sistema procesa con OCR (Tesseract/Google Vision)
- 3e. Sistema extrae valores y pobla formulario
- 3f. Nutriólogo revisa y corrige valores extraídos
- Retorna a paso 6

**FA-002:** Copiar Estudio Previo
- 3a. Nutriólogo selecciona estudio previo
- 3b. Nutriólogo selecciona "Duplicar"
- 3c. Sistema copia valores como plantilla
- 3d. Nutriólogo actualiza valores modificados
- Retorna a paso 6

**Flujos de Excepción:**

**FE-001:** Valores Críticos Detectados
- 6a. Sistema detecta valor crítico (ej: glucosa >400 mg/dL)
- 6b. Sistema muestra alerta visual prominente
- 6c. Sistema requiere confirmación explícita del nutriólogo
- 6d. Sistema marca estudio con bandera crítica
- 6e. (Opcional) Sistema envía notificación al paciente
- Retorna a paso 7

**FE-002:** Falla de IA
- 9a. API de Gemini no responde o retorna error
- 9b. Sistema registra error en logs
- 9c. Sistema muestra mensaje al usuario
- 9d. Sistema permite guardar sin interpretación IA
- 9e. Sistema agenda reintento automático
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** Glucosa en ayunas >126 mg/dL sugiere diabetes
- **RN-002:** HbA1c >6.5% sugiere diabetes
- **RN-003:** HOMA-IR se calcula: (Glucosa × Insulina) / 405
- **RN-004:** Índice aterogénico: Colesterol Total / HDL
- **RN-005:** TFG se estima con ecuación CKD-EPI
- **RN-006:** Valores críticos requieren confirmación

**Interfaz:**
```
┌────────────────────────────────────────────────────────────┐
│ Laboratorio - Nuevo Estudio                                │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Fecha del estudio: [15/01/2025]  Ayunas: [✓]             │
│                                                             │
│  ┌─── Química Sanguínea ─────────────────────────────┐    │
│  │ Glucosa:        [95] mg/dL   Rango: 70-100        │    │
│  │ Urea:           [30] mg/dL   Rango: 10-50    ✓    │    │
│  │ Creatinina:     [0.9] mg/dL  Rango: 0.6-1.2       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─── Perfil de Lípidos ──────────────────────────────┐    │
│  │ Colesterol:     [185] mg/dL  Rango: <200           │    │
│  │ Triglicéridos:  [110] mg/dL  Rango: <150      ✓    │    │
│  │ HDL:            [55] mg/dL   Rango: >40            │    │
│  │ LDL:            [108] mg/dL  Rango: <100      ⚠    │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  [Guardar y Analizar con IA]  [Cancelar]                  │
└────────────────────────────────────────────────────────────┘
```

---

### 4.3 Módulo: Archivos Clínicos (OCR)

#### CU-003: Subir y Analizar Archivos Clínicos con OCR

**ID:** CU-003
**Actor Principal:** Nutriólogo
**Actores Secundarios:** Tesseract OCR, PyMuPDF, Google Vision API

**Descripción:**
Permite subir documentos clínicos en PDF o imagen, extraer texto automáticamente con OCR, y almacenar en el expediente del paciente con búsqueda de texto completo.

**Precondiciones:**
- Expediente del paciente existe
- Usuario autenticado como Nutriólogo
- Archivo a subir es PDF o imagen (JPG/PNG)

**Postcondiciones:**
- Archivo almacenado en sistema
- Texto extraído con OCR
- Archivo vinculado al expediente
- Texto indexado para búsqueda

**Flujo Principal:**

1. Nutriólogo accede a "Archivos Clínicos" en expediente
2. Sistema muestra lista de archivos previamente subidos
3. Nutriólogo selecciona "Subir Nuevo Archivo"
4. Sistema muestra diálogo de carga con drag & drop
5. Nutriólogo selecciona tipo de documento:
   - Estudio de Laboratorio
   - Estudio de Imagen (Rayos X, Ultrasonido)
   - Receta Médica
   - Informe Médico
   - Consentimiento Informado
   - Otro
6. Nutriólogo arrastra archivo o selecciona desde explorador
7. Sistema valida:
   - Formato de archivo (PDF, JPG, PNG)
   - Tamaño máximo (10 MB)
   - No es archivo corrupto
8. Sistema muestra preview del archivo
9. Nutriólogo confirma y presiona "Procesar"
10. Sistema procesa archivo:
    - 10.1. Si es PDF: Extrae texto con PyMuPDF
    - 10.2. Si es imagen: Aplica OCR con Tesseract
    - 10.3. Si OCR tiene baja confianza: Usa Google Vision API como fallback
11. Sistema muestra texto extraído en panel editable
12. Nutriólogo revisa y corrige texto si es necesario
13. Nutriólogo agrega notas adicionales (opcional)
14. Nutriólogo guarda archivo
15. Sistema:
    - Almacena archivo original
    - Almacena texto extraído
    - Indexa texto para búsqueda
    - Vincula a expediente del paciente
16. Sistema muestra confirmación de éxito

**Flujos Alternos:**

**FA-001:** Múltiples Archivos
- 6a. Nutriólogo arrastra múltiples archivos
- 6b. Sistema muestra lista de archivos en cola
- 6c. Sistema procesa archivos secuencialmente
- 6d. Sistema muestra progreso global
- Retorna a paso 16

**FA-002:** Búsqueda en Archivos
- 1a. Nutriólogo usa barra de búsqueda en vista de archivos
- 1b. Sistema busca en texto extraído de todos los archivos
- 1c. Sistema muestra archivos coincidentes con highlights
- 1d. Nutriólogo selecciona archivo para ver
- Fin del caso de uso

**Flujos de Excepción:**

**FE-001:** Archivo No Válido
- 7a. Sistema detecta formato no soportado
- 7b. Sistema muestra mensaje de error
- 7c. Sistema lista formatos aceptados
- Retorna a paso 6

**FE-002:** OCR Falla Completamente
- 10a. OCR no puede extraer texto legible
- 10b. Sistema notifica al usuario
- 10c. Sistema guarda archivo sin texto extraído
- 10d. Sistema permite agregar texto manualmente
- Retorna a paso 14

**FE-003:** Archivo Muy Grande
- 7a. Archivo excede 10 MB
- 7b. Sistema muestra mensaje de error
- 7c. Sistema sugiere comprimir o dividir archivo
- Retorna a paso 6

**Reglas de Negocio:**

- **RN-001:** Formatos soportados: PDF, JPG, JPEG, PNG
- **RN-002:** Tamaño máximo: 10 MB por archivo
- **RN-003:** Archivos se almacenan encriptados
- **RN-004:** Archivos se vinculan permanentemente al paciente
- **RN-005:** Solo nutriólogo asignado puede eliminar archivos
- **RN-006:** Texto extraído debe ser editable post-OCR

**Interfaz:**
```
┌────────────────────────────────────────────────────────────┐
│ Archivos Clínicos - Paciente: María Hernández              │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  [📤 Subir Nuevo Archivo]  [🔍 Buscar en archivos...]     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 📄 Laboratorio_15-01-2025.pdf                        │  │
│  │    Tipo: Estudio de Laboratorio                      │  │
│  │    Fecha: 15/01/2025  Tamaño: 2.3 MB                │  │
│  │    Texto extraído: "Química sanguínea completa..."   │  │
│  │    [Ver] [Descargar] [Eliminar]                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 📷 Ultrasonido_abdominal.jpg                         │  │
│  │    Tipo: Estudio de Imagen                           │  │
│  │    Fecha: 10/01/2025  Tamaño: 1.8 MB                │  │
│  │    Texto extraído: "Hígado de morfología normal..."  │  │
│  │    [Ver] [Descargar] [Eliminar]                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

### 4.4 Módulo: Mensajería WhatsApp

#### CU-004: Enviar Mensajes WhatsApp a Pacientes

**ID:** CU-004
**Actor Principal:** Nutriólogo
**Actores Secundarios:** Twilio WhatsApp API, Paciente

**Descripción:**
Permite enviar mensajes y recordatorios a pacientes vía WhatsApp, incluyendo recordatorios de citas, notificaciones de plan listo, mensajes motivacionales y seguimiento personalizado.

**Precondiciones:**
- Usuario autenticado como Nutriólogo
- Paciente tiene número de teléfono registrado
- Twilio WhatsApp configurado en .env

**Postcondiciones:**
- Mensaje enviado a WhatsApp del paciente
- Historial de mensaje registrado en BD
- Estado de entrega rastreado

**Flujo Principal:**

1. Nutriólogo accede a "WhatsApp Manager" desde menú
2. Sistema muestra dos tabs: "Enviar Mensajes" y "Historial"
3. Sistema muestra acciones rápidas predefinidas:
   - 🗓️ Recordatorio de Cita
   - 📋 Plan de Alimentación Listo
   - 💪 Mensaje Motivacional
   - 👋 Seguimiento General
   - ✉️ Mensaje Personalizado
4. Nutriólogo selecciona tipo de mensaje
5. Sistema muestra formulario con:
   - Paciente (selector con búsqueda)
   - Teléfono (auto-completado desde expediente)
   - Plantilla de mensaje (editable)
   - Variables dinámicas ({nombre}, {fecha_cita}, {nutriologo})
6. Nutriólogo personaliza mensaje si es necesario
7. Nutriólogo presiona "Enviar"
8. Sistema valida:
   - Teléfono en formato válido (+52...)
   - Mensaje no vacío
   - Paciente existe
9. Sistema envía mensaje a Twilio API
10. Twilio procesa y envía vía WhatsApp
11. Sistema recibe confirmación de Twilio (SID del mensaje)
12. Sistema guarda registro en tabla `whatsapp_messages`:
    - ID del paciente
    - Tipo de mensaje
    - Cuerpo del mensaje
    - Teléfono destinatario
    - Twilio SID
    - Estado: 'sent'
    - Timestamp
13. Sistema muestra confirmación: "✅ Mensaje enviado exitosamente"
14. Sistema actualiza contador de mensajes enviados

**Flujos Alternos:**

**FA-001:** Programar Mensaje para Envío Futuro
- 7a. Nutriólogo selecciona "Programar envío"
- 7b. Sistema muestra selector de fecha/hora
- 7c. Nutriólogo elige fecha y hora futura
- 7d. Sistema guarda mensaje con estado 'scheduled'
- 7e. Job programado enviará mensaje en fecha indicada
- Fin del caso de uso

**FA-002:** Enviar a Múltiples Pacientes
- 4a. Nutriólogo selecciona "Envío Masivo"
- 4b. Sistema muestra selector múltiple de pacientes
- 4c. Nutriólogo selecciona pacientes (con filtros)
- 4d. Sistema muestra confirmación de cantidad
- 4e. Sistema envía mensajes secuencialmente
- Retorna a paso 13

**FA-003:** Ver Historial de Mensajes
- 2a. Nutriólogo selecciona tab "Historial"
- 2b. Sistema muestra tabla de mensajes enviados:
   - Paciente
   - Tipo de mensaje
   - Fecha/Hora
   - Estado (Sent/Delivered/Read/Failed)
   - Twilio SID
- 2c. Nutriólogo puede filtrar por paciente, fecha o estado
- Fin del caso de uso

**Flujos de Excepción:**

**FE-001:** Teléfono Inválido
- 8a. Sistema detecta formato de teléfono inválido
- 8b. Sistema muestra mensaje de error
- 8c. Sistema sugiere formato correcto (+52...)
- Retorna a paso 6

**FE-002:** Falla de Twilio
- 9a. API de Twilio retorna error
- 9b. Sistema captura error y guarda en logs
- 9c. Sistema muestra mensaje de error al usuario
- 9d. Sistema guarda mensaje con estado 'failed'
- 9e. Sistema permite reintentar envío
- Fin del caso de uso

**FE-003:** Límite de Mensajes Excedido
- 9a. Twilio retorna error de límite excedido
- 9b. Sistema muestra mensaje explicativo
- 9c. Sistema sugiere esperar o actualizar plan de Twilio
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** Formato de teléfono: +52 (10 dígitos)
- **RN-002:** Mensajes máximo 1600 caracteres
- **RN-003:** Solo nutriólogo puede enviar mensajes
- **RN-004:** Paciente puede responder (respuestas se registran)
- **RN-005:** Mensajes se archivan por 90 días mínimo
- **RN-006:** Modo sandbox usa números de prueba de Twilio

**Plantillas de Mensajes:**

**Recordatorio de Cita:**
```
¡Hola {nombre_paciente}! 👋

Te recordamos tu cita de nutrición:
📅 Fecha: {fecha_cita}
🕐 Hora: {hora_cita}
👩‍⚕️ Nutrióloga: {nombre_nutriologo}

Por favor, asiste puntual. Si necesitas reagendar, avísanos con anticipación.

¡Te esperamos! 🥗
```

**Plan Listo:**
```
¡Hola {nombre_paciente}! 🎉

Tu plan de alimentación personalizado ya está listo.

Puedes consultarlo en tu plataforma Nutrition Intelligence.

Si tienes dudas, ¡no dudes en contactarme!

{nombre_nutriologo}
Nutrióloga 🥗
```

---

### 4.5 Módulo: Generador de Dietas

#### CU-005: Generar Plan de Alimentación Personalizado

**ID:** CU-005
**Actor Principal:** Nutriólogo
**Actores Secundarios:** Sistema SMAE

**Descripción:**
Permite generar planes de alimentación personalizados basados en requerimientos nutricionales, preferencias del paciente, y equivalencias del Sistema Mexicano de Alimentos Equivalentes (SMAE).

**Precondiciones:**
- Expediente del paciente existe
- Datos antropométricos disponibles (peso, talla)
- Usuario autenticado como Nutriólogo

**Postcondiciones:**
- Plan de alimentación generado
- PDF del plan disponible para descarga
- Plan almacenado en expediente

**Flujo Principal:**

1. Nutriólogo accede a "Generador de Dietas"
2. Nutriólogo selecciona paciente
3. Sistema carga datos del paciente:
   - Peso, talla, edad, sexo
   - Actividad física
   - Objetivos (bajar/subir peso, mantener)
   - Patologías (diabetes, hipertensión, etc.)
4. Sistema muestra "Calculadora de Requerimientos"
5. Nutriólogo selecciona fórmula de cálculo:
   - Harris-Benedict
   - Mifflin-St Jeor (recomendada)
   - FAO/OMS
6. Sistema calcula GET (Gasto Energético Total)
7. Sistema aplica factor de actividad física
8. Sistema ajusta por objetivo (déficit/superávit calórico)
9. Sistema muestra distribución de macronutrientes:
   - Proteínas: 15-20% (ajustable)
   - Lípidos: 25-30% (ajustable)
   - Carbohidratos: 50-60% (ajustable)
10. Nutriólogo ajusta distribución si es necesario
11. Nutriólogo especifica preferencias:
    - Alimentos a evitar (alergias, intolerancias)
    - Alimentos preferidos
    - Tiempos de comida (3-6 comidas al día)
12. Nutriólogo presiona "Generar Plan"
13. Sistema consulta base de datos SMAE
14. Sistema genera plan con equivalencias:
    - Desayuno
    - Colación 1 (opcional)
    - Comida
    - Colación 2 (opcional)
    - Cena
15. Sistema muestra plan generado con:
    - Lista de alimentos por tiempo de comida
    - Cantidades en gramos y equivalencias
    - Aporte nutricional por tiempo
    - Totales del día
16. Nutriólogo revisa y puede:
    - Modificar alimentos
    - Ajustar cantidades
    - Agregar notas
17. Nutriólogo guarda plan
18. Sistema genera PDF profesional
19. Sistema almacena en expediente
20. Sistema permite enviar por WhatsApp (opcional)

**Flujos Alternos:**

**FA-001:** Usar Plantilla Predefinida
- 12a. Nutriólogo selecciona "Usar Plantilla"
- 12b. Sistema muestra plantillas disponibles:
   - Plan para diabetes
   - Plan para hipertensión
   - Plan vegetariano
   - Plan para deportistas
- 12c. Nutriólogo selecciona plantilla
- 12d. Sistema adapta plantilla a requerimientos del paciente
- Retorna a paso 15

**FA-002:** Clonar Plan Previo
- 2a. Nutriólogo selecciona plan previo del paciente
- 2b. Nutriólogo presiona "Clonar"
- 2c. Sistema copia plan como base
- 2d. Nutriólogo modifica según necesidad
- Retorna a paso 17

**Flujos de Excepción:**

**FE-001:** Datos Insuficientes
- 3a. Faltan datos antropométricos
- 3b. Sistema muestra mensaje de error
- 3c. Sistema redirige a expediente para completar datos
- Fin del caso de uso

**FE-002:** Combinación Imposible
- 14a. Sistema no puede generar plan con restricciones dadas
- 14b. Sistema muestra mensaje explicativo
- 14c. Sistema sugiere relajar algunas restricciones
- Retorna a paso 11

**Reglas de Negocio:**

- **RN-001:** Calorías mínimas: 1200 kcal/día
- **RN-002:** Proteína mínima: 0.8 g/kg peso
- **RN-003:** Distribución por defecto: 55% CHO, 15% PROT, 30% LIP
- **RN-004:** Usar equivalencias mexicanas (SMAE)
- **RN-005:** PDF incluye logotipo y datos del nutriólogo

---

### 4.6 Módulo: Análisis de Fotos con IA

#### CU-006: Analizar Foto de Alimento con IA

**ID:** CU-006
**Actor Principal:** Paciente, Nutriólogo
**Actores Secundarios:** Google Gemini, Anthropic Claude

**Descripción:**
Permite subir foto de un plato de comida y obtener análisis nutricional automático usando IA (Gemini o Claude), identificando alimentos, porciones y aporte nutricional estimado.

**Precondiciones:**
- Usuario autenticado (Paciente o Nutriólogo)
- Foto clara de alimento
- API de IA configurada

**Postcondiciones:**
- Foto almacenada
- Análisis IA generado
- Información nutricional disponible

**Flujo Principal:**

1. Usuario accede a "Análisis de Fotos IA"
2. Sistema muestra interfaz de carga con:
   - Drag & drop para foto
   - Botón de cámara (en móvil)
   - Selector de modelo IA:
     * Gemini (rápido, económico)
     * Claude (preciso, más caro)
     * Híbrido (Gemini primero, Claude si baja confianza)
3. Usuario selecciona o captura foto
4. Sistema valida:
   - Formato de imagen (JPG, PNG, HEIC)
   - Tamaño máximo (5 MB)
   - Imagen contiene contenido visible
5. Sistema muestra preview de foto
6. Usuario confirma "Analizar"
7. Sistema comprime imagen si es necesaria
8. Sistema envía a API de IA seleccionada con prompt:
   ```
   Analiza esta foto de alimento mexicano y proporciona:
   1. Lista de alimentos identificados
   2. Porción estimada de cada uno (en gramos)
   3. Aporte nutricional total (kcal, proteínas, carbohidratos, lípidos)
   4. Si es un platillo tradicional mexicano, identifícalo
   5. Nivel de confianza del análisis (%)
   ```
9. IA procesa imagen y retorna análisis JSON
10. Sistema parsea respuesta y extrae:
    - Alimentos detectados
    - Porciones
    - Calorías totales
    - Macronutrientes
    - Confianza del análisis
11. Si modo híbrido Y confianza <75%:
    - 11a. Sistema reenvía a Claude para mejor análisis
    - 11b. Sistema usa resultado de Claude
12. Sistema muestra resultado visual:
    - Foto original
    - Lista de alimentos con íconos
    - Tabla nutricional
    - Gráfica de macronutrientes
    - Badge de confianza
13. Usuario puede:
    - Guardar análisis en recordatorio 24h
    - Descargar resultado como PDF
    - Compartir con nutriólogo
14. Sistema guarda en historial del usuario

**Flujos Alternos:**

**FA-001:** Modo Comparación
- 6a. Usuario selecciona "Comparar con mi plan"
- 6b. Sistema carga plan de alimentación del día
- 6c. Sistema compara análisis de foto con plan
- 6d. Sistema muestra diferencias (exceso/déficit)
- Retorna a paso 13

**FA-002:** Múltiples Fotos (Comida Completa)
- 3a. Usuario sube múltiples fotos (plato + bebida + postre)
- 3b. Sistema analiza cada foto independientemente
- 3c. Sistema suma aportes nutricionales
- 3d. Sistema muestra análisis combinado
- Retorna a paso 13

**Flujos de Excepción:**

**FE-001:** Foto No Clara
- 8a. IA retorna confianza <30%
- 8b. Sistema muestra mensaje: "Foto poco clara"
- 8c. Sistema sugiere:
   - Mejor iluminación
   - Acercar cámara
   - Foto desde arriba
- 8d. Sistema permite reintentar
- Fin del caso de uso

**FE-002:** Falla de API
- 8a. API de IA no responde (timeout/error)
- 8b. Sistema registra error en logs
- 8c. Si es modo híbrido: intenta con otro modelo
- 8d. Sistema muestra mensaje de error al usuario
- 8e. Sistema guarda foto para análisis posterior
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** Gemini: $0.35 por 1M tokens (económico)
- **RN-002:** Claude: $3.00 por 1M tokens (preciso)
- **RN-003:** Híbrido ahorra 85% vs solo Claude
- **RN-004:** Confianza <75% → usar modelo más potente
- **RN-005:** Fotos se almacenan 30 días
- **RN-006:** Análisis se guarda permanentemente

---

### 4.7 Módulo: Gamificación Mexicana

#### CU-007: Usar Sistema de Gamificación

**ID:** CU-007
**Actor Principal:** Paciente
**Actores Secundarios:** Nutriólogo (observa progreso)

**Descripción:**
Permite a pacientes ganar puntos, insignias y logros por cumplir metas nutricionales, crear un sistema motivacional basado en cultura mexicana.

**Precondiciones:**
- Usuario autenticado como Paciente
- Paciente tiene plan de alimentación activo

**Postcondiciones:**
- Puntos otorgados
- Logros desbloqueados
- Nivel actualizado

**Flujo Principal:**

1. Paciente accede a "Gamificación"
2. Sistema muestra dashboard gamificado:
   - Puntos totales (XP)
   - Nivel actual (Guerrero Azteca, Sabio Maya, etc.)
   - Barra de progreso a siguiente nivel
   - Racha de días consecutivos
3. Sistema muestra secciones:
   - 🏆 Logros Desbloqueados
   - 🎯 Metas Semanales
   - 📊 Estadísticas
   - 🎁 Recompensas
4. Sistema lista logros disponibles:
   - **Inicio del Viaje** - Completar primer día (10 pts)
   - **Guerrero del Nopal** - Comer nopal 5 veces (50 pts)
   - **Maestro del Maíz** - Incluir maíz 10 veces (100 pts)
   - **Guardián del Agua** - 8 vasos de agua por 7 días (150 pts)
   - **Racha de Fuego** - 30 días consecutivos (500 pts)
5. Paciente registra actividad:
   - Completar comida del plan
   - Registrar ejercicio
   - Tomar agua
   - Subir foto de alimento
6. Sistema valida cumplimiento
7. Sistema otorga puntos según actividad:
   - Comida completa: +20 pts
   - Ejercicio 30min: +30 pts
   - 2L agua: +10 pts
   - Foto subida: +15 pts
8. Sistema verifica si se desbloqueó logro
9. Si logro desbloqueado:
   - Sistema muestra animación celebratoria
   - Sistema otorga insignia virtual
   - Sistema guarda en perfil del paciente
   - Sistema notifica a nutriólogo (opcional)
10. Sistema actualiza nivel si se alcanzó XP necesario
11. Sistema muestra mensaje de felicitación

**Niveles del Sistema:**
```
1. Novato Nahual         (0-100 XP)
2. Aprendiz Azteca       (101-300 XP)
3. Guerrero del Nopal    (301-600 XP)
4. Sabio Maya            (601-1000 XP)
5. Guardián de la Milpa  (1001-1500 XP)
6. Maestro de Salud      (1501+ XP)
```

**Flujos Alternos:**

**FA-001:** Compartir Logro
- 9a. Paciente selecciona logro desbloqueado
- 9b. Paciente presiona "Compartir"
- 9c. Sistema genera imagen con logro
- 9d. Sistema permite compartir en redes sociales
- Fin del caso de uso

**FA-002:** Competencia con Otros Pacientes
- 2a. Paciente accede a "Tabla de Líderes"
- 2b. Sistema muestra ranking semanal/mensual
- 2c. Sistema muestra solo posiciones relativas (privacidad)
- 2d. Paciente ve su posición
- Fin del caso de uso

**Flujos de Excepción:**

**FE-001:** Trampa Detectada
- 6a. Sistema detecta patrón inusual (100 actividades en 1 hora)
- 6b. Sistema marca para revisión
- 6c. Sistema notifica a nutriólogo
- 6d. Sistema no otorga puntos hasta validación
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** Puntos no son transferibles
- **RN-002:** Logros permanecen una vez desbloqueados
- **RN-003:** Racha se rompe si falta 1 día completo
- **RN-004:** Máximo 200 puntos por día (anti-spam)
- **RN-005:** Tema mexicano en todos los logros

---

### 4.8 Módulo: Chat con Nutriólogo IA

#### CU-008: Chatear con Nutriólogo Virtual

**ID:** CU-008
**Actor Principal:** Paciente
**Actores Secundarios:** Anthropic Claude API

**Descripción:**
Permite a pacientes hacer preguntas nutricionales a un chatbot con IA (Claude) que responde basándose en datos del paciente y conocimiento nutricional profesional.

**Precondiciones:**
- Usuario autenticado como Paciente
- Claude API configurada

**Postcondiciones:**
- Conversación registrada
- Respuesta IA generada
- Historial de chat almacenado

**Flujo Principal:**

1. Paciente accede a "Chat Nutriólogo IA"
2. Sistema muestra interfaz de chat estilo WhatsApp
3. Sistema carga contexto del paciente:
   - Plan de alimentación activo
   - Alergias/intolerancias
   - Objetivos nutricionales
   - Historial de consultas previas (últimas 10)
4. Sistema muestra mensaje de bienvenida:
   ```
   ¡Hola! Soy tu asistente nutricional virtual.
   Puedo ayudarte con dudas sobre tu plan de alimentación,
   recetas saludables, equivalencias de alimentos, y más.
   ¿En qué puedo ayudarte hoy?
   ```
5. Paciente escribe pregunta (texto o voz)
6. Sistema valida pregunta:
   - No está vacía
   - No contiene lenguaje inapropiado
   - Es relacionada con nutrición
7. Sistema envía a Claude API con prompt estructurado:
   ```
   Eres un asistente nutricional profesional mexicano.
   Contexto del paciente:
   - Plan: {plan_alimentacion}
   - Alergias: {alergias}
   - Objetivo: {objetivo}

   Pregunta: {pregunta_paciente}

   Responde de forma clara, amigable y profesional.
   Usa referencias mexicanas cuando sea apropiado.
   Si la pregunta es médica crítica, recomienda consultar al nutriólogo.
   ```
8. Claude procesa y genera respuesta
9. Sistema recibe respuesta y la valida:
   - No contiene información médica peligrosa
   - Es apropiada y profesional
   - Está en español
10. Sistema muestra respuesta en interfaz de chat
11. Sistema ofrece opciones de seguimiento:
    - "¿Necesitas más detalles?"
    - "¿Otra pregunta?"
    - "Agendar consulta con nutriólogo"
12. Sistema guarda conversación en BD
13. Si paciente hace pregunta crítica (ej: "tengo dolor fuerte"):
    - Sistema prioriza respuesta
    - Sistema sugiere contactar nutriólogo real
    - Sistema notifica a nutriólogo (alerta)

**Ejemplos de Preguntas:**

```
Paciente: "¿Puedo sustituir el pollo por pescado en mi cena?"
IA: "¡Claro que sí! El pescado es una excelente fuente de proteína.
Puedes sustituir 100g de pechuga de pollo por 120g de pescado blanco
(como tilapia o robalo). Esto te dará proteínas similares y además
ácidos grasos omega-3. ¿Te gustaría una receta de pescado al horno? 🐟"
```

```
Paciente: "¿Cuántas tortillas puedo comer al día?"
IA: "Según tu plan de alimentación, tienes asignadas 6 tortillas
de maíz al día (distribuidas en comidas). Cada tortilla equivale
a 1 porción de cereales. Puedes comerlas en desayuno, comida y cena.
Recuerda que las tortillas de maíz son parte importante de nuestra
cultura alimentaria mexicana. 🌮"
```

**Flujos Alternos:**

**FA-001:** Entrada por Voz
- 5a. Paciente presiona botón de micrófono
- 5b. Sistema graba audio
- 5c. Sistema convierte a texto (Speech-to-Text)
- 5d. Sistema muestra texto transcrito
- 5e. Paciente confirma o edita
- Retorna a paso 6

**FA-002:** Sugerencia de Receta
- 8a. Respuesta de IA incluye receta
- 8b. Sistema formatea receta con:
   - Ingredientes (con cantidades)
   - Preparación paso a paso
   - Información nutricional
- 8c. Sistema ofrece guardar receta
- Retorna a paso 11

**Flujos de Excepción:**

**FE-001:** Pregunta Fuera de Scope
- 6a. Sistema detecta pregunta no relacionada con nutrición
- 6b. Sistema responde amablemente:
   ```
   Lo siento, solo puedo ayudarte con temas de nutrición
   y alimentación. ¿Tienes alguna pregunta sobre tu plan
   alimenticio o recetas saludables?
   ```
- Retorna a paso 5

**FE-002:** Falla de API
- 8a. Claude API no responde
- 8b. Sistema muestra mensaje:
   ```
   Disculpa, estoy teniendo problemas técnicos.
   ¿Podrías intentar de nuevo en un momento?
   Mientras tanto, puedes consultar tu plan de alimentación.
   ```
- Sistema registra error para análisis
- Fin del caso de uso

**Reglas de Negocio:**

- **RN-001:** No sustituye consulta con nutriólogo real
- **RN-002:** Conversaciones privadas y encriptadas
- **RN-003:** No dar diagnósticos médicos
- **RN-004:** Recomendar consulta profesional si es necesario
- **RN-005:** Respuestas basadas en evidencia científica
- **RN-006:** Máximo 50 mensajes por día por usuario

---

## 5. Flujos Detallados

### 5.1 Flujo Completo: Consulta Nutricional Integral

Este flujo muestra cómo se integran múltiples casos de uso en una consulta real:

```
1. PREPARACIÓN (Nutriólogo)
   ├─► Revisar expediente del paciente (CU-001)
   ├─► Consultar datos de laboratorio previos (CU-002)
   └─► Revisar archivos clínicos (CU-003)

2. CONSULTA INICIAL
   ├─► Actualizar mediciones antropométricas
   ├─► Registrar signos vitales
   ├─► Actualizar historia clínica
   └─► Subir nuevos estudios de laboratorio (CU-002)

3. ANÁLISIS
   ├─► IA interpreta laboratorios (CU-002)
   ├─► Nutriólogo revisa interpretación
   └─► Nutriólogo define objetivos

4. PLAN DE ALIMENTACIÓN
   ├─► Calcular requerimientos (CU-005)
   ├─► Generar plan personalizado (CU-005)
   ├─► Revisar y ajustar plan
   └─► Exportar PDF del plan

5. SEGUIMIENTO
   ├─► Enviar plan por WhatsApp (CU-004)
   ├─► Programar recordatorio de seguimiento (CU-004)
   └─► Paciente activa gamificación (CU-007)

6. MONITOREO CONTINUO
   ├─► Paciente sube fotos de alimentos (CU-006)
   ├─► Paciente hace preguntas a IA (CU-008)
   ├─► Paciente gana puntos por cumplimiento (CU-007)
   └─► Nutriólogo monitorea progreso
```

---

## 6. Matriz de Trazabilidad

### 6.1 Casos de Uso vs. Requisitos Funcionales

| Caso de Uso | Req. Funcional | Prioridad | Estado |
|-------------|----------------|-----------|--------|
| CU-001 | RF-001: Gestión de expedientes | Alta | ✅ Implementado |
| CU-002 | RF-002: Análisis de laboratorio con IA | Alta | ✅ Implementado |
| CU-003 | RF-003: OCR de archivos clínicos | Media | ✅ Implementado |
| CU-004 | RF-004: Mensajería WhatsApp | Alta | ✅ Implementado |
| CU-005 | RF-005: Generador de dietas | Alta | ✅ Implementado |
| CU-006 | RF-006: Análisis de fotos con IA | Alta | ✅ Implementado |
| CU-007 | RF-007: Gamificación mexicana | Media | ✅ Implementado |
| CU-008 | RF-008: Chat nutriólogo IA | Media | ✅ Implementado |

### 6.2 Casos de Uso vs. Actores

|Caso de Uso|Nutriólogo|Paciente|Admin|
|-----------|:--------:|:------:|:---:|
| CU-001 | ✅ | 👁️ | ❌ |
| CU-002 | ✅ | ❌ | ❌ |
| CU-003 | ✅ | ❌ | ❌ |
| CU-004 | ✅ | 📩 | ❌ |
| CU-005 | ✅ | 👁️ | ❌ |
| CU-006 | ✅ | ✅ | ❌ |
| CU-007 | 👁️ | ✅ | ❌ |
| CU-008 | 👁️ | ✅ | ❌ |

**Leyenda:**
- ✅ Actor principal
- 👁️ Solo consulta
- 📩 Recibe notificaciones
- ❌ Sin acceso

---

## 📝 Control de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | 2025-01-15 | Arquitectura | Versión inicial - Fase 2 completa |

---

**Fin del Documento - Casos de Uso**
