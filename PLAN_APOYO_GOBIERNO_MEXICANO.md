# Plan Exhaustivo: Apoyo a Iniciativas del Gobierno Mexicano en Nutrición 2025

**Fecha**: Noviembre 2025
**Contexto**: Gobierno de la Presidenta Claudia Sheinbaum - Mañanera del Pueblo

---

## RESUMEN EJECUTIVO

Nutrition Intelligence se alineará con las políticas del gobierno mexicano en nutrición y alimentación, específicamente:

1. **Alimentación para el Bienestar** (25,600 Tiendas Bienestar)
2. **Programa Nacional de Soberanía Alimentaria**
3. **NOM-051 Fase 3** (octubre 2025)
4. **Lineamientos Escolares** (marzo 2025)
5. **Guías Alimentarias Saludables y Sostenibles**

---

## FASE 1: INTEGRACIÓN INMEDIATA (0-3 meses)

### 1.1 Base de Datos de Productos Nacionales

**Objetivo**: Catalogar productos de las Tiendas Bienestar y marca "Bienestar"

**Acciones**:
- [ ] Crear base de datos específica de productos "Bienestar"
  - Maíz
  - Frijol
  - Arroz
  - Cacao
  - Café
  - Miel
  - Canasta básica (450 pesos)

**Implementación Técnica**:
```sql
-- Nueva tabla para productos gobierno
CREATE TABLE productos_bienestar (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100), -- maiz, frijol, arroz, cacao, cafe, miel
    precio_justo DECIMAL(10, 2), -- precio pagado a productores
    precio_publico DECIMAL(10, 2), -- precio en tiendas
    origen_estado VARCHAR(100), -- estado productor
    productor_tipo VARCHAR(50), -- pequeño, mediano
    certificacion BOOLEAN DEFAULT FALSE,
    info_nutricional JSONB,
    cumple_nom051 BOOLEAN DEFAULT TRUE,
    disponible_tiendas_bienestar BOOLEAN DEFAULT TRUE,
    codigo_barras VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_productos_bienestar_categoria ON productos_bienestar(categoria);
CREATE INDEX idx_productos_bienestar_estado ON productos_bienestar(origen_estado);
```

**API Endpoints**:
```
GET /api/v1/productos-bienestar
GET /api/v1/productos-bienestar/{id}
GET /api/v1/productos-bienestar/categoria/{categoria}
GET /api/v1/productos-bienestar/estado/{estado}
GET /api/v1/tiendas-bienestar/cercanas?lat={lat}&lon={lon}
```

### 1.2 NOM-051 Fase 3 Compliance

**Objetivo**: Actualizar sistema para cumplir con criterios más estrictos de Fase 3

**Cambios Técnicos**:

**Fase 3 (Octubre 2025)**: Criterios más estrictos para nutrientes añadidos Y no añadidos

**Actualización de Algoritmo de Sellos**:
```python
# backend/services/nom051_phase3.py

LIMITES_FASE3 = {
    "calorias": {
        "solidos": 275,  # kcal por 100g (más estricto que Fase 2: 300)
        "liquidos": 70   # kcal por 100ml (más estricto que Fase 2: 80)
    },
    "azucares": {
        "solidos": 10,   # % de energía (más estricto que Fase 2: 15%)
        "liquidos": 5    # % de energía (más estricto que Fase 2: 7.5%)
    },
    "grasas_saturadas": {
        "solidos": 10,   # % de energía (igual que Fase 2)
        "liquidos": 10
    },
    "grasas_trans": {
        "todos": 1       # % de energía (igual que Fase 2)
    },
    "sodio": {
        "solidos": 300,  # mg por 100g (más estricto que Fase 2: 350)
        "liquidos": 100  # mg por 100ml (más estricto que Fase 2: 120)
    }
}

# Actualizar para incluir nutrientes NO añadidos
def evaluar_producto_fase3(producto):
    """
    Evalúa producto según NOM-051 Fase 3 (octubre 2025)
    Incluye nutrientes añadidos Y no añadidos
    """
    sellos = []

    # Evaluar todos los nutrientes críticos (sin distinción de añadidos)
    if producto.calorias_por_100g > LIMITES_FASE3["calorias"]["solidos"]:
        sellos.append("EXCESO_CALORIAS")

    # ... resto de evaluaciones más estrictas

    return sellos
```

