# CATÁLOGO DE COMPONENTES Y SERVICIOS
## Nutrition Intelligence Platform

**Versión**: 1.0
**Fecha**: 2025-11-05
**Autor**: Arquitectura de Software - Equipo de Desarrollo
**Dominio**: https://nutrition-intelligence.scram2k.com

---

## TABLA DE CONTENIDOS

1. [Componentes del Sistema](#componentes-del-sistema)
2. [Servicios Backend](#servicios-backend)
3. [Componentes Frontend](#componentes-frontend)
4. [Servicios Externos](#servicios-externos)
5. [Infraestructura](#infraestructura)
6. [Base de Datos](#base-de-datos)

---

## 1. COMPONENTES DEL SISTEMA

### 1.1 Visión General

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO FINAL                            │
│              (Paciente / Nutriólogo / Admin)                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                     HTTPS / Port 443
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FRONTEND - React 18                          │  │
│  │  - Material-UI v6                                        │  │
│  │  - 44 Componentes                                        │  │
│  │  - React Router                                          │  │
│  │  - Axios (HTTP Client)                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                       REST API / JSON
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              BACKEND API - FastAPI                        │  │
│  │  - 18 Routers                                            │  │
│  │  - 95+ Endpoints                                         │  │
│  │  - JWT Authentication                                    │  │
│  │  - CORS Middleware                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    CAPA DE DOMINIO                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         MODELOS DE NEGOCIO - SQLModel                    │  │
│  │  - 14 Dominios                                           │  │
│  │  - Lógica de Negocio                                     │  │
│  │  - Validaciones                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    CAPA DE SERVICIOS                             │
│  ┌──────────────┬──────────────┬──────────────┬─────────────┐  │
│  │  AI Vision   │  Email       │  WhatsApp    │   Storage   │  │
│  │  Service     │  Service     │  Service     │   Service   │  │
│  └──────────────┴──────────────┴──────────────┴─────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    CAPA DE DATOS                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         PostgreSQL 16 + Redis 7                          │  │
│  │  - 15+ Tablas                                            │  │
│  │  - Relaciones                                            │  │
│  │  - Índices                                               │  │
│  │  - Cache                                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. SERVICIOS BACKEND

### 2.1 Authentication Service

**Componente**: `api/routers/auth_complete.py`
**Responsabilidad**: Gestión completa de autenticación y autorización

**Funciones principales**:
- Registro de usuarios (pacientes y nutriólogos)
- Login con JWT
- Recuperación de contraseña
- Validación de tokens
- Gestión de refresh tokens

**Endpoints**:
| Método | Ruta | Descripción | Seguridad |
|--------|------|-------------|-----------|
| POST | `/api/v1/auth/register` | Registro de usuario | Público |
| POST | `/api/v1/auth/login` | Login | Público |
| POST | `/api/v1/auth/logout` | Logout | Autenticado |
| POST | `/api/v1/auth/forgot-password` | Solicitar reset | Público |
| POST | `/api/v1/auth/reset-password` | Reset con token | Público |
| GET | `/api/v1/auth/validate-nutritionist/{email}` | Validar nutriólogo | Público |

**Modelos utilizados**:
- `AuthUser` - Usuario principal
- `PasswordResetToken` - Tokens de recuperación

**Dependencias**:
- `core.security` - JWT y hashing
- `core.database` - Sesión de BD
- `services.email_service` - Envío de emails

---

### 2.2 Patient Management Service

**Componente**: `api/routers/patients.py`
**Responsabilidad**: Gestión de perfiles de pacientes y datos clínicos

**Funciones principales**:
- CRUD de perfiles de pacientes
- Gestión de mediciones antropométricas
- Historia clínica
- Archivos clínicos

**Endpoints**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| GET | `/api/v1/patients/me` | Ver mi perfil | PATIENT |
| POST | `/api/v1/patients/me` | Crear perfil | PATIENT |
| PUT | `/api/v1/patients/me` | Actualizar perfil | PATIENT |
| GET | `/api/v1/patients/{id}` | Ver paciente | NUTRITIONIST |
| GET | `/api/v1/patients/me/anthropometrics` | Mis mediciones | PATIENT |
| POST | `/api/v1/patients/me/anthropometrics` | Nueva medición | PATIENT, NUTRITIONIST |
| GET | `/api/v1/patients/me/medical-history` | Mi historia | PATIENT |
| POST | `/api/v1/patients/me/medical-history` | Crear historia | PATIENT |

**Modelos utilizados**:
- `Patient` - Perfil del paciente
- `AnthropometricRecord` - Mediciones corporales
- `MedicalHistory` - Historia clínica

**Validaciones**:
- Edad: >= 2 años
- Peso: 20-300 kg
- Altura: 50-250 cm
- IMC: calculado automáticamente

---

### 2.3 Food Management Service

**Componente**: `api/routers/foods.py`
**Responsabilidad**: Gestión del catálogo de alimentos SMAE

**Funciones principales**:
- CRUD de alimentos
- Búsqueda y filtrado
- Aprobación de alimentos
- Categorización SMAE

**Endpoints**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| GET | `/api/v1/foods` | Listar alimentos | Todos |
| GET | `/api/v1/foods/{id}` | Ver alimento | Todos |
| POST | `/api/v1/foods` | Crear alimento | NUTRITIONIST, ADMIN |
| PUT | `/api/v1/foods/{id}` | Actualizar | NUTRITIONIST, ADMIN |
| POST | `/api/v1/foods/{id}/approve` | Aprobar | ADMIN |
| POST | `/api/v1/foods/{id}/reject` | Rechazar | ADMIN |
| GET | `/api/v1/foods/categories` | Categorías | Todos |
| GET | `/api/v1/foods/search/suggestions` | Sugerencias | Todos |

**Categorías SMAE**:
1. CEREALS - Cereales y tubérculos
2. VEGETABLES - Verduras
3. FRUITS - Frutas
4. LEGUMES - Leguminosas
5. MEATS_LOW_FAT - Carnes bajas en grasa
6. MEATS_MEDIUM_FAT - Carnes medias en grasa
7. MEATS_HIGH_FAT - Carnes altas en grasa
8. MILK_SKIMMED - Leches descremadas
9. MILK_SEMI_SKIMMED - Leches semidescremadas
10. MILK_WHOLE - Leches enteras
11. FATS - Grasas
12. SUGARS - Azúcares

**Modelos utilizados**:
- `Food` - Alimento principal
- `FoodEquivalent` - Equivalentes SMAE
- `NutritionalGoal` - Metas nutricionales

---

### 2.4 AI Vision Service

**Componente**: `services/ai/vision.py`
**Responsabilidad**: Análisis de imágenes de alimentos con IA

**Funciones principales**:
- Análisis de fotos con Gemini Vision
- Fallback a Claude Vision
- Detección de platillos mexicanos
- Cálculo nutricional
- Análisis NOM-051

**Endpoint**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| POST | `/api/v1/vision/analyze-food` | Analizar foto | Autenticado |
| GET | `/api/v1/vision/health` | Health check | Todos |
| GET | `/api/v1/vision/config` | Configuración | ADMIN |

**Configuración**:
```python
AI_VISION_MODEL: "hybrid"  # gemini | claude | hybrid
AI_VISION_CONFIDENCE_THRESHOLD: 75
MAX_FILE_SIZE: 10_000_000  # 10 MB
ALLOWED_FORMATS: [".jpg", ".jpeg", ".png", ".webp"]
```

**Prompt especializado**:
- 170 líneas de instrucciones
- Enfocado en comida mexicana
- Análisis NOM-051
- Clasificación SMAE
- Recomendaciones personalizadas

**Response Schema**:
```json
{
  "dish_name": "Tacos de carne asada",
  "confidence": 92,
  "total_calories": 450,
  "total_protein_g": 28,
  "total_carbs_g": 35,
  "total_fat_g": 18,
  "ingredients": [
    {
      "name": "Tortillas de maíz",
      "quantity": "3 piezas",
      "calories": 165,
      "category": "CEREALS"
    }
  ],
  "nom051_seals": ["EXCESS_CALORIES", "EXCESS_FATS"],
  "health_score": 7,
  "recommendations": ["Agregar verduras", "Moderar consumo"]
}
```

---

### 2.5 Nutrition Calculator Service

**Componente**: `api/routers/nutrition_calculator.py`
**Responsabilidad**: Cálculos de requerimientos nutricionales

**Funciones principales**:
- Cálculo de TMB (Tasa Metabólica Basal)
- Cálculo de TDEE (Total Daily Energy Expenditure)
- Distribución de macronutrientes
- Creación de planes nutricionales

**Endpoints**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| POST | `/api/v1/nutrition-calculator/calculate-bmr` | Calcular TMB | Autenticado |
| POST | `/api/v1/nutrition-calculator/calculate-tdee` | Calcular TDEE | Autenticado |
| POST | `/api/v1/nutrition-calculator/calculate-macros` | Calcular macros | Autenticado |
| POST | `/api/v1/nutrition-calculator/create-nutrition-plan` | Crear plan | NUTRITIONIST |
| GET | `/api/v1/nutrition-calculator/activity-levels` | Niveles actividad | Todos |
| GET | `/api/v1/nutrition-calculator/nutritional-goals` | Objetivos | Todos |

**Fórmulas utilizadas**:

**TMB (Harris-Benedict Revisado)**:
- Hombres: `66.47 + (13.75 × peso_kg) + (5.003 × altura_cm) - (6.755 × edad)`
- Mujeres: `655.1 + (9.563 × peso_kg) + (1.850 × altura_cm) - (4.676 × edad)`

**TDEE (Factor de actividad)**:
- Sedentario: TMB × 1.2
- Ligera actividad: TMB × 1.375
- Moderada: TMB × 1.55
- Intensa: TMB × 1.725
- Muy intensa: TMB × 1.9

**Distribución de macros**:
- Proteína: 1.6-2.2 g/kg peso corporal
- Grasas: 20-35% de calorías totales
- Carbohidratos: Resto de calorías

---

### 2.6 Meal Planning Service

**Componente**: `api/routers/weekly_planning.py`
**Responsabilidad**: Planificación de menús semanales

**Funciones principales**:
- Creación de planes semanales
- Distribución por tiempos de comida
- Asignación de equivalentes SMAE
- Publicación de planes

**Endpoints**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| POST | `/api/v1/weekly-planning/create-weekly-plan` | Crear plan semanal | NUTRITIONIST |
| GET | `/api/v1/weekly-planning/weekly-plans` | Mis planes | PATIENT |
| GET | `/api/v1/weekly-planning/weekly-plans/{id}` | Ver plan | PATIENT, NUTRITIONIST |
| GET | `/api/v1/weekly-planning/weekly-plans/{id}/daily-plans` | Planes diarios | PATIENT |
| POST | `/api/v1/weekly-planning/weekly-plans/{id}/publish` | Publicar | NUTRITIONIST |
| POST | `/api/v1/weekly-planning/weekly-plans/{id}/feedback` | Dar feedback | PATIENT |
| GET | `/api/v1/weekly-planning/meal-times` | Tiempos de comida | Todos |
| GET | `/api/v1/weekly-planning/weekdays` | Días de la semana | Todos |

**Tiempos de comida**:
1. **Desayuno** - 25% calorías diarias
2. **Colación AM** - 10%
3. **Comida** - 35%
4. **Colación PM** - 10%
5. **Cena** - 20%

**Estructura del plan**:
```json
{
  "patient_id": 1,
  "start_date": "2025-11-05",
  "end_date": "2025-11-11",
  "daily_calories": 2000,
  "daily_protein_g": 150,
  "daily_carbs_g": 200,
  "daily_fat_g": 67,
  "status": "published",
  "daily_distribution": {
    "desayuno": {"percentage": 25, "calories": 500},
    "colacion1": {"percentage": 10, "calories": 200},
    "comida": {"percentage": 35, "calories": 700},
    "colacion2": {"percentage": 10, "calories": 200},
    "cena": {"percentage": 20, "calories": 400}
  },
  "weekly_schedule": [
    {
      "day": "lunes",
      "desayuno": [...],
      "colacion1": [...],
      "comida": [...],
      "colacion2": [...],
      "cena": [...]
    }
  ]
}
```

---

### 2.7 Laboratory Service

**Componente**: `api/routers/laboratory.py`
**Responsabilidad**: Gestión de estudios de laboratorio

**Funciones principales**:
- Registro de resultados
- Upload de archivos PDF
- Análisis de tendencias
- Interpretación con IA

**Endpoints**:
| Método | Ruta | Descripción | Roles |
|--------|------|-------------|-------|
| POST | `/api/v1/laboratory` | Crear registro | PATIENT, NUTRITIONIST |
| GET | `/api/v1/laboratory/{id}` | Ver registro | PATIENT, NUTRITIONIST |
| GET | `/api/v1/laboratory/patient/{id}` | Historial paciente | PATIENT, NUTRITIONIST |
| PUT | `/api/v1/laboratory/{id}` | Actualizar | PATIENT, NUTRITIONIST |
| DELETE | `/api/v1/laboratory/{id}` | Eliminar | PATIENT, NUTRITIONIST |
| GET | `/api/v1/laboratory/trends/patient/{id}` | Tendencias | PATIENT, NUTRITIONIST |
| POST | `/api/v1/laboratory/{id}/reanalyze` | Re-analizar | NUTRITIONIST |
| POST | `/api/v1/laboratory/files` | Crear archivo | PATIENT, NUTRITIONIST |
| GET | `/api/v1/laboratory/files/patient/{id}` | Archivos paciente | PATIENT, NUTRITIONIST |
| POST | `/api/v1/laboratory/files/upload` | Upload PDF | PATIENT, NUTRITIONIST |

**Tipos de estudios soportados**:
1. Química Sanguínea (25-30 días)
2. Perfil de Lípidos (25-30 días)
3. Hemograma Completo (25-30 días)
4. Función Hepática (25-30 días)
5. Función Renal (25-30 días)
6. Perfil Tiroideo (25-30 días)
7. Hemoglobina Glic ads (90 días)
8. Glucosa en Ayunas (7-14 días)

**Valores de referencia incluidos**:
- Glucosa: 70-100 mg/dL
- Colesterol Total: < 200 mg/dL
- Colesterol LDL: < 100 mg/dL
- Colesterol HDL: > 40 mg/dL (H), > 50 mg/dL (M)
- Triglicéridos: < 150 mg/dL
- HbA1c: < 5.7%
- Creatinina: 0.7-1.3 mg/dL (H), 0.6-1.1 mg/dL (M)
- Ácido Úrico: 3.5-7.2 mg/dL (H), 2.6-6.0 mg/dL (M)

---

### 2.8 Email Service

**Componente**: `services/email_service.py`
**Responsabilidad**: Envío de notificaciones por correo

**Funciones principales**:
- Email de bienvenida
- Recuperación de contraseña
- Notificaciones de planes
- Recordatorios

**Configuración**:
```python
EMAIL_BACKEND: "sendgrid"  # sendgrid | smtp
SENDGRID_API_KEY: "..."
SMTP_HOST: "smtp.gmail.com"
SMTP_PORT: 587
EMAIL_FROM: "noreply@nutrition-intelligence.scram2k.com"
```

**Templates disponibles**:
1. `welcome_email.html` - Bienvenida
2. `password_reset.html` - Recuperación
3. `meal_plan_published.html` - Plan publicado
4. `appointment_reminder.html` - Recordatorio

---

### 2.9 WhatsApp Service (Producción)

**Componente**: `api/routers/whatsapp.py`
**Responsabilidad**: Integración con WhatsApp Business

**Funciones principales**:
- Envío de mensajes
- Recepción de mensajes
- Webhooks
- Templates de mensajes

**Estado**: Implementado en producción

---

## 3. COMPONENTES FRONTEND

### 3.1 Authentication Components

**Componente**: `components/auth/`
**Archivos**:
- `Login.js` - Formulario de login
- `Register.js` - Formulario de registro
- `ForgotPassword.js` - Recuperación de contraseña
- `ResetPassword.js` - Reset con token
- `PrivateRoute.js` - Protección de rutas

**Funcionalidades**:
- Validación de formularios
- Manejo de errores
- Redirección post-login
- Almacenamiento seguro de tokens

---

### 3.2 Dashboard Components

**Componente**: `components/dashboard/RoleBasedDashboard.js`
**Responsabilidad**: Dashboard dinámico según rol

**Vistas**:
1. **Dashboard Paciente**:
   - Resumen nutricional
   - Plan del día
   - Progreso de metas
   - Próxima cita
   - Historial de peso

2. **Dashboard Nutriólogo**:
   - Lista de pacientes
   - Citas del día
   - Tareas pendientes
   - Estadísticas generales

3. **Dashboard Admin**:
   - Estadísticas del sistema
   - Gestión de usuarios
   - Logs de auditoría
   - Configuración

---

### 3.3 Food Analysis Components

**Componente**: `components/analisis-fotos/AnalizadorFotosMejorado.js`
**Responsabilidad**: Análisis de fotos de alimentos

**Funcionalidades**:
- Captura con cámara
- Upload de archivos
- Preview de imagen
- Análisis con IA
- Visualización de resultados
- Guardar en historial

**Librerías utilizadas**:
- `react-webcam` - Captura de cámara
- `framer-motion` - Animaciones
- `@mui/material` - UI Components
- `axios` - HTTP requests

---

### 3.4 Clinical Record Components

**Componente**: `components/expediente/ExpedienteClinico.js`
**Responsabilidad**: Expediente clínico completo

**Secciones**:
1. **DatosGeneralesView** - Datos personales
2. **HistoriaClinicaView** - Historia médica
3. **DatosLaboratorioView** - Estudios de laboratorio
4. **HabitosAlimenticiosView** - Hábitos alimenticios
5. **ActividadFisicaView** - Actividad física
6. **MedicionesAntropometricasView** - Mediciones

**Características**:
- Navegación por pestañas
- Edición inline
- Guardado automático
- Validación de datos

---

### 3.5 Nutrition Calculator Components

**Componente**: `components/calculator/CalculadoraRequerimientos.js`
**Responsabilidad**: Cálculo de requerimientos nutricionales

**Pasos del wizard**:
1. Datos personales (edad, sexo, peso, altura)
2. Nivel de actividad física
3. Objetivo nutricional
4. Resultados y plan

**Visualizaciones**:
- Gráfica de macros (pie chart)
- Distribución de calorías (bar chart)
- Comparativa de actividad

---

### 3.6 Equivalences Components

**Componente**: `components/equivalences/EquivalentesMexicanos.js`
**Responsabilidad**: Navegador de equivalentes SMAE

**Funcionalidades**:
- Navegación por grupos
- Búsqueda de alimentos
- Calculadora de porciones
- Sustituciones inteligentes
- Comparativas nutricionales

**Grupos SMAE**:
- Cereales (tortilla, pan, arroz)
- Verduras
- Frutas
- Leguminosas
- Carnes y sustitutos
- Leches
- Grasas
- Azúcares

---

### 3.7 Meal Planning Components

**Componente**: `components/dietas/GeneradorDietas.js`
**Responsabilidad**: Generador de planes alimenticios

**Funcionalidades**:
- Selección de paciente
- Configuración de calorías
- Distribución por tiempos
- Vista semanal
- Asignación de alimentos
- Publicación de plan

---

### 3.8 24-Hour Recall Components

**Componente**: `components/recordatorio/Recordatorio24Horas.js`
**Responsabilidad**: Recordatorio de 24 horas

**Características**:
- Registro por tiempos de comida
- Búsqueda de alimentos
- Cantidades personalizadas
- Totales nutricionales
- Exportación de datos

**Tiempos de comida**:
- Desayuno
- Colación AM
- Comida
- Colación PM
- Cena
- Colación extra

---

## 4. SERVICIOS EXTERNOS

### 4.1 Google Gemini Vision API

**Proveedor**: Google Cloud
**Servicio**: Generative AI - Vision Models
**Modelo**: `gemini-1.5-flash-latest`

**Uso**:
- Análisis primario de fotos
- Detección de platillos
- Cálculo nutricional

**Configuración**:
```python
GOOGLE_API_KEY: "..."
GEMINI_MODEL: "gemini-1.5-flash-latest"
MAX_TOKENS: 2048
TEMPERATURE: 0.7
```

---

### 4.2 Anthropic Claude API

**Proveedor**: Anthropic
**Servicio**: Claude Vision
**Modelo**: `claude-3-5-sonnet-20241022`

**Uso**:
- Análisis de respaldo (confidence < 75%)
- Validación de resultados
- Análisis detallado

**Configuración**:
```python
ANTHROPIC_API_KEY: "..."
CLAUDE_MODEL: "claude-3-5-sonnet-20241022"
MAX_TOKENS: 4096
```

---

### 4.3 SendGrid Email API

**Proveedor**: SendGrid (Twilio)
**Servicio**: Email Delivery

**Uso**:
- Emails transaccionales
- Notificaciones
- Recuperación de contraseña

**Configuración**:
```python
SENDGRID_API_KEY: "..."
FROM_EMAIL: "noreply@nutrition-intelligence.scram2k.com"
FROM_NAME: "Nutrition Intelligence"
```

---

### 4.4 WhatsApp Business API

**Proveedor**: Meta (Facebook)
**Servicio**: WhatsApp Business Platform

**Uso**:
- Notificaciones push
- Recordatorios
- Chat con pacientes

**Estado**: Implementado en producción

---

## 5. INFRAESTRUCTURA

### 5.1 Servicios Docker

| Servicio | Imagen | Puerto | Descripción |
|----------|--------|--------|-------------|
| **backend** | python:3.11-slim | 8000 | API FastAPI |
| **frontend** | nginx:alpine | 3003 | React App |
| **postgres** | postgres:16 | 5432 | Base de datos |
| **redis** | redis:7-alpine | 6379 | Cache y sesiones |
| **pgadmin** | dpage/pgadmin4 | 5050 | Admin de BD |

---

### 5.2 Networks

**nutrition-network** (interno):
- Backend ↔ PostgreSQL
- Backend ↔ Redis
- Frontend ↔ Backend (via proxy)

**traefik-public** (externo):
- Routing con Traefik
- SSL/TLS automático
- Load balancing

---

### 5.3 Volumes

| Volume | Uso | Persistencia |
|--------|-----|--------------|
| `postgres_data` | Datos de PostgreSQL | Permanente |
| `redis_data` | Cache de Redis | Volátil |
| `pgadmin_data` | Config de PgAdmin | Permanente |
| `backend_data` | Archivos clínicos | Permanente |

---

## 6. BASE DE DATOS

### 6.1 Tablas Principales

**auth_users** (15 columnas):
- Usuarios del sistema
- Roles y permisos
- Estado de cuenta
- Timestamps

**patients** (12 columnas):
- Perfiles de pacientes
- Datos demográficos
- Objetivos nutricionales
- Relación con nutriólogo

**foods** (20 columnas):
- Catálogo de alimentos
- Información nutricional
- Categoría SMAE
- Estado de aprobación

**meal_plans** (10 columnas):
- Planes alimenticios
- Distribución de macros
- Estado de publicación
- Fechas de vigencia

**laboratory_data** (12 columnas):
- Estudios de laboratorio
- Resultados
- Interpretación
- Recomendaciones

**anthropometric_records** (15 columnas):
- Mediciones corporales
- IMC calculado
- Porcentaje de grasa
- Masa muscular

**medical_histories** (10 columnas):
- Historia clínica
- Condiciones médicas
- Alergias e intolerancias
- Medicamentos

**food_equivalents** (10 columnas):
- Equivalentes SMAE
- Porciones
- Conversiones

**recipes** (15 columnas):
- Recetas mexicanas
- Ingredientes
- Instrucciones
- Información nutricional

**audit_logs** (10 columnas):
- Registro de auditoría
- Cambios en entidades
- Usuario responsable
- Timestamp

---

### 6.2 Relaciones

```
auth_users (1) ─────── (1) patients
auth_users (1) ─────── (N) audit_logs
patients (1) ─────────── (N) anthropometric_records
patients (1) ─────────── (1) medical_history
patients (1) ─────────── (N) meal_plans
patients (1) ─────────── (N) laboratory_data
foods (1) ────────────── (1) food_equivalents
foods (N) ────────────── (N) recipes (via recipe_items)
```

---

## RESUMEN

### Métricas del Catálogo

| Categoría | Cantidad |
|-----------|----------|
| **Backend Services** | 9 principales |
| **API Routers** | 18 |
| **API Endpoints** | 95+ |
| **Frontend Components** | 44 |
| **External Services** | 4 |
| **Docker Services** | 5 |
| **Database Tables** | 15+ |
| **Models/Entities** | 20+ |

### Estado de Implementación

| Componente | Estado | Cobertura |
|------------|--------|-----------|
| Authentication | ✅ Completo | 100% |
| Patient Management | ✅ Completo | 100% |
| Food Management | ✅ Completo | 100% |
| AI Vision | ✅ Completo | 100% |
| Meal Planning | ✅ Completo | 90% |
| Laboratory | ✅ Completo | 85% |
| WhatsApp | ✅ En producción | 100% |
| Email Service | ✅ Completo | 100% |
| Frontend Dashboard | ✅ Completo | 95% |
| Mobile App | 🟡 Planificado | 0% |

---

**Fin del Catálogo de Componentes**
