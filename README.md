# Nutrition Intelligence Platform

## Visión
Plataforma integral de nutrición inteligente que democratiza el acceso a atención nutricional profesional en México, utilizando IA para mejorar la salud poblacional y generar datos valiosos para la investigación nutricional.

## Características Principales

### 🏥 Gestión Clínica Completa
- Expedientes nutricionales digitales
- Seguimiento antropométrico automatizado
- Integración con laboratorios clínicos
- Planes alimenticios personalizados

### 🤖 Inteligencia Artificial
- Reconocimiento de alimentos por fotografía
- Estimación automática de porciones
- Recomendaciones nutricionales personalizadas
- Detección de patrones alimentarios

### 🌍 Impacto Social
- Base de datos del Sistema Mexicano de Alimentos Equivalentes
- Adaptación a alimentos regionales y económicos
- Soporte para poblaciones vulnerables
- Contribución a investigación nutricional nacional

### 🔒 Seguridad y Cumplimiento
- Cifrado de datos sensibles
- Auditoría completa de accesos
- Cumplimiento con normativas mexicanas
- Consentimiento informado versionado

## Arquitectura

```
nutrition-intelligence/
├── backend/          # FastAPI + PostgreSQL + Celery
├── frontend/         # Expo React Native + Web
├── infra/           # Docker, scripts, configuraciones
└── docs/            # Documentación técnica y compliance
```

## Stack Tecnológico

### Backend
- **API**: FastAPI con arquitectura hexagonal
- **Base de datos**: PostgreSQL + SQLModel
- **Cache/Eventos**: Redis + Firestore
- **IA**: TensorFlow/PyTorch (placeholders)
- **Tareas async**: Celery

### Frontend
- **Framework**: Expo + React Native Web
- **Estado**: Zustand
- **Navegación**: React Navigation
- **UI**: NativeBase/Tamagui

### Infraestructura
- **Contenedores**: Docker + Docker Compose
- **Storage**: Google Cloud Storage / MinIO
- **Monitoreo**: OpenTelemetry + Prometheus
- **CI/CD**: GitHub Actions

## Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Node.js 18+ (para frontend)
- Python 3.11+ (para desarrollo backend)

### Instalación

```bash
# Clonar y configurar
git clone <repo-url>
cd nutrition-intelligence

# Configurar variables de entorno
cp .env.example .env

# Levantar servicios
make up

# Aplicar migraciones y seeds
make migrate
make seed

# Acceder a la aplicación
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Desarrollo

### Comandos principales
```bash
make up          # Levantar todos los servicios
make down        # Detener servicios
make migrate     # Aplicar migraciones
make seed        # Cargar datos iniciales
make test        # Ejecutar tests
make lint        # Verificar código
make logs        # Ver logs en tiempo real
```

### Estructura de desarrollo
- **Backend**: Seguir principios DDD y SOLID
- **Frontend**: Componentes reutilizables y hooks personalizados
- **Tests**: Pirámide de testing (unit → integration → e2e)
- **Docs**: Documentación automática con OpenAPI

## Roadmap

### Fase 1: MVP (3 meses)
- [x] Arquitectura base y autenticación
- [x] Gestión de usuarios y expedientes
- [x] CRUD de alimentos y recetas
- [x] Planes alimenticios básicos
- [x] App móvil básica

### Fase 2: IA y Automatización 
- [ ] Reconocimiento de alimentos
- [ ] Motor de recomendaciones
- [ ] Chat asistido con IA
- [ ] Análisis predictivo

### Fase 3: Escalabilidad y Social 
- [ ] Microservicios
- [ ] Features sociales
- [ ] Dashboard para autoridades
- [ ] Expansión internacional

## Contribuir

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## Contacto

- **Equipo**: nutrition-intelligence@example.com
- **Issues**: [GitHub Issues](https://github.com/org/nutrition-intelligence/issues)
- **Docs**: [Documentación completa](./docs/README.md)

---

*"Democratizando el acceso a la nutrición profesional a través de la tecnología"*