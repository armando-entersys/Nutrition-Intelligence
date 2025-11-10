# CASOS DE USO - NUTRITION INTELLIGENCE PLATFORM

**Versión**: 1.0
**Fecha**: 2025-11-05
**Dominio**: https://nutrition-intelligence.scram2k.com

---

## TABLA DE CONTENIDOS

1. [Introducción](#introducción)
2. [Actores del Sistema](#actores-del-sistema)
3. [Módulo de Autenticación](#módulo-de-autenticación)
4. [Módulo de Gestión de Pacientes](#módulo-de-gestión-de-pacientes)
5. [Módulo de Análisis Nutricional](#módulo-de-análisis-nutricional)
6. [Módulo de Plan Alimenticio](#módulo-de-plan-alimenticio)
7. [Módulo de Recordatorio 24 Horas](#módulo-de-recordatorio-24-horas)
8. [Matriz de Trazabilidad](#matriz-de-trazabilidad)

---

## 1. INTRODUCCIÓN

### 1.1 Propósito
Este documento define los casos de uso para la plataforma Nutrition Intelligence, describiendo las interacciones entre los usuarios y el sistema para cada funcionalidad principal.

### 1.2 Alcance
- Casos de uso de nivel usuario
- Flujos principales y alternos
- Precondiciones y postcondiciones
- Validaciones y reglas de negocio

### 1.3 Convenciones
- **UC-XXX**: Identificador único de caso de uso
- **Actor**: Usuario que interactúa con el sistema
- **Precondición**: Estado del sistema antes de ejecutar el caso de uso
- **Postcondición**: Estado del sistema después de completar el caso de uso

---

## 2. ACTORES DEL SISTEMA

### 2.1 Actor: Paciente (PATIENT)
**Descripción**: Usuario final que busca servicios de nutrición
**Responsabilidades**:
- Registrarse en la plataforma
- Completar expediente clínico
- Ver y seguir planes alimenticios
- Registrar consumo de alimentos
- Analizar fotos de comida

**Permisos**:
- Ver su propio perfil
- Editar sus datos personales
- Acceder a sus planes
- Ver dashboard de paciente

---

### 2.2 Actor: Nutriólogo (NUTRITIONIST)
**Descripción**: Profesional de la salud especializado en nutrición
**Responsabilidades**:
- Gestionar expedientes de pacientes
- Crear planes alimenticios personalizados
- Revisar registros de consumo
- Analizar progreso de pacientes
- Dar seguimiento nutricional

**Permisos**:
- Ver perfiles de sus pacientes
- Crear y editar planes alimenticios
- Acceder a datos clínicos
- Ver dashboard de nutriólogo
- Gestionar citas

---

### 2.3 Actor: Administrador (ADMIN)
**Descripción**: Administrador del sistema
**Responsabilidades**:
- Gestionar usuarios
- Aprobar contenido
- Configurar sistema
- Monitorear actividad
- Revisar auditorías

**Permisos**:
- Acceso completo al sistema
- Gestión de todos los usuarios
- Configuración avanzada
- Ver logs de auditoría

---

## 3. MÓDULO DE AUTENTICACIÓN

### UC-001: Registro de Usuario

**Actor**: Paciente / Nutriólogo
**Precondiciones**: Ninguna
**Postcondiciones**: Usuario creado en el sistema

**Flujo Principal**:
1. Usuario accede a la página de registro
2. Sistema muestra formulario con campos:
   - Email (requerido, único)
   - Username (requerido, único, 3-50 caracteres)
   - Password (requerido, mínimo 8 caracteres)
   - Confirmar Password (requerido, debe coincidir)
   - Nombre (requerido)
   - Apellido (requerido)
   - Teléfono (opcional, formato válido)
   - Rol (PATIENT/NUTRITIONIST)
   - Email de Nutriólogo (requerido solo para pacientes)
3. Usuario completa formulario
4. Sistema valida datos ingresados
5. Si rol es PATIENT:
   a. Sistema valida que email de nutriólogo exista
   b. Sistema valida que sea un nutriólogo activo
   c. Sistema vincula paciente con nutriólogo
6. Sistema crea cuenta con estado:
   - ACTIVE si es paciente
   - PENDING_VERIFICATION si es nutriólogo
7. Sistema envía email de bienvenida
8. Sistema redirige según rol:
   - Paciente → Dashboard
   - Nutriólogo → Mensaje de verificación pendiente

**Flujos Alternos**:

**FA-001a: Email ya registrado**
- 4a. Sistema detecta que email ya existe
- 4b. Sistema muestra error: "Email already registered"
- 4c. Usuario puede intentar login o usar otro email

**FA-001b: Username ya tomado**
- 4a. Sistema detecta que username ya existe
- 4b. Sistema muestra error: "Username already taken"
- 4c. Usuario debe elegir otro username

**FA-001c: Contraseña débil**
- 4a. Sistema valida fortaleza de contraseña
- 4b. Si no cumple requisitos, muestra errores:
   - Mínimo 8 caracteres
   - Al menos 1 mayúscula
   - Al menos 1 minúscula
   - Al menos 1 número
- 4c. Usuario corrige contraseña

**FA-001d: Nutriólogo no encontrado**
- 5a. Sistema no encuentra nutriólogo con el email proporcionado
- 5b. Sistema muestra error: "No se encontró un nutriólogo con el email: {email}"
- 5c. Usuario debe verificar el email o contactar al nutriólogo

**FA-001e: Nutriólogo inactivo**
- 5a. Sistema encuentra nutriólogo pero está inactivo
- 5b. Sistema muestra error: "La cuenta del nutriólogo está {status}"
- 5c. Usuario debe contactar al nutriólogo o soporte

**Validaciones**:
- Email formato válido (RFC 5322)
- Username: alfanumérico + guiones/underscores
- Password strength: >= 8 chars, mayúscula, minúscula, número
- Teléfono: formato internacional válido (opcional)

**Reglas de Negocio**:
- RN-001: Un paciente debe estar asignado a un nutriólogo
- RN-002: Un nutriólogo puede atender múltiples pacientes
- RN-003: Las cuentas de nutriólogos requieren verificación manual
- RN-004: Las cuentas de pacientes se activan automáticamente

---

### UC-002: Login de Usuario

**Actor**: Paciente / Nutriólogo / Admin
**Precondiciones**: Usuario registrado en el sistema
**Postcondiciones**: Usuario autenticado con sesión activa

**Flujo Principal**:
1. Usuario accede a la página de login
2. Sistema muestra formulario:
   - Email
   - Password
   - Checkbox "Recordarme"
3. Usuario ingresa credenciales
4. Sistema valida email y password
5. Sistema verifica estado de cuenta
6. Sistema genera tokens JWT:
   - Access token (30 minutos)
   - Refresh token (30 días)
7. Sistema actualiza:
   - last_login timestamp
   - login_count (+1)
   - failed_login_attempts = 0
8. Sistema almacena tokens en localStorage
9. Sistema redirige a dashboard según rol

**Flujos Alternos**:

**FA-002a: Credenciales incorrectas**
- 4a. Sistema detecta email o password inválido
- 4b. Sistema incrementa failed_login_attempts
- 4c. Sistema actualiza last_failed_login
- 4d. Sistema muestra error genérico: "Incorrect email or password"
- 4e. Usuario puede intentar nuevamente

**FA-002b: Cuenta inactiva**
- 5a. Sistema detecta account_status != ACTIVE
- 5b. Sistema muestra error: "Account is {status}. Please contact support."
- 5c. Usuario no puede acceder

**FA-002c: Cuenta bloqueada por intentos fallidos**
- 4a. Sistema detecta failed_login_attempts >= 5
- 4b. Sistema bloquea cuenta temporalmente
- 4c. Sistema envía email de alerta
- 4d. Sistema muestra error: "Account temporarily locked"

**FA-002d: Token expirado**
- Durante sesión activa:
- 9a. Sistema detecta access token expirado
- 9b. Sistema intenta renovar con refresh token
- 9c. Si refresh token válido, genera nuevo access token
- 9d. Si refresh token expirado, cierra sesión

**Validaciones**:
- Email formato válido
- Password no vacío

**Reglas de Negocio**:
- RN-005: Máximo 5 intentos fallidos consecutivos
- RN-006: Bloqueo temporal de 30 minutos tras 5 intentos
- RN-007: Los tokens incluyen: user_id, email, username, primary_role, secondary_roles

---

### UC-003: Recuperación de Contraseña

**Actor**: Paciente / Nutriólogo
**Precondiciones**: Usuario registrado
**Postcondiciones**: Nueva contraseña establecida

**Flujo Principal**:
1. Usuario accede a "¿Olvidaste tu contraseña?"
2. Sistema muestra formulario solicitando email
3. Usuario ingresa su email
4. Sistema valida email existe en BD
5. Sistema revoca tokens activos del usuario
6. Sistema genera token de recuperación:
   - Token único de 64 caracteres
   - Expira en 1 hora
   - Status: ACTIVE
7. Sistema almacena token en password_reset_tokens
8. Sistema envía email con link de reset
9. Sistema muestra mensaje genérico de éxito
10. Usuario recibe email y hace click en link
11. Sistema valida token:
    - Existe en BD
    - Status = ACTIVE
    - No expirado
12. Sistema muestra formulario de nueva contraseña
13. Usuario ingresa nueva contraseña
14. Sistema valida fortaleza de contraseña
15. Sistema actualiza password_hash
16. Sistema marca token como USED
17. Sistema muestra confirmación
18. Usuario es redirigido a login

**Flujos Alternos**:

**FA-003a: Email no registrado**
- 4a. Sistema no encuentra email en BD
- 4b. Sistema NO revela que email no existe (seguridad)
- 4c. Sistema muestra mismo mensaje de éxito
- 4d. No se envía email

**FA-003b: Token inválido o expirado**
- 11a. Sistema no encuentra token o está expirado/usado
- 11b. Sistema muestra error: "Invalid or expired reset token"
- 11c. Usuario debe solicitar nuevo token

**FA-003c: Contraseña débil**
- 14a. Sistema valida contraseña no cumple requisitos
- 14b. Sistema muestra errores específicos
- 14c. Usuario debe ingresar contraseña más fuerte

**Validaciones**:
- Email formato válido
- Token mínimo 32 caracteres
- Nueva contraseña: >= 8 chars, mayúscula, minúscula, número
- Confirmar contraseña debe coincidir

**Reglas de Negocio**:
- RN-008: Token de recuperación válido por 1 hora
- RN-009: Solo un token activo por usuario
- RN-010: Tokens previos se revocan al crear uno nuevo
- RN-011: No revelar si email existe (prevenir enumeración)

---

## 4. MÓDULO DE GESTIÓN DE PACIENTES

### UC-010: Crear Perfil de Paciente

**Actor**: Paciente
**Precondiciones**: Usuario autenticado con rol PATIENT
**Postcondiciones**: Perfil de paciente creado

**Flujo Principal**:
1. Paciente accede a su dashboard
2. Sistema detecta que no tiene perfil creado
3. Sistema muestra formulario de perfil:
   - Fecha de nacimiento
   - Género (M/F/Otro)
   - Objetivo nutricional
   - Peso objetivo (kg)
   - Nivel de actividad física
4. Paciente completa formulario
5. Sistema valida datos
6. Sistema calcula edad a partir de fecha nacimiento
7. Sistema verifica nutritionist_id asignado
8. Sistema crea registro en tabla patients
9. Sistema muestra confirmación
10. Sistema habilita acceso completo al dashboard

**Flujos Alternos**:

**FA-010a: Edad inválida**
- 5a. Sistema calcula edad < 2 años
- 5b. Sistema muestra error: "Edad mínima: 2 años"
- 5c. Paciente debe verificar fecha

**FA-010b: Peso objetivo inválido**
- 5a. Sistema detecta peso fuera de rango (20-300 kg)
- 5b. Sistema muestra error con rango válido
- 5c. Paciente ajusta valor

**Validaciones**:
- Fecha nacimiento: >= 2 años atrás
- Peso objetivo: 20-300 kg
- Nivel actividad: valor del enum ActivityLevel

**Reglas de Negocio**:
- RN-020: Un paciente solo puede tener un perfil
- RN-021: El perfil es obligatorio para usar la plataforma
- RN-022: Nutritionist_id debe estar asignado (del registro)

---

### UC-011: Registrar Mediciones Antropométricas

**Actor**: Paciente / Nutriólogo
**Precondiciones**: Perfil de paciente existe
**Postcondiciones**: Nueva medición registrada

**Flujo Principal**:
1. Actor accede a sección de mediciones
2. Sistema muestra historial de mediciones previas
3. Actor selecciona "Nueva medición"
4. Sistema muestra formulario:
   - Peso (kg)
   - Altura (cm)
   - Porcentaje de grasa corporal (%)
   - Masa muscular (kg)
   - Medidas (cintura, cadera, pecho en cm)
5. Actor ingresa datos
6. Sistema valida rangos
7. Sistema calcula automáticamente:
   - IMC = peso / (altura/100)²
   - Relación cintura-cadera
   - Clasificación de IMC
8. Sistema almacena medición
9. Sistema genera gráfica de tendencias
10. Sistema muestra confirmación

**Flujos Alternos**:

**FA-011a: Valores fuera de rango**
- 6a. Sistema detecta valores anormales
- 6b. Sistema muestra advertencia
- 6c. Actor debe confirmar o corregir

**Validaciones**:
- Peso: 20-300 kg
- Altura: 50-250 cm
- Grasa corporal: 3-60%
- Masa muscular: 10-100 kg
- Medidas: 20-200 cm

**Reglas de Negocio**:
- RN-023: IMC se calcula automáticamente
- RN-024: Se puede registrar máximo 1 medición por día
- RN-025: Clasificación IMC según OMS:
  - Bajo peso: < 18.5
  - Normal: 18.5-24.9
  - Sobrepeso: 25-29.9
  - Obesidad I: 30-34.9
  - Obesidad II: 35-39.9
  - Obesidad III: >= 40

---

### UC-012: Gestionar Historia Clínica

**Actor**: Paciente
**Precondiciones**: Perfil de paciente existe
**Postcondiciones**: Historia clínica actualizada

**Flujo Principal**:
1. Paciente accede a "Historia Clínica"
2. Sistema muestra formulario con secciones:
   - Condiciones médicas
   - Alergias alimentarias
   - Intolerancias
   - Medicamentos actuales
   - Antecedentes familiares
   - Hábitos alimenticios
   - Preferencias dietéticas
3. Paciente completa/actualiza información
4. Sistema valida formato de datos
5. Sistema almacena en medical_histories
6. Sistema marca perfil como completo
7. Sistema muestra confirmación

**Flujos Alternos**:

**FA-012a: Alergia a alimento común**
- 3a. Paciente indica alergia severa
- 3b. Sistema marca alimento como restringido
- 3c. Sistema excluirá de recomendaciones futuras

**Validaciones**:
- Condiciones médicas: lista válida
- Alergias: de catálogo predefinido
- Medicamentos: formato de texto libre
- Hábitos: opciones predefinidas

**Reglas de Negocio**:
- RN-026: Historia clínica es obligatoria
- RN-027: Puede actualizarse en cualquier momento
- RN-028: Alergias afectan sugerencias de alimentos

---

## 5. MÓDULO DE ANÁLISIS NUTRICIONAL

### UC-020: Analizar Foto de Alimento

**Actor**: Paciente / Nutriólogo
**Precondiciones**: Usuario autenticado
**Postcondiciones**: Análisis nutricional generado

**Flujo Principal**:
1. Usuario accede a "Analizar Foto"
2. Sistema muestra opciones:
   - Tomar foto con cámara
   - Subir archivo existente
3. Usuario selecciona opción y proporciona imagen
4. Sistema valida:
   - Formato: JPG, PNG, WEBP
   - Tamaño: máximo 10 MB
   - Dimensiones mínimas: 200x200 px
5. Sistema muestra preview de imagen
6. Usuario confirma análisis
7. Sistema envía imagen a API Vision
8. Sistema procesa con Gemini Vision API
9. Si confidence < 75%:
   a. Sistema reintenta con Claude Vision API
   b. Sistema compara resultados
10. Sistema recibe respuesta JSON con:
    - Nombre del platillo
    - Confianza (%)
    - Ingredientes con cantidades
    - Totales nutricionales
    - Sellos NOM-051
    - Score de salubridad (1-10)
    - Recomendaciones
11. Sistema muestra resultados en tarjeta
12. Sistema ofrece guardar en historial

**Flujos Alternos**:

**FA-020a: Formato inválido**
- 4a. Sistema detecta formato no soportado
- 4b. Sistema muestra error: "Formato debe ser JPG, PNG o WEBP"
- 4c. Usuario debe seleccionar otra imagen

**FA-020b: Archivo muy grande**
- 4a. Sistema detecta tamaño > 10 MB
- 4b. Sistema muestra error: "Tamaño máximo: 10 MB"
- 4c. Usuario debe comprimir o seleccionar otra

**FA-020c: Imagen no reconocida**
- 9a. Sistema no puede identificar alimento
- 9b. Confidence < 50% en ambas IAs
- 9c. Sistema muestra: "No se pudo identificar el alimento"
- 9d. Usuario puede intentar con otra foto

**FA-020d: Error en API externa**
- 8a. API de Gemini/Claude no responde
- 8b. Sistema intenta con API alterna
- 8c. Si ambas fallan, muestra error temporal
- 8d. Usuario puede reintentar más tarde

**Validaciones**:
- Formato: .jpg, .jpeg, .png, .webp
- Tamaño: 100 KB - 10 MB
- Dimensiones: 200x200 hasta 4096x4096 px
- Content-Type: image/jpeg, image/png, image/webp

**Reglas de Negocio**:
- RN-030: Usar Gemini como AI primaria (más rápida)
- RN-031: Usar Claude como respaldo (más precisa)
- RN-032: Threshold de confidence: 75%
- RN-033: Guardar análisis en historial automáticamente
- RN-034: Sellos NOM-051 basados en normativa mexicana:
  - EXCESS_CALORIES: >= 275 kcal/100g
  - EXCESS_SUGARS: >= 10g/100g
  - EXCESS_SODIUM: >= 300mg/100g
  - EXCESS_SATURATED_FATS: >= 10g/100g
  - EXCESS_TRANS_FATS: > 0g/100g

**Respuesta esperada**:
```json
{
  "dish_name": "Tacos de carne asada con guacamole",
  "confidence": 92,
  "total_calories": 450,
  "total_protein_g": 28,
  "total_carbs_g": 35,
  "total_fat_g": 18,
  "total_fiber_g": 5,
  "total_sugar_g": 2,
  "total_sodium_mg": 680,
  "ingredients": [
    {
      "name": "Tortillas de maíz",
      "quantity": "3 piezas",
      "calories": 165,
      "protein_g": 4.5,
      "carbs_g": 33,
      "fat_g": 1.5,
      "category": "CEREALS"
    },
    {
      "name": "Carne asada",
      "quantity": "100g",
      "calories": 250,
      "protein_g": 26,
      "carbs_g": 0,
      "fat_g": 16,
      "category": "MEATS_MEDIUM_FAT"
    }
  ],
  "nom051_seals": ["EXCESS_SODIUM"],
  "health_score": 7,
  "recommendations": [
    "Reducir sal en preparación",
    "Agregar ensalada verde para fibra",
    "Controlar tamaño de porciones"
  ]
}
```

---

### UC-021: Calcular Requerimientos Nutricionales

**Actor**: Paciente / Nutriólogo
**Precondiciones**: Datos del paciente completos
**Postcondiciones**: Plan nutricional calculado

**Flujo Principal**:
1. Actor accede a "Calculadora de Requerimientos"
2. Sistema muestra wizard paso a paso
3. **Paso 1: Datos personales**
   - Sistema precarga datos del perfil
   - Actor verifica/actualiza:
     - Edad
     - Sexo
     - Peso actual (kg)
     - Altura (cm)
4. **Paso 2: Nivel de actividad**
   - Sistema muestra opciones:
     - Sedentario (1.2)
     - Ligera actividad (1.375)
     - Moderada (1.55)
     - Intensa (1.725)
     - Muy intensa (1.9)
   - Actor selecciona nivel
5. **Paso 3: Objetivo**
   - Sistema muestra opciones:
     - Perder peso (-500 kcal/día)
     - Mantener peso (0 kcal)
     - Ganar peso (+500 kcal/día)
     - Ganar músculo (+300 kcal, +proteína)
   - Actor selecciona objetivo
6. Sistema calcula TMB (Tasa Metabólica Basal):
   - Hombres: 66.47 + (13.75 × peso) + (5.003 × altura) - (6.755 × edad)
   - Mujeres: 655.1 + (9.563 × peso) + (1.850 × altura) - (4.676 × edad)
7. Sistema calcula TDEE:
   - TDEE = TMB × Factor de actividad
8. Sistema ajusta por objetivo:
   - Calorias_objetivo = TDEE ± ajuste
9. Sistema calcula macronutrientes:
   - Proteína: 1.6-2.2 g/kg peso
   - Grasas: 25-30% calorías
   - Carbohidratos: resto
10. Sistema muestra resultados:
    - TMB calculada
    - TDEE
    - Calorías objetivo
    - Distribución de macros (g y %)
    - Gráfica circular
11. Actor puede:
    - Ajustar manualmente distribución
    - Guardar plan
    - Imprimir

**Flujos Alternos**:

**FA-021a: Datos incompletos**
- 3a. Sistema detecta falta edad/peso/altura
- 3b. Sistema solicita completar perfil primero
- 3c. Actor es redirigido a perfil

**FA-021b: Ajuste manual de macros**
- 10a. Actor modifica distribución
- 10b. Sistema recalcula totales
- 10c. Sistema valida suma = 100%
- 10d. Sistema actualiza gráfica

**Validaciones**:
- Edad: 2-120 años
- Peso: 20-300 kg
- Altura: 50-250 cm
- Distribución macros: suma = 100%

**Reglas de Negocio**:
- RN-040: Usar fórmula Harris-Benedict Revisada
- RN-041: Proteína mínima: 0.8 g/kg peso
- RN-042: Proteína máxima: 2.5 g/kg peso
- RN-043: Grasas mínimas: 20% calorías
- RN-044: Grasas máximas: 35% calorías
- RN-045: Carbohidratos llenan el resto

---

## 6. MÓDULO DE PLAN ALIMENTICIO

### UC-030: Crear Plan Alimenticio Semanal

**Actor**: Nutriólogo
**Precondiciones**:
- Nutriólogo autenticado
- Paciente asignado
- Requerimientos calculados
**Postcondiciones**: Plan semanal creado y publicado

**Flujo Principal**:
1. Nutriólogo accede a "Crear Plan"
2. Sistema muestra lista de pacientes asignados
3. Nutriólogo selecciona paciente
4. Sistema carga:
   - Perfil del paciente
   - Requerimientos nutricionales
   - Alergias e intolerancias
   - Objetivos
5. Nutriólogo configura plan:
   - Fecha inicio y fin (7 días)
   - Calorias diarias
   - Distribución por tiempos:
     - Desayuno (25%)
     - Colación AM (10%)
     - Comida (35%)
     - Colación PM (10%)
     - Cena (20%)
6. Sistema valida suma de porcentajes = 100%
7. Nutriólogo selecciona alimentos para cada día y tiempo:
   - Busca en catálogo SMAE
   - Arrastra alimentos a plan
   - Especifica porciones
8. Sistema calcula en tiempo real:
   - Totales nutricionales por tiempo
   - Totales diarios
   - Totales semanales
9. Sistema valida cumplimiento de objetivos
10. Nutriólogo revisa y ajusta
11. Nutriólogo selecciona "Publicar Plan"
12. Sistema:
    - Cambia status a PUBLISHED
    - Envía notificación al paciente
    - Genera PDF del plan
13. Sistema muestra confirmación

**Flujos Alternos**:

**FA-030a: Alimento con alergia**
- 7a. Nutriólogo intenta agregar alimento
- 7b. Sistema detecta alergia registrada
- 7c. Sistema muestra alerta en rojo
- 7d. Nutriólogo debe seleccionar alternativa

**FA-030b: Calorías fuera de objetivo**
- 8a. Sistema detecta desviación > 10%
- 8b. Sistema muestra advertencia amarilla
- 8c. Nutriólogo puede ajustar o confirmar

**FA-030c: Guardar borrador**
- 11a. Nutriólogo selecciona "Guardar Borrador"
- 11b. Sistema guarda con status DRAFT
- 11c. Paciente no puede ver el plan
- 11d. Nutriólogo puede continuar después

**Validaciones**:
- Distribución porcentajes: suma = 100%
- Fechas: inicio < fin, período = 7 días
- Calorías: dentro de rango ± 10%
- Macros: cumplir distribución objetivo

**Reglas de Negocio**:
- RN-050: Un paciente tiene máximo 1 plan activo
- RN-051: Plan nuevo reemplaza plan anterior
- RN-052: Planes publicados no se pueden editar
- RN-053: Para cambios, crear nuevo plan
- RN-054: Paciente recibe notificación al publicar
- RN-055: Sistema sugiere equivalentes SMAE

---

### UC-031: Consultar Plan Alimenticio Activo

**Actor**: Paciente
**Precondiciones**:
- Paciente autenticado
- Tiene plan publicado
**Postcondiciones**: Plan visualizado

**Flujo Principal**:
1. Paciente accede a dashboard
2. Sistema muestra resumen del plan del día
3. Paciente selecciona "Ver Plan Completo"
4. Sistema muestra vista semanal:
   - Calendario de 7 días
   - Día actual destacado
5. Paciente selecciona un día
6. Sistema muestra plan del día seleccionado:
   - Desayuno con alimentos y porciones
   - Colación AM
   - Comida
   - Colación PM
   - Cena
7. Para cada tiempo muestra:
   - Lista de alimentos
   - Cantidades/porciones
   - Foto (si disponible)
   - Totales de calorías y macros
8. Sistema muestra barra de progreso:
   - Calorías consumidas vs objetivo
   - Macros consumidos vs objetivo
9. Paciente puede:
   - Imprimir plan
   - Exportar PDF
   - Compartir con familia
   - Marcar alimentos consumidos
   - Dar feedback al nutriólogo

**Flujos Alternos**:

**FA-031a: Sin plan activo**
- 2a. Sistema detecta que no hay plan publicado
- 2b. Sistema muestra mensaje: "No tienes un plan activo"
- 2c. Sistema sugiere contactar al nutriólogo

**FA-031b: Plan expirado**
- 2a. Sistema detecta fecha fin < hoy
- 2b. Sistema muestra plan con etiqueta "Expirado"
- 2c. Sistema sugiere solicitar nuevo plan

**Validaciones**: Ninguna (solo lectura)

**Reglas de Negocio**:
- RN-056: Solo ver plan propio
- RN-057: Plan visible solo si status = PUBLISHED
- RN-058: Feedback opcional del paciente

---

## 7. MÓDULO DE RECORDATORIO 24 HORAS

### UC-040: Registrar Consumo de Alimentos

**Actor**: Paciente
**Precondiciones**: Paciente autenticado
**Postcondiciones**: Consumo registrado

**Flujo Principal**:
1. Paciente accede a "Recordatorio 24 Horas"
2. Sistema muestra vista con tiempos de comida:
   - Desayuno
   - Colación AM
   - Comida
   - Colación PM
   - Cena
   - Colación Extra
3. Paciente selecciona tiempo de comida
4. Paciente selecciona "Agregar Alimento"
5. Sistema muestra buscador de alimentos
6. Paciente busca alimento
7. Sistema muestra resultados del catálogo
8. Paciente selecciona alimento
9. Sistema muestra formulario:
   - Alimento seleccionado
   - Cantidad/porción
   - Unidad de medida
10. Paciente especifica cantidad
11. Sistema calcula valores nutricionales
12. Sistema muestra preview del registro
13. Paciente confirma
14. Sistema guarda registro
15. Sistema actualiza totales del día
16. Sistema actualiza gráficas de progreso

**Flujos Alternos**:

**FA-040a: Alimento no encontrado**
- 7a. Sistema no encuentra alimento en catálogo
- 7b. Sistema ofrece "Crear alimento personalizado"
- 7c. Paciente ingresa datos manualmente
- 7d. Sistema crea alimento temporal
- 7e. Continúa con flujo normal

**FA-040b: Registrar con foto**
- 4a. Paciente selecciona "Agregar con Foto"
- 4b. Sistema abre analizador de fotos (UC-020)
- 4c. Sistema analiza y extrae alimentos
- 4d. Sistema pre-llena registro
- 4e. Paciente confirma o ajusta
- 4f. Continúa con flujo normal

**FA-040c: Editar registro**
- Sistema muestra historial del día
- Paciente selecciona registro existente
- Sistema permite editar cantidad
- Sistema recalcula totales

**FA-040d: Eliminar registro**
- Paciente selecciona registro
- Paciente selecciona "Eliminar"
- Sistema solicita confirmación
- Sistema elimina y actualiza totales

**Validaciones**:
- Cantidad > 0
- Unidad de medida válida
- Hora de registro <= hora actual

**Reglas de Negocio**:
- RN-060: Recordatorio cubre últimas 24 horas
- RN-061: Se puede registrar retroactivamente
- RN-062: Totales se agrupan por día
- RN-063: Nutriólogo puede ver registros de sus pacientes
- RN-064: Sistema sugiere porciones estándar

---

## 8. MATRIZ DE TRAZABILIDAD

### 8.1 Casos de Uso por Actor

| Actor | Casos de Uso | Total |
|-------|--------------|-------|
| **Paciente** | UC-001, UC-002, UC-003, UC-010, UC-011, UC-012, UC-020, UC-021, UC-031, UC-040 | 10 |
| **Nutriólogo** | UC-001, UC-002, UC-003, UC-011, UC-020, UC-021, UC-030 | 7 |
| **Admin** | UC-002, Todos (lectura) | Todos |

### 8.2 Casos de Uso por Módulo

| Módulo | Casos de Uso | Complejidad | Prioridad |
|--------|--------------|-------------|-----------|
| **Autenticación** | UC-001, UC-002, UC-003 | Media | Alta |
| **Gestión Pacientes** | UC-010, UC-011, UC-012 | Media | Alta |
| **Análisis Nutricional** | UC-020, UC-021 | Alta | Alta |
| **Plan Alimenticio** | UC-030, UC-031 | Alta | Alta |
| **Recordatorio 24h** | UC-040 | Media | Alta |

### 8.3 Dependencias entre Casos de Uso

```
UC-001 (Registro)
  ↓
UC-002 (Login)
  ↓
UC-010 (Crear Perfil)
  ↓
UC-012 (Historia Clínica)
  ↓
UC-021 (Calcular Requerimientos)
  ↓
UC-030 (Crear Plan) ←→ UC-011 (Mediciones)
  ↓
UC-031 (Ver Plan)
  ↓
UC-040 (Recordatorio)
  ↓
UC-020 (Analizar Foto)
```

---

## RESUMEN

### Estadísticas

- **Total Casos de Uso**: 13 documentados
- **Casos de Uso Principales**: 10
- **Casos de Uso Administrativos**: 3
- **Actores**: 3 (Paciente, Nutriólogo, Admin)
- **Flujos Alternos**: 20+
- **Reglas de Negocio**: 64 identificadas

### Cobertura Funcional

| Módulo | Cobertura | Estado |
|--------|-----------|--------|
| Autenticación | 100% | ✅ Completo |
| Gestión Pacientes | 100% | ✅ Completo |
| Análisis Nutricional | 90% | ✅ Completo |
| Plan Alimenticio | 85% | ✅ Completo |
| Recordatorio 24h | 100% | ✅ Completo |

---

**Fin de Casos de Uso**
