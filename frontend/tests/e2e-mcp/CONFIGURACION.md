# 📋 Configuración Completa - Chrome DevTools MCP

## Resumen de Configuración Profesional

Este documento detalla toda la configuración implementada para las pruebas E2E usando **chrome-devtools-mcp** como arquitecto de software profesional.

---

## ✅ Archivos Creados

### 1. **Configuración Principal**

#### `.mcp-config.json` (Frontend root)
```
C:\Nutrition Intelligence\frontend\.mcp-config.json
```

**Propósito:** Configuración central de chrome-devtools-mcp

**Características:**
- ✅ Chrome executable path configurable
- ✅ Viewport 1920x1080 para pruebas consistentes
- ✅ Timeouts configurables (30s default)
- ✅ Directorios de screenshots, videos y reportes
- ✅ Configuración de reportes (HTML, JSON, JUnit)
- ✅ Opciones de launch del navegador
- ✅ Integración con Prometheus para métricas
- ✅ Captura de network traffic
- ✅ Captura de console messages
- ✅ Performance metrics (Web Vitals)
- ✅ Code coverage (JS/CSS)
- ✅ Accessibility checks (WCAG AA)

---

### 2. **Tests E2E**

#### `e2e-clinical-workflow.test.js`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\e2e-clinical-workflow.test.js
```

**Coverage:** 5 test cases principales
- E2E-001: Carga de aplicación con Web Vitals
- E2E-002: Navegación a Expediente Clínico
- E2E-003: Acceso a Historia Clínica
- E2E-004: Datos de Laboratorio
- E2E-005: Responsive Design (Mobile)

**Características Avanzadas:**
- ✅ Captura automática de screenshots
- ✅ Métricas de performance (FCP, LCP)
- ✅ Validación de tiempos de carga (<5s)
- ✅ Request/Response logging
- ✅ Console error tracking
- ✅ Page error handling

#### `e2e-whatsapp-integration.test.js`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\e2e-whatsapp-integration.test.js
```

**Coverage:** 5 test cases WhatsApp
- E2E-WA-001: Navegación a WhatsApp Manager
- E2E-WA-002: Mensajes Rápidos
- E2E-WA-003: Envío de Recordatorio
- E2E-WA-004: Historial de Mensajes
- E2E-WA-005: Configuración Twilio

**Características:**
- ✅ Validación de UI de mensajería
- ✅ Simulación de envío de mensajes
- ✅ Verificación de historial
- ✅ Screenshots por step

#### `e2e-ai-vision.test.js`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\e2e-ai-vision.test.js
```

**Coverage:** 5 test cases AI Vision
- E2E-AI-001: Navegación a Análisis de Fotos
- E2E-AI-002: Interfaz de Carga
- E2E-AI-003: Configuración IA (Gemini/Claude)
- E2E-AI-004: Manejo de Errores
- E2E-AI-005: Accesibilidad

**Características:**
- ✅ Performance metrics capture
- ✅ AI API request interception
- ✅ Accessibility validation
- ✅ Contrast checking

---

### 3. **Test Runner Profesional**

#### `run-tests.js`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\run-tests.js
```

**Características del Runner:**

✅ **Service Health Checks**
- Verifica que Frontend esté en http://localhost:3002
- Verifica que Backend esté en http://localhost:8000
- Muestra warnings si algún servicio no responde

✅ **Ejecución de Tests con Mocha**
- Framework: Mocha + Chai
- Timeout configurable (30s default)
- Reintentos automáticos (2 retries)
- Colored output en consola

✅ **Generación de Reportes HTML**
- Dashboard visual profesional
- Estadísticas: Passed, Failed, Skipped, Total
- Barra de progreso con % de éxito
- Detalles de cada test con duración
- Mensajes de error formateados
- Timestamps localizados (es-MX)
- Diseño responsive y moderno
- Gradientes y animaciones CSS

✅ **Generación de Reportes JSON**
- Formato estructurado para CI/CD
- Incluye todos los resultados
- Timestamps ISO 8601
- Duración total de ejecución

✅ **Organización de Resultados**
- Tests agrupados por suite
- Estados claramente identificados
- Duración por test en ms

---

### 4. **Configuración del Proyecto**

