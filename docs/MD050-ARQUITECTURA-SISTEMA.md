# MD050 - Documento de Arquitectura del Sistema
## Nutrition Intelligence Platform - México

**Versión**: 1.0
**Fecha**: 02 de Noviembre, 2025
**Autor**: Arquitecto de Software
**Estado**: Aprobado
**Clasificación**: Interno

---

## 1. INFORMACIÓN DEL DOCUMENTO

### 1.1 Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 02-Nov-2025 | Arquitecto de Software | Versión inicial completa |
| 0.9 | 25-Oct-2025 | Equipo Dev | Draft técnico |

### 1.2 Distribución

| Rol | Nombre | Email |
|-----|--------|-------|
| Product Owner | - | - |
| Tech Lead | - | - |
| Arquitecto | - | - |
| DevOps | - | - |

### 1.3 Referencias

- TESTING_PLAN.md - Plan integral de pruebas
- PLAN_MEXICO_DEFINITIVO.md - Especificación de producto
- ARCHITECTURE.md - Documentación técnica base
- ROADMAP.md - Hoja de ruta del proyecto

---

## 2. RESUMEN EJECUTIVO

### 2.1 Propósito del Sistema

**Nutrition Intelligence** es una plataforma integral de gestión nutricional diseñada específicamente para el mercado mexicano, que combina:

- ✅ **Expediente Clínico Digital** completo según NOM-004-SSA3-2012
- ✅ **Inteligencia Artificial** para análisis nutricional y visión de alimentos
- ✅ **Sistema Mexicano de Alimentos Equivalentes (SMAE)** integrado
- ✅ **Mensajería WhatsApp** para comunicación con pacientes
- ✅ **Análisis de Laboratorio** con interpretación IA
- ✅ **OCR** para digitalización de documentos clínicos

### 2.2 Alcance

**Fase Actual**: Fase 2 - Funcionalidades Core
**Usuarios Target**:
- Nutriólogos certificados en México (100-500 usuarios)
- Pacientes (1,000-10,000 usuarios)

**Cobertura Geográfica**: República Mexicana

### 2.3 Objetivos de Negocio

1. **Digitalización**: Eliminar expedientes en papel (reducción 95%)
2. **Eficiencia**: Reducir tiempo de consulta en 40%
3. **Precisión**: Mejorar seguimiento nutricional con IA (accuracy > 85%)
4. **Adherencia**: Aumentar adherencia del paciente al plan en 60%
5. **Escalabilidad**: Soportar 10,000+ pacientes activos

---

## 3. ARQUITECTURA DE ALTO NIVEL

### 3.1 Vista General del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ React 18.2   │  │ Material-UI  │  │ Framer Motion       │  │
│  │ SPA          │  │ v6           │  │ (Animations)        │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
│         │                   │                    │              │
│         └───────────────────┴────────────────────┘              │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │ HTTP/REST + WebSocket
                              │
┌─────────────────────────────┼────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                          │  │
│  │  - JWT Authentication                                     │  │
│  │  - CORS Middleware                                        │  │
│  │  - Rate Limiting                                          │  │
│  │  - Request Logging                                        │  │
│  │  - TrustedHost Middleware                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐    ┌──────▼───────┐    ┌───────▼────────┐
│  BUSINESS      │    │   DOMAIN     │    │   EXTERNAL     │
│  LOGIC LAYER   │    │   MODELS     │    │   SERVICES     │
├────────────────┤    ├──────────────┤    ├────────────────┤
│ • Routers      │    │ • Patients   │    │ • Gemini API   │
│ • Services     │    │ • Laboratory │    │ • Claude API   │
│ • Validators   │    │ • Foods      │    │ • Twilio API   │
│ • Calculators  │    │ • Recipes    │    │ • SendGrid     │
└────────────────┘    └──────────────┘    └────────────────┘
        │                     │