### 1.3 Módulo de Soberanía Alimentaria

**Objetivo**: Promover productos nacionales y autoabastecimiento

**Funcionalidades**:
1. Badge "Producto Nacional" en escáner
2. Filtro "Hecho en México" en búsquedas
3. Mapa de productores locales por estado
4. Información de origen del producto

**UI Component**:
```javascript
// frontend/src/components/scanner/NationalProductBadge.js

const NationalProductBadge = ({ producto }) => {
  if (!producto.es_nacional) return null;

  return (
    <div className="bg-green-100 border-2 border-green-600 rounded-lg p-4 my-4">
      <div className="flex items-center gap-3">
        <span className="text-3xl">🇲🇽</span>
        <div>
          <h4 className="font-bold text-green-800">Producto Nacional</h4>
          <p className="text-sm text-green-700">
            Apoya la soberanía alimentaria mexicana
          </p>
          {producto.origen_estado && (
            <p className="text-xs text-green-600 mt-1">
              Producido en: {producto.origen_estado}
            </p>
          )}
        </div>
      </div>

      {producto.disponible_tiendas_bienestar && (
        <div className="mt-3 flex items-center gap-2 text-sm">
          <svg className="w-4 h-4 text-green-600">...</svg>
          <span>Disponible en Tiendas Bienestar</span>
        </div>
      )}
    </div>
  );
};
```

---

## FASE 2: INTEGRACIÓN CON SISTEMA EDUCATIVO (3-6 meses)

### 2.1 Módulo Escolar para Cafeterías

**Objetivo**: Cumplir con lineamientos escolares (vigentes desde marzo 2025)

**Nuevos Lineamientos Escolares**:
- Prohibición de venta de productos con sellos de advertencia
- Promoción de productos regionales de temporada
- Menús saludables certificados
- Educación nutricional integrada

**Sistema para Escuelas**:

**Base de Datos Escolar**:
```sql
CREATE TABLE escuelas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cct VARCHAR(20) UNIQUE NOT NULL, -- Clave de Centro de Trabajo
    nivel VARCHAR(50), -- preescolar, primaria, secundaria, preparatoria
    estado VARCHAR(100),
    municipio VARCHAR(100),
    tipo VARCHAR(50), -- pública, privada
    tiene_cafeteria BOOLEAN DEFAULT FALSE,
    certificada_salud BOOLEAN DEFAULT FALSE,
    responsable_nombre VARCHAR(255),
    responsable_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE menus_escolares (
    id SERIAL PRIMARY KEY,
    escuela_id INTEGER REFERENCES escuelas(id),
    fecha DATE NOT NULL,
    turno VARCHAR(20), -- matutino, vespertino
    menu_json JSONB, -- desayuno, refrigerio, comida
    calorias_totales INTEGER,
    cumple_lineamientos BOOLEAN DEFAULT FALSE,
    productos_regionales INTEGER DEFAULT 0,
    aprobado_por VARCHAR(255),
    aprobado_fecha TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE productos_permitidos_escuelas (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER REFERENCES productos_nom051(id),
    nivel_educativo VARCHAR(50),
    permitido BOOLEAN DEFAULT TRUE,
    razon_restriccion TEXT,
    alternativa_sugerida INTEGER REFERENCES productos_nom051(id)
);
```

**Dashboard para Nutriólogos Escolares**:
```
/dashboard/escuelas
  - Registro de escuela
  - Crear menú semanal
  - Verificar cumplimiento de lineamientos
  - Generar reportes para SEP
  - Catálogo de productos permitidos
  - Educación nutricional (materiales descargables)
```

### 2.2 Contenido Educativo

**Materiales para Escuelas**:
- Videos educativos sobre NOM-051
- Guías de lectura de etiquetas para niños
- Actividades interactivas sobre alimentación saludable
- Recetas con productos nacionales
- Material para padres de familia

---

