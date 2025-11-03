# Sistema de Logging - Nutrition Intelligence API

Documentación completa del sistema de logging avanzado con rotación diaria y formatos duales.

## ✅ Estado Actual

**Sistema de logging profesional completamente funcional:**

- ✅ **Rotación diaria automática** - Nuevo archivo cada día (formato `YYYY-MM-DD`)
- ✅ **Rotación por tamaño** - Rota cuando supera 100MB
- ✅ **Compresión automática** - Archivos antiguos se comprimen a `.gz`
- ✅ **Retención de 30 días** - Logs antiguos se archivan y eliminan
- ✅ **Formato dual** - JSON estructurado + Legacy con pipes
- ✅ **Thread-safe** - Manejo seguro en entorno asíncrono
- ✅ **Logs de negocio** - Funciones especializadas para contextos nutricionales

---

## 📊 Ubicación de Logs

```
backend/
└── logs/
    └── nutrition-intelligence-api/
        ├── 2025-10-30.json         # Log JSON del 30 de octubre
        ├── 2025-10-30.legacy       # Log legacy del 30 de octubre
        ├── 2025-10-31.json         # Log JSON de hoy (1.2 MB)
        ├── 2025-10-31.legacy       # Log legacy de hoy (256 KB)
        └── archives/                # Logs comprimidos antiguos
            ├── 2025-10-15.json.gz
            └── 2025-10-15.legacy.gz
```

---

## 📝 Formatos de Log

### 1. Formato JSON (Estructurado)

**Archivo**: `YYYY-MM-DD.json`

**Características**:
- Un objeto JSON por línea (newline-delimited JSON)
- Fácil de parsear con herramientas modernas
- Incluye todos los campos estructurados
- Ideal para análisis con ELK Stack, Splunk, etc.

**Ejemplo**:
```json
{
  "status": "Success",
  "application": "nutrition-intelligence-api",
  "timestamp": "2025-10-31T23:18:57.656449Z",
  "request_id": "req_618786ee",
  "message": "GET /health - 200",
  "endpoint": "/health",
  "method": "GET",
  "user_id": null,
  "response_time_ms": 0,
  "status_code": 200,
  "metadata": {
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0...",
    "content_type": "",
    "query_params": null
  },
  "business_context": {
    "http_method": "GET",
    "endpoint_category": "system"
  },
  "legacy_format": "Success|nutrition-intelligence-api|2025-10-31T23:18:57.656449Z|Mensaje: GET /health - 200"
}
```

### 2. Formato Legacy (Pipes)

**Archivo**: `YYYY-MM-DD.legacy`

**Características**:
- Formato tradicional con pipes `|`
- Fácil de leer con `tail`, `grep`, `awk`
- Compatible con scripts antiguos
- Más liviano que JSON

**Formato**:
```
Status|Application|Timestamp|Mensaje: [mensaje] - Contexto: [contexto]
```

**Ejemplo**:
```
Success|nutrition-intelligence-api|2025-10-31T23:18:57.656449Z|Mensaje: GET /health - 200 - Contexto: http_method:GET, endpoint_category:system
Error|nutrition-intelligence-api|2025-10-31T14:32:15.123456Z|Mensaje: Database connection failed - Contexto: database:postgres, retry_attempt:3
```

---

## 🔄 Rotación de Logs

### Rotación Diaria (Automática)

**Cómo funciona**:
1. Cada día a las 00:00:00 se crea un nuevo archivo
2. Nombre del archivo: `YYYY-MM-DD.json` y `YYYY-MM-DD.legacy`
3. Los logs del día anterior se cierran automáticamente

**Ejemplo**:
```
2025-10-30.json    <- Ayer (151 KB)
2025-10-31.json    <- Hoy (1.2 MB)  ← Archivo activo
```

### Rotación por Tamaño (100 MB)

**Cómo funciona**:
1. Si un archivo supera 100 MB, se rota automáticamente
2. Se comprime con gzip
3. Se mueve a `archives/` con timestamp
4. Se crea un nuevo archivo vacío