#### `package.json`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\package.json
```

**Scripts Disponibles:**
```json
{
  "test": "node run-tests.js",
  "test:headless": "HEADLESS=true node run-tests.js",
  "test:watch": "nodemon --watch *.test.js --exec 'node run-tests.js'",
  "report": "open ../reports/html/test-report.html",
  "clean": "rm -rf ../reports/* ../screenshots/* ../videos/*"
}
```

**Dependencias Instaladas:**
- ✅ `mocha` ^10.2.0 - Framework de testing
- ✅ `chai` ^4.3.10 - Assertions library
- ✅ `playwright` ^1.40.1 - Browser automation
- ✅ `chrome-devtools-mcp` - Chrome DevTools Protocol
- ✅ `nodemon` - Watch mode (dev)
- ✅ `open` - Open reports in browser

---

### 5. **Documentación**

#### `README.md`
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\README.md
```

**Contenido:**
- ✅ Características del framework
- ✅ Requisitos previos
- ✅ Guía de instalación
- ✅ Instrucciones de configuración
- ✅ Comandos de ejecución
- ✅ Estructura de tests
- ✅ Guía de reportes
- ✅ Integración CI/CD (GitHub Actions, GitLab CI)
- ✅ Troubleshooting completo
- ✅ Guía de contribución

#### `CONFIGURACION.md` (Este archivo)
```
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\CONFIGURACION.md
```

Resumen técnico de toda la configuración implementada.

---

### 6. **Scripts de Setup**

#### `setup.sh` (Linux/Mac)
```bash
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\setup.sh
```

#### `setup.bat` (Windows)
```batch
C:\Nutrition Intelligence\frontend\tests\e2e-mcp\setup.bat
```

**Funcionalidades:**
- ✅ Verificación de Node.js v18+
- ✅ Instalación de dependencias npm
- ✅ Instalación global de chrome-devtools-mcp
- ✅ Instalación de navegadores Playwright
- ✅ Creación de directorios de reportes
- ✅ Health check de servicios
- ✅ Mensajes de ayuda y next steps

---

## 🎯 Matriz de Casos de Prueba Implementados

### Expediente Clínico (5 casos)

| ID | Test Case | Status |
|----|-----------|--------|
| E2E-001 | Carga de aplicación con métricas | ✅ |
| E2E-002 | Navegación a Expediente | ✅ |
| E2E-003 | Historia Clínica tab | ✅ |
| E2E-004 | Datos de Laboratorio | ✅ |
| E2E-005 | Responsive Design | ✅ |

### WhatsApp Integration (5 casos)

| ID | Test Case | Status |
|----|-----------|--------|
| E2E-WA-001 | Navegación WhatsApp Manager | ✅ |
| E2E-WA-002 | Mensajes Rápidos UI | ✅ |
| E2E-WA-003 | Envío Recordatorio | ✅ |
| E2E-WA-004 | Historial Mensajes | ✅ |
| E2E-WA-005 | Config Twilio | ✅ |

### AI Vision (5 casos)

| ID | Test Case | Status |
|----|-----------|--------|
| E2E-AI-001 | Nav Análisis Fotos | ✅ |
| E2E-AI-002 | Interfaz Carga | ✅ |
| E2E-AI-003 | Config IA | ✅ |
| E2E-AI-004 | Manejo Errores | ✅ |
| E2E-AI-005 | Accesibilidad | ✅ |

**Total: 15 casos E2E implementados**

---

## 📊 Estructura de Reportes

```
frontend/tests/
├── reports/
│   ├── html/
│   │   └── test-report.html          # Reporte visual profesional
│   └── json/
│       └── test-results.json         # Datos estructurados
├── screenshots/
│   ├── 01-app-loaded-{timestamp}.png
│   ├── 02-expediente-view-{timestamp}.png
│   └── ...                            # Screenshots automáticos
└── videos/
    └── {test-name}-{timestamp}.webm   # Grabaciones (si habilitado)
```

---

## 🚀 Guía de Uso Rápido

### Instalación Inicial
```bash
cd "C:\Nutrition Intelligence\frontend\tests\e2e-mcp"
npm install
```

O usa el script de setup:
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Ejecutar Tests
```bash
# Todos los tests
npm test

# Modo headless
npm run test:headless

# Watch mode
npm run test:watch
```

