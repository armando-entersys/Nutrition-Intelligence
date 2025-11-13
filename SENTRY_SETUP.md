# Sentry Error Monitoring Setup

## Descripción

Sentry está configurado para monitorear errores y rendimiento de la aplicación en producción. Captura excepciones no manejadas, errores de validación, y métricas de performance.

## Características Configuradas

### 1. Error Tracking
- ✅ Captura automática de todas las excepciones no manejadas
- ✅ Stack traces completos con contexto
- ✅ Filtrado de datos sensibles (headers, passwords, tokens)
- ✅ Breadcrumbs para debugging (últimas 50 acciones)
- ✅ Context tags para facilitar búsqueda

### 2. Performance Monitoring
- ✅ Transactions HTTP por endpoint
- ✅ Integración con SQLAlchemy para queries
- ✅ Integración con Redis para cache operations
- ✅ Sample rate: 100% en development, 10% en production

### 3. Integraciones Activas
- **FastAPI Integration**: Captura errores HTTP y rutas
- **SQLAlchemy Integration**: Monitorea queries lentas
- **Redis Integration**: Tracking de operaciones de cache
- **Logging Integration**: Captura logs de ERROR level como eventos

### 4. Filtros de Seguridad
Se filtran automáticamente antes de enviar a Sentry:
- Headers: `authorization`, `cookie`, `x-api-key`
- Query params: `password`, `token`
- Health checks: `/health`, `/metrics` no generan eventos

## Configuración

### 1. Obtener DSN de Sentry

1. Crear cuenta en [sentry.io](https://sentry.io)
2. Crear nuevo proyecto tipo "Python" → "FastAPI"
3. Copiar el DSN que aparece

### 2. Configurar Variables de Entorno

Agregar al archivo `.env`:

```bash
# Sentry Error Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
ENVIRONMENT=production  # o development, staging
```

### 3. Verificar Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# El backend se inicia automáticamente con Sentry
docker-compose up -d backend

# Verificar logs
docker logs nutrition-intelligence-backend | grep -i sentry
```

## Uso en Código

### 1. Capturar Excepciones Manualmente

```python
from core.sentry import capture_exception, add_breadcrumb

try:
    # código riesgoso
    result = process_payment(order_id)
except PaymentError as e:
    # Agregar contexto
    add_breadcrumb(
        message=f"Payment failed for order {order_id}",
        category="payment",
        level="error",
        data={"order_id": order_id, "amount": amount}
    )

    # Capturar excepción
    capture_exception(e, context={
        "payment": {
            "order_id": order_id,
            "amount": amount,
            "method": payment_method
        }
    })
    raise
```

### 2. Capturar Mensajes

```python
from core.sentry import capture_message

capture_message(
    "Usuario intentó acceder a recurso sin permisos",
    level="warning",
    context={
        "user_id": user_id,
        "resource": resource_name
    }
)
```

### 3. Establecer Contexto de Usuario

```python
from core.sentry import set_user_context

# En el middleware de autenticación
set_user_context(
    user_id=current_user.id,
    email=current_user.email,
    role=current_user.role
)
```

### 4. Performance Tracking

```python
from core.sentry import start_transaction

# Monitorear operación específica
with start_transaction(name="process_nutrition_plan", op="function"):
    plan = generate_meal_plan(patient_id)
    save_plan_to_db(plan)
```

## Dashboards en Sentry

### Issues Dashboard
- Ver todos los errores por frecuencia
- Agrupar por tipo de error
- Ver stack traces completos
- Asignar errores a developers

### Performance Dashboard
- Transactions más lentas
- Throughput por endpoint
- P50, P75, P95, P99 percentiles
- Queries SQL lentas

### Releases
- Comparar estabilidad entre versiones
- Ver errores introducidos en cada release
- Tracking de despliegues

## Alertas Configuradas

### 1. Error Spike (Recomendado)
```yaml
Condition: Más de 10 errores en 1 minuto
Action: Enviar email + Slack notification
```

### 2. New Issue (Recomendado)
```yaml
Condition: Primer error de un tipo nuevo
Action: Enviar email a equipo
```

### 3. Performance Degradation
```yaml
Condition: P95 response time > 2 segundos
Action: Enviar notificación
```

## Mejores Prácticas

### ✅ DO

1. **Agregar Breadcrumbs**: Usar `add_breadcrumb()` antes de operaciones críticas
2. **Context Rico**: Incluir IDs de usuarios, recursos, timestamps
3. **Niveles Apropiados**:
   - `debug`: Información de debugging
   - `info`: Operaciones normales
   - `warning`: Situaciones anormales pero manejables
   - `error`: Errores que requieren atención
4. **Releases**: Actualizar version en `core/config.py`
5. **Environment Tags**: Usar diferentes proyectos para dev/staging/prod

### ❌ DON'T

1. **No enviar PII**: Datos personales sensibles (números de tarjeta, SSN, etc.)
2. **No sobre-reportar**: Health checks y endpoints internos
3. **No ignorar errores**: Si captura manualmente, también debe manejar
4. **No en loops**: Evitar `capture_exception()` dentro de loops grandes
5. **No datos masivos**: Limitar tamaño de contexto (<1MB)

## Troubleshooting

### Error: "Sentry DSN not configured"

```bash
# Verificar que la variable existe
echo $SENTRY_DSN

# Si está vacía, agregar al .env
echo "SENTRY_DSN=https://your-dsn@sentry.io/123456" >> backend/.env

# Reiniciar backend
docker-compose restart backend
```

### Error: "sentry_sdk module not found"

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# O reconstruir contenedor
docker-compose build backend
```

### No aparecen errores en Sentry

1. Verificar que DSN es correcto
2. Verificar que environment no es "test"
3. Forzar un error de prueba:
   ```python
   from core.sentry import capture_message
   capture_message("Test message", level="error")
   ```
4. Revisar logs del backend:
   ```bash
   docker logs nutrition-intelligence-backend | grep -i sentry
   ```

## Costos

Sentry ofrece:
- **Free Tier**: 5,000 eventos/mes (suficiente para desarrollo)
- **Team Plan**: $26/mes - 50,000 eventos
- **Business Plan**: $80/mes - 500,000 eventos

Recomendación: Empezar con Free Tier y monitorear uso.

## Referencias

- [Sentry Python SDK](https://docs.sentry.io/platforms/python/)
- [FastAPI Integration](https://docs.sentry.io/platforms/python/guides/fastapi/)
- [Performance Monitoring](https://docs.sentry.io/product/performance/)
- [Best Practices](https://docs.sentry.io/platforms/python/best-practices/)