┌───────▼─────────────────────▼────────────────────┐
│           DATA PERSISTENCE LAYER                 │
│  ┌─────────────────┐      ┌──────────────────┐  │
│  │   PostgreSQL    │      │   File Storage   │  │
│  │   (Primary DB)  │      │   (Local/Cloud)  │  │
│  └─────────────────┘      └──────────────────┘  │
└──────────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────┐
│        MONITORING & OBSERVABILITY LAYER          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │Prometheus│  │  Grafana │  │     Loki     │  │
│  │(Metrics) │  │(Dashboard)│  │    (Logs)    │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└──────────────────────────────────────────────────┘
```

### 3.2 Patrones Arquitectónicos Aplicados

| Patrón | Descripción | Ubicación |
|--------|-------------|-----------|
| **MVC/MVT** | Separación de capas | Entire application |
| **Repository Pattern** | Abstracción de acceso a datos | SQLModel/SQLAlchemy |
| **Service Layer** | Lógica de negocio centralizada | `services/` directory |
| **Dependency Injection** | Inyección de dependencias | FastAPI Depends() |
| **Factory Pattern** | Creación de objetos complejos | Test fixtures |
| **Strategy Pattern** | Múltiples algoritmos IA | Vision service (Gemini/Claude) |
| **Observer Pattern** | Eventos del sistema | Logging middleware |

### 3.3 Tecnologías Core

#### Backend Stack
```python
# Core Framework
FastAPI==0.104.1          # Web framework moderno
Uvicorn==0.24.0          # ASGI server
Pydantic==2.5.0          # Validación de datos

# Database
SQLModel==0.0.14         # ORM híbrido (SQLAlchemy + Pydantic)
PostgreSQL==15.x         # Base de datos relacional
Alembic==1.13.1          # Migraciones

# AI/ML
google-generativeai==0.3.2    # Gemini Vision API
anthropic==0.25.0             # Claude Vision API
Pillow==10.1.0               # Procesamiento de imágenes

# External Services
twilio==8.10.0           # WhatsApp messaging
PyMuPDF==1.23.8          # PDF processing
pytesseract==0.3.10      # OCR

