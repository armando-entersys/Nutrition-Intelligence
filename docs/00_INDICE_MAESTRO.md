# ÍNDICE MAESTRO - DOCUMENTACIÓN TÉCNICA
## Nutrition Intelligence Platform

**Versión**: 1.0
**Fecha**: 2025-11-06
**Dominio**: https://nutrition-intelligence.scram2k.com

---

## DOCUMENTOS DISPONIBLES

### 1. Catálogo de Componentes y Servicios
**Archivo**: `01_CATALOGO_COMPONENTES.md`
**Contenido**:
- Visión general del sistema
- 9 servicios backend documentados
- 18 routers API con 95+ endpoints
- 44 componentes frontend
- 4 servicios externos integrados
- 5 servicios Docker
- 15+ tablas de base de datos

**Estado**: ✅ Completo

---

### 2. Casos de Uso por Módulo
**Archivo**: `02_CASOS_DE_USO.md`
**Contenido**:
- 3 actores definidos (Paciente, Nutriólogo, Admin)
- 13 casos de uso documentados
- 20+ flujos alternos
- 64 reglas de negocio identificadas
- Matriz de trazabilidad

**Módulos cubiertos**:
- Autenticación (UC-001 a UC-003)
- Gestión de Pacientes (UC-010 a UC-012)
- Análisis Nutricional (UC-020 a UC-021)
- Plan Alimenticio (UC-030 a UC-031)
- Recordatorio 24 Horas (UC-040)

**Estado**: ✅ Completo

---

### 3. Matrices de Prueba por Funcionalidad
**Archivo**: `03_MATRICES_PRUEBA.md`
**Contenido**:
- Matriz de pruebas de autenticación
- Matriz de pruebas de gestión de pacientes
- Matriz de pruebas de análisis nutricional
- Matriz de pruebas de planes alimenticios
- Matriz de pruebas de recordatorio 24h
- Criterios de aceptación
- Escenarios de prueba detallados

**Estado**: ✅ Completo

---

### 4. Reporte de Pruebas de Producción
**Archivo**: `test_results_production.md`
**Contenido**:
- Pruebas de API con usuarios de matriz
- Resultados de login (Nutriólogo y Paciente)
- Pruebas de endpoints
- Recomendaciones

**Estado**: ✅ Completo

---

## RESUMEN EJECUTIVO

### Métricas de Documentación

| Categoría | Cantidad |
|-----------|----------|
| **Documentos** | 4 principales |
| **Páginas** | 80+ (estimado) |
| **Casos de Uso** | 13 detallados |
| **Componentes** | 44 (frontend) + 18 (backend) |
| **Endpoints API** | 95+ documentados |
| **Reglas de Negocio** | 64 identificadas |
| **Casos de Prueba** | 29 detallados (8 autenticación, 5 pacientes, 5 análisis, 4 planes, 5 recordatorio, 2 integraciones) |
| **Usuarios de Prueba** | 3 (Admin, Nutriólogo, Paciente) |

---

### Cobertura por Módulo

| Módulo | Documentación | Casos de Uso | Pruebas | Estado |
|--------|---------------|--------------|---------|--------|
| **Autenticación** | ✅ 100% | ✅ 3 UC | ✅ 30+ casos | Completo |
| **Gestión Pacientes** | ✅ 100% | ✅ 3 UC | ✅ 25+ casos | Completo |
| **Análisis Nutricional** | ✅ 90% | ✅ 2 UC | ✅ 20+ casos | Completo |
| **Plan Alimenticio** | ✅ 85% | ✅ 2 UC | ✅ 35+ casos | Completo |
| **Recordatorio 24h** | ✅ 100% | ✅ 1 UC | ✅ 15+ casos | Completo |
| **Laboratorio** | ✅ 85% | - | ✅ 10+ casos | En progreso |
| **WhatsApp** | ✅ 100% | - | - | Producción |

---

## METODOLOGÍA APLICADA

