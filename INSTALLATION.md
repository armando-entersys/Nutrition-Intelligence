# Guía de Instalación - Nutrition Intelligence Platform

Esta guía te llevará paso a paso por la instalación y configuración completa de la plataforma Nutrition Intelligence.

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación del Backend](#instalación-del-backend)
3. [Instalación del Frontend](#instalación-del-frontend)
4. [Configuración de AI Vision](#configuración-de-ai-vision)
5. [Base de Datos](#base-de-datos)
6. [Verificación de la Instalación](#verificación-de-la-instalación)
7. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos del Sistema

### Software Requerido

- **Python 3.11 o superior**
  - Descarga: https://www.python.org/downloads/
  - Verifica: `python --version`

- **Node.js 16 o superior** y npm
  - Descarga: https://nodejs.org/
  - Verifica: `node --version` y `npm --version`

- **Git**
  - Descarga: https://git-scm.com/
  - Verifica: `git --version`

### Cuentas API (Opcionales)

Para habilitar el análisis de fotos con IA, necesitarás al menos una de estas:

- **Google AI Studio** (Gemini Vision) - **GRATIS** para desarrollo
  - Registro: https://ai.google.dev/

- **Anthropic Console** (Claude Vision) - Pay-as-you-go
  - Registro: https://console.anthropic.com/

### Requisitos de Hardware

**Mínimo:**
- RAM: 4 GB
- Espacio en disco: 2 GB
- Procesador: Dual-core 2.0 GHz

**Recomendado:**
- RAM: 8 GB o más
- Espacio en disco: 5 GB
- Procesador: Quad-core 2.5 GHz o superior

---

## Instalación del Backend

### Paso 1: Clonar el Repositorio

```bash
git clone <repository-url>
cd "Nutrition Intelligence"
```

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` en tu terminal, indicando que el entorno virtual está activo.

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencias principales instaladas:**
- FastAPI 0.104
- SQLAlchemy 2.0
- Uvicorn
- Pydantic 2.0
- google-generativeai (Gemini)
- anthropic (Claude)
- Pillow (procesamiento de imágenes)
- python-dotenv

### Paso 4: Configurar Variables de Entorno

1. **Copia el archivo de ejemplo:**
```bash
cp .env.example .env
```

Si `.env.example` no existe, crea un nuevo archivo `.env`:

```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

2. **Edita `backend/.env` con tu editor preferido:**

```env
# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DATABASE_URL=sqlite:///./nutrition_intelligence.db

# ============================================================================
# AI VISION CONFIGURATION
# ============================================================================

# Google Gemini API Key (Get from: https://ai.google.dev/)
GOOGLE_API_KEY=your-google-gemini-api-key-here

# Claude API Key (Get from: https://console.anthropic.com/settings/keys)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# AI Vision Model Selection
# Options: gemini | claude | hybrid
AI_VISION_MODEL=gemini

# Confidence threshold for hybrid mode (0-100)
# If Gemini confidence < threshold, use Claude as fallback
AI_VISION_CONFIDENCE_THRESHOLD=75

# ============================================================================
# SECURITY
# ============================================================================
SECRET_KEY=change-this-to-a-random-secret-key-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================================================
# SERVER
# ============================================================================
HOST=0.0.0.0
PORT=8000
```

**Notas importantes:**
- NO uses comillas en los valores
- NO agregues espacios alrededor del signo `=`
- Por ahora puedes dejar las API keys con los valores placeholder si no vas a usar AI Vision

### Paso 5: Inicializar Base de Datos

El backend creará automáticamente la base de datos SQLite al iniciar:

```bash
# Esto creará nutrition_intelligence.db
python -c "from models.user import Base; from sqlalchemy import create_engine; engine = create_engine('sqlite:///./nutrition_intelligence.db'); Base.metadata.create_all(bind=engine); print('Database initialized')"
```

### Paso 6: Iniciar el Servidor Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Opciones adicionales:**
```bash
# Con auto-reload para desarrollo
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# En background (Windows PowerShell)
Start-Process -NoNewWindow uvicorn -ArgumentList "main:app --host 0.0.0.0 --port 8000"
```

**Verificación:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Deberías ver un mensaje como:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Solución: Si el puerto 8000 está ocupado

```bash
# Usa otro puerto temporalmente
uvicorn main:app --host 0.0.0.0 --port 8001

# Recuerda actualizar la configuración del frontend (ver siguiente sección)
```

---

## Instalación del Frontend

### Paso 1: Navegar al Directorio Frontend

Abre una **nueva terminal** (mantén el backend corriendo):

```bash
cd "Nutrition Intelligence/frontend"
```

### Paso 2: Instalar Dependencias

```bash
npm install
```

**Dependencias principales instaladas:**
- react 18.2
- react-dom 18.2
- @mui/material 6.0
- @mui/icons-material 6.0
- axios
- react-router-dom
- framer-motion
- recharts

**Tiempo estimado:** 2-5 minutos dependiendo de tu conexión

### Paso 3: Configurar Variables de Entorno (Opcional)

Crea `frontend/.env`:

```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

Edita el archivo:

```env
# URL del backend (cambia si usaste otro puerto)
REACT_APP_API_BASE_URL=http://localhost:8000
```

**Nota:** La configuración por defecto usa `frontend/src/config/api.js`:

```javascript
export const API_BASE_URL = 'http://localhost:8001';
```

Si el backend está en puerto 8000, edita este archivo:

```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

### Paso 4: Configurar Puerto del Frontend (Opcional)

Por defecto, React usa el puerto 3000, pero este proyecto está configurado para 3005.

**Windows:**
```bash
set PORT=3005 && npm start
```

**Linux/Mac:**
```bash
PORT=3005 npm start
```

**O edita `package.json`:**
```json
{
  "scripts": {
    "start": "PORT=3005 react-scripts start"
  }
}
```

### Paso 5: Iniciar el Servidor Frontend

```bash
npm start
```

**Verificación:**
- El navegador debería abrirse automáticamente en http://localhost:3005
- Deberías ver la página de inicio de Nutrition Intelligence

---

## Configuración de AI Vision

El análisis de fotos con IA es **opcional** pero recomendado. Sin API keys, el sistema funcionará con datos mock.

### Opción 1: Gemini Vision (Gratis para Desarrollo) ⭐

**Paso 1: Obtener API Key**

1. Ve a [Google AI Studio](https://ai.google.dev/)
2. Inicia sesión con tu cuenta de Google
3. Click en **"Get API Key"**
4. Selecciona o crea un proyecto
5. Copia la API key generada (empieza con `AIzaSy...`)

**Paso 2: Configurar**

Edita `backend/.env`:

```env
GOOGLE_API_KEY=AIzaSy... tu-key-aqui
AI_VISION_MODEL=gemini
```

**Paso 3: Verificar**

Reinicia el backend y ejecuta:

```bash
curl http://localhost:8000/api/v1/vision/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "ai-vision",
  "models": {
    "gemini": {
      "available": true,
      "model": "gemini-1.5-pro-latest"
    }
  },
  "mode": "gemini"
}
```

### Opción 2: Claude Vision (Máxima Precisión)

**Paso 1: Obtener API Key**

1. Ve a [Anthropic Console](https://console.anthropic.com/settings/keys)
2. Inicia sesión o crea una cuenta
3. Agrega créditos a tu cuenta
4. Click en **"Create Key"**
5. Copia la API key generada (empieza con `sk-ant-...`)

**Paso 2: Configurar**

Edita `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-... tu-key-aqui
AI_VISION_MODEL=claude
```

**Paso 3: Verificar**

```bash
curl http://localhost:8000/api/v1/vision/health
```

### Opción 3: Modo Híbrido (Recomendado para Producción) 🎯

Combina Gemini (económico) con Claude (preciso) para optimizar costos.

**Configuración:**

```env
GOOGLE_API_KEY=AIzaSy... tu-key-de-gemini
ANTHROPIC_API_KEY=sk-ant-... tu-key-de-claude
AI_VISION_MODEL=hybrid
AI_VISION_CONFIDENCE_THRESHOLD=75
```

**Funcionamiento:**
1. Gemini analiza primero (rápido y económico)
2. Si confianza >= 75% → usa resultado de Gemini ✅
3. Si confianza < 75% → llama a Claude (máxima precisión) 🔄
4. Ahorro: ~85% vs usar solo Claude

**Ver documentación completa:** `backend/AI_VISION_SETUP.md`

---

## Base de Datos

### SQLite (Desarrollo) - Por Defecto

El proyecto usa SQLite por defecto, lo cual es perfecto para desarrollo:

```env
DATABASE_URL=sqlite:///./nutrition_intelligence.db
```

**Ubicación:** `backend/nutrition_intelligence.db`

**Ventajas:**
- Sin instalación adicional
- Portátil (un solo archivo)
- Ideal para desarrollo y pruebas

### PostgreSQL (Producción) - Recomendado

Para producción, se recomienda PostgreSQL:

**Paso 1: Instalar PostgreSQL**

- **Windows:** https://www.postgresql.org/download/windows/
- **Mac:** `brew install postgresql`
- **Linux:** `sudo apt-get install postgresql`

**Paso 2: Crear Base de Datos**

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE nutrition_intelligence;

# Crear usuario
CREATE USER nutrition_user WITH PASSWORD 'tu_password_seguro';

# Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO nutrition_user;

# Salir
\q
```

**Paso 3: Actualizar `backend/.env`**

```env
DATABASE_URL=postgresql://nutrition_user:tu_password_seguro@localhost:5432/nutrition_intelligence
```

**Paso 4: Instalar Driver**

```bash
pip install psycopg2-binary
```

**Paso 5: Ejecutar Migraciones**

```bash
# El backend creará las tablas automáticamente al iniciar
python main.py
```

---

## Verificación de la Instalación

### Checklist de Verificación

**Backend (http://localhost:8000):**

- [ ] Health endpoint responde
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] API docs carga correctamente
  ```
  http://localhost:8000/docs
  ```

- [ ] Endpoints de alimentos funcionan
  ```bash
  curl http://localhost:8000/api/v1/foods?skip=0&limit=10
  ```

- [ ] AI Vision configurado (si aplicable)
  ```bash
  curl http://localhost:8000/api/v1/vision/health
  ```

**Frontend (http://localhost:3005):**

- [ ] Página de inicio carga
- [ ] Navegación funciona
- [ ] Componentes de Material-UI se renderizan
- [ ] No hay errores en la consola del navegador

**Integración:**

- [ ] Frontend puede conectarse al backend
- [ ] Login/registro funciona
- [ ] Búsqueda de alimentos funciona
- [ ] Recetas se cargan
- [ ] Recordatorio 24 horas funciona
- [ ] Calculadora de requerimientos funciona

### Test End-to-End Básico

**1. Registro de Usuario:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

**2. Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_user&password=Test123!"
```

**3. Listar Alimentos:**
```bash
curl "http://localhost:8000/api/v1/foods?skip=0&limit=5"
```

**4. Probar AI Vision (si configurado):**
```bash
curl -X POST "http://localhost:8000/api/v1/vision/analyze-food" \
  -F "file=@path/to/food-image.jpg"
```

---

## Solución de Problemas

### Backend no inicia

**Error: `ModuleNotFoundError: No module named 'fastapi'`**

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstala dependencias
pip install -r requirements.txt
```

---

**Error: `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)`**

**Causa:** Puerto 8000 ya está en uso

**Solución 1 - Usar otro puerto:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

Actualiza `frontend/src/config/api.js`:
```javascript
export const API_BASE_URL = 'http://localhost:8001';
```

**Solución 2 - Encontrar y cerrar proceso:**

Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Linux/Mac:
```bash
lsof -ti:8000 | xargs kill -9
```

---

**Error: `Google API key not configured`**

**Causa:** Variables de entorno no se cargan correctamente

**Solución:**
1. Verifica que `backend/.env` existe
2. Verifica formato (sin comillas, sin espacios):
   ```env
   GOOGLE_API_KEY=AIzaSy...
   ```
3. Reinicia el servidor backend completamente

---

### Frontend no inicia

**Error: `npm: command not found`**

**Solución:** Instala Node.js desde https://nodejs.org/

---

**Error: `Could not find required file index.html`**

**Causa:** No estás en el directorio correcto

**Solución:**
```bash
cd "Nutrition Intelligence/frontend"
npm start
```

---

**Error: `CORS policy: No 'Access-Control-Allow-Origin'`**

**Causa:** Backend no permite peticiones del frontend

**Solución:** Verifica `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3005", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### AI Vision no funciona

**Error: `Invalid API key`**

**Solución:**
1. Verifica que la API key es correcta
2. Para Gemini: key empieza con `AIzaSy`
3. Para Claude: key empieza con `sk-ant-`
4. No incluyas comillas en `.env`

---

**Error: `Rate limit exceeded`**

**Causa:** Demasiadas peticiones

**Solución:**
- Gemini free tier: máximo 15 requests/minuto
- Espera 1 minuto o actualiza a plan de pago

---

**Error: `Invalid JSON response from Gemini/Claude`**

**Causa:** La imagen es de mala calidad o el modelo no respondió en JSON

**Solución:**
1. Usa imagen de mejor calidad
2. Prueba con otra imagen
3. Revisa logs del backend para ver respuesta raw
4. Cambia a modo híbrido

---

### Base de Datos

**Error: `No such table: users`**

**Causa:** Base de datos no inicializada

**Solución:**
```bash
cd backend
python -c "from models.user import Base; from sqlalchemy import create_engine; engine = create_engine('sqlite:///./nutrition_intelligence.db'); Base.metadata.create_all(bind=engine)"
```

---

**Error: `Database is locked`**

**Causa:** Múltiples procesos accediendo SQLite

**Solución:**
1. Cierra todas las instancias del backend
2. Reinicia solo una instancia
3. O considera usar PostgreSQL para producción

---

## Instalación Rápida (Resumen)

Para desarrolladores experimentados:

```bash
# Clone
git clone <repo-url>
cd "Nutrition Intelligence"

# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # o source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edita las API keys
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (nueva terminal)
cd frontend
npm install
set PORT=3005 && npm start  # o PORT=3005 npm start

# Acceder
# Frontend: http://localhost:3005
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Próximos Pasos

Una vez instalado:

1. **Lee la documentación de uso:** `USER_GUIDE.md`
2. **Explora la API:** http://localhost:8000/docs
3. **Configura AI Vision:** `backend/AI_VISION_SETUP.md`
4. **Revisa la arquitectura:** `ARCHITECTURE.md`
5. **Contribuye:** Ve a `README.md` sección "Contribuir"

---

## Soporte

Si encuentras problemas no cubiertos en esta guía:

- Revisa `backend/AI_VISION_SETUP.md` para problemas de IA
- Consulta la documentación de FastAPI: https://fastapi.tiangolo.com/
- Consulta la documentación de React: https://react.dev/
- Abre un issue en GitHub

---

**Última actualización:** 2025-10-31