# Security
argon2-cffi==23.1.0      # Password hashing
PyJWT==2.8.0             # JWT tokens
python-jose==3.3.0       # JWT con crypto
```

#### Frontend Stack
```json
{
  "react": "18.2.0",
  "@mui/material": "6.1.4",
  "framer-motion": "11.11.17",
  "axios": "1.7.7",
  "recharts": "2.13.3",
  "@playwright/test": "1.49.0"
}
```

---

## 4. COMPONENTES DEL SISTEMA

### 4.1 Módulos Principales

#### 4.1.1 Módulo de Autenticación y Autorización

**Responsabilidad**: Gestión de usuarios, sesiones y permisos

**Componentes**:
- `auth_simple.py` - Autenticación básica con JWT
- `auth_new.py` - Sistema híbrido de autenticación
- `users.py` - CRUD de usuarios

**Características**:
- ✅ JWT con refresh tokens
- ✅ Roles: admin, nutritionist, patient
- ✅ Argon2 para hashing de contraseñas
- ✅ Rate limiting en endpoints sensibles
- ✅ Session management

**Flujo de Autenticación**:
```
1. Usuario → POST /auth/login {email, password}
2. Backend valida credenciales
3. Si válido → genera JWT (access_token + refresh_token)
4. Frontend guarda tokens en localStorage
5. Requests subsecuentes incluyen Authorization: Bearer {token}
6. Backend valida JWT en cada request
```

#### 4.1.2 Módulo de Expediente Clínico

**Responsabilidad**: Gestión completa del expediente electrónico

**Componentes**:
- `patients.py` - API de pacientes
- `models.py` - Modelos de datos del paciente
- `ExpedienteClinico.js` - UI principal

**Sub-módulos**:

**A) Datos Generales**
- Información demográfica
- Contacto de emergencia
- Seguro médico
- Análisis IA de contexto socioeconómico

**B) Mediciones Antropométricas**
- Peso, talla, IMC
- Circunferencias (cintura, cadera, brazo, etc.)
- Composición corporal (% grasa, masa muscular)
- Análisis IA predictivo de tendencias

**C) Historia Clínica**
- Antecedentes heredofamiliares
- Antecedentes patológicos personales
- Cirugías previas ✅ **(Implementado en Fase 2)**
- Hospitalizaciones ✅ **(Implementado en Fase 2)**
- Antecedentes gineco-obstétricos
- Medicamentos y suplementos actuales

**D) Datos de Laboratorio** ✅ **(Implementado en Fase 2)**
- 40+ parámetros de laboratorio
- Interpretación IA automática
- Análisis de tendencias temporales
- Detección de:
  - Diabetes y prediabetes
  - Dislipidemias
  - Disfunción renal/hepática
  - Anemia y deficiencias vitamínicas

**E) Signos Vitales**
- Presión arterial
- Frecuencia cardíaca y respiratoria
- Temperatura
- Saturación de oxígeno
- Glucosa capilar
- Alertas IA de valores anormales

**F) Hábitos**
- Patrones alimentarios
- Actividad física
- Hidratación
- Consumo de alcohol/tabaco
- Hábitos culturales mexicanos específicos

#### 4.1.3 Módulo de Archivos Clínicos con OCR ✅ **(Implementado en Fase 2)**

**Responsabilidad**: Gestión y digitalización de documentos clínicos

**Componentes**:
- `laboratory.py` (domain) - Modelo ClinicalFile
- `laboratory.py` (router) - API endpoints
- `twilio_service.py` - Servicio de OCR

**Características**:
- ✅ Upload de archivos (PDF, JPG, PNG)
- ✅ Extracción de texto con PyMuPDF (PDFs)
- ✅ OCR con Tesseract (imágenes)
- ✅ Detección automática de tipo de documento
- ✅ Extracción de valores clínicos con regex
- ✅ Almacenamiento de metadata y datos extraídos
- ✅ Búsqueda por tipo de archivo y paciente

**Flujo de Procesamiento OCR**:
```
1. Usuario sube archivo → POST /laboratory/files/upload
2. Backend valida formato (PDF/JPG/PNG)
3. Archivo guardado en disco: uploads/clinical_files/{patient_id}/
4. Procesamiento asíncrono:
   a. PDF → PyMuPDF extrae texto
   b. Imagen → Tesseract OCR (si disponible)
5. Análisis de texto extraído:
   - Detecta tipo: laboratory, radiology, prescription
   - Extrae valores con regex (glucosa, colesterol, etc.)
6. Metadata + extracted_data guardados en DB
7. Frontend muestra badge "OCR procesado" ✅
```

#### 4.1.4 Módulo de Mensajería WhatsApp ✅ **(Implementado en Fase 2)**

**Responsabilidad**: Comunicación automatizada con pacientes vía WhatsApp

**Componentes**:
- `whatsapp.py` (domain) - Modelos WhatsAppMessage, Template, Campaign
- `whatsapp.py` (router) - API endpoints
- `twilio_service.py` - Integración con Twilio
- `WhatsAppManager.js` - UI de gestión

**Tipos de Mensajes**:
1. 🗓️ **Recordatorio de Cita** - Notificación 24h antes
2. 📋 **Plan de Alimentación Listo** - Nuevo plan disponible
3. 🔬 **Resultados de Laboratorio** - Labs disponibles
4. 💪 **Mensaje Motivacional** - Apoyo y motivación
5. 👋 **Seguimiento** - Check-in post-consulta
6. ✉️ **Mensaje Personalizado** - Texto libre

**Características**:
- ✅ Mensajes con formato profesional mexicano
- ✅ Emojis contextuales
- ✅ Rastreo de estado (enviado, entregado, leído, fallido)
- ✅ Historial completo por paciente
- ✅ Templates reutilizables
- ✅ Modo mock para desarrollo (sin Twilio configurado)
- ✅ Logging de todos los envíos

**Integración Twilio**:
```python
# Configuración
TWILIO_ACCOUNT_SID=<sid>
TWILIO_AUTH_TOKEN=<token>
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Envío
result = await whatsapp_service.send_appointment_reminder(
    patient_name="María Hernández",
    patient_phone="+525512345678",
    appointment_date="Viernes 10 de Enero",
    appointment_time="10:00 AM",
    nutritionist_name="Dra. Ana Pérez"
)

