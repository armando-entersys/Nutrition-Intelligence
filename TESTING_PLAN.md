# Plan de Pruebas Integral - Nutrition Intelligence México
## Documento de Arquitectura y Testing Profesional

**Versión**: 1.0
**Fecha**: 02 de Noviembre, 2025
**Responsable**: Arquitecto de Software
**Proyecto**: Nutrition Intelligence Platform - Fase 2

---

## 1. Resumen Ejecutivo

Este documento describe el plan de pruebas integral para la plataforma Nutrition Intelligence, implementando las mejores prácticas de la industria incluyendo:

- ✅ Pruebas Unitarias (Unit Testing)
- ✅ Pruebas de Integración (Integration Testing)
- ✅ Pruebas End-to-End (E2E Testing)
- ✅ Pruebas de Carga (Load Testing)
- ✅ Pruebas de Seguridad (Security Testing)
- ✅ Monitoreo Aplicativo (Application Monitoring)
- ✅ Reporte Web Automatizado

---

## 2. Arquitectura de Testing

### 2.1 Stack Tecnológico de Pruebas

**Backend Testing**:
- `pytest` - Framework principal de testing
- `pytest-asyncio` - Soporte para código asíncrono
- `pytest-cov` - Cobertura de código
- `httpx` - Cliente HTTP para testing de APIs
- `faker` - Generación de datos de prueba
- `factory-boy` - Factories para modelos

**Frontend Testing**:
- `@playwright/test` - E2E testing
- `jest` - Unit testing (ya instalado con React)
- `@testing-library/react` - Testing de componentes

**Load Testing**:
- `locust` - Framework Python para load testing

**Monitoring & Reporting**:
- `pytest-html` - Reportes HTML
- `allure-pytest` - Reportes avanzados con Allure
- Integración con Prometheus/Grafana existente

### 2.2 Estructura de Directorios

```
backend/
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_api_laboratory.py
│   │   ├── test_api_whatsapp.py
│   │   └── test_api_files.py
│   ├── e2e/
│   │   └── test_complete_workflows.py
│   ├── load/
│   │   └── locustfile.py
│   ├── fixtures/
│   │   └── test_data.py
│   └── conftest.py

frontend/
├── tests/
│   ├── e2e/
│   │   ├── expediente.spec.js
│   │   ├── laboratory.spec.js
│   │   └── whatsapp.spec.js
│   └── playwright.config.js
```

---

## 3. Matriz de Pruebas Completa

### 3.1 PRUEBAS UNITARIAS - Backend

#### Módulo: Laboratory Data Models

| ID | Caso de Prueba | Entrada | Salida Esperada | Prioridad | Estado |
|----|----------------|---------|-----------------|-----------|--------|
| UT-LAB-001 | Creación de laboratorio válido | Datos completos de lab | Objeto LaboratoryData creado | Alta | ⏳ |
| UT-LAB-002 | Validación de valores fuera de rango | Glucosa = 300 mg/dL | Alerta en interpretación IA | Alta | ⏳ |
| UT-LAB-003 | Cálculo automático HOMA-IR | Glucosa=100, Insulina=10 | HOMA-IR calculado correctamente | Media | ⏳ |
| UT-LAB-004 | Detección diabetes por HbA1c | HbA1c > 6.5% | Diagnóstico "Diabetes" | Alta | ⏳ |
| UT-LAB-005 | Índice aterogénico alto | Col=250, HDL=30 | Alerta riesgo cardiovascular | Media | ⏳ |

#### Módulo: WhatsApp Service

| ID | Caso de Prueba | Entrada | Salida Esperada | Prioridad | Estado |
|----|----------------|---------|-----------------|-----------|--------|
| UT-WA-001 | Envío mensaje sin Twilio config | Datos mensaje válidos | Respuesta mock exitosa | Alta | ⏳ |
| UT-WA-002 | Formato número telefónico | +525512345678 | Formato whatsapp:+525512345678 | Alta | ⏳ |
| UT-WA-003 | Mensaje mayor a 1600 chars | Texto 1700 chars | Error validación longitud | Media | ⏳ |
| UT-WA-004 | Recordatorio cita formato válido | Datos cita completos | Mensaje formateado con emojis | Media | ⏳ |
| UT-WA-005 | Manejo error Twilio API | API error 500 | Respuesta failed con error | Alta | ⏳ |

#### Módulo: OCR Processing

