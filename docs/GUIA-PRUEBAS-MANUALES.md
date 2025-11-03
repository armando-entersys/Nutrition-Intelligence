# Guía de Pruebas Manuales - Nutrition Intelligence

## Sistema de Pruebas Colaborativo E2E

**Versión:** 1.0.0
**Fecha:** Enero 2025
**Total de Casos:** 13 pruebas manuales
**Participantes:** Área Técnica, Área Funcional, Nutriólogos, Pacientes

---

## 📋 Índice

1. [Introducción](#1-introducción)
2. [Roles y Responsabilidades](#2-roles-y-responsabilidades)
3. [Acceso al Dashboard de Pruebas](#3-acceso-al-dashboard-de-pruebas)
4. [Casos de Prueba Manuales](#4-casos-de-prueba-manuales)
5. [Cómo Ejecutar una Prueba](#5-cómo-ejecutar-una-prueba)
6. [Cómo Reportar Resultados](#6-cómo-reportar-resultados)
7. [FAQs](#7-faqs)

---

## 1. Introducción

### 1.1 Propósito

Esta guía describe cómo ejecutar las **13 pruebas manuales** del sistema Nutrition Intelligence Platform. Estas pruebas complementan las 2 pruebas automatizadas (E2E-001 y E2E-002) y requieren intervención humana para validar la experiencia de usuario real.

### 1.2 Casos Automatizados vs. Manuales

| Tipo | Cantidad | Casos | Ejecutor |
|------|----------|-------|----------|
| **Automatizadas** | 2 | E2E-001, E2E-002 | Sistema (chrome-devtools-mcp) |
| **Manuales** | 13 | E2E-003 a E2E-AI-005 | Humanos (siguiendo esta guía) |
| **Total** | 15 | - | - |

---

## 2. Roles y Responsabilidades

### 👨‍💻 Área Técnica (QA)
**Responsable:** Validar aspectos técnicos, performance, seguridad

**Casos Asignados:**
- E2E-004: Datos de Laboratorio
- E2E-WA-004: Historial de Mensajes WhatsApp
- E2E-WA-005: Configuración Twilio
- E2E-AI-003: Configuración IA (Gemini/Claude)

**Tareas:**
- Ejecutar caso de prueba según script
- Verificar tiempos de respuesta
- Validar integraciones con APIs externas
- Reportar bugs técnicos con logs
- Agregar comentarios en Dashboard de Pruebas

---

### 📋 Área Funcional (Analistas)
**Responsable:** Validar flujos de negocio, usabilidad, cumplimiento de requisitos

**Casos Asignados:**
- E2E-WA-002: Mensajes Rápidos WhatsApp
- E2E-AI-001: Navegación Análisis de Fotos
- E2E-AI-005: Accesibilidad

**Tareas:**
- Validar que los flujos cumplen requisitos funcionales
- Verificar mensajes y textos en español correcto
- Validar usabilidad y experiencia de usuario
- Comparar con casos de uso documentados
- Agregar feedback funcional en Dashboard

---

### 🥗 Nutriólogos
**Responsable:** Validar desde perspectiva de usuario profesional real

**Casos Asignados:**
- E2E-003: Acceso a Historia Clínica
- E2E-WA-001: Navegación WhatsApp Manager
- E2E-WA-003: Envío de Recordatorio
- E2E-AI-002: Interfaz de Carga de Fotos
- E2E-AI-004: Análisis de Foto Real

**Tareas:**
- Usar el sistema como lo harían en consulta real
- Validar que las funcionalidades son útiles
- Verificar terminología nutricional correcta
- Probar con datos de pacientes reales (anonimizados)
- Reportar mejoras desde experiencia clínica

---

### 😊 Pacientes (Usuarios Finales)
**Responsable:** Validar experiencia de usuario final

**Casos Asignados:**
- E2E-005: Responsive Design (Mobile)
- E2E-WA-003: Recepción de Recordatorios (junto con nutriólogo)
- E2E-AI-002: Subir Foto desde Móvil (junto con nutriólogo)
- E2E-AI-004: Análisis de Foto desde Perspectiva de Paciente

**Tareas:**
- Probar en dispositivos reales (smartphone, tablet)
- Validar que la app es fácil de usar
- Reportar confusiones o dudas
- Validar que reciben notificaciones WhatsApp
- Dar feedback honesto sobre experiencia

---

## 3. Acceso al Dashboard de Pruebas

### 3.1 URL de Acceso

```
http://localhost:3002
```

**Nota:** Para acceso remoto, solicitar URL al administrador

### 3.2 Login

1. Abrir navegador (Chrome recomendado)
2. Navegar a http://localhost:3002
3. Hacer clic en el selector de rol (arriba a la derecha)
4. Seleccionar: **Admin**
5. En el sidebar, ir a: **Administración** → **Dashboard de Pruebas** (badge QA)

### 3.3 Interfaz del Dashboard

El Dashboard muestra:

```
┌──────────────────────────────────────────────────────┐
│  Dashboard de Pruebas                                │
├──────────────────────────────────────────────────────┤
│                                                       │
│  [Total: 15]  [Pasaron: 2]  [Automatizadas: 2]      │
│  [Manuales: 13]                                      │
│                                                       │
│  Progreso: ████░░░░░░░░░░░░░░ 13.3%                 │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ ID  │ Categoría │ Título │ Asignado │ Estado│    │
│  ├─────┼───────────┼────────┼──────────┼───────┤    │
│  │E2E-003│Expediente│Historia│Nutriólogo│Pending│    │
│  │       │          │Clínica │          │       │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## 4. Casos de Prueba Manuales

### 📂 Expediente Clínico

#### ✅ E2E-003: Acceso a Historia Clínica

**Asignado a:** Nutriólogo
**Prioridad:** Media
**Duración Estimada:** 10 minutos

**Objetivo:**
Validar que un nutriólogo puede acceder, visualizar y editar la historia clínica de un paciente de forma correcta y segura.

**Precondiciones:**
- Usuario logueado como Nutriólogo
- Al menos 1 paciente existe en el sistema

**Pasos a Ejecutar:**

1. Desde el menú lateral, clic en "Expediente Clínico"
2. Seleccionar un paciente de la lista (o crear uno nuevo)
3. Una vez en el expediente, clic en el tab "Historia Clínica"
4. Verificar que se muestran las siguientes secciones:
   - Antecedentes Heredofamiliares
   - Antecedentes Personales No Patológicos
   - Antecedentes Personales Patológicos
   - Cirugías Previas
   - Hospitalizaciones
5. Intentar editar un campo (ej: agregar una alergia)
6. Guardar cambios
7. Recargar la página y verificar que los cambios persisten

**Criterios de Aceptación:**

✅ El tab de Historia Clínica es visible y clickeable
✅ Todas las secciones se muestran correctamente
✅ Los campos son editables
✅ Los cambios se guardan correctamente
✅ La información persiste después de recargar
✅ No hay errores en consola (F12 → Console)

**Reportar en Dashboard:**
- **Estado:** Passed / Failed / Blocked
- **Comentario:** Describir observaciones, errores encontrados, o sugerencias

---

#### ✅ E2E-004: Datos de Laboratorio

**Asignado a:** Técnico + Nutriólogo
**Prioridad:** Alta
**Duración Estimada:** 15 minutos

**Objetivo:**
Validar que los datos de laboratorio se pueden ingresar, que la IA los interpreta correctamente, y que la integración funciona end-to-end.

**Precondiciones:**
- Usuario logueado como Nutriólogo
- Paciente con expediente activo
- API de Gemini configurada

**Pasos a Ejecutar:**

1. Ir a Expediente Clínico → Seleccionar paciente
2. Clic en tab "Laboratorio"
3. Clic en "Nuevo Estudio"
4. Ingresar valores de laboratorio:
   - Glucosa en ayunas: **125 mg/dL** (valor límite)
   - Colesterol Total: **220 mg/dL** (elevado)
   - Triglicéridos: **180 mg/dL** (elevado)
   - HDL: **35 mg/dL** (bajo)
   - HbA1c: **6.2%** (prediabetes)
5. Marcar como "En ayunas"
6. Clic en "Guardar y Analizar con IA"
7. Esperar respuesta de IA (5-10 segundos)
8. Verificar interpretación generada por IA

**Criterios de Aceptación (Técnico):**

✅ Formulario de laboratorio carga en <3 segundos
✅ Validaciones funcionan (no acepta valores negativos)
✅ Request a API de Gemini se envía correctamente
✅ Response de API retorna en <10 segundos
✅ No hay errores 500 en Network tab (F12)
✅ Datos se guardan en base de datos

**Criterios de Aceptación (Nutriólogo):**

✅ La interpretación IA es coherente
✅ IA detecta valores fuera de rango
✅ IA sugiere prediabetes por HbA1c
✅ IA calcula HOMA-IR si hay insulina
✅ Recomendaciones nutricionales son apropiadas

**Reportar:**
- Tiempo de respuesta de IA (segundos)
- Calidad de interpretación (1-5 estrellas)
- Errores encontrados

---

#### ✅ E2E-005: Responsive Design (Mobile)

**Asignado a:** Paciente
**Prioridad:** Media
**Duración Estimada:** 15 minutos

**Objetivo:**
Validar que la aplicación funciona correctamente en dispositivos móviles (smartphone y tablet).

**Precondiciones:**
- Acceso desde smartphone (iOS/Android) o tablet
- O usar modo responsive del navegador (F12 → Toggle device toolbar)

**Pasos a Ejecutar:**

1. Abrir navegador en móvil y navegar a http://localhost:3002
   (O en desktop: F12 → Click icono de móvil, seleccionar iPhone 12)
2. Verificar que aparece menú hamburguesa (☰) en lugar de sidebar
3. Clic en menú hamburguesa
4. Verificar que el drawer se abre con opciones de menú
5. Navegar a "Expediente Clínico"
6. Verificar que los tabs se muestran correctamente
7. Intentar hacer scroll vertical y horizontal
8. Probar con orientación portrait y landscape
9. Navegar a "Gamificación"
10. Verificar que las tarjetas se adaptan al ancho

**Criterios de Aceptación:**

✅ Menú hamburguesa aparece en móvil (<768px)
✅ Drawer se abre y cierra correctamente
✅ NO hay scroll horizontal indeseado
✅ Todo el texto es legible (tamaño adecuado)
✅ Botones son fáciles de presionar con el dedo
✅ Imágenes y gráficas se adaptan al ancho
✅ Funciona en portrait y landscape
✅ Animaciones son fluidas (no lag)

**Dispositivos a Probar:**

- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] Tablet iPad
- [ ] Modo responsive navegador

**Reportar:**
- Dispositivo usado
- Sistema operativo y navegador
- Screenshots de problemas encontrados

---

### 📱 WhatsApp

#### ✅ E2E-WA-001: Navegación WhatsApp Manager

**Asignado a:** Nutriólogo
**Prioridad:** Media
**Duración Estimada:** 5 minutos

**Objetivo:**
Validar que un nutriólogo puede acceder al módulo de WhatsApp Manager y navegar por sus secciones.

**Pasos:**

1. Desde el menú lateral, buscar "WhatsApp" o "Mensajería"
2. Clic en la opción de WhatsApp
3. Verificar que la vista carga correctamente
4. Verificar que hay 2 tabs: "Enviar Mensajes" y "Historial"
5. Navegar entre ambos tabs

**Criterios de Aceptación:**

✅ Opción de WhatsApp visible en sidebar
✅ Vista carga sin errores
✅ Tabs son visibles y clickeables
✅ Iconos de WhatsApp se muestran correctamente
✅ No hay errores en consola

---

#### ✅ E2E-WA-002: Mensajes Rápidos

**Asignado a:** Funcional
**Prioridad:** Media
**Duración Estimada:** 10 minutos

**Objetivo:**
Validar que las opciones de mensajes rápidos predefinidos se muestran y funcionan correctamente.

**Pasos:**

1. Ir a WhatsApp Manager → Tab "Enviar Mensajes"
2. Verificar que aparecen tarjetas de acciones rápidas:
   - 🗓️ Recordatorio de Cita
   - 📋 Plan de Alimentación Listo
   - 💪 Mensaje Motivacional
3. Hacer clic en cada tarjeta
4. Verificar que hay botón "Enviar"
5. NO enviar mensaje real (solo validar UI)

**Criterios de Aceptación:**

✅ Mínimo 3 tarjetas de acción rápida visibles
✅ Cada tarjeta tiene:
   - Icono apropiado
   - Título descriptivo
   - Botón de acción
✅ Hover effect funciona
✅ Textos en español correcto
✅ UI es intuitiva y profesional

**Validación Funcional:**

✅ Los tipos de mensaje cubren casos de uso reales
✅ Las plantillas son apropiadas para contexto mexicano
✅ El flujo es lógico y fácil de entender

---

#### ✅ E2E-WA-003: Envío de Recordatorio

**Asignado a:** Nutriólogo + Paciente
**Prioridad:** Alta
**Duración Estimada:** 10 minutos

**Objetivo:**
Validar el flujo completo de envío de un recordatorio de cita por WhatsApp, desde el nutriólogo hasta la recepción por el paciente.

**Precondiciones:**
- Twilio configurado (modo sandbox o producción)
- Paciente con número de WhatsApp válido registrado
- Paciente tiene WhatsApp instalado

**Pasos (Nutriólogo):**

1. Ir a WhatsApp Manager
2. Clic en "Recordatorio de Cita"
3. Sistema debe mostrar datos de ejemplo o permitir editarlos:
   - Paciente: María Guadalupe Hernández López
   - Teléfono: +525512345678 (o tu número de prueba)
   - Fecha de cita: Viernes 17 de Enero, 2025
   - Hora: 10:00 AM
4. Clic en "Enviar Recordatorio"
5. Esperar confirmación del sistema

**Pasos (Paciente):**

6. Abrir WhatsApp en smartphone
7. Buscar mensaje de Twilio/Nutrition Intelligence
8. Verificar que el mensaje llegó
9. Leer contenido del mensaje

**Criterios de Aceptación (Nutriólogo):**

✅ Formulario se muestra correctamente
✅ Datos del paciente se autocompl etan
✅ Sistema muestra confirmación de éxito
✅ No hay errores en pantalla

**Criterios de Aceptación (Paciente):**

✅ Mensaje llega en <1 minuto
✅ Formato del mensaje es correcto
✅ Datos son correctos (nombre, fecha, hora)
✅ Mensaje es claro y profesional
✅ Incluye emoji apropiados

**Mensaje Esperado:**
```
¡Hola María Guadalupe! 👋

Te recordamos tu cita de nutrición:
📅 Fecha: Viernes 17 de Enero, 2025
🕐 Hora: 10:00 AM
👩‍⚕️ Nutrióloga: Dra. Ana Pérez Lizaur

Por favor, asiste puntual. Si necesitas reagendar, avísanos con anticipación.

¡Te esperamos! 🥗
```

**Reportar:**
- Tiempo de entrega del mensaje (segundos)
- Screenshot del mensaje recibido
- Calidad del mensaje (claridad, tono, profesionalismo)

---

#### ✅ E2E-WA-004: Historial de Mensajes

**Asignado a:** Técnico
**Prioridad:** Media
**Duración Estimada:** 8 minutos

**Objetivo:**
Validar que el historial de mensajes WhatsApp se muestra correctamente y está completo.

**Precondiciones:**
- Al menos 1 mensaje enviado previamente (E2E-WA-003)

**Pasos:**

1. Ir a WhatsApp Manager
2. Clic en tab "Historial"
3. Verificar que aparecen mensajes enviados
4. Revisar detalles de un mensaje:
   - Paciente
   - Tipo de mensaje
   - Fecha y hora
   - Estado (Sent/Delivered/Read/Failed)
   - Twilio SID
5. Intentar usar botón "Actualizar"

**Criterios de Aceptación:**

✅ Historial carga en <3 segundos
✅ Mensajes se muestran en orden cronológico (más reciente primero)
✅ Todos los campos requeridos están presentes
✅ Estados de entrega son correctos
✅ Twilio SID es válido (formato SMxxxxxxxxxxxxxxxx)
✅ Botón "Actualizar" recarga la lista
✅ Si no hay mensajes, muestra mensaje amigable

**Reportar:**
- Tiempo de carga (segundos)
- Cantidad de mensajes en historial
- Screenshots de la tabla

---

#### ✅ E2E-WA-005: Configuración Twilio

**Asignado a:** Técnico
**Prioridad:** Baja
**Duración Estimada:** 5 minutos

**Objetivo:**
Validar que la información sobre configuración de Twilio es clara y útil.

**Pasos:**

1. Ir a WhatsApp Manager
2. Buscar alert o mensaje informativo sobre Twilio
3. Leer contenido del mensaje
4. Verificar que menciona:
   - Twilio como proveedor
   - Configuración en .env
   - Modo de prueba vs. producción

**Criterios de Aceptación:**

✅ Alert informativo está visible
✅ Mensaje es claro y profesional
✅ Incluye enlace a documentación o .env.example
✅ Explica cómo configurar Twilio
✅ Diferencia entre modo sandbox y producción

---

### 🤖 AI Vision

#### ✅ E2E-AI-001: Navegación Análisis de Fotos

**Asignado a:** Funcional
**Prioridad:** Media
**Duración Estimada:** 5 minutos

**Objetivo:**
Validar acceso al módulo de análisis de fotos con IA.

**Pasos:**

1. Desde el menú lateral, buscar "Análisis de Fotos" o "AI Vision"
2. Clic en la opción
3. Verificar que la vista carga
4. Identificar componentes principales de la UI

**Criterios de Aceptación:**

✅ Opción visible en sidebar
✅ Vista carga sin errores
✅ Se muestra interfaz de carga de fotos
✅ Hay indicaciones claras de qué hacer
✅ UI es intuitiva

---

#### ✅ E2E-AI-002: Interfaz de Carga

**Asignado a:** Nutriólogo + Paciente
**Prioridad:** Media
**Duración Estimada:** 10 minutos

**Objetivo:**
Validar que la interfaz de carga de fotos es fácil de usar tanto para nutriólogos como pacientes.

**Pasos (Desktop):**

1. Ir a Análisis de Fotos
2. Intentar drag & drop de una imagen
3. Intentar clic en botón "Seleccionar archivo"
4. Verificar preview de imagen

**Pasos (Móvil):**

5. Abrir en smartphone
6. Buscar botón de cámara
7. Intentar tomar foto con cámara
8. Verificar que la foto se captura

**Criterios de Aceptación:**

✅ Drag & drop funciona (desktop)
✅ Selector de archivos funciona
✅ Preview de imagen se muestra
✅ Botón de cámara visible en móvil
✅ Formatos aceptados: JPG, PNG, HEIC
✅ Tamaño máximo: 5 MB
✅ Mensaje de error si archivo no válido

---

#### ✅ E2E-AI-003: Configuración IA (Gemini/Claude)

**Asignado a:** Técnico
**Prioridad:** Alta
**Duración Estimada:** 10 minutos

**Objetivo:**
Validar que se puede seleccionar el modelo de IA y que la configuración funciona.

**Pasos:**

1. Ir a Análisis de Fotos
2. Buscar selector de modelo de IA
3. Verificar opciones disponibles:
   - Gemini (rápido, económico)
   - Claude (preciso, más caro)
   - Híbrido (Gemini primero, Claude fallback)
4. Seleccionar cada opción
5. Verificar que la selección se guarda

**Criterios de Aceptación:**

✅ Selector de modelo visible
✅ 3 opciones disponibles (Gemini, Claude, Híbrido)
✅ Descripción clara de cada opción
✅ Selección se persiste (localStorage o BD)
✅ Modo híbrido es la opción recomendada

**Validación Técnica:**

✅ API keys configuradas en backend/.env
✅ Endpoint de IA responde correctamente
✅ Error handling si API falla

---

#### ✅ E2E-AI-004: Análisis de Foto Real

**Asignado a:** Paciente + Nutriólogo
**Prioridad:** Alta
**Duración Estimada:** 15 minutos

**Objetivo:**
Validar que el análisis de fotos con IA funciona end-to-end con comida real.

**Precondiciones:**
- API de Gemini o Claude configurada
- Foto de alimento mexicano disponible

**Pasos:**

1. Tomar foto de un platillo mexicano (tacos, enchiladas, etc.)
   O usar foto de ejemplo
2. Subir foto al sistema
3. Seleccionar modelo: Híbrido
4. Clic en "Analizar"
5. Esperar resultado (10-30 segundos)
6. Revisar análisis generado:
   - Lista de alimentos detectados
   - Porciones estimadas
   - Calorías totales
   - Macronutrientes (proteínas, carbohidratos, lípidos)
   - Nivel de confianza

**Ejemplo de Foto:**
```
Platillo: 3 tacos de pollo con tortillas de maíz
Contenido esperado:
- Tortillas de maíz: 3 piezas (60g)
- Pollo deshebrado: 90g
- Lechuga: 30g
- Tomate: 40g
- Cebolla: 20g
- Salsa verde: 30g

Resultado esperado:
Calorías: ~450 kcal
Proteínas: ~30g
Carbohidratos: ~40g
Lípidos: ~15g
```

**Criterios de Aceptación (Paciente):**

✅ Proceso es fácil de seguir
✅ Resultado se muestra en <30 segundos
✅ Información es clara y entendible
✅ UI es atractiva

**Criterios de Aceptación (Nutriólogo):**

✅ IA identifica correctamente los alimentos
✅ Porciones son razonables
✅ Calorías están en rango esperado (±20%)
✅ Si es platillo mexicano, lo reconoce
✅ Nivel de confianza >70% para fotos claras

**Casos a Probar:**

- [ ] Tacos (tortilla + proteína)
- [ ] Ensalada con pollo
- [ ] Plato de frutas
- [ ] Bebida (jugo, refresco)
- [ ] Foto poco clara (validar rechazo)

**Reportar:**
- Foto usada (adjuntar)
- Modelo de IA usado
- Tiempo de análisis (segundos)
- Precisión del resultado (1-5 estrellas)
- Comentarios sobre la experiencia

---

#### ✅ E2E-AI-005: Accesibilidad

**Asignado a:** Funcional
**Prioridad:** Media
**Duración Estimada:** 15 minutos

**Objetivo:**
Validar que la aplicación cumple con estándares de accesibilidad WCAG 2.1 Nivel AA.

**Herramientas:**
- WAVE Browser Extension
- axe DevTools
- Navegación con teclado
- Lector de pantalla (opcional)

**Pasos:**

1. Instalar extensión WAVE (https://wave.webaim.org/extension/)
2. Navegar a Nutrition Intelligence
3. Activar WAVE
4. Revisar reporte de errores
5. Usar solo teclado para navegar:
   - Tab para avanzar
   - Shift+Tab para retroceder
   - Enter para activar
6. Verificar contraste de colores
7. Verificar que todos los botones tienen labels

**Criterios de Aceptación:**

✅ 0 errores críticos en WAVE
✅ Contraste de texto: mínimo 4.5:1
✅ Todos los botones tienen aria-label o texto
✅ Headings en orden jerárquico (h1 → h2 → h3)
✅ Imágenes tienen alt text
✅ Formularios tienen labels
✅ Navegación por teclado funciona
✅ Focus visible en elementos interactivos

**Reportar:**
- Screenshot de reporte WAVE
- Problemas de contraste encontrados
- Elementos sin labels
- Sugerencias de mejora

---

## 5. Cómo Ejecutar una Prueba

### Paso 1: Preparación

1. Leer el caso de prueba asignado completamente
2. Verificar que cumples las precondiciones
3. Preparar herramientas necesarias (dispositivo, screenshots)
4. Anotar hora de inicio

### Paso 2: Ejecución

1. Seguir los pasos exactamente como están descritos
2. Anotar cualquier desviación o error
3. Tomar screenshots de pantallas relevantes
4. Si encuentras un bug, intenta reproducirlo 2 veces

### Paso 3: Documentación

1. Anotar resultado: Passed / Failed / Blocked
2. Si Failed:
   - Describir el problema claramente
   - Adjuntar screenshots
   - Copiar mensajes de error (Console F12)
   - Indicar en qué paso falló
3. Si Blocked:
   - Explicar por qué no se pudo completar
   - Ej: "API de Gemini no configurada"

### Paso 4: Reportar

1. Ir al Dashboard de Pruebas
2. Buscar tu caso de prueba en la tabla
3. Clic en ícono de comentario 💬
4. Completar formulario:
   - **Rol:** Seleccionar tu rol (Técnico/Funcional/Nutriólogo/Paciente)
   - **Comentario:** Describir resultado, observaciones, bugs
   - **Cambiar Estado:** Seleccionar Passed/Failed/Blocked
5. Clic en "Agregar Comentario"

---

## 6. Cómo Reportar Resultados

### Formato de Comentario Exitoso (Passed)

```
[✅ PASSED]

Ejecutado por: Ana García (Nutrióloga)
Fecha: 15/01/2025 14:30

Resultado: La prueba pasó exitosamente.

Observaciones:
- Tiempo de carga: 2.5 segundos
- UI es intuitiva y clara
- Todos los datos se guardaron correctamente

Sugerencias:
- Sería útil tener un botón de "Duplicar estudio"
- El mensaje de confirmación podría ser más visible
```

### Formato de Comentario con Falla (Failed)

```
[❌ FAILED]

Ejecutado por: Carlos Pérez (QA Técnico)
Fecha: 15/01/2025 15:45

Paso donde falló: Paso 9 (Análisis con IA)

Error encontrado:
Al hacer clic en "Analizar con IA", aparece error 500:
"Error: API key not configured"

Evidencia:
- Screenshot: error_500_gemini.png
- Console log: "Failed to fetch https://api.google.dev/..."

Impacto: Crítico - Bloquea funcionalidad principal

Reproducible: Sí (100% de las veces)

Ambiente:
- Navegador: Chrome 120
- SO: Windows 11
- Backend: Local (localhost:8000)
```

### Formato de Comentario Bloqueado

```
[🚫 BLOCKED]

Ejecutado por: María López (Paciente Prueba)
Fecha: 15/01/2025 16:00

Razón del bloqueo:
No puedo completar la prueba porque no tengo un número de WhatsApp válido registrado en el sistema de pruebas.

Precondición faltante:
- Necesito que un nutriólogo me agregue con mi número real

Acción requerida:
Solicitar al administrador que configure mi cuenta con número +52 55 1234-5678
```

---

## 7. FAQs

### Q1: ¿Qué hago si encuentro un bug?

**R:** Documentarlo detalladamente en el Dashboard de Pruebas con:
- Pasos para reproducir
- Resultado esperado vs. resultado actual
- Screenshots
- Logs de consola (F12)
- Marcar el caso como "Failed"

### Q2: ¿Puedo probar en un ambiente diferente?

**R:** Sí, pero especifica claramente el ambiente en tus comentarios:
- Local (localhost)
- Staging (si existe)
- Producción (NO recomendado para pruebas)

### Q3: ¿Qué navegador debo usar?

**R:** Chrome es recomendado, pero también prueba en:
- Firefox
- Safari (Mac/iOS)
- Edge

Especifica el navegador en tu reporte.

### Q4: ¿Puedo agregar nuevos casos de prueba?

**R:** Sí! Si encuentras un flujo importante no cubierto:
1. Documéntalo en el Dashboard
2. Notifica al líder de QA
3. Proponlo para la siguiente iteración

### Q5: ¿Cuánto tiempo tengo para completar mi prueba?

**R:** Cada prueba tiene duración estimada. Si toma más tiempo, repórtalo en comentarios.

### Q6: ¿Qué hago si necesito ayuda?

**R:** Contacta a:
- **Soporte Técnico:** soporte@nutrition-intelligence.com
- **Slack:** #testing-qa
- **Líder de QA:** [Nombre del líder]

---

## 📊 Dashboard de Progreso

### Monitoreo en Tiempo Real

El Dashboard muestra progreso en tiempo real:

- **Barra de Progreso:** % de casos completados
- **Estadísticas:** Total, Passed, Failed, Pending
- **Comentarios:** Todos los comentarios de todos los roles
- **Exportar:** Botón para descargar resultados en JSON

### Métricas de Éxito

El proyecto se considera exitoso si:

- ✅ 90%+ de casos pasan (13+ de 15)
- ✅ 0 bugs críticos
- ✅ <3 bugs menores
- ✅ Todas las áreas reportan resultados

---

## 🎯 Próximos Pasos

Una vez completadas todas las pruebas:

1. **Revisión de Resultados** (Equipo QA + Product Owner)
2. **Corrección de Bugs** (Desarrollo)
3. **Re-testing** (Solo casos que fallaron)
4. **Aprobación Final** (Product Owner)
5. **Deploy a Producción** 🚀

---

## 📞 Contacto

**Equipo de QA:**
- Email: qa@nutrition-intelligence.com
- Slack: #nutrition-qa
- Reunión diaria: 10:00 AM (Teams)

**Documentación:**
- Plan de Pruebas: TESTING_PLAN.md
- Casos de Uso: CASOS-DE-USO.md
- Arquitectura: MD050-ARQUITECTURA-SISTEMA.md

---

**¡Gracias por tu colaboración en las pruebas!**

Tu feedback es invaluable para mejorar Nutrition Intelligence y ofrecer la mejor experiencia a nutriólogos y pacientes. 🥗✨