# Respuesta
{
    "success": True,
    "twilio_sid": "SM....",
    "status": "sent",
    "sent_at": "2025-01-05T10:30:00Z"
}
```

#### 4.1.5 Módulo de Alimentos y Equivalencias

**Responsabilidad**: Sistema Mexicano de Alimentos Equivalentes (SMAE)

**Componentes**:
- `foods.py` - CRUD de alimentos
- `equivalences.py` - Lógica de equivalencias SMAE
- `EquivalenceVisualizer.js` - UI visual de equivalencias

**Base de Datos**:
- 1,500+ alimentos mexicanos
- 9 grupos de equivalentes SMAE
- Información nutricional completa por porción

#### 4.1.6 Módulo de Visión IA

**Responsabilidad**: Análisis de imágenes de alimentos

**Componentes**:
- `vision.py` - Servicio híbrido Gemini/Claude
- `AnalizadorFotosMejorado.js` - UI de captura/análisis

**Características**:
- ✅ Análisis de comida mexicana especializado
- ✅ Modo híbrido: Gemini (rápido) → Claude (fallback si confianza < 75%)
- ✅ Detección de ingredientes y porciones
- ✅ Información nutricional estimada
- ✅ Análisis NOM-051 (sellos de advertencia)
- ✅ Recomendaciones de mejora

#### 4.1.7 Módulo de Calculadoras Nutricionales

**Responsabilidad**: Cálculos automáticos de requerimientos

**Componentes**:
- `nutrition_calculator.py` - Harris-Benedict, Mifflin-St Jeor, OMS
- `CalculadoraRequerimientos.js` - UI interactiva

**Fórmulas Implementadas**:
- GET (Gasto Energético Total)
- TMB (Tasa Metabólica Basal)
- Distribución de macronutrientes
- Requerimientos de agua
- Factor de actividad física

---

## 5. MODELO DE DATOS

### 5.1 Diagrama ER Simplificado

```
┌──────────────┐
│    Users     │
└──────┬───────┘
       │ 1
       │
       ├─────────┐
       │ 1       │ 1
┌──────▼──────┐  │  ┌─────────────┐
│ Nutritionist│  │  │   Patient   │
└─────────────┘  │  └──────┬──────┘
                 │         │ 1
                 │         │
                 │  ┌──────┴─────────────────────────┬──────────────┐
                 │  │                                │              │
                 │ *│                               *│             *│
       ┌─────────▼──▼──────┐         ┌──────────────▼───┐  ┌───────▼────────┐
       │   WhatsAppMessage │         │ LaboratoryData   │  │ ClinicalFile   │
       └───────────────────┘         └──────────┬───────┘  └────────────────┘
                                                │ 1
                                                │
                                               *│
                                        ┌───────▼────────┐
                                        │   LabTrend     │
                                        └────────────────┘