| ID | Caso de Prueba | Entrada | Salida Esperada | Prioridad | Estado |
|----|----------------|---------|-----------------|-----------|--------|
| UT-OCR-001 | Extracción texto PDF | PDF con texto embebido | Texto extraído correctamente | Alta | ⏳ |
| UT-OCR-002 | OCR imagen sin Tesseract | Imagen JPEG | Warning + retorno None | Media | ⏳ |
| UT-OCR-003 | Detección tipo documento lab | Texto con "glucosa", "colesterol" | document_type="laboratory" | Alta | ⏳ |
| UT-OCR-004 | Extracción valor glucosa | Texto "Glucosa: 105 mg/dL" | Valor detectado: 105 | Media | ⏳ |
| UT-OCR-005 | Archivo formato no soportado | Archivo .docx | Error formato no soportado | Baja | ⏳ |

### 3.2 PRUEBAS DE INTEGRACIÓN - API

#### API: Laboratory Endpoints

| ID | Caso de Prueba | Método | Endpoint | Validación | Prioridad | Estado |
|----|----------------|--------|----------|------------|-----------|--------|
| IT-LAB-001 | Crear laboratorio completo | POST | /api/v1/laboratory/ | Status 201, datos guardados | Alta | ⏳ |
| IT-LAB-002 | Obtener labs de paciente | GET | /api/v1/laboratory/patient/1 | Lista de labs con paginación | Alta | ⏳ |
| IT-LAB-003 | Actualizar valores lab | PUT | /api/v1/laboratory/{id} | Status 200, datos actualizados | Media | ⏳ |
| IT-LAB-004 | Análisis de tendencias | GET | /api/v1/laboratory/trends/patient/1 | Comparación con labs previos | Alta | ⏳ |
| IT-LAB-005 | Eliminar laboratorio | DELETE | /api/v1/laboratory/{id} | Status 204, registro eliminado | Baja | ⏳ |

#### API: WhatsApp Endpoints

| ID | Caso de Prueba | Método | Endpoint | Validación | Prioridad | Estado |
|----|----------------|--------|----------|------------|-----------|--------|
| IT-WA-001 | Enviar recordatorio cita | POST | /api/v1/whatsapp/send/appointment-reminder | Status 200, mensaje guardado | Alta | ⏳ |
| IT-WA-002 | Enviar notif plan listo | POST | /api/v1/whatsapp/send/meal-plan-notification | Status 200, Twilio SID presente | Alta | ⏳ |
| IT-WA-003 | Historial mensajes paciente | GET | /api/v1/whatsapp/messages/patient/1 | Lista con paginación | Media | ⏳ |
| IT-WA-004 | Crear template mensaje | POST | /api/v1/whatsapp/templates | Status 201, template creado | Media | ⏳ |
| IT-WA-005 | Validación teléfono inválido | POST | /api/v1/whatsapp/send/custom-message | Error 400 o envío fallido | Baja | ⏳ |

#### API: Files & OCR Endpoints

| ID | Caso de Prueba | Método | Endpoint | Validación | Prioridad | Estado |
|----|----------------|--------|----------|------------|-----------|--------|
| IT-FILE-001 | Upload PDF válido | POST | /api/v1/laboratory/files/upload | Status 201, OCR procesado | Alta | ⏳ |
| IT-FILE-002 | Upload imagen JPG | POST | /api/v1/laboratory/files/upload | Status 201, archivo guardado | Alta | ⏳ |
| IT-FILE-003 | Obtener archivos paciente | GET | /api/v1/laboratory/files/patient/1 | Lista con metadata completa | Media | ⏳ |
| IT-FILE-004 | Ver detalles archivo OCR | GET | /api/v1/laboratory/files/{id} | Datos extraídos visibles | Media | ⏳ |
| IT-FILE-005 | Eliminar archivo clínico | DELETE | /api/v1/laboratory/files/{id} | Status 204, archivo físico borrado | Media | ⏳ |

### 3.3 PRUEBAS END-TO-END

#### Flujo: Gestión de Laboratorios