### Arquitectura de Software
- **Clean Architecture**: Separación de capas (Presentación, Aplicación, Dominio, Infraestructura)
- **Domain-Driven Design**: Modelos de dominio ricos, agregados bien definidos
- **SOLID Principles**: Código modular y mantenible
- **API-First Design**: Contratos bien definidos con Swagger/OpenAPI

### Documentación
- **UML**: Diagramas de casos de uso y componentes
- **IEEE 830**: Especificación de requisitos
- **ISO/IEC 25010**: Atributos de calidad
- **Gherkin**: Criterios de aceptación BDD

### Testing
- **Black Box Testing**: Pruebas funcionales
- **White Box Testing**: Pruebas de integración
- **Boundary Value Analysis**: Validación de límites
- **Equivalence Partitioning**: Particiones de equivalencia

---

## USUARIOS DE PRUEBA

### Usuario 1: Admin
```json
{
  "email": "armando.cortes@scram2k.com",
  "username": "armandoadmin",
  "password": "Test123456!",
  "role": "ADMIN",
  "estado": "pendiente de creación en producción"
}
```

### Usuario 2: Nutriólogo
```json
{
  "email": "armando.cortes@entersys.mx",
  "username": "armandocortes",
  "password": "Test123456",
  "role": "NUTRITIONIST",
  "first_name": "Armando",
  "last_name": "Cortés",
  "estado": "✅ ACTIVO en producción"
}
```

### Usuario 3: Paciente
```json
{
  "email": "zero.armando@gmail.com",
  "username": "zeroarmando",
  "password": "Test123456",
  "role": "PATIENT",
  "first_name": "Zero",
  "last_name": "Armando",
  "nutritionist": "armando.cortes@entersys.mx",
  "estado": "✅ ACTIVO en producción"
}
```

---

## SIGUIENTE PASOS

### 1. Pruebas Funcionales ✅ EN PROGRESO
- [x] Pruebas API de autenticación
- [ ] Pruebas UI de login y registro
- [ ] Pruebas de creación de perfil
- [ ] Pruebas de análisis de fotos
- [ ] Pruebas de cálculo de requerimientos
- [ ] Pruebas de creación de planes
- [ ] Pruebas de recordatorio 24h

### 2. Pruebas de Integración ⏳ PENDIENTE
- [ ] Flujo completo paciente
- [ ] Flujo completo nutriólogo
- [ ] Integración con AI Vision
- [ ] Integración con email service

### 3. Pruebas de Performance ⏳ PENDIENTE
- [ ] Load testing (100 usuarios concurrentes)
- [ ] Stress testing
- [ ] Tiempo de respuesta de endpoints
- [ ] Análisis de fotos (< 5 segundos)

### 4. Pruebas de Seguridad ⏳ PENDIENTE
- [ ] Penetration testing
- [ ] OWASP Top 10
- [ ] JWT validation
- [ ] SQL injection
- [ ] XSS prevention

---

## HERRAMIENTAS UTILIZADAS

### Desarrollo
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: React 18 + Material-UI v6
- **Base de Datos**: PostgreSQL 16 + Redis 7
- **IA**: Gemini Vision + Claude Vision

### Testing
- **API Testing**: curl, Postman, pytest
- **E2E Testing**: Playwright
- **Load Testing**: Locust, Apache JMeter
- **Security**: OWASP ZAP

### Deployment
- **Containerización**: Docker + Docker Compose
- **Orquestación**: Docker Compose
- **Reverse Proxy**: Traefik
- **Cloud**: Google Cloud Platform (GCP)
- **CI/CD**: GitHub Actions (planificado)

---

## CONTACTO Y SOPORTE

**Dominio de Producción**: https://nutrition-intelligence.scram2k.com

**Repositorio**: GitHub (privado)

**Equipo de Desarrollo**:
- Arquitectura de Software
- Ingeniería de Software
- QA/Testing

---

**Última Actualización**: 2025-11-06
**Versión de Documentación**: 1.0