**Ejemplo**:
```bash
# Archivo original
2025-10-31.json  (105 MB)

# Después de rotación
2025-10-31.json  (0 KB)     ← Nuevo archivo vacío
archives/2025-10-31_143052.json.gz  (8 MB)  ← Comprimido
```

### Retención de 30 Días

**Cómo funciona**:
1. Logs mayores a 30 días se comprimen
2. Se mueven a `archives/`
3. Después de comprimir, se eliminan los archivos originales
4. La limpieza ocurre automáticamente a medianoche

**Configuración actual**:
```python
self.keep_days = 30  # Retener logs por 30 días
```

---

## 🎯 Niveles de Log

```python
class LogLevel(str, Enum):
    SUCCESS = "Success"   # Operación exitosa
    ERROR = "Error"       # Error en la operación
    WARNING = "Warning"   # Advertencia, operación completada con problemas
    INFO = "Info"         # Información general
    DEBUG = "Debug"       # Información de depuración
```

---

## 💻 Uso del Sistema de Logging

### Importar el Logger

```python
from core.logging import (
    log_success,
    log_error,
    log_warning,
    log_info,
    log_nutritional_calculation,
    log_recipe_interaction,
    log_meal_plan_assignment,
    log_equivalences_tracking
)
```

### Logs Genéricos

```python
# Log de éxito simple
log_success("Usuario creado exitosamente")

# Log de éxito con contexto de negocio
log_success(
    "Plan nutricional generado",
    business_context={
        "patient_id": 123,
        "nutritionist_id": 456,
        "plan_duration_days": 7,
        "total_recipes": 21
    }
)

# Log de error
log_error(
    "Error al conectar con base de datos",
    business_context={
        "database": "postgresql",
        "retry_attempt": 3,
        "error_code": "connection_timeout"
    }
)

# Log de advertencia
log_warning(
    "Memoria RAM alta",
    metadata={
        "memory_usage_percent": 85,
        "threshold": 80
    }
)
```

### Logs Específicos de Negocio

#### 1. Cálculos Nutricionales

```python
log_nutritional_calculation(
    patient_id=123,
    calories=2000.0,
    equivalents={
        "cereales": 8,
        "verduras": 5,
        "frutas": 4,
        "proteinas": 7,
        "lacteos": 3,
        "grasas": 6
    },
    success=True
)
```

**Resultado en log**:
```
Success|nutrition-intelligence-api|2025-10-31T14:30:00.000000Z|Mensaje: Cálculo nutricional completado - 2000.0 kcal, 6 grupos - Contexto: action:nutritional_calculation, patient_id:123, target_calories:2000.0, equivalents_count:6, equivalents_detail:cereales:8, verduras:5, frutas:4, proteinas:7, lacteos:3, grasas:6
```

#### 2. Interacciones con Recetas

```python
# Usuario vio una receta
log_recipe_interaction(
    user_id="user_789",
    recipe_id=42,
    action="viewed"
)

# Usuario calificó una receta
log_recipe_interaction(
    user_id="user_789",
    recipe_id=42,
    action="rated",
    rating=5
)
```

#### 3. Asignación de Planes Alimenticios

```python
log_meal_plan_assignment(
    nutritionist_id="nutri_456",
    patient_id=123,
    plan_id=789,
    recipes_count=21
)
```

**Resultado**:
```
Success|nutrition-intelligence-api|2025-10-31T14:35:00.000000Z|Mensaje: Plan alimenticio asignado - 21 recetas para paciente 123 - Contexto: action:meal_plan_assignment, nutritionist_id:nutri_456, patient_id:123, plan_id:789, recipes_count:21
```

#### 4. Seguimiento de Equivalentes

```python
log_equivalences_tracking(
    patient_id=123,
    equivalents_consumed={
        "cereales": 6.5,
        "verduras": 4.0,
        "frutas": 3.5,
        "proteinas": 7.0,
        "lacteos": 2.0,
        "grasas": 5.5
    },
    adherence_pct=87.5
)
```

### Logs con Request Context (Middleware)

El sistema automáticamente registra todos los requests HTTP:

```python
# Automático para cada request
Success|nutrition-intelligence-api|2025-10-31T14:40:00.000000Z|Mensaje: POST /api/v1/recipes - 201 - Contexto: http_method:POST, endpoint_category:recipes, response_time_ms:45, user_id:user_123
```