| ID | Caso de Prueba | Pasos | Validación | Prioridad | Estado |
|----|----------------|-------|------------|-----------|--------|
| E2E-LAB-001 | Agregar laboratorio completo | 1. Login<br>2. Ir a Expediente<br>3. Tab Laboratorios<br>4. Click "Agregar"<br>5. Llenar formulario<br>6. Guardar | Lab aparece en lista<br>Interpretación IA visible | Alta | ⏳ |
| E2E-LAB-002 | Ver tendencias de laboratorio | 1. Abrir Expediente<br>2. Tab Laboratorios<br>3. Tab Tendencias<br>4. Seleccionar parámetro | Gráfica se muestra<br>Dirección de tendencia correcta | Alta | ⏳ |
| E2E-LAB-003 | Subir archivo PDF laboratorio | 1. Tab Archivos<br>2. Click "Subir"<br>3. Seleccionar PDF<br>4. Completar metadata<br>5. Upload | Archivo en lista<br>OCR procesado badge verde | Alta | ⏳ |
| E2E-LAB-004 | Ver detalles interpretación IA | 1. Click en laboratorio<br>2. Ver dialog detalles | Alertas críticas visibles<br>Valores fuera de rango destacados | Media | ⏳ |
| E2E-LAB-005 | Eliminar laboratorio | 1. Click en laboratorio<br>2. Click eliminar<br>3. Confirmar | Lab removido de lista | Baja | ⏳ |

#### Flujo: Mensajería WhatsApp

| ID | Caso de Prueba | Pasos | Validación | Prioridad | Estado |
|----|----------------|-------|------------|-----------|--------|
| E2E-WA-001 | Enviar recordatorio de cita | 1. Ir a WhatsApp Manager<br>2. Click "Recordatorio Cita"<br>3. Confirmar | Mensaje en historial<br>Status "sent" | Alta | ⏳ |
| E2E-WA-002 | Enviar mensaje motivacional | 1. Click "Mensaje Motivacional"<br>2. Ver confirmación | Mensaje enviado exitosamente | Media | ⏳ |
| E2E-WA-003 | Ver historial de mensajes | 1. Tab "Historial"<br>2. Ver lista | Mensajes ordenados por fecha<br>Estados con colores | Media | ⏳ |
| E2E-WA-004 | Actualizar historial | 1. En historial<br>2. Click "Actualizar" | Lista recargada con nuevos mensajes | Baja | ⏳ |
| E2E-WA-005 | Manejo de error sin Twilio | 1. Enviar cualquier mensaje<br>2. Ver respuesta | Nota "Mock response" visible | Baja | ⏳ |

### 3.4 PRUEBAS DE CARGA

| ID | Escenario | Usuarios | Duración | Criterio Éxito | Prioridad | Estado |
|----|-----------|----------|----------|----------------|-----------|--------|
| LOAD-001 | Carga normal API | 50 | 5 min | Response time < 500ms<br>Error rate < 1% | Alta | ⏳ |
| LOAD-002 | Pico de tráfico | 200 | 2 min | Response time < 1000ms<br>No crashes | Alta | ⏳ |
| LOAD-003 | Upload múltiples archivos | 20 simultáneos | 3 min | Todos completan<br>OCR procesa todos | Media | ⏳ |
| LOAD-004 | Envío masivo WhatsApp | 100 mensajes | 5 min | Rate limit respetado<br>Todos enviados o en cola | Media | ⏳ |
| LOAD-005 | Consultas de laboratorio | 100 usuarios | 10 min | DB no se satura<br>Queries optimizadas | Media | ⏳ |

### 3.5 PRUEBAS DE SEGURIDAD

| ID | Caso de Prueba | Tipo Ataque | Validación | Prioridad | Estado |
|----|----------------|-------------|------------|-----------|--------|
| SEC-001 | SQL Injection en búsqueda | SQLi | Query parametrizada, sin inyección | Crítica | ⏳ |
| SEC-002 | XSS en mensajes WhatsApp | XSS | Contenido sanitizado | Crítica | ⏳ |
| SEC-003 | Path Traversal en archivos | LFI | Solo acceso a directorio uploads | Alta | ⏳ |
| SEC-004 | Validación JWT tokens | Auth bypass | Endpoints protegidos funcionan | Crítica | ⏳ |
| SEC-005 | CORS configuración | CORS | Solo orígenes permitidos | Alta | ⏳ |

---

## 4. Cobertura de Código Objetivo

| Componente | Cobertura Mínima | Cobertura Objetivo |
|------------|------------------|-------------------|
| Models & Schemas | 80% | 95% |
| API Endpoints | 85% | 95% |
| Services | 90% | 98% |
| Utils & Helpers | 75% | 90% |
| **Global Backend** | **85%** | **95%** |
| Frontend Components | 70% | 85% |