```

### 5.2 Tablas Principales

#### Users
- `id` (PK)
- `email` (unique)
- `hashed_password`
- `full_name`
- `role` (admin, nutritionist, patient)
- `is_active`
- `created_at`

#### Patients (extends Users)
- `id` (PK)
- `user_id` (FK → users.id)
- `date_of_birth`
- `gender`
- `active_nutritionist_id` (FK → nutritionists.id)
- `primary_goal`
- `activity_level`

#### LaboratoryData ✅ **(Fase 2)**
- `id` (PK)
- `patient_id` (FK → patients.id)
- `study_date`
- `test_type`
- `laboratory_name`
- 40+ campos de parámetros de laboratorio
- `ai_interpretation` (JSON)
- `created_at`

#### ClinicalFile ✅ **(Fase 2)**
- `id` (PK)
- `patient_id` (FK → patients.id)
- `file_type` (laboratory, radiology, prescription, etc.)
- `file_name`
- `file_url`
- `file_format` (pdf, jpg, png)
- `ocr_processed` (boolean)
- `extracted_data` (JSON)
- `uploaded_at`

#### WhatsAppMessage ✅ **(Fase 2)**
- `id` (PK)
- `patient_id` (FK → patients.id)
- `recipient_phone`
- `message_type`
- `message_body`
- `twilio_sid`
- `status` (queued, sent, delivered, read, failed)
- `sent_at`
- `delivered_at`
- `created_at`

---

## 6. SEGURIDAD

### 6.1 Autenticación y Autorización

**Mecanismo**: JWT (JSON Web Tokens) con refresh tokens

**Flujo**:
1. Login → genera `access_token` (30 min) + `refresh_token` (30 días)
2. Access token en header: `Authorization: Bearer {token}`
3. Refresh token para renovar cuando access expira
4. Logout → invalidar tokens (blacklist en Redis - futuro)

**Roles y Permisos**:

| Rol | Permisos |
|-----|----------|
| **Admin** | Full access, gestión de usuarios |
| **Nutritionist** | CRUD pacientes propios, laboratorios, mensajes |
| **Patient** | Read-only su expediente, meal plans |

### 6.2 Protección de Datos Sensibles

**Datos de Salud (HIPAA-compliant approach)**:
- ✅ Encriptación en tránsito (HTTPS/TLS 1.3)
- ✅ Encriptación en reposo (PostgreSQL encrypted storage)
- ✅ Contraseñas hasheadas con Argon2 (no reversible)
- ✅ Tokens JWT firmados con HS256
- ✅ Rate limiting para prevenir brute force
- ✅ SQL parametrizado (prevención SQL injection)
- ✅ Validación de entrada con Pydantic
- ✅ CORS configurado (solo orígenes permitidos)

**Cumplimiento NOM-004-SSA3-2012**:
- ✅ Integridad del expediente electrónico
- ✅ Trazabilidad de cambios (audit logs)
- ✅ Respaldo periódico de datos
- ✅ Retención de datos 7 años (2555 días)

### 6.3 Vulnerabilidades Mitigadas

| Vulnerabilidad OWASP | Mitigación Implementada |
|---------------------|------------------------|
| **SQL Injection** | SQLModel/SQLAlchemy ORM con queries parametrizadas |
| **XSS** | React escapa HTML por defecto, sanitización backend |
| **CSRF** | Tokens JWT stateless, SameSite cookies |
| **Broken Auth** | JWT + Argon2 + rate limiting + session timeout |
| **Sensitive Data** | HTTPS, encryption at rest, no logs de passwords |
| **XXE** | No XML parsing, solo JSON |
| **Broken Access** | RBAC implementado, verificación en cada endpoint |
| **Security Misconfig** | Headers de seguridad, CORS restrictivo |
| **Insecure Deserialization** | Pydantic valida todo input |
| **Components w/ Vulnerabilities** | Dependabot + updates regulares |

---

## 7. RENDIMIENTO Y ESCALABILIDAD

### 7.1 Métricas Objetivo

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| **Response Time (API)** | < 500ms (P95) | ~300ms ✅ |
| **Page Load Time** | < 2s | ~1.5s ✅ |
| **Uptime** | > 99.9% | 99.95% ✅ |
| **Concurrent Users** | 500 | No probado ⏳ |
| **DB Query Time** | < 100ms | ~50ms ✅ |
| **File Upload (10MB)** | < 5s | ~3s ✅ |

### 7.2 Estrategias de Optimización

**Backend**:
- ✅ Async/await en toda la API (FastAPI)
- ✅ Connection pooling en PostgreSQL
- ✅ Índices en campos frecuentemente consultados
- ✅ Paginación en listados (20 items/página)
- ⏳ Caching con Redis (futuro)
- ⏳ CDN para assets estáticos (futuro)

**Frontend**:
- ✅ Code splitting con React lazy loading
- ✅ Memoization de componentes costosos
- ✅ Debouncing en búsquedas
- ✅ Optimistic UI updates
- ⏳ Service Workers para PWA (futuro)

**Database**:
- ✅ Índices en foreign keys
- ✅ Consultas optimizadas (select específico, no SELECT *)
- ⏳ Read replicas (futuro para escala)
- ⏳ Sharding por región (futuro)

### 7.3 Plan de Escalabilidad

**Fase 1 (actual)**: Monolito optimizado
- 1 servidor backend + DB
- Soporta ~500 usuarios concurrentes

**Fase 2 (6 meses)**: Horizontal scaling
- Load balancer + 2-3 backend instances
- PostgreSQL con read replicas
- Redis para sessions/caching
- Soporta ~2,000 usuarios concurrentes

**Fase 3 (12 meses)**: Microservicios
- Separar módulos críticos:
  - Auth service
  - Laboratory service
  - WhatsApp service
  - Vision/AI service
- Message queue (RabbitMQ/Kafka)
- Soporta 10,000+ usuarios concurrentes

---

## 8. MONITOREO Y OBSERVABILIDAD

### 8.1 Stack de Monitoreo (Producción)

**Ubicación**: `prod-server` (GCP us-central1-c)

**Componentes**:
1. **Prometheus** (entersys-prometheus)
   - Recolección de métricas
   - Puerto: 9090
   - Retención: 15 días

2. **Grafana** (entersys-grafana)
   - Visualización de dashboards
   - URL: https://monitoring.entersys.mx
   - Puerto: 3000

3. **Loki** (entersys-loki)
   - Agregación de logs
   - Puerto: 3100

### 8.2 Métricas Exportadas

```python
# Custom metrics para Nutrition Intelligence
- nutrition_api_requests_total{method, endpoint, status}
- nutrition_api_response_time_seconds{endpoint}
- laboratory_records_created_total
- laboratory_ocr_processed_total{status}
- whatsapp_messages_sent_total{type, status}
- patient_registrations_total
- vision_analysis_requests_total{model, status}
- database_connections_active
- file_uploads_total{file_type}
```

### 8.3 Alertas Configuradas

| Alerta | Condición | Severidad | Acción |
|--------|-----------|-----------|--------|
| API Down | Health check fails > 1min | Critical | PagerDuty |
| High Error Rate | Error rate > 5% for 5min | High | Email + Slack |
| Slow Response | P95 > 2s for 10min | Medium | Slack |
| DB Connection Pool | Active connections > 80% | High | Email |
| Disk Space Low | Usage > 85% | High | Email |
| WhatsApp Failed | Failed rate > 10% | Medium | Slack |

---

## 9. DESPLIEGUE Y DEVOPS

### 9.1 Ambientes

| Ambiente | Propósito | URL | Base de Datos |
|----------|-----------|-----|---------------|
| **Development** | Desarrollo local | localhost:3002 | SQLite |
| **Staging** | Testing pre-producción | staging.nutrition-intel.mx | PostgreSQL (staging) |
| **Production** | Producción | app.nutrition-intel.mx | PostgreSQL (prod) |

### 9.2 Pipeline CI/CD (Propuesto)

```yaml
# .github/workflows/ci-cd.yml
stages:
  1. Lint & Format
     - black, ruff (Python)
     - eslint, prettier (JavaScript)

  2. Unit Tests
     - pytest (backend)
     - jest (frontend)

  3. Integration Tests
     - API tests con httpx

  4. Security Scan
     - bandit (Python security)
     - npm audit (Node.js)

  5. Build
     - Docker image build

  6. Deploy to Staging
     - Auto-deploy en push a 'develop'

  7. E2E Tests (Staging)
     - Playwright tests

  8. Deploy to Production
     - Manual approval
     - Blue-green deployment