## FASE 3: GUÍAS ALIMENTARIAS OFICIALES (6-9 meses)

### 3.1 Integración de Guías Alimentarias Saludables y Sostenibles

**Objetivo**: Implementar las Guías Alimentarias oficiales publicadas en 2025

**Características de las Guías**:
- Basadas en Ley General de Alimentación Adecuada y Sostenible (abril 2024)
- Plan Nacional de Desarrollo 2025-2030
- Programa Sectorial de Salud 2025-2030
- Énfasis en alimentos de temporada
- Producción familiar y mediana
- Sostenibilidad ambiental

**Implementación en IA Chat**:
```python
# backend/services/guias_alimentarias.py

GUIAS_ALIMENTARIAS_2025 = {
    "cereales_tuberculos": {
        "porciones_diarias": "6-8",
        "preferir": ["maíz nixtamalizado", "tortilla", "frijol", "arroz integral"],
        "nacionales": True,
        "temporada": ["maíz: todo el año", "frijol: octubre-marzo"]
    },
    "frutas_verduras": {
        "porciones_diarias": "5+",
        "preferir": ["nopales", "quelites", "chayote", "guayaba", "papaya"],
        "locales_temporada": True,
        "color_variado": True
    },
    "leguminosas": {
        "porciones_diarias": "2-3",
        "preferir": ["frijol negro", "frijol pinto", "lenteja", "garbanzo"],
        "proteina_sostenible": True
    },
    "productos_animales": {
        "porciones_diarias": "1-2",
        "moderar": True,
        "preferir": ["pescado local", "pollo sin piel", "huevo"],
        "limitar": ["carnes rojas", "embutidos"]
    },
    "evitar": [
        "bebidas azucaradas",
        "productos ultraprocesados con sellos",
        "comida rápida frecuente",
        "alimentos con grasas trans"
    ]
}

class GuiasAlimentariasService:
    def evaluar_plan_alimenticio(self, plan):
        """Evalúa si un plan cumple con las Guías Alimentarias 2025"""
        evaluacion = {
            "cumple_porciones": self._verificar_porciones(plan),
            "productos_nacionales": self._contar_nacionales(plan),
            "productos_temporada": self._verificar_temporada(plan),
            "sostenibilidad": self._evaluar_sostenibilidad(plan),
            "recomendaciones": []
        }
        return evaluacion
```

**Actualización del Chat IA**:
```
Prompt System adicional:

"Eres un nutricionista que sigue las Guías Alimentarias Saludables y
Sostenibles para la Población Mexicana (2025). Debes:

1. Priorizar alimentos mexicanos de temporada
2. Promover productos de pequeños y medianos productores
3. Recomendar alimentos disponibles en Tiendas Bienestar
4. Fomentar la soberanía alimentaria
5. Considerar la sostenibilidad ambiental
6. Respetar la cultura alimentaria mexicana tradicional
7. Promover el consumo de nopales, quelites, frijol, maíz nixtamalizado

Cuando un usuario pregunte sobre alimentación, considera:
- Disponibilidad regional
- Temporada del año
- Accesibilidad económica (priorizar Tiendas Bienestar)
- Impacto ambiental
- Cultura local"
```

---

## FASE 4: COLABORACIÓN INSTITUCIONAL (9-12 meses)

### 4.1 Integración con Tiendas Bienestar

**Objetivo**: Facilitar acceso a productos de 25,600 Tiendas Bienestar