---

## 5. Estrategia de Ejecución

### 5.1 Pipeline de CI/CD

```yaml
stages:
  - lint
  - unit-tests
  - integration-tests
  - e2e-tests
  - security-scan
  - load-tests
  - deploy
```

### 5.2 Frecuencia de Ejecución

- **Unit Tests**: Cada commit (pre-commit hook)
- **Integration Tests**: Cada push a develop/main
- **E2E Tests**: Diario + antes de releases
- **Load Tests**: Semanal + antes de releases
- **Security Tests**: Semanal + antes de releases

### 5.3 Criterios de Aceptación

Para considerar el software **LISTO PARA PRODUCCIÓN**:

✅ Todas las pruebas unitarias pasan (100%)
✅ Cobertura de código >= 85%
✅ Todas las pruebas de integración pasan (100%)
✅ E2E tests críticos pasan (100%)
✅ No vulnerabilidades críticas de seguridad
✅ Load tests dentro de SLA (< 1s response time)
✅ Sin errores 500 en producción últimas 48h

---

## 6. Monitoreo Aplicativo

### 6.1 Métricas Clave (KPIs)

**Performance**:
- Response time promedio: < 500ms
- P95 response time: < 1000ms
- P99 response time: < 2000ms

**Disponibilidad**:
- Uptime: > 99.9%
- Error rate: < 0.1%

**Recursos**:
- CPU usage: < 70%
- Memory usage: < 80%
- Disk usage: < 85%

### 6.2 Integración con Prometheus/Grafana

**Métricas Custom Exportadas**:
```python
# Backend metrics
- http_requests_total{method, endpoint, status}
- http_request_duration_seconds{method, endpoint}
- laboratory_records_created_total
- whatsapp_messages_sent_total{status}
- file_uploads_total{file_type}
- ocr_processing_duration_seconds
- database_query_duration_seconds{query_type}
```

**Alertas Configuradas**:
- Error rate > 5% por 5 minutos
- Response time > 2s por 5 minutos
- Servicio caído por 1 minuto
- Disk usage > 90%

---

## 7. Reportes y Documentación

### 7.1 Reporte HTML Automatizado

Se genera después de cada ejecución de tests:

📊 **Ubicación**: `backend/tests/reports/test-report.html`

**Contenido**:
- ✅ Resumen ejecutivo con % de éxito
- 📈 Gráficas de cobertura
- ⏱️ Tiempos de ejecución
- ❌ Tests fallidos con detalles
- 📊 Tendencias históricas

### 7.2 Dashboard Grafana

**Dashboard**: "Nutrition Intelligence - Testing & Quality"

**Paneles**:
1. Test Success Rate (últimas 24h)
2. Code Coverage Trend
3. E2E Test Duration
4. Failed Tests by Module
5. Security Scan Results
6. Load Test Metrics

---

## 8. Responsabilidades

| Rol | Responsabilidad |
|-----|-----------------|
| **Desarrolladores** | Escribir unit tests, mantener cobertura > 85% |
| **QA Engineer** | Ejecutar tests manuales, mantener E2E tests |
| **DevOps** | Configurar CI/CD, monitorear métricas |
| **Arquitecto** | Revisar estrategia, aprobar releases |

---

## 9. Anexos

### 9.1 Comandos Útiles

```bash
# Ejecutar todas las pruebas unitarias
pytest backend/tests/unit -v

# Ejecutar con cobertura
pytest backend/tests --cov=backend --cov-report=html

# Ejecutar solo tests de laboratorio
pytest backend/tests -k "laboratory"

# Ejecutar E2E tests
cd frontend && npx playwright test

# Generar reporte HTML
pytest --html=backend/tests/reports/test-report.html

# Load testing
locust -f backend/tests/load/locustfile.py --host=http://localhost:8000
```

### 9.2 Enlaces Importantes

- 📊 **Grafana**: https://monitoring.entersys.mx
- 🔥 **Prometheus**: http://prod-server:9090
- 📈 **Test Reports**: `/backend/tests/reports/`
- 📖 **Documentación**: `/TESTING_PLAN.md`

---

**Documento preparado por**: Arquitecto de Software
**Última actualización**: 02 Nov 2025
**Próxima revisión**: 02 Dic 2025
