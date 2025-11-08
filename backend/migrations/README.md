# Database Migrations

Este directorio contiene scripts de migración SQL para la base de datos de Nutrition Intelligence.

## Migraciones Disponibles

### 001_add_nutritionist_id.sql
**Fecha**: 2025-11-04
**Descripción**: Agrega la relación paciente-nutricionista

**Cambios**:
- Agrega columna `nutritionist_id` a la tabla `auth_users`
- Crea índice para mejorar el rendimiento de búsquedas
- Documenta la columna con comentarios en español

### 002_create_notifications_table.sql
**Fecha**: 2025-11-08
**Descripción**: Crea el sistema completo de notificaciones

**Cambios**:
- Crea 3 tipos ENUM: `notification_type`, `notification_priority`, `notification_status`
- Crea tabla `notifications` con 20+ campos
- Crea 9 índices optimizados para consultas comunes
- Documenta todas las columnas con comentarios en español

## Cómo Ejecutar las Migraciones

### Opción 1: Usando Docker Compose (Desarrollo Local)

```bash
# 1. Asegúrate de que el contenedor de PostgreSQL esté corriendo
docker compose up -d postgres

# 2. Ejecuta la migración desde el contenedor del backend
docker compose exec backend sh -c 'psql $DATABASE_URL -f /app/migrations/002_create_notifications_table.sql'
```

### Opción 2: Usando psql directamente (Desarrollo Local)

```bash
# 1. Conectarse a la base de datos local
psql -h localhost -U nutrition_user -d nutrition_intelligence

# 2. Ejecutar el script
\i backend/migrations/002_create_notifications_table.sql

# 3. Verificar que la tabla fue creada
\dt notifications
\d notifications
```

### Opción 3: Usando Docker en Producción

```bash
# SSH al servidor de producción
gcloud compute ssh prod-server --zone=us-central1-c --project=mi-infraestructura-web

# Navegar al directorio del proyecto
cd /srv/scram-apps/nutrition-intelligence

# Pull de los últimos cambios
git pull origin main

# Ejecutar la migración
docker compose exec -T backend sh -c 'psql $DATABASE_URL -f /app/migrations/002_create_notifications_table.sql'

# Verificar que la tabla fue creada
docker compose exec -T postgres psql -U nutrition_user -d nutrition_intelligence -c '\dt notifications'
docker compose exec -T postgres psql -U nutrition_user -d nutrition_intelligence -c '\d notifications'
```

## Verificar el Estado de las Migraciones

### Verificar que la tabla notifications existe

```sql
-- Listar todas las tablas
\dt

-- Ver la estructura de la tabla notifications
\d notifications

-- Ver los tipos ENUM creados
\dT notification_type
\dT notification_priority
\dT notification_status

-- Contar registros en la tabla
SELECT COUNT(*) FROM notifications;
```

### Verificar los índices creados

```sql
-- Ver todos los índices de la tabla notifications
\di notifications*

-- O con una consulta SQL
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'notifications';
```

## Rollback de Migraciones

Si necesitas revertir una migración, aquí están los comandos de rollback:

### Rollback de 002_create_notifications_table.sql

```sql
-- Eliminar tabla
DROP TABLE IF EXISTS notifications CASCADE;

-- Eliminar tipos ENUM
DROP TYPE IF EXISTS notification_type;
DROP TYPE IF EXISTS notification_priority;
DROP TYPE IF EXISTS notification_status;
```

### Rollback de 001_add_nutritionist_id.sql

```sql
-- Eliminar índice
DROP INDEX IF EXISTS idx_auth_users_nutritionist_id;

-- Eliminar columna
ALTER TABLE auth_users DROP COLUMN IF EXISTS nutritionist_id;
```

## Mejores Prácticas

1. **Siempre haz backup antes de ejecutar migraciones en producción**
   ```bash
   # Backup de la base de datos completa
   docker compose exec postgres pg_dump -U nutrition_user nutrition_intelligence > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Prueba las migraciones en desarrollo primero**
   - Ejecuta la migración en tu entorno local
   - Verifica que no hay errores
   - Prueba la funcionalidad que depende de los cambios
   - Solo después despliega a producción

3. **Documenta todos los cambios**
   - Cada migración debe tener un comentario describiendo los cambios
   - Incluye la fecha de la migración
   - Explica por qué se hizo el cambio

4. **Usa transacciones cuando sea posible**
   ```sql
   BEGIN;
   -- Tus cambios aquí
   COMMIT;
   -- O ROLLBACK; si algo sale mal
   ```

5. **Verifica después de ejecutar**
   - Siempre verifica que la migración se aplicó correctamente
   - Revisa logs de errores
   - Prueba las operaciones básicas de la aplicación

## Troubleshooting

### Error: "relation already exists"
La migración ya fue ejecutada. Verifica con `\dt` si la tabla existe.

### Error: "type already exists"
El tipo ENUM ya existe. Puedes continuar sin problemas o usar `DROP TYPE IF EXISTS` primero.

### Error: "permission denied"
Asegúrate de que el usuario de la base de datos tiene permisos suficientes. Revisa las líneas de `GRANT` al final del script.

### Error: "could not connect to database"
Verifica que:
- El contenedor de PostgreSQL está corriendo: `docker compose ps postgres`
- La variable `DATABASE_URL` está configurada correctamente
- El puerto 5432 está accesible

## Contacto

Si tienes preguntas sobre las migraciones, contacta al equipo de desarrollo.