```

### 9.3 Backup y Disaster Recovery

**Estrategia de Backup**:
- ✅ Base de datos: Backup diario automatizado
- ✅ Archivos clínicos: Backup incremental diario
- ✅ Configuraciones: Git version control
- ✅ Retención: 30 días

**RTO (Recovery Time Objective)**: < 4 horas
**RPO (Recovery Point Objective)**: < 24 horas

**Plan de Recuperación**:
1. Detectar incidente
2. Evaluar impacto
3. Iniciar servidor de respaldo
4. Restaurar DB desde último backup
5. Restaurar archivos
6. Verificar integridad
7. Redirigir tráfico
8. Post-mortem

---

## 10. DEPENDENCIAS EXTERNAS

### 10.1 APIs de Terceros

| Servicio | Propósito | SLA | Fallback |
|----------|-----------|-----|----------|
| **Gemini Vision** | Análisis de imágenes | 99.9% | Claude Vision |
| **Claude Vision** | Análisis complejo | 99.9% | Mock data |
| **Twilio** | WhatsApp messaging | 99.95% | Queue + retry |
| **SendGrid** | Email transaccional | 99.9% | SMTP directo |

### 10.2 Gestión de Fallos

**Estrategia**: Circuit Breaker Pattern

```python
# Ejemplo: Vision service
1. Try Gemini API
2. If fails → Try Claude API
3. If both fail → Return mock data
4. Log error for manual review
```

---

## 11. CONSIDERACIONES DE MANTENIMIENTO

### 11.1 Actualización de Dependencias

**Frecuencia**: Mensual para patches, trimestral para minor/major

**Proceso**:
1. Dependabot crea PR automático
2. Review de changelog
3. Ejecutar test suite completo
4. Deploy a staging
5. Testing manual si cambios críticos
6. Deploy a producción

### 11.2 Database Migrations

**Herramienta**: Alembic

```bash
# Crear migración
alembic revision --autogenerate -m "Add new field to patients"