**API de Localización**:
```python
# backend/api/tiendas_bienestar.py

from fastapi import APIRouter, Depends
from services.geolocation import calcular_distancia

router = APIRouter(prefix="/api/v1/tiendas-bienestar", tags=["Tiendas Bienestar"])

@router.get("/cercanas")
async def obtener_tiendas_cercanas(
    lat: float,
    lon: float,
    radio_km: int = 5
):
    """
    Encuentra Tiendas Bienestar cercanas a ubicación del usuario
    """
    tiendas = await db.query(
        """
        SELECT *,
               calcular_distancia($1, $2, latitud, longitud) as distancia_km
        FROM tiendas_bienestar
        WHERE calcular_distancia($1, $2, latitud, longitud) <= $3
        ORDER BY distancia_km
        LIMIT 20
        """,
        lat, lon, radio_km
    )

    return {
        "success": True,
        "total": len(tiendas),
        "tiendas": tiendas
    }

@router.get("/productos-disponibles/{tienda_id}")
async def productos_disponibles_tienda(tienda_id: int):
    """
    Lista productos Bienestar disponibles en tienda específica
    """
    productos = await db.query(
        """
        SELECT pb.*, td.stock, td.precio_actual
        FROM productos_bienestar pb
        JOIN tienda_disponibilidad td ON pb.id = td.producto_id
        WHERE td.tienda_id = $1 AND td.stock > 0
        ORDER BY pb.categoria
        """,
        tienda_id
    )

    return productos
```

**Mapa Interactivo en Frontend**:
```javascript
// frontend/src/components/tiendas/MapaTiendasBienestar.js

const MapaTiendasBienestar = () => {
  const [ubicacion, setUbicacion] = useState(null);
  const [tiendas, setTiendas] = useState([]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        const { latitude, longitude } = pos.coords;
        setUbicacion({ lat: latitude, lon: longitude });
        cargarTiendasCercanas(latitude, longitude);
      });
    }
  }, []);

  const cargarTiendasCercanas = async (lat, lon) => {
    const res = await api.get(`/tiendas-bienestar/cercanas?lat=${lat}&lon=${lon}&radio_km=10`);
    setTiendas(res.data.tiendas);
  };

  return (
    <div className="mapa-tiendas">
      <h2>Tiendas Bienestar Cercanas</h2>
      <div className="mapa-container">
        {/* Integrar Google Maps / OpenStreetMap */}
        <MapaInteractivo
          centro={ubicacion}
          marcadores={tiendas}
        />
      </div>

      <div className="lista-tiendas">
        {tiendas.map(tienda => (
          <TiendaBienestarCard
            key={tienda.id}
            tienda={tienda}
            onVerProductos={() => navigate(`/tiendas-bienestar/${tienda.id}`)}
          />
        ))}
      </div>
    </div>
  );
};
```

### 4.2 Dashboard para GISAMAC

**GISAMAC**: Gabinete Intersectorial del Sistema Nacional de Salud, Alimentación, Medio Ambiente y Competitividad

**Objetivo**: Proveer datos para coordinación de políticas públicas

**Métricas para Gobierno**:
```python
# backend/api/analytics/gobierno.py

@router.get("/analytics/gobierno/dashboard")
async def dashboard_gobierno(
    estado: Optional[str] = None,
    fecha_inicio: date = None,
    fecha_fin: date = None
):
    """
    Dashboard de métricas para análisis gubernamental
    """
    metricas = {
        "adopcion_nom051": {
            "usuarios_escanean_sellos": await contar_usuarios_activos_sellos(),
            "productos_mas_escaneados": await productos_top_escaneados(),
            "conciencia_sellos_pct": await calcular_conciencia_sellos()
        },

        "productos_nacionales": {
            "preferencia_productos_nacionales_pct": await calcular_preferencia_nacional(),
            "productos_bienestar_consumidos": await contar_productos_bienestar(),
            "estados_mayor_consumo_local": await ranking_estados_consumo_local()
        },

        "escuelas": {
            "escuelas_registradas": await contar_escuelas(),
            "menus_certificados": await contar_menus_certificados(),
            "cumplimiento_lineamientos_pct": await calcular_cumplimiento_escolar()
        },

        "salud_poblacional": {
            "usuarios_mejorando_dieta": await usuarios_progreso_positivo(),
            "reduccion_productos_ultraprocesados_pct": await calcular_reduccion_ultraprocesados(),
            "aumento_consumo_frutas_verduras_pct": await calcular_aumento_frutas_verduras()
        },

        "soberania_alimentaria": {
            "usuarios_prefieren_locales": await contar_usuarios_locales(),
            "productos_temporada_consumidos": await contar_productos_temporada(),
            "impacto_tiendas_bienestar": await calcular_impacto_tiendas()
        }
    }

    if estado:
        metricas["estado_especifico"] = await metricas_por_estado(estado)

    return metricas
```