---

## 🔍 Consultar Logs

### Ver logs en tiempo real

```bash
# Log JSON (formato estructurado)
tail -f backend/logs/nutrition-intelligence-api/$(date +%Y-%m-%d).json

# Log legacy (más legible)
tail -f backend/logs/nutrition-intelligence-api/$(date +%Y-%m-%d).legacy

# Últimas 100 líneas
tail -n 100 backend/logs/nutrition-intelligence-api/2025-10-31.legacy
```

### Buscar por patrón

```bash
# Buscar errores del día
grep "Error" backend/logs/nutrition-intelligence-api/2025-10-31.legacy

# Buscar logs de un paciente específico
grep "patient_id:123" backend/logs/nutrition-intelligence-api/2025-10-31.legacy

# Buscar cálculos nutricionales
grep "nutritional_calculation" backend/logs/nutrition-intelligence-api/2025-10-31.legacy

# Buscar por endpoint
grep "/api/v1/recipes" backend/logs/nutrition-intelligence-api/2025-10-31.legacy
```

### Análisis con jq (JSON)

```bash
# Instalar jq (si no lo tienes)
# Windows: choco install jq
# Mac: brew install jq
# Linux: apt-get install jq

# Contar requests por status
cat backend/logs/nutrition-intelligence-api/2025-10-31.json | jq -r '.status' | sort | uniq -c

# Listar todos los errores del día
cat backend/logs/nutrition-intelligence-api/2025-10-31.json | jq 'select(.status=="Error")'

# Ver tiempos de respuesta lentos (>1000ms)
cat backend/logs/nutrition-intelligence-api/2025-10-31.json | jq 'select(.response_time_ms > 1000)'

# Extraer business_context de logs de cálculos nutricionales
cat backend/logs/nutrition-intelligence-api/2025-10-31.json | \
  jq 'select(.business_context.action=="nutritional_calculation") | .business_context'
```

### Análisis con Python

```python
import json
from datetime import date
from collections import Counter

# Leer log del día
log_file = f"backend/logs/nutrition-intelligence-api/{date.today()}.json"

with open(log_file) as f:
    logs = [json.loads(line) for line in f]

# Contar por status
status_counts = Counter(log['status'] for log in logs)
print("Status counts:", status_counts)

# Calcular tiempo promedio de respuesta
response_times = [log['response_time_ms'] for log in logs if log['response_time_ms']]
avg_response = sum(response_times) / len(response_times) if response_times else 0
print(f"Average response time: {avg_response:.2f}ms")

# Listar endpoints más utilizados
endpoints = Counter(log['endpoint'] for log in logs if log['endpoint'])
print("Top 10 endpoints:")
for endpoint, count in endpoints.most_common(10):
    print(f"  {endpoint}: {count}")
```

---

## 📈 Integración con Herramientas de Monitoreo

### ELK Stack (Elasticsearch, Logstash, Kibana)

**Configuración de Logstash**:

```ruby
# logstash.conf
input {
  file {
    path => "C:/Nutrition Intelligence/backend/logs/nutrition-intelligence-api/*.json"
    codec => "json"
    type => "nutrition-api"
  }
}

filter {
  if [type] == "nutrition-api" {
    mutate {
      add_field => { "[@metadata][index_name]" => "nutrition-api-%{+YYYY.MM.dd}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "%{[@metadata][index_name]}"
  }
}
```

### Grafana Loki

**Promtail configuration**:

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:3100/loki/api/v1/push

