# PostgreSQL Setup - Nutrition Intelligence

Guía completa para migrar de SQLite a PostgreSQL.

## Por qué PostgreSQL

**SQLite es excelente para desarrollo**, pero PostgreSQL es necesario para producción porque:

✅ **Concurrencia**: Múltiples usuarios simultáneos sin bloqueos
✅ **Escalabilidad**: Mejor rendimiento con grandes volúmenes de datos
✅ **Características avanzadas**: Full-text search, JSON, extensiones
✅ **Integridad**: Transacciones ACID robustas
✅ **Producción**: Es el estándar para aplicaciones web profesionales

---

## Opción 1: Usar Docker (Recomendado) 🐳

Esta es la forma más rápida y no requiere instalación manual.

### Paso 1: Iniciar Docker Desktop

**Windows:**
1. Abre Docker Desktop desde el menú de inicio
2. Espera a que muestre "Docker Desktop is running"

**Verificar que Docker está corriendo:**
```bash
docker ps
```

Deberías ver una lista de contenedores (puede estar vacía).

### Paso 2: Iniciar PostgreSQL con Docker Compose

```bash
cd "C:\Nutrition Intelligence"
docker-compose up -d postgres redis
```

Esto iniciará:
- ✅ PostgreSQL 16 en puerto `5432`
- ✅ Redis en puerto `6379`
- ✅ PgAdmin en puerto `5050` (opcional)

**Verificar que está corriendo:**
```bash
docker ps
```

Deberías ver los contenedores `nutrition-intelligence-db` y `nutrition-intelligence-redis`.

### Paso 3: Actualizar configuración del backend

Edita `backend/.env`:

```env
# Cambiar de SQLite:
# DATABASE_URL=sqlite+aiosqlite:///./nutrition_intelligence.db

# A PostgreSQL:
DATABASE_URL=postgresql+asyncpg://nutrition_user:nutrition_password_dev@localhost:5432/nutrition_intelligence
```

### Paso 4: Ejecutar migraciones

```bash
cd backend
python -c "from models.user import Base; from sqlalchemy import create_engine; from core.config import get_settings; settings = get_settings(); engine = create_engine(settings.database_url.replace('asyncpg', 'psycopg2')); Base.metadata.create_all(bind=engine); print('✅ Tablas creadas')"
```

O si tienes Alembic configurado:
```bash
alembic upgrade head
```

### Paso 5: Reiniciar backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 6: Verificar conexión

```bash
curl http://localhost:8000/health
```

---

## Opción 2: Instalar PostgreSQL manualmente

Si prefieres no usar Docker:

### Windows (Chocolatey)

```bash
# Instalar PostgreSQL
choco install postgresql16

# Iniciar servicio
net start postgresql-x64-16

# Crear usuario y base de datos
psql -U postgres
```

En la consola de PostgreSQL:
```sql
CREATE DATABASE nutrition_intelligence;
CREATE USER nutrition_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO nutrition_user;
\q
```

### Windows (Instalador oficial)

1. Descarga desde https://www.postgresql.org/download/windows/
2. Ejecuta el instalador
3. Durante la instalación:
   - Puerto: `5432` (default)
   - Password para postgres: (guárdalo bien)
   - Locale: `Spanish_Mexico` o `C`
4. Abre pgAdmin 4 (incluido)
5. Crea la base de datos `nutrition_intelligence`
6. Crea el usuario `nutrition_user`

### Linux/Mac

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Mac (Homebrew)
brew install postgresql@16
brew services start postgresql@16

# Crear base de datos
sudo -u postgres psql
CREATE DATABASE nutrition_intelligence;
CREATE USER nutrition_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO nutrition_user;
\q
```

---

## Configuración del Backend

### 1. Actualizar `.env`

```env
# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# PostgreSQL (Production/Development)
DATABASE_URL=postgresql+asyncpg://nutrition_user:nutrition_password_dev@localhost:5432/nutrition_intelligence

# PostgreSQL alternativo con psycopg2 (sync)
# DATABASE_URL=postgresql://nutrition_user:nutrition_password_dev@localhost:5432/nutrition_intelligence