**API Key para Instituciones Gubernamentales**:
```
Acceso especial para:
- Secretaría de Salud
- Secretaría de Agricultura (SADER)
- Secretaría de Economía
- SEP (Secretaría de Educación Pública)
- DIF Nacional
- GISAMAC

Con endpoints de solo lectura para análisis de políticas públicas
```

---

## FASE 5: CAMPAÑAS DE CONCIENTIZACIÓN (12+ meses)

### 5.1 Programa "México Saludable"

**Objetivo**: Campaña nacional de educación nutricional

**Componentes**:

1. **Serie de Webinars Gratuitos**
   - "Cómo leer etiquetas NOM-051"
   - "Cocina con productos nacionales"
   - "Alimentación escolar saludable"
   - "Soberanía alimentaria familiar"

2. **Reto Nacional "30 Días México Saludable"**
   - Consumir solo productos sin sellos por 30 días
   - Priorizar productos de Tiendas Bienestar
   - Recetas con productos regionales
   - Gamificación con badges y premios

3. **Alianzas con Influencers**
   - Nutriólogos certificados
   - Chefs que promuevan cocina mexicana saludable
   - Creadores de contenido de salud

### 5.2 Colaboración con Medios

**Difusión en Mañanera del Pueblo**:
- Presentar estadísticas de impacto
- Casos de éxito de usuarios
- Datos sobre adopción de productos nacionales
- Resultados de programas escolares

---

## INDICADORES DE ÉXITO (KPIs)

### Métricas de Impacto Social

| Indicador | Meta Año 1 | Meta Año 3 |
|-----------|------------|------------|
| Usuarios activos | 100,000 | 1,000,000 |
| Productos Bienestar catalogados | 500 | 2,000 |
| Escuelas usando el sistema | 500 | 5,000 |
| Escaneos de productos nacionales | 50,000/mes | 500,000/mes |
| Usuarios que prefieren productos sin sellos | 60% | 85% |
| Incremento consumo productos locales | 25% | 50% |
| Nutriólogos profesionales en plataforma | 500 | 5,000 |

### Métricas Gubernamentales

| Indicador | Descripción |
|-----------|-------------|
| Conciencia NOM-051 | % usuarios que entienden sellos |
| Adopción Guías Alimentarias | % usuarios siguiendo guías oficiales |
| Impacto Tiendas Bienestar | Usuarios comprando en Tiendas Bienestar |
| Cumplimiento Escolar | % escuelas cumpliendo lineamientos |
| Soberanía Alimentaria | % productos nacionales vs importados |

---

## PRESUPUESTO ESTIMADO

### Fase 1 (0-3 meses): $150,000 MXN
- Desarrollo base de datos productos Bienestar: $50,000
- Actualización NOM-051 Fase 3: $40,000
- Módulo soberanía alimentaria: $40,000
- Testing y QA: $20,000

### Fase 2 (3-6 meses): $200,000 MXN
- Sistema escolar completo: $100,000
- Contenido educativo: $50,000
- Integración con SEP: $30,000
- Marketing inicial: $20,000

### Fase 3 (6-9 meses): $180,000 MXN
- Integración Guías Alimentarias: $60,000
- Actualización IA Chat: $50,000
- Contenido regional: $40,000
- Certificaciones: $30,000

### Fase 4 (9-12 meses): $250,000 MXN
- API Tiendas Bienestar: $80,000
- Mapa interactivo: $50,000
- Dashboard GISAMAC: $70,000
- Infraestructura adicional: $50,000

### Fase 5 (12+ meses): $300,000 MXN
- Campaña nacional: $150,000
- Webinars y eventos: $50,000
- Influencers y contenido: $70,000
- Análisis y reportes: $30,000

**TOTAL ESTIMADO AÑO 1**: $1,080,000 MXN (~$54,000 USD)

---

## FINANCIAMIENTO PROPUESTO

### Fuentes Potenciales:

1. **Subsidio Gubernamental**
   - Solicitar apoyo de SADER para módulo productores
   - SEP para sistema escolar
   - Secretaría de Salud para campaña preventiva

