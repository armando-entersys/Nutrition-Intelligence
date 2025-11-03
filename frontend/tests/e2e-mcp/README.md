# 🧪 Nutrition Intelligence - E2E Testing Suite

## Chrome DevTools MCP + Mocha Professional Testing Framework

Este directorio contiene la suite completa de pruebas E2E (End-to-End) para Nutrition Intelligence, utilizando **chrome-devtools-mcp** como herramienta principal de automatización de navegador.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Estructura de Tests](#estructura-de-tests)
- [Reportes](#reportes)
- [Integración con CI/CD](#integración-con-cicd)
- [Troubleshooting](#troubleshooting)

---

## ✨ Características

✅ **Chrome DevTools Protocol (CDP)** - Control total del navegador a nivel de protocolo
✅ **Reportes HTML Profesionales** - Visualización interactiva de resultados
✅ **Captura Automática de Screenshots** - Screenshots en fallo o bajo demanda
✅ **Métricas de Performance** - Web Vitals (FCP, LCP, TTI, CLS)
✅ **Monitoring Integration** - Exportación a Prometheus/Grafana
✅ **Network Traffic Capture** - Interceptación y logging de requests
✅ **Console & Error Tracking** - Captura de errores de JavaScript
✅ **Accessibility Checks** - Validación de estándares WCAG 2.1 AA
✅ **Responsive Testing** - Pruebas en múltiples viewports
✅ **Retry & Recovery** - Reintentos automáticos en caso de fallo

---

## 🔧 Requisitos Previos

Antes de ejecutar las pruebas, asegúrate de tener:

### 1. Node.js y npm
```bash
node --version  # v18.0.0 o superior
npm --version   # v9.0.0 o superior
```

### 2. Chrome/Chromium Instalado
El sistema utilizará la instalación de Chrome del sistema o descargará Chromium automáticamente.

### 3. Servicios Corriendo

**Frontend:**
```bash
cd C:\Nutrition Intelligence\frontend
npm install
npm start  # Debe correr en http://localhost:3002
```

**Backend:**
```bash
cd C:\Nutrition Intelligence\backend
pip install -r requirements.txt
python -m uvicorn main:app --reload  # http://localhost:8000
```

### 4. chrome-devtools-mcp (Instalado Globalmente)
```bash
npm install -g chrome-devtools-mcp@latest
```

---

## 📦 Instalación

```bash
cd "C:\Nutrition Intelligence\frontend\tests\e2e-mcp"
npm install
```

Esto instalará todas las dependencias necesarias:
- `mocha` - Framework de testing
- `chai` - Librería de assertions
- `playwright` - Control de navegador
- `chrome-devtools-mcp` - Protocolo Chrome DevTools

---

## ⚙️ Configuración

### Archivo de Configuración Principal

El archivo `.mcp-config.json` en el directorio `frontend/` contiene toda la configuración:

```json
{
  "testConfig": {
    "baseURL": "http://localhost:3002",
    "timeout": 30000,
    "retries": 2
  },
  "monitoring": {
    "enabled": true,
    "metricsEndpoint": "http://localhost:9090/api/v1/write"
  }
}
```

### Variables de Entorno

Puedes sobrescribir la configuración con variables de entorno:

```bash
# Base URL del frontend
export BASE_URL=http://localhost:3002

# Backend API URL
export BACKEND_URL=http://localhost:8000

# Modo headless (sin UI)
export HEADLESS=false

# Timeout por test (ms)
export TIMEOUT=30000

# Número de reintentos
export RETRIES=2

# Parallel execution
export PARALLEL=false
```

---

## 🚀 Ejecución de Pruebas

### Ejecutar Todos los Tests

```bash
npm test
```

O directamente con Node:

```bash
node run-tests.js
```

### Ejecutar en Modo Headless

```bash
npm run test:headless
```

O con variable de entorno:

```bash
HEADLESS=true node run-tests.js
```

### Ejecutar con Watch Mode

```bash
npm run test:watch
```

Esto reiniciará las pruebas automáticamente cuando detecte cambios en los archivos `.test.js`.

### Ejecutar Test Específico

```bash
npx mocha e2e-clinical-workflow.test.js
```

### Ver Reporte HTML

```bash
npm run report
```

Esto abrirá automáticamente el reporte HTML en tu navegador.

---

## 📂 Estructura de Tests

```
tests/e2e-mcp/
├── .mcp-config.json                    # Configuración MCP
├── package.json                        # Dependencias del proyecto
├── run-tests.js                        # Runner principal con generación de reportes
├── README.md                           # Esta documentación
│
├── e2e-clinical-workflow.test.js       # Tests de Expediente Clínico
│   ├── E2E-001: Carga de aplicación
│   ├── E2E-002: Navegación a Expediente
│   ├── E2E-003: Historia Clínica
│   ├── E2E-004: Datos de Laboratorio
│   └── E2E-005: Responsive Design
│
├── e2e-whatsapp-integration.test.js    # Tests de WhatsApp
│   ├── E2E-WA-001: Navegación WhatsApp Manager
│   ├── E2E-WA-002: Mensajes Rápidos
│   ├── E2E-WA-003: Enviar Recordatorio
│   ├── E2E-WA-004: Historial de Mensajes
│   └── E2E-WA-005: Configuración Twilio
│
└── e2e-ai-vision.test.js               # Tests de AI Vision
    ├── E2E-AI-001: Navegación Análisis Fotos
    ├── E2E-AI-002: Interfaz de Carga
    ├── E2E-AI-003: Configuración IA
    ├── E2E-AI-004: Validación Errores
    └── E2E-AI-005: Accesibilidad
```

---

## 📊 Reportes

### Reporte HTML

Después de ejecutar las pruebas, se genera automáticamente un reporte HTML profesional:

**Ubicación:** `tests/reports/html/test-report.html`

**Características:**
- ✅ Dashboard visual con estadísticas
- ✅ Barra de progreso de éxito
- ✅ Detalles de cada test (passed/failed/skipped)
- ✅ Timestamps y duración de tests
- ✅ Mensajes de error formateados
- ✅ Diseño responsive y moderno

### Reporte JSON

Para integración con CI/CD:

**Ubicación:** `tests/reports/json/test-results.json`

```json
{
  "tests": [...],
  "passes": 12,
  "failures": 0,
  "pending": 2,
  "duration": 45230
}
```

### Screenshots

Todas las capturas de pantalla se guardan en:

**Ubicación:** `tests/screenshots/`

Formato de nombre: `{test-name}-{timestamp}.png`

Ejemplo: `01-app-loaded-2025-01-15T10-30-45-123Z.png`

### Videos (Opcional)

Si está habilitado en la configuración:

**Ubicación:** `tests/videos/`

---

## 🔗 Integración con CI/CD

### GitHub Actions

Crea `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend/tests/e2e-mcp
          npm install

      - name: Start services
        run: |
          cd backend && python -m uvicorn main:app --reload &
          cd frontend && npm start &
          sleep 10

      - name: Run E2E tests
        run: |
          cd frontend/tests/e2e-mcp
          HEADLESS=true npm test

      - name: Upload test reports
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: frontend/tests/reports/
```

### GitLab CI

Crea `.gitlab-ci.yml`:

```yaml
e2e_tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0
  script:
    - cd frontend/tests/e2e-mcp
    - npm install
    - HEADLESS=true npm test
  artifacts:
    paths:
      - frontend/tests/reports/
    expire_in: 1 week
```

---

## 🐛 Troubleshooting

### Problema: "Chrome no se puede lanzar"

**Solución:**
```bash
# Instalar dependencias de Playwright
npx playwright install chromium
npx playwright install-deps
```

### Problema: "Frontend/Backend no responde"

**Solución:**
```bash
# Verificar que los servicios estén corriendo
curl http://localhost:3002  # Frontend
curl http://localhost:8000/docs  # Backend

# Reiniciar servicios si es necesario
```

### Problema: "Tests tardan mucho tiempo"

**Solución:**
- Incrementar timeout en `.mcp-config.json`
- Verificar que no haya issues de red
- Revisar performance del backend

### Problema: "Screenshots no se guardan"

**Solución:**
```bash
# Verificar permisos del directorio
mkdir -p tests/screenshots
chmod 755 tests/screenshots
```

### Problema: "Error: Cannot find module 'mocha'"

**Solución:**
```bash
cd frontend/tests/e2e-mcp
npm install
```

---

## 📚 Documentación Adicional

- [TESTING_PLAN.md](../../../TESTING_PLAN.md) - Plan integral de pruebas
- [MD050-ARQUITECTURA-SISTEMA.md](../../../docs/MD050-ARQUITECTURA-SISTEMA.md) - Arquitectura del sistema
- [chrome-devtools-mcp Docs](https://github.com/modelcontextprotocol/servers) - Documentación oficial

---

## 🤝 Contribuir

Para agregar nuevos tests:

1. Crea un nuevo archivo `e2e-{feature-name}.test.js`
2. Sigue la estructura existente de los tests
3. Documenta cada test case con su ID (E2E-XXX-001)
4. Agrega el archivo a `run-tests.js` en el array `testFiles`
5. Ejecuta las pruebas para validar

---

## 📄 Licencia

Copyright © 2025 Nutrition Intelligence Platform
MIT License

---

## 👥 Soporte

Para reportar issues o solicitar features:
- **Email:** soporte@nutrition-intelligence.com
- **Slack:** #testing-automation
- **GitHub Issues:** [Crear Issue](https://github.com/nutrition-intelligence/platform/issues)

---

**Desarrollado con ❤️ por el equipo de Nutrition Intelligence**