scrape_configs:
  - job_name: nutrition-api
    static_configs:
      - targets:
          - localhost
        labels:
          job: nutrition-api
          __path__: C:/Nutrition Intelligence/backend/logs/nutrition-intelligence-api/*.json
```

### Splunk

```bash
# Agregar input en Splunk
[monitor://C:\Nutrition Intelligence\backend\logs\nutrition-intelligence-api\*.json]
disabled = false
sourcetype = _json
index = nutrition_api
```

---

## ⚙️ Configuración

### Cambiar Retención de Logs

Edita `backend/core/logging/nutrition_logger.py`:

```python
class NutritionLogger:
    def __init__(self, ...):
        # ...
        self.keep_days = 30  # Cambiar a 7, 60, 90, etc.
```

### Cambiar Tamaño de Rotación

```python
class NutritionLogger:
    def __init__(self, ...):
        # ...
        self.max_file_size_mb = 100  # Cambiar a 50, 200, etc.
```

### Cambiar Ubicación de Logs

```python
# En main.py o donde inicialices
from core.logging import NutritionLogger

# Custom logs directory
logger = NutritionLogger(
    app_name="nutrition-intelligence-api",
    logs_base_dir="/var/log/nutrition"  # Cambiar ruta
)
```

---

## 🚨 Alertas y Monitoreo

### Script de Alerta por Errores

```bash
#!/bin/bash
# alert_on_errors.sh

LOG_FILE="backend/logs/nutrition-intelligence-api/$(date +%Y-%m-%d).legacy"
ERROR_COUNT=$(grep -c "Error" "$LOG_FILE")

if [ $ERROR_COUNT -gt 10 ]; then
    echo "⚠️ ALERTA: $ERROR_COUNT errores detectados hoy"
    # Enviar email, Slack, etc.
fi
```

### Monitoreo de Espacio en Disco

```bash
#!/bin/bash
# monitor_disk_space.sh

LOGS_DIR="backend/logs"
USAGE=$(du -sh "$LOGS_DIR" | cut -f1)

echo "📊 Espacio usado por logs: $USAGE"

# Limpiar si es necesario
if [ $(du -s "$LOGS_DIR" | cut -f1) -gt 1000000 ]; then  # >1GB
    echo "⚠️ Logs ocupan más de 1GB, considerar limpieza"
fi
```

---

## 📊 Estadísticas Actuales

**Logs de hoy** (2025-10-31):
```
2025-10-31.json     1.2 MB   (JSON estructurado)
2025-10-31.legacy   256 KB   (Formato legacy)
```

**Logs de ayer** (2025-10-30):
```
2025-10-30.json     151 KB
2025-10-30.legacy    35 KB
```

**Total de logs**: ~1.6 MB

**Archives**: Logs comprimidos antiguos

---

## 🎯 Best Practices

### ✅ Hacer

1. **Usar logs específicos de negocio** cuando sea posible
   ```python
   # Bueno
   log_nutritional_calculation(patient_id, calories, equivalents)

   # En lugar de
   log_info(f"Calculation done for patient {patient_id}")
   ```

2. **Incluir contexto relevante**
   ```python
   log_success(
       "Receta guardada",
       business_context={
           "recipe_id": 123,
           "category": "desayuno",
           "calories": 350
       }
   )
   ```

3. **Usar niveles apropiados**
   - `ERROR`: Fallos que requieren atención inmediata
   - `WARNING`: Problemas potenciales, operación completada
   - `SUCCESS`: Operaciones exitosas importantes
   - `INFO`: Información general
   - `DEBUG`: Solo en desarrollo

### ❌ Evitar

1. **No loggear información sensible**
   ```python
   # MAL ❌
   log_info(f"User logged in with password: {password}")

   # BIEN ✅
   log_success("User logged in", business_context={"user_id": user.id})
   ```

2. **No hacer logging excesivo**
   ```python
   # MAL ❌
   for item in items:
       log_info(f"Processing item {item}")  # Miles de logs

   # BIEN ✅
   log_info(f"Processing {len(items)} items")
   log_success(f"Processed {len(items)} items successfully")
   ```

3. **No loggear en loops de alta frecuencia**
   - Agrupar logs
   - Usar sampling (1 de cada N)

---

## 📚 Recursos Adicionales

- **Documentación structlog**: https://www.structlog.org/
- **JSON Lines format**: http://jsonlines.org/
- **Python logging**: https://docs.python.org/3/library/logging.html
- **ELK Stack**: https://www.elastic.co/elk-stack

---

**Sistema de logging configurado y funcionando** ✅
**Rotación diaria**: ✅ Automática
**Retención**: ✅ 30 días con compresión
**Formatos**: ✅ JSON + Legacy

**Última actualización**: 2025-10-31
