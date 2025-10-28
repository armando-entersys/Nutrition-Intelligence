# Nutrition Intelligence Platform - Setup Guide

## Arquitectura del Sistema

La plataforma está diseñada con una arquitectura moderna y escalable:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Expo RN)     │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         └──────────────│   (Cache/Jobs)  │──────────────┘
                        │   Port: 6379    │
                        └─────────────────┘
```

## Requisitos del Sistema

### Software Requerido
- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Node.js** >= 18 (para desarrollo frontend)
- **Python** >= 3.11 (para desarrollo backend)
- **Git**

### Hardware Recomendado
- **RAM**: 8GB mínimo, 16GB recomendado
- **CPU**: 4 cores mínimo
- **Disco**: 10GB espacio libre
- **Red**: Conexión estable a internet

## Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd nutrition-intelligence
```

### 2. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus valores específicos
```

### 3. Instalación Completa
```bash
make setup
```

Este comando ejecutará:
- Instalación de dependencias
- Construcción de imágenes Docker
- Inicio de servicios
- Migraciones de base de datos
- Carga de datos iniciales

### 4. Verificar Instalación
```bash
make health
```

## Configuración Detallada

### Variables de Entorno Críticas

Edita el archivo `.env` con los siguientes valores:

```bash
# Seguridad (OBLIGATORIO cambiar en producción)
SECRET_KEY=tu-clave-secreta-de-al-menos-32-caracteres

# Base de datos
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nutrition_intelligence

# Redis
REDIS_URL=redis://localhost:6379/0

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000
```

### Servicios y Puertos

| Servicio | Puerto | URL | Credenciales |
|----------|--------|-----|--------------|
| Frontend | 3000 | http://localhost:3000 | - |
| Backend API | 8000 | http://localhost:8000 | - |
| API Docs | 8000 | http://localhost:8000/docs | - |
| PostgreSQL | 5432 | - | postgres:postgres |
| Redis | 6379 | - | - |
| PgAdmin | 5050 | http://localhost:5050 | admin@nutrition.com:admin |
| MinIO Console | 9001 | http://localhost:9001 | admin:password123 |

## Comandos de Desarrollo

### Gestión de Servicios
```bash
make up          # Iniciar servicios
make down        # Detener servicios
make restart     # Reiniciar servicios
make logs        # Ver logs
make status      # Estado de servicios
```

### Base de Datos
```bash
make migrate                           # Aplicar migraciones
make migrate-create MESSAGE="cambio"  # Crear migración
make seed                             # Cargar datos iniciales
make backup-db                        # Backup de base de datos
```

### Desarrollo
```bash
make dev-backend   # Ejecutar backend en modo desarrollo
make dev-frontend  # Ejecutar frontend en modo desarrollo
make shell-backend # Shell en contenedor backend
make shell-db      # Shell PostgreSQL
```

### Testing y Calidad
```bash
make test          # Ejecutar todos los tests
make test-backend  # Tests solo backend
make lint          # Verificar código
make lint-fix      # Corregir formato
```

## Estructura del Proyecto

```
nutrition-intelligence/
├── backend/                 # API FastAPI
│   ├── core/               # Configuración central
│   ├── domain/             # Modelos de dominio
│   ├── infrastructure/     # Persistencia y servicios externos
│   ├── application/        # Casos de uso
│   ├── api/               # Endpoints REST
│   ├── services/          # Servicios (IA, externos)
│   └── tests/             # Tests unitarios
├── frontend/               # App React Native/Web
│   ├── src/
│   │   ├── app/           # Navegación
│   │   ├── components/    # Componentes reutilizables
│   │   ├── screens/       # Pantallas principales
│   │   ├── services/      # Cliente API
│   │   └── state/         # Gestión de estado
├── infra/                 # Infraestructura
│   ├── docker/           # Dockerfiles y compose
│   └── scripts/          # Scripts de despliegue
└── docs/                 # Documentación
```

## Datos de Prueba

El sistema incluye datos de prueba automáticos:

### Usuarios de Prueba
| Email | Password | Rol |
|-------|----------|-----|
| admin@nutrition.com | admin123 | Administrador |
| nutriologo@test.com | test123 | Nutriólogo |
| paciente@test.com | test123 | Paciente |

### Base de Datos de Alimentos
- +15 alimentos mexicanos básicos del SMAE
- Información nutricional completa
- Categorización por grupo alimentario
- Datos regionales y estacionales

## Desarrollo Local (Sin Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Solución de Problemas

### Error: Puerto en Uso
```bash
# Verificar qué proceso usa el puerto
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Detener servicios
make down
```

### Error: Base de Datos No Conecta
```bash
# Verificar estado de PostgreSQL
docker-compose -f infra/docker/docker-compose.yml ps postgres

# Recrear base de datos
make down
docker volume rm nutrition-intelligence_postgres_data
make up
make migrate
```

### Error: Dependencias Frontend
```bash
# Limpiar caché y reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Error: Permisos Docker (Linux)
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar
```

## Siguientes Pasos

Una vez instalado el sistema:

1. **Explora la API**: http://localhost:8000/docs
2. **Prueba el Frontend**: http://localhost:3000
3. **Revisa los logs**: `make logs`
4. **Crea tu primer usuario**: Usar endpoints de registro
5. **Explora la base de datos**: PgAdmin en puerto 5050

## Contribuir

1. Fork del proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Hacer cambios y tests: `make test`
4. Verificar calidad: `make lint`
5. Commit: `git commit -am 'Agregar nueva funcionalidad'`
6. Push: `git push origin feature/nueva-funcionalidad`
7. Crear Pull Request

## Soporte

Para reportar problemas o solicitar ayuda:
- **Issues**: GitHub Issues del proyecto
- **Documentación**: Revisar carpeta `docs/`
- **Logs**: `make logs` para diagnóstico