# SQLite (Solo para desarrollo local rápido)
# DATABASE_URL=sqlite+aiosqlite:///./nutrition_intelligence.db
```

**Formato de la URL:**
```
postgresql+asyncpg://[usuario]:[password]@[host]:[port]/[database]
```

**Componentes:**
- `postgresql+asyncpg`: Driver asíncrono (recomendado para FastAPI)
- `nutrition_user`: Usuario de PostgreSQL
- `nutrition_password_dev`: Contraseña (cámbiala en producción)
- `localhost`: Servidor (o IP del servidor)
- `5432`: Puerto de PostgreSQL (default)
- `nutrition_intelligence`: Nombre de la base de datos

### 2. Verificar drivers instalados

Los drivers ya están en `requirements.txt`:
```txt
asyncpg==0.29.0          # Driver async para PostgreSQL
psycopg2-binary==2.9.9   # Driver sync (backup)
```

Si falta alguno:
```bash
pip install asyncpg psycopg2-binary
```

---

## Migrar datos de SQLite a PostgreSQL

Si ya tienes datos en SQLite que quieres migrar:

### Opción 1: Script Python

```python
# backend/scripts/migrate_sqlite_to_postgres.py
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

# Conectar a SQLite
sqlite_conn = sqlite3.connect('nutrition_intelligence.db')
sqlite_cursor = sqlite_conn.cursor()

# Conectar a PostgreSQL
pg_conn = psycopg2.connect(
    host='localhost',
    database='nutrition_intelligence',
    user='nutrition_user',
    password='nutrition_password_dev'
)
pg_cursor = pg_conn.cursor()

# Migrar cada tabla
tables = ['users', 'foods', 'recipes', 'patients']  # Ajusta según tus tablas

for table in tables:
    # Obtener datos de SQLite
    sqlite_cursor.execute(f'SELECT * FROM {table}')
    rows = sqlite_cursor.fetchall()

    # Obtener nombres de columnas
    columns = [desc[0] for desc in sqlite_cursor.description]

    if rows:
        # Insertar en PostgreSQL
        insert_query = f"INSERT INTO {table} ({','.join(columns)}) VALUES %s ON CONFLICT DO NOTHING"
        execute_values(pg_cursor, insert_query, rows)
        print(f"✅ Migradas {len(rows)} filas de {table}")

pg_conn.commit()
print("✅ Migración completada")
```

Ejecutar:
```bash
python backend/scripts/migrate_sqlite_to_postgres.py
```

### Opción 2: Herramienta pgloader

```bash
# Instalar pgloader
# Windows: https://pgloader.io/
# Linux: apt-get install pgloader
# Mac: brew install pgloader

# Migrar
pgloader sqlite:///path/to/nutrition_intelligence.db \
  postgresql://nutrition_user:password@localhost/nutrition_intelligence
```

---

## Gestión de la Base de Datos

### Usando PgAdmin (GUI)

**Acceso:**
- URL: http://localhost:5050 (si usas Docker Compose)
- Email: `admin@nutrition-intelligence.com`
- Password: `admin`

**Conectar al servidor:**
1. Click derecho en "Servers" → "Register" → "Server"
2. Nombre: `Nutrition Intelligence Local`
3. Tab "Connection":
   - Host: `postgres` (si usas Docker) o `localhost`
   - Port: `5432`
   - Database: `nutrition_intelligence`
   - Username: `nutrition_user`
   - Password: `nutrition_password_dev`
4. Save

### Usando psql (CLI)

```bash
# Conectar a la base de datos
psql -h localhost -U nutrition_user -d nutrition_intelligence

# Comandos útiles
\dt              # Listar tablas
\d table_name    # Describir tabla
\l               # Listar bases de datos
\du              # Listar usuarios
\q               # Salir

# Queries
SELECT * FROM users LIMIT 10;
SELECT COUNT(*) FROM foods;
```

---

## Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f postgres

# Ver logs específicos
docker logs nutrition-intelligence-db

# Ejecutar psql en el contenedor
docker exec -it nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence

# Backup de la base de datos
docker exec nutrition-intelligence-db pg_dump -U nutrition_user nutrition_intelligence > backup.sql

# Restaurar backup
docker exec -i nutrition-intelligence-db psql -U nutrition_user nutrition_intelligence < backup.sql

# Reiniciar solo PostgreSQL
docker-compose restart postgres

# Ver estado de contenedores
docker-compose ps
```