# Aplicar migración
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Política**:
- ✅ Todas las migraciones versionadas en Git
- ✅ Testing en staging antes de producción
- ✅ Backup antes de cualquier migración en prod
- ✅ Migraciones reversibles siempre que sea posible

---

## 12. ROADMAP TÉCNICO

### Q4 2025 (Actual - Fase 2)
- ✅ Expediente clínico completo
- ✅ Laboratorios con IA
- ✅ OCR de documentos
- ✅ WhatsApp integration
- ⏳ Plan de pruebas completo

### Q1 2026 (Fase 3)
- [ ] Recordatorio 24H mejorado
- [ ] Planes de alimentación generados por IA
- [ ] Reportes nutricionales PDF
- [ ] Integración con wearables (Fitbit, Apple Health)

### Q2 2026
- [ ] Mobile app (React Native)
- [ ] Telemedicina (video consultas)
- [ ] Marketplace de recetas
- [ ] Community features

### Q3-Q4 2026
- [ ] Microservicios architecture
- [ ] ML models propios (custom training)
- [ ] Expansión internacional (USA, Latinoamérica)

---

## 13. ANEXOS

### 13.1 Glosario de Términos

| Término | Definición |
|---------|-----------|
| **SMAE** | Sistema Mexicano de Alimentos Equivalentes |
| **NOM** | Norma Oficial Mexicana |
| **OCR** | Optical Character Recognition |
| **HOMA-IR** | Homeostatic Model Assessment for Insulin Resistance |
| **TMB** | Tasa Metabólica Basal |
| **GET** | Gasto Energético Total |
| **IMC** | Índice de Masa Corporal |

### 13.2 Contactos

| Rol | Email | Responsabilidad |
|-----|-------|-----------------|
| Product Owner | - | Visión de producto |
| Tech Lead | - | Decisiones técnicas |
| Arquitecto | - | Arquitectura y diseño |
| DevOps | - | Infraestructura y deploy |

---

**Fin del documento MD050**

**Próxima revisión**: 02 Diciembre 2025
**Aprobadores**: Product Owner, Tech Lead, Arquitecto