### Ver Reportes
```bash
# Abrir reporte HTML en navegador
npm run report

# O navegar manualmente a:
# C:\Nutrition Intelligence\frontend\tests\reports\html\test-report.html
```

### Limpiar Archivos
```bash
npm run clean
```

---

## 🔧 Integración con Prometheus

Los tests están configurados para exportar métricas a Prometheus:

**Endpoint:** `http://localhost:9090/api/v1/write`

**Métricas exportadas:**
- `page_load_time` - Tiempo de carga completo
- `first_contentful_paint` - FCP (Web Vital)
- `largest_contentful_paint` - LCP (Web Vital)
- `time_to_interactive` - TTI
- `total_blocking_time` - TBT
- `cumulative_layout_shift` - CLS (Web Vital)

**Intervalo de exportación:** 5 segundos

---

## 🎨 Características del Reporte HTML

1. **Header con Branding**
   - Gradiente moderno (purple-blue)
   - Logo de Nutrition Intelligence
   - Título y descripción

2. **Dashboard de Estadísticas**
   - 4 tarjetas: Passed, Failed, Skipped, Total
   - Colores distintos por estado
   - Hover effects
   - Iconos visuales

3. **Barra de Progreso**
   - Animada con transiciones CSS
   - Muestra % de éxito
   - Gradiente verde

4. **Resultados Detallados**
   - Tests agrupados por suite
   - Estados con badges de color
   - Duración en ms
   - Mensajes de error formateados

5. **Footer Informativo**
   - Timestamp localizado (es-MX)
   - Información de tecnologías
   - Branding

---

## 📈 Métricas de Performance

Los tests capturan y validan:

- **Page Load Time** < 5000ms
- **First Contentful Paint** < 2500ms
- **Largest Contentful Paint** < 4000ms
- **Time to Interactive** < 5000ms
- **Cumulative Layout Shift** < 0.1

Estas métricas se comparan contra umbrales definidos en los tests.

---

## 🔐 Validaciones de Accesibilidad

- ✅ Headings hierarchy (h1-h6)
- ✅ Buttons con text o aria-label
- ✅ Contraste de colores
- ✅ Keyboard navigation
- ✅ ARIA attributes
- ✅ WCAG 2.1 Level AA compliance

---

## 🌐 Network Traffic Capture

Los tests interceptan y logguean:

- ✅ Todas las requests HTTP/HTTPS
- ✅ Method (GET, POST, PUT, DELETE)
- ✅ URL completa
- ✅ Status codes
- ✅ Response times
- ✅ Request/Response headers (opcional)

Logs en consola con formato:
```
📡 Request: GET http://localhost:8000/api/v1/patients
```

---

## 🐛 Error Tracking

Capturas automáticas:

1. **Console Errors**
   ```
   ❌ Console Error: TypeError: Cannot read property 'x' of undefined
   ```

2. **Page Errors**
   ```
   💥 Page Error: Uncaught ReferenceError: foo is not defined
   ```

3. **Network Errors**
   - Failed requests
   - Timeout errors
   - CORS issues

---

## 📝 Next Steps Recomendados

1. ✅ **Ejecutar Tests Iniciales**
   ```bash
   npm test
   ```

2. ✅ **Revisar Reporte HTML**
   ```bash
   npm run report
   ```

3. ⏳ **Implementar Tests Adicionales**
   - Crear `e2e-diets.test.js` para Generador de Dietas
   - Crear `e2e-scanner.test.js` para NOM-051
   - Crear `e2e-gamification.test.js` para Gamificación

4. ⏳ **Integrar con CI/CD**
   - Configurar GitHub Actions
   - Configurar GitLab CI
   - Exportar reportes como artifacts

5. ⏳ **Configurar Monitoring Continuo**
   - Grafana dashboards para métricas
   - Alertas de performance degradation
   - Historical trending

---

## 🤝 Soporte y Contacto

Para dudas o problemas con la configuración:

- **Documentación:** `README.md`
- **Plan de Pruebas:** `../../../TESTING_PLAN.md`
- **Arquitectura:** `../../../docs/MD050-ARQUITECTURA-SISTEMA.md`

---

**Configuración completada por:** Arquitecto de Software IA
**Fecha:** Enero 2025
**Versión:** 1.0.0

---

✅ **Sistema de Pruebas E2E Profesional Completamente Configurado**