---

## Troubleshooting

### Error: "could not connect to server"

**Causa**: PostgreSQL no está corriendo

**Solución**:
```bash
# Si usas Docker:
docker-compose up -d postgres

# Si instalaste manualmente (Windows):
net start postgresql-x64-16

# Linux/Mac:
sudo systemctl start postgresql
```

### Error: "password authentication failed"

**Causa**: Contraseña incorrecta en DATABASE_URL

**Solución**: Verifica que la contraseña en `.env` coincide con la del usuario PostgreSQL

### Error: "database does not exist"

**Causa**: La base de datos no se creó

**Solución**:
```bash
docker exec -it nutrition-intelligence-db psql -U nutrition_user -d postgres -c "CREATE DATABASE nutrition_intelligence;"
```

### Error: "relation does not exist"

**Causa**: Las tablas no se han creado

**Solución**: Ejecuta las migraciones (Paso 4 de Opción 1)

### PostgreSQL consume mucha memoria

**Solución**: Edita `docker-compose.yml`:
```yaml
postgres:
  command:
    - -c
    - max_connections=50
    - -c
    - shared_buffers=256MB
```

---

## Optimización para Producción

### 1. Configuración de PostgreSQL

Edita `docker-compose.yml` para agregar variables de optimización:

```yaml
postgres:
  environment:
    # ... variables existentes
    POSTGRES_MAX_CONNECTIONS: 100
    POSTGRES_SHARED_BUFFERS: 256MB
    POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
    POSTGRES_WORK_MEM: 16MB
```

### 2. Índices

Crea índices para mejorar rendimiento:

```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_foods_name ON foods(name);
CREATE INDEX idx_foods_category ON foods(category);
CREATE INDEX idx_recipes_rating ON recipes(rating DESC);
CREATE INDEX idx_patients_nutritionist_id ON patients(nutritionist_id);

-- Índice de texto completo (búsqueda en español)
CREATE INDEX idx_foods_name_fts ON foods USING gin(to_tsvector('spanish', name));
CREATE INDEX idx_recipes_name_fts ON recipes USING gin(to_tsvector('spanish', name));
```

### 3. Backups Automáticos

Agrega a `docker-compose.yml`:

```yaml
services:
  backup:
    image: prodrigestivill/postgres-backup-local
    container_name: nutrition-intelligence-backup
    restart: unless-stopped
    volumes:
      - ./backups:/backups
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: nutrition_intelligence
      POSTGRES_USER: nutrition_user
      POSTGRES_PASSWORD: nutrition_password_dev
      SCHEDULE: "@daily"
      BACKUP_KEEP_DAYS: 7
    depends_on:
      - postgres
```

---

## Estado Actual del Proyecto

**✅ Configurado:**
- Docker Compose con PostgreSQL 16, Redis, PgAdmin
- Drivers instalados (asyncpg, psycopg2-binary)
- Script de inicialización SQL
- Documentación completa

**⏳ Pendiente:**
- Iniciar Docker Desktop
- Ejecutar `docker-compose up -d`
- Actualizar `.env` con URL de PostgreSQL
- Ejecutar migraciones

**📝 Actualmente usando:**
- SQLite (perfecto para desarrollo rápido)
- Listo para cambiar a PostgreSQL en cualquier momento

---

## Cambio Rápido: SQLite ↔ PostgreSQL

Solo necesitas cambiar una línea en `backend/.env`:

```env
# Desarrollo rápido (SQLite):
DATABASE_URL=sqlite+aiosqlite:///./nutrition_intelligence.db

# Desarrollo/Producción (PostgreSQL):
DATABASE_URL=postgresql+asyncpg://nutrition_user:nutrition_password_dev@localhost:5432/nutrition_intelligence
```

Y reiniciar el backend. ¡Así de simple!

---

**Última actualización**: 2025-10-31