2. **Convenios Institucionales**
   - GISAMAC
   - DIF Nacional
   - IMSS/ISSSTE (prevención)

3. **Modelo Freemium**
   - Usuarios básicos: Gratis
   - Escuelas: Plan institucional
   - Nutriólogos: Suscripción profesional
   - Empresas: Plan corporativo wellness

4. **Patrocinios**
   - Productores nacionales certificados
   - Cooperativas agrícolas
   - Marcas comprometidas con salud

---

## RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Cambios en políticas gubernamentales | Media | Alto | Diseño modular y flexible |
| Falta de datos de Tiendas Bienestar | Alta | Medio | Convenio directo con SADER |
| Resistencia escuelas privadas | Media | Medio | Enfoque en beneficios, no obligación |
| Desinformación sobre NOM-051 | Alta | Alto | Campaña educativa masiva |
| Problemas técnicos de integración | Media | Medio | APIs bien documentadas |

---

## CRONOGRAMA DE IMPLEMENTACIÓN

### Q1 2025 (Enero - Marzo)
- ✅ Investigación de políticas
- ✅ Diseño de arquitectura
- 🔄 Desarrollo Fase 1
- 🔄 Pruebas iniciales

### Q2 2025 (Abril - Junio)
- Lanzamiento módulo productos Bienestar
- Actualización NOM-051 Fase 3 (antes de octubre)
- Inicio sistema escolar
- Primera campaña educativa

### Q3 2025 (Julio - Septiembre)
- Sistema escolar completo
- Integración Guías Alimentarias
- Preparación para Fase 3 NOM-051 (oct 1)
- Convenios con escuelas piloto

### Q4 2025 (Octubre - Diciembre)
- Lanzamiento oficial NOM-051 Fase 3
- API Tiendas Bienestar
- Dashboard GISAMAC beta
- Evaluación de resultados

### 2026
- Expansión nacional
- Campaña masiva
- Análisis de impacto poblacional
- Nuevas funcionalidades según feedback

---

## PRÓXIMOS PASOS INMEDIATOS

1. **Esta Semana**
   - ✅ Crear este plan estratégico
   - [ ] Presentar plan a equipo
   - [ ] Definir prioridades técnicas
   - [ ] Contactar SADER/Secretaría de Salud

2. **Próximo Mes**
   - [ ] Desarrollo base de datos productos Bienestar
   - [ ] Actualizar algoritmo NOM-051 Fase 3
   - [ ] Crear mockups de UI para módulos nuevos
   - [ ] Solicitar reunión con GISAMAC

3. **Próximos 3 Meses**
   - [ ] Lanzar beta de productos Bienestar
   - [ ] Convenio con 10 escuelas piloto
   - [ ] Campaña inicial en redes sociales
   - [ ] Presentación en foro de nutrición

---

## CONCLUSIÓN

Este plan alinea Nutrition Intelligence con las principales iniciativas del Gobierno de México bajo la presidencia de Claudia Sheinbaum:

✅ **Alimentación para el Bienestar** - Catalogar y promover productos de 25,600 tiendas
✅ **Soberanía Alimentaria** - Priorizar productos nacionales y productores locales
✅ **NOM-051 Fase 3** - Cumplimiento total de etiquetado más estricto
✅ **Educación Nutricional** - Sistema para escuelas y familias
✅ **Guías Alimentarias Oficiales** - Implementación de recomendaciones 2025

La plataforma se convierte en un **aliado tecnológico del gobierno** para mejorar la salud nutricional de la población mexicana, promover la economía local, y garantizar la soberanía alimentaria.

**Impacto Esperado**: 1,000,000 de mexicanos con acceso a información nutricional de calidad, cumplimiento de políticas gubernamentales, y promoción de una alimentación saludable, sostenible y nacional.

---

**Elaborado por**: Claude Code
**Para**: Nutrition Intelligence Platform
**En apoyo a**: Gobierno de México - Presidenta Claudia Sheinbaum
**Alineado con**: Mañanera del Pueblo - Lunes de Vida Saludable
