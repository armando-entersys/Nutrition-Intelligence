# Monitoreo y Observabilidad - Nutrition Intelligence

Este documento describe el sistema de monitoreo configurado para Nutrition Intelligence.

## 🎯 Stack de Monitoreo

El servidor prod-server ya tiene instalado un stack completo de monitoreo:

- **Prometheus** - Recolección de métricas
- **Grafana** - Visualización de dashboards
- **Loki** - Agregación de logs
- **Promtail** - Recolección de logs desde containers
- **AlertManager** - Gestión de alertas

## 📊 Dashboards Disponibles

### Grafana Dashboard

URL: `http://[prod-server-ip]:3000` (acceso via Traefik)

Dashboard: **Nutrition Intelligence - System Overview**

Métricas incluidas:
- Estado de servicios (UP/DOWN)
- Uso de memoria y CPU del backend
- Tasa de requests HTTP
- Tiempos de respuesta (p95)
- Conexiones a base de datos
- Uso de memoria de Redis
- Requests al sistema RAG
- Tasa de errores (4xx y 5xx)

## 🏥 Health Checks

### Script de Health Check Manual

```bash
cd /srv/scram/nutrition-intelligence
bash backend/scripts/health_check.sh
```

Este script verifica:
- ✓ Backend API (/health)
- ✓ Sistema RAG (/api/v1/rag/health)
- ✓ Chat de Nutriólogo (/api/v1/nutritionist-chat/health)
- ✓ Base de datos PostgreSQL
- ✓ Redis
- ✓ Frontend
- ✓ Uso de disco
- ✓ Uso de memoria
- ✓ Integridad de datos (conteo de productos y alimentos)

### Endpoints de Health

- **Backend**: `GET /health`
- **RAG System**: `GET /api/v1/rag/health`
- **Nutritionist Chat**: `GET /api/v1/nutritionist-chat/health`

## 🚨 Alertas Configuradas

### Alertas Críticas

1. **NutritionBackendDown**
   - Trigger: Backend no responde por más de 2 minutos
   - Severidad: Critical

2. **NutritionDatabaseDown**
   - Trigger: PostgreSQL no responde por más de 1 minuto
   - Severidad: Critical

### Alertas de Warning

3. **NutritionHighMemory**
   - Trigger: Uso de memoria del backend > 85% por 5 minutos
   - Severidad: Warning

4. **NutritionSlowResponses**
   - Trigger: Tiempo de respuesta p95 > 2 segundos por 5 minutos
   - Severidad: Warning

5. **NutritionHighErrorRate**
   - Trigger: Tasa de errores 5xx > 5% por 5 minutos
   - Severidad: Warning

6. **NutritionRedisDown**
   - Trigger: Redis no responde por más de 2 minutos
   - Severidad: Warning

## 📝 Logs

### Acceso a Logs en Tiempo Real

```bash
# Backend logs
docker logs -f nutrition-intelligence-backend

# Frontend logs
docker logs -f nutrition-intelligence-frontend

# Database logs
docker logs -f nutrition-intelligence-db

# Redis logs
docker logs -f nutrition-intelligence-redis
```

### Loki (Log Aggregation)

Los logs están siendo recolectados automáticamente por Promtail y enviados a Loki.

Acceso via Grafana:
1. Ir a Grafana → Explore
2. Seleccionar fuente de datos: Loki
3. Filtrar por container: `{container="nutrition-intelligence-backend"}`

Queries útiles:
```
# Errores del backend
{container="nutrition-intelligence-backend"} |= "ERROR"

# Requests HTTP lentos
{container="nutrition-intelligence-backend"} | json | process_time > 2

# Errores 5xx
{container="nutrition-intelligence-backend"} | json | status >= 500
```

## 📈 Métricas Importantes

### Uso de Recursos (Estado Actual)

- **Backend**: ~314 MB RAM (3.95%)
- **PostgreSQL**: ~25 MB RAM (0.31%)
- **Redis**: ~3.4 MB RAM (0.04%)
- **Frontend**: ~3.5 MB RAM (0.04%)

### Umbrales Recomendados

- **CPU**: < 70% promedio
- **Memoria**: < 80% del límite
- **Disco**: < 80% de uso
- **Tiempo de respuesta**: < 1 segundo (p95)
- **Error rate**: < 1%

## 🔧 Mantenimiento

### Rotación de Logs

Los logs de Docker se rotan automáticamente con la configuración:
- Tamaño máximo por archivo: 10m
- Archivos a mantener: 3

### Limpieza de Métricas Antiguas

Prometheus retiene métricas por 15 días por defecto. Para cambiar:
```yaml
storage:
  tsdb:
    retention.time: 30d
```

## 🆘 Troubleshooting

### Backend no responde

```bash
# Verificar estado del container
docker ps | grep nutrition-intelligence-backend

# Ver logs recientes
docker logs nutrition-intelligence-backend --tail 100

# Reiniciar backend
docker restart nutrition-intelligence-backend
```

### Alto uso de memoria

```bash
# Ver uso de recursos en tiempo real
docker stats nutrition-intelligence-backend

# Si es necesario, reiniciar
docker restart nutrition-intelligence-backend
```

### Base de datos lenta

```bash
# Verificar conexiones activas
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "SELECT count(*) FROM pg_stat_activity;"

# Ver queries lentos
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';"
```

## 📞 Contactos

Para problemas críticos:
- Revisar logs en Grafana
- Verificar alertas en AlertManager
- Ejecutar health check manual

## 🔄 Actualizaciones

Última actualización: 2025-11-12
- Configuración inicial de monitoreo
- Health checks implementados
- Dashboards de Grafana creados
- Alertas de Prometheus configuradas
