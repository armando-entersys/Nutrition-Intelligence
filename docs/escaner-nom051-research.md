# Investigación: Escáner NOM-051
## Base de Datos de Productos Mexicanos con Información Nutricional

**Fecha:** 2025-11-09
**Objetivo:** Encontrar soluciones para implementar un escáner de códigos de barras que muestre información nutricional y sellos NOM-051 de productos mexicanos.

---

## 📊 Resumen Ejecutivo

La investigación reveló que **NO existe una base de datos pública centralizada** en México que contenga productos con sus sellos NOM-051. Sin embargo, existen varias opciones viables para implementar el Escáner NOM-051:

### ✅ Recomendación Principal: Enfoque Híbrido
1. **Open Food Facts API** (gratuita) como fuente principal
2. **Base de datos propia** para productos locales/faltantes
3. **Captura manual con AI Vision** para productos no encontrados

---

## 🔍 Hallazgos de Investigación

### 1. Open Food Facts (Recomendado)

**URL:** https://world.openfoodfacts.org
**API Docs:** https://openfoodfacts.github.io/openfoodfacts-server/api/

#### ✅ Ventajas
- **Gratuita y open source** - Sin costos de API
- **11,972 productos mexicanos** actualmente en la base de datos
- **12,402 productos adicionales** marcados como "to be completed"
- **Soporte oficial para México** - Wiki dedicada y canal Slack (#mexico)
- **API REST completa** - Búsqueda por código de barras
- **Datos de NOM-051** - Mencionado en wiki de soporte para México
- **Comunidad activa** - Scan Parties en México para agregar productos
- **Más de 4 millones de productos globales**

#### ⚠️ Limitaciones
- Cobertura limitada en México (~12k productos vs decenas de miles existentes)
- Calidad de datos variable (depende de contribuciones comunitarias)
- No todos los productos tienen información NOM-051 completa
- Puede faltar información de productos muy locales o nuevos

#### 📡 Endpoints Clave
```
GET https://world.openfoodfacts.org/api/v2/product/{barcode}
GET https://world.openfoodfacts.org/country/en:mexico
```

#### 💡 Integración
- Hit rate estimado: 30-40% para productos mexicanos
- Latencia: < 500ms en promedio
- Rate limit: 1 llamada = 1 escaneo real de usuario (muy generoso)

---

### 2. COFEPRIS (Gobierno de México)

**URL:** https://www.gob.mx/cofepris
**Datos Abiertos:** https://datos.gob.mx/busca/dataset?organization=cofepris

#### ✅ Ventajas
- **45 datasets publicados** con información sanitaria
- Datos oficiales de permisos de importación
- Certificaciones de alimentos
- Información de suplementos alimenticios

#### ⚠️ Limitaciones
- **NO tiene API pública documentada**
- Acceso principalmente a través de portal web
- Datos disponibles en datos.gob.mx pero no programáticamente consultables
- No existe endpoint para búsqueda por código de barras
- Enfocado en permisos y certificaciones, no en base de productos para consumidores

#### 📋 Conclusión
No viable para implementación actual. Los datos existen pero no son accesibles vía API.

---

### 3. Sellos NOM-051 - Norma Oficial

**Fase actual:** Fase 2 (hasta octubre 2025)
**Próxima fase:** Fase 3 - 1 de octubre de 2025 (criterios más estrictos)

#### 📜 Marco Regulatorio
- **NOM-051-SCFI/SSA1-2010** - Especificaciones de etiquetado
- 5 sellos de advertencia principales:
  - Exceso de calorías
  - Exceso de azúcares
  - Exceso de grasas saturadas
  - Exceso de grasas trans
  - Exceso de sodio
- 2 leyendas adicionales:
  - Contiene edulcorantes
  - Contiene cafeína

#### ⚠️ **HALLAZGO CRÍTICO**
**NO existe una base de datos pública centralizada** con productos y sus sellos NOM-051.

Los sellos se:
- Validan por COFEPRIS, Secretaría de Economía y Secretaría de Salud
- Verifican directamente en el empaque físico del producto
- Calculan según tabla oficial de nutrientes críticos

#### 📊 Fase 3 (Oct 2025)
Criterios más estrictos - más productos requerirán sellos de advertencia.

---

### 4. Códigos de Barras en México

**Estándar:** EAN-13 y UPC-A
**Prefijo México:** 750 (asignado por GS1 México)
**Organismo:** GS1 México (único emisor de códigos 750)

#### 📱 Formatos Soportados
- EAN-13 (más común en México y Europa)
- UPC-A (productos norteamericanos)
- EAN-8 (productos pequeños)

---

### 5. APIs Comerciales Alternativas

| API | Productos | Cobertura México | Costo | Hit Rate | Notas |
|-----|-----------|------------------|-------|----------|-------|
| **LogMeal** | 3M | 150 países | 💰 Comercial | N/D | Incluye México, amplia cobertura |
| **FatSecret** | N/D | Global | 💰 Comercial | 90% | Alta precisión de códigos de barras |
| **Edamam** | N/D | Global | $19/mes | N/D | 200 búsquedas/min por barcode |
| **Chomp Food API** | 875k | Principalmente USA | 💰 Comercial | N/D | Limitado para México |
| **Barcode Lookup** | N/D | Global | 💰 Comercial | N/D | Base de datos general UPC/EAN |

#### 💡 Evaluación
Todas son comerciales y su cobertura específica de productos mexicanos es **desconocida**.
No garantizan datos de NOM-051.

---

## 🛠️ Librerías de Escaneo para React

### Opción 1: react-qr-barcode-scanner (Recomendada)
```bash
npm install react-qr-barcode-scanner
```

**Ventajas:**
- ✅ Compatible con iOS 11+ y Android
- ✅ Usa react-webcam + @zxing/library
- ✅ TypeScript
- ✅ Componente simple de integrar
- ✅ Funciona en computadoras y móviles

---

### Opción 2: html5-qrcode
```bash
npm install html5-qrcode
```

**Ventajas:**
- ✅ Muy popular y bien mantenida
- ✅ Open source
- ✅ Alta precisión
- ✅ Soporta QR y códigos de barras 1D
- ✅ Componente React disponible en scanapp-org/html5-qrcode-react

---

### Opción 3: react-zxing
```bash
npm install react-zxing
```

**Ventajas:**
- ✅ Basada en ZXing (estándar de facto)
- ✅ Soporte amplio de formatos
- ✅ Buena documentación

---

## 🏗️ Arquitectura Propuesta

### Enfoque Híbrido (Recomendado)

```
┌─────────────────────────────────────────────────────────┐
│                  Usuario escanea código                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│          1. Búsqueda en Base de Datos Local             │
│             (PostgreSQL - productos_nom051)              │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ├─── ✅ Encontrado ───────────┐
                    │                              │
                    ├─── ❌ No encontrado         │
                    │                              ▼
                    ▼                    ┌──────────────────┐
┌─────────────────────────────────┐     │ Mostrar resultado │
│  2. Búsqueda en Open Food Facts │     │  con sellos y    │
│     API (productos globales)     │     │  recomendaciones │
└───────────────┬─────────────────┘     └──────────────────┘
                │
                ├─── ✅ Encontrado ──────────┐
                │                             │
                ├─── ❌ No encontrado        │
                │                             ▼
                ▼                   ┌──────────────────────┐
┌──────────────────────────────┐   │   Calcular sellos    │
│ 3. Captura manual asistida   │   │   NOM-051 desde      │
│    con AI Vision API         │   │   tabla nutricional  │
│  - Usuario toma foto etiqueta│   └──────────────────────┘
│  - Gemini extrae info        │
│  - Se guarda en BD local     │
└──────────────────────────────┘
```

---

## 💾 Esquema de Base de Datos Propuesta

```sql
-- Tabla de productos escaneados
CREATE TABLE productos_nom051 (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    marca VARCHAR(255),

    -- Información nutricional (por 100g/ml)
    porcion_gramos DECIMAL(10,2),
    calorias DECIMAL(10,2),
    proteinas DECIMAL(10,2),
    carbohidratos DECIMAL(10,2),
    azucares DECIMAL(10,2),
    grasas_totales DECIMAL(10,2),
    grasas_saturadas DECIMAL(10,2),
    grasas_trans DECIMAL(10,2),
    fibra DECIMAL(10,2),
    sodio DECIMAL(10,2),

    -- Sellos NOM-051
    exceso_calorias BOOLEAN DEFAULT FALSE,
    exceso_azucares BOOLEAN DEFAULT FALSE,
    exceso_grasas_saturadas BOOLEAN DEFAULT FALSE,
    exceso_grasas_trans BOOLEAN DEFAULT FALSE,
    exceso_sodio BOOLEAN DEFAULT FALSE,
    contiene_edulcorantes BOOLEAN DEFAULT FALSE,
    contiene_cafeina BOOLEAN DEFAULT FALSE,

    -- Metadatos
    fuente VARCHAR(50), -- 'open_food_facts', 'manual', 'ai_vision'
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER REFERENCES auth_users(id),
    validado BOOLEAN DEFAULT FALSE,

    -- Imagen del producto
    imagen_url TEXT,

    -- Búsqueda
    ingredientes TEXT,
    categoria VARCHAR(100),

    CONSTRAINT valid_barcode CHECK (LENGTH(codigo_barras) >= 8)
);

-- Índices
CREATE INDEX idx_productos_nom051_barcode ON productos_nom051(codigo_barras);
CREATE INDEX idx_productos_nom051_marca ON productos_nom051(marca);
CREATE INDEX idx_productos_nom051_categoria ON productos_nom051(categoria);

-- Tabla de historial de escaneos (analytics)
CREATE TABLE escaneos_historia (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES auth_users(id),
    producto_id INTEGER REFERENCES productos_nom051(id),
    codigo_barras VARCHAR(20) NOT NULL,
    encontrado BOOLEAN,
    fuente VARCHAR(50),
    fecha_escaneo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_escaneos_usuario ON escaneos_historia(usuario_id);
CREATE INDEX idx_escaneos_fecha ON escaneos_historia(fecha_escaneo DESC);
```

---

## 🎯 Plan de Implementación

### Fase 1: MVP - Funcionalidad Básica (1-2 semanas)

1. **Implementar escaneo de código de barras**
   - Integrar react-qr-barcode-scanner
   - UI de cámara con overlay
   - Validación de código EAN-13/UPC-A
   - Feedback visual y sonoro

2. **Crear base de datos local**
   - Migración SQL para tabla productos_nom051
   - Endpoints FastAPI básicos (GET, POST)
   - Validación de datos

3. **Integrar Open Food Facts API**
   - Cliente Python para API OFF
   - Mapeo de datos OFF a esquema local
   - Cálculo de sellos NOM-051 desde datos nutricionales
   - Cache de resultados

4. **UI básica de resultados**
   - Card con información del producto
   - Visualización de sellos (octágonos negros)
   - Información nutricional
   - Botón "Reportar error"

### Fase 2: Captura Manual Asistida (2-3 semanas)

5. **Implementar captura con AI Vision**
   - Interfaz para tomar foto de etiqueta
   - Prompt especializado para NOM-051
   - Extracción de tabla nutricional
   - Validación y confirmación del usuario

6. **Contribución a base de datos**
   - Sistema de aprobación de productos
   - Moderación de contenido
   - Gamificación (puntos por contribuir)

### Fase 3: Funcionalidades Avanzadas (2-3 semanas)

7. **Analytics y recomendaciones**
   - Historial de productos escaneados
   - Análisis de patrones alimenticios
   - Recomendaciones personalizadas
   - Comparación de productos similares

8. **Optimizaciones**
   - PWA para instalación móvil
   - Modo offline con cache
   - Sincronización de datos
   - Optimización de rendimiento

---

## 📈 Estimación de Cobertura

### Escenario Realista (6 meses)

- **Open Food Facts:** 40% de hit rate (mejorando con tiempo)
- **Base de datos local:** 30% (contribuciones de usuarios)
- **Captura manual:** 30% (productos no encontrados)

**Total esperado:** ~70-80% de cobertura en productos comunes

### Estrategia de Crecimiento

1. **Alianzas con tiendas locales** - Pre-cargar productos populares
2. **Gamificación** - Incentivar a usuarios a agregar productos
3. **Contribuir a Open Food Facts** - Mejorar la base de datos global
4. **Eventos Scan Party** - Captura masiva en supermercados

---

## 💰 Análisis de Costos

| Componente | Costo Mensual | Notas |
|------------|---------------|-------|
| Open Food Facts API | **$0** | Gratuita |
| Base de datos PostgreSQL | $0 | Ya incluida en stack |
| Gemini Vision API | ~$10-50 | Basado en uso real, solo para captura manual |
| Storage (imágenes) | ~$5-20 | CloudFlare R2 o similar |
| **TOTAL** | **$15-70/mes** | Escalable según uso |

### Comparación con Alternativas Comerciales

- LogMeal / FatSecret / Edamam: **$100-500+/mes**
- Desarrollo de scraping propio: **Alto riesgo legal, mantenimiento costoso**

**✅ Enfoque híbrido es 80-90% más económico**

---

## ⚠️ Consideraciones Legales

1. **Open Food Facts**
   - Licencia: Open Database License (ODbL)
   - Contenido: Database Contents License
   - ✅ Uso comercial permitido con atribución
   - ✅ Modificación y redistribución permitida

2. **Captura de etiquetas de productos**
   - ✅ Información nutricional es de dominio público (NOM-051)
   - ⚠️ Logos y marcas requieren Fair Use
   - ✅ Uso educativo y de salud pública generalmente permitido

3. **Contribución a Open Food Facts**
   - ✅ Beneficia a la comunidad global
   - ✅ Mejora la base de datos para todos
   - ✅ Alineado con misión de salud pública

---

## 🎯 Métricas de Éxito

### KPIs Iniciales (3 meses)

- [ ] **Tasa de escaneos exitosos:** > 60%
- [ ] **Tiempo promedio de respuesta:** < 2 segundos
- [ ] **Productos en BD local:** > 500
- [ ] **Precisión de sellos NOM-051:** > 95%
- [ ] **Usuarios activos escaneando:** > 100/mes
- [ ] **Contribuciones a Open Food Facts:** > 50 productos

---

## 📚 Referencias

1. **Open Food Facts**
   - Wiki México: https://wiki.openfoodfacts.org/Country_Support_-_Mexico
   - API Docs: https://openfoodfacts.github.io/openfoodfacts-server/api/
   - Datos Abiertos: https://world.openfoodfacts.org/data

2. **NOM-051**
   - Manual Oficial COFEPRIS: https://www.gob.mx/cms/uploads/attachment/file/653733/MANUAL_NOM051_v16.pdf
   - DOF 2020: https://www.dof.gob.mx/2020/SEECO/NOM_051.pdf

3. **GS1 México**
   - Blog Códigos de Barras: https://blog.gs1mexico.org/codigo-de-barras

4. **Librerías React**
   - react-qr-barcode-scanner: https://www.npmjs.com/package/react-qr-barcode-scanner
   - html5-qrcode: https://github.com/mebjas/html5-qrcode

---

## ✅ Conclusiones y Recomendaciones

### ✅ Enfoque Recomendado: Sistema Híbrido

1. **Open Food Facts como base** (gratuita, 12k productos)
2. **Base de datos propia** para productos mexicanos específicos
3. **AI Vision para captura manual** de productos faltantes
4. **Contribución comunitaria** gamificada

### 🚀 Siguientes Pasos

1. Crear migración de base de datos `productos_nom051`
2. Implementar endpoints FastAPI para CRUD de productos
3. Crear cliente para Open Food Facts API
4. Implementar cálculo automático de sellos NOM-051
5. Integrar librería de escaneo en frontend React
6. Diseñar UI/UX de resultados con sellos

### 💡 Valor Agregado

Este enfoque no solo resuelve el problema de datos hardcodeados, sino que:
- **Crea valor real** para usuarios (información verificada)
- **Es escalable** sin costos prohibitivos
- **Contribuye al bien común** (Open Food Facts)
- **Se diferencia** de competencia (base de datos mexicana)
- **Cumple con NOM-051** (educación nutricional)

---

**Documento preparado por:** Claude AI
**Fecha:** 2025-11-09
**Próxima revisión:** Al completar Fase 1 del MVP
