# Arquitectura - Nutrition Intelligence Platform

Este documento describe la arquitectura técnica completa de la plataforma Nutrition Intelligence.

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura de Alto Nivel](#arquitectura-de-alto-nivel)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Backend Architecture](#backend-architecture)
6. [Frontend Architecture](#frontend-architecture)
7. [Base de Datos](#base-de-datos)
8. [AI Vision Integration](#ai-vision-integration)
9. [Flujo de Datos](#flujo-de-datos)
10. [Seguridad](#seguridad)
11. [Escalabilidad](#escalabilidad)

---

## Visión General

Nutrition Intelligence es una aplicación web full-stack construida con arquitectura cliente-servidor:

- **Backend**: API RESTful construida con FastAPI (Python)
- **Frontend**: SPA construida con React 18
- **Base de Datos**: SQLite (dev) / PostgreSQL (prod)
- **AI Services**: Gemini Vision + Claude Vision (híbrido)

### Principios de Diseño

1. **Separation of Concerns**: Backend y Frontend completamente desacoplados
2. **API-First**: Toda la lógica de negocio expuesta via REST API
3. **Type Safety**: Pydantic en backend, PropTypes/TypeScript en frontend
4. **Modular**: Componentes y servicios reutilizables
5. **Escalable**: Diseño que permite crecimiento horizontal
6. **Culturalmente Apropiado**: Enfocado en contexto mexicano (SMAE, NOM-051)

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   React 18 SPA (Material-UI v6)                      │   │
│  │                                                       │   │
│  │  Components:                                         │   │
│  │  ├─ Análisis de Fotos IA                            │   │
│  │  ├─ Recordatorio 24 Horas                           │   │
│  │  ├─ Calculadora de Requerimientos                   │   │
│  │  ├─ Recetas Mexicanas                               │   │
│  │  ├─ Gestión de Pacientes                            │   │
│  │  └─ Dashboard de Nutriólogo                         │   │
│  │                                                       │   │
│  │  State Management: React Hooks + Context API        │   │
│  │  Routing: React Router DOM v6                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓ Axios HTTP ↓                          │
└─────────────────────────────────────────────────────────────┘
                              │
                   ┌──────────┴──────────┐
                   │   CORS Middleware   │
                   └──────────┬──────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              REST API Routers                        │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ /api/v1/auth         - Autenticación          │  │   │
│  │  │ /api/v1/users        - Gestión usuarios       │  │   │
│  │  │ /api/v1/foods        - CRUD alimentos SMAE    │  │   │
│  │  │ /api/v1/recipes      - CRUD recetas           │  │   │
│  │  │ /api/v1/meal-plans   - Planes alimenticios    │  │   │
│  │  │ /api/v1/vision       - AI Vision analysis     │  │   │
│  │  │ /api/v1/nutrition-calculator - Calculadora    │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                       │   │
│  │  Business Logic:                                     │   │
│  │  ├─ FoodVisionService (AI analysis)                 │   │
│  │  ├─ NutritionCalculator (requirements)              │   │
│  │  ├─ MealPlanGenerator (weekly plans)                │   │
│  │  └─ SMAE Database (equivalentes mexicanos)          │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓ SQLAlchemy ORM ↓                      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLite (Dev) / PostgreSQL (Prod)                   │   │
│  │                                                       │   │
│  │  Tables:                                             │   │
│  │  ├─ users                                            │   │
│  │  ├─ foods (SMAE data)                               │   │
│  │  ├─ recipes                                          │   │
│  │  ├─ meal_plans                                       │   │
│  │  ├─ patients                                         │   │
│  │  ├─ consultations                                    │   │
│  │  └─ photo_analyses (history)                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL AI SERVICES                        │
│  ┌───────────────────────┐  ┌──────────────────────────┐    │
│  │  Gemini 1.5 Pro       │  │  Claude 3.5 Sonnet       │    │
│  │  (Google AI)          │  │  (Anthropic)             │    │
│  │                       │  │                          │    │
│  │  - Food recognition   │  │  - Fallback for low      │    │
│  │  - Nutrition analysis │  │    confidence cases      │    │
│  │  - SMAE categorization│  │  - Maximum precision     │    │
│  └───────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11+ | Lenguaje principal |
| **FastAPI** | 0.104 | Framework web ASGI |
| **Uvicorn** | Latest | Servidor ASGI |
| **SQLAlchemy** | 2.0 | ORM |
| **Pydantic** | 2.0 | Validación de datos |
| **python-dotenv** | Latest | Variables de entorno |
| **Pillow** | Latest | Procesamiento de imágenes |
| **google-generativeai** | 0.3.2 | Gemini Vision API |
| **anthropic** | 0.25.0 | Claude Vision API |
| **python-jose** | Latest | JWT tokens |
| **passlib** | Latest | Password hashing |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.2 | UI library |
| **React Router** | 6.x | Enrutamiento SPA |
| **Material-UI** | 6.0 | Componentes UI |
| **Axios** | Latest | HTTP client |
| **Framer Motion** | Latest | Animaciones |
| **Recharts** | Latest | Gráficas |
| **date-fns** | Latest | Manejo de fechas |

### Base de Datos

- **Desarrollo**: SQLite 3
- **Producción**: PostgreSQL 14+

### DevOps & Tools

- **Git** - Control de versiones
- **Playwright** - E2E testing
- **pytest** - Backend testing
- **Jest** - Frontend testing

---

## Estructura del Proyecto

```
Nutrition Intelligence/
│
├── backend/                          # Backend Python/FastAPI
│   ├── api/                          # API Layer
│   │   ├── routers/                  # API Endpoints
│   │   │   ├── auth_simple.py        # Autenticación JWT
│   │   │   ├── users.py              # CRUD usuarios
│   │   │   ├── foods.py              # CRUD alimentos SMAE
│   │   │   ├── recipes.py            # CRUD recetas
│   │   │   ├── meal_plans.py         # Planes alimenticios
│   │   │   ├── vision.py             # AI Vision endpoints
│   │   │   ├── nutrition_calculator.py  # Calculadora nutricional
│   │   │   ├── weekly_planning.py    # Planificación semanal
│   │   │   ├── nutritionists.py      # Portal nutriólogos
│   │   │   └── patients.py           # Gestión pacientes
│   │   └── deps.py                   # Dependencias comunes
│   │
│   ├── models/                       # Database Models
│   │   └── user.py                   # User, Patient, Consultation models
│   │
│   ├── services/                     # Business Logic
│   │   └── ai/
│   │       └── vision.py             # FoodVisionService
│   │
│   ├── data/                         # Static Data
│   │   └── smae/                     # Sistema Mexicano Alimentos Equivalentes
│   │       ├── cereales.txt
│   │       ├── frutas.txt
│   │       ├── verduras.txt
│   │       ├── lacteos.txt
│   │       ├── carnes.txt
│   │       ├── leguminosas.txt
│   │       ├── grasas.txt
│   │       └── azucares.txt
│   │
│   ├── main.py                       # FastAPI Application
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables
│   ├── .env.example                  # Template de configuración
│   ├── AI_VISION_SETUP.md           # Guía AI Vision
│   └── nutrition_intelligence.db     # SQLite database (dev)
│
├── frontend/                         # Frontend React
│   ├── public/                       # Static assets
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   ├── src/                          # Source code
│   │   ├── components/               # React Components
│   │   │   ├── analisis-fotos/
│   │   │   │   └── AnalizadorFotosMejorado.js  # AI Photo Analyzer
│   │   │   ├── recipes/
│   │   │   │   ├── RecipesList.js
│   │   │   │   ├── RecipeDetail.js
│   │   │   │   └── RecipeRating.js
│   │   │   ├── recall/
│   │   │   │   └── Recordatorio24Horas.js  # 24-hour food recall
│   │   │   └── requirements/
│   │   │       └── CalculadoraRequerimientos.js
│   │   │
│   │   ├── config/
│   │   │   └── api.js                # API configuration
│   │   │
│   │   ├── theme/                    # Material-UI Theme
│   │   │   └── theme.js              # Custom theme configuration
│   │   │
│   │   ├── App.js                    # Main App component
│   │   ├── App.css                   # Global styles
│   │   ├── index.js                  # Entry point
│   │   └── index.css                 # Base styles
│   │
│   ├── package.json                  # Node dependencies
│   ├── package-lock.json
│   └── .env                          # Environment variables
│
├── README.md                         # Main documentation
├── INSTALLATION.md                   # Installation guide
├── ARCHITECTURE.md                   # This file
├── USER_GUIDE.md                     # User manual
└── LICENSE                           # MIT License
```

---

## Backend Architecture

### Capas de la Arquitectura

```
┌────────────────────────────────────────┐
│         API Layer (Routers)            │  ← REST Endpoints
├────────────────────────────────────────┤
│      Business Logic (Services)         │  ← Core logic
├────────────────────────────────────────┤
│      Data Access (Models + ORM)        │  ← Database
└────────────────────────────────────────┘
```

### 1. API Layer (Routers)

**Responsabilidad**: Exponer endpoints REST, validación de entrada, manejo de errores HTTP

**Archivo**: `backend/api/routers/*.py`

**Ejemplo - Vision Router** (`vision.py:1`):

```python
from fastapi import APIRouter, File, UploadFile
from services.ai.vision import analyze_food_image

router = APIRouter()

@router.post("/analyze-food")
async def analyze_food_photo(file: UploadFile = File(...)):
    """
    Analiza foto de comida con IA
    - Acepta: JPG, PNG, WEBP
    - Retorna: JSON con análisis nutricional
    """
    # Validación
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Procesar
    image_bytes = await file.read()
    result = await analyze_food_image(image_bytes)

    return JSONResponse(content=result)
```

**Routers disponibles**:
- `/api/v1/auth` - Autenticación (login, register, refresh)
- `/api/v1/users` - CRUD usuarios
- `/api/v1/foods` - CRUD alimentos SMAE
- `/api/v1/recipes` - CRUD recetas mexicanas
- `/api/v1/meal-plans` - Generación de planes
- `/api/v1/vision` - AI Vision analysis
- `/api/v1/nutrition-calculator` - Cálculos nutricionales
- `/api/v1/weekly-planning` - Planificación semanal

### 2. Business Logic Layer (Services)

**Responsabilidad**: Lógica de negocio, integración con APIs externas

**Ejemplo - FoodVisionService** (`services/ai/vision.py:177`):

```python
class FoodVisionService:
    def __init__(self):
        self.gemini_available = gemini_model is not None
        self.claude_available = anthropic_client is not None
        self.model_mode = AI_VISION_MODEL

    async def analyze_food_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Hybrid AI approach:
        1. Try Gemini first (fast & cheap)
        2. If confidence < threshold, use Claude (accurate)
        3. Fallback to mock data if no APIs
        """
        # Gemini analysis
        if self.model_mode in ["gemini", "hybrid"]:
            result = await self._analyze_with_gemini(image_bytes)

            # Hybrid mode: check confidence
            if self.model_mode == "hybrid":
                confidence = result.get("confidence_score", 0)
                if confidence < CONFIDENCE_THRESHOLD:
                    return await self._analyze_with_claude(image_bytes)

            return result

        # Claude analysis
        elif self.model_mode == "claude":
            return await self._analyze_with_claude(image_bytes)
```

**Características clave**:
- Modo híbrido inteligente (optimiza costos)
- Prompt especializado en comida mexicana (170 líneas)
- Análisis NOM-051 (sellos de advertencia)
- Categorización SMAE automática
- Fallback a datos mock si no hay APIs

### 3. Data Access Layer (Models + ORM)

**Responsabilidad**: Modelos de datos, acceso a base de datos

**Ejemplo - User Model** (`models/user.py:1`):

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="user")  # user | nutritionist | admin
    created_at = Column(DateTime)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    # ... más campos
```

### Configuración de FastAPI

**Main Application** (`main.py:1`):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import (
    auth_simple, users, foods, recipes,
    meal_plans, vision, nutrition_calculator
)

app = FastAPI(
    title="Nutrition Intelligence API",
    description="API para análisis nutricional con IA",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3005",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_simple.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(foods.router, prefix="/api/v1/foods", tags=["foods"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
app.include_router(vision.router, prefix="/api/v1/vision", tags=["ai-vision"])
# ... más routers
```

---

## Frontend Architecture

### Estructura de Componentes

```
App.js
├── Router
│   ├── Home
│   ├── Login/Register
│   ├── Dashboard
│   │   ├── AnalizadorFotosMejorado    ← AI Photo Analysis
│   │   ├── Recordatorio24Horas        ← Food diary
│   │   ├── CalculadoraRequerimientos  ← Requirements calculator
│   │   ├── RecipesList                ← Recipe catalog
│   │   └── MealPlanner                ← Weekly planner
│   └── Nutritionist Portal
│       ├── PatientList
│       ├── PatientDetail
│       └── Consultations
```

### Componente Principal - AnalizadorFotosMejorado

**Archivo**: `frontend/src/components/analisis-fotos/AnalizadorFotosMejorado.js`

**Funcionalidades**:
1. Captura de foto con cámara (MediaDevices API)
2. Upload de imagen desde archivo
3. Análisis con backend AI Vision
4. Visualización de resultados:
   - Platillo identificado
   - Ingredientes detectados
   - Información nutricional completa
   - Sellos NOM-051
   - Score de salubridad
   - Recomendaciones personalizadas

**Código clave**:

```javascript
const analyzeImageWithAI = async (imageFile) => {
  setAnalyzing(true);

  try {
    // Crear FormData para upload
    const formData = new FormData();
    formData.append('file', imageFile);

    // Llamar backend con Gemini Vision
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/vision/analyze-food`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      }
    );

    const result = response.data;

    // Procesar y mostrar resultados
    setAnalysisResult({
      ...result,
      timestamp: new Date().toISOString(),
      image_url: imagePreview,
    });

  } catch (error) {
    console.error('Error al analizar:', error);
    // Manejo de errores...
  } finally {
    setAnalyzing(false);
  }
};
```

### State Management

**Estrategia**: React Hooks + Context API (sin Redux)

```javascript
// Global state (si necesario)
const AuthContext = React.createContext();

// Component-level state
const [analysisResult, setAnalysisResult] = useState(null);
const [analyzing, setAnalyzing] = useState(false);
const [history, setHistory] = useState([]);
```

### Routing

**React Router DOM v6**:

```javascript
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/login" element={<Login />} />
    <Route path="/dashboard" element={<Dashboard />}>
      <Route path="analisis-fotos" element={<AnalizadorFotos />} />
      <Route path="recordatorio" element={<Recordatorio24H />} />
      <Route path="recetas" element={<RecipesList />} />
    </Route>
  </Routes>
</BrowserRouter>
```

### Material-UI Theme

**Archivo**: `frontend/src/theme/theme.js`

```javascript
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32',  // Verde mexicano
    },
    secondary: {
      main: '#D84315',  // Naranja terracota
    },
  },
  typography: {
    fontFamily: '"Roboto", "Arial", sans-serif',
  },
});

export default theme;
```

---

## Base de Datos

### Esquema de Tablas

```sql
-- Users & Authentication
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SMAE Foods Database
CREATE TABLE foods (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- cereales, frutas, verduras, etc.
    serving_size VARCHAR(50),
    calories DECIMAL(6,2),
    protein DECIMAL(5,2),
    carbs DECIMAL(5,2),
    fats DECIMAL(5,2),
    fiber DECIMAL(5,2),
    sodium DECIMAL(6,2),
    equivalentes INTEGER DEFAULT 1
);

-- Recipes
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    difficulty VARCHAR(20),
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER,
    calories_per_serving DECIMAL(6,2),
    protein DECIMAL(5,2),
    carbs DECIMAL(5,2),
    fats DECIMAL(5,2),
    ingredients JSON,  -- Lista de ingredientes
    instructions JSON,  -- Pasos de preparación
    image_url VARCHAR(500),
    rating DECIMAL(3,2),
    created_at TIMESTAMP
);

-- Patients (for nutritionists)
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    nutritionist_id INTEGER REFERENCES users(id),
    user_id INTEGER REFERENCES users(id) NULL,
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    gender VARCHAR(10),
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    activity_level VARCHAR(20),
    goal VARCHAR(50),
    created_at TIMESTAMP
);

-- Consultations
CREATE TABLE consultations (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    nutritionist_id INTEGER REFERENCES users(id),
    date TIMESTAMP,
    notes TEXT,
    weight DECIMAL(5,2),
    measurements JSON,
    recommendations TEXT
);

-- Meal Plans
CREATE TABLE meal_plans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    patient_id INTEGER REFERENCES patients(id) NULL,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    daily_calories INTEGER,
    daily_protein DECIMAL(5,2),
    daily_carbs DECIMAL(5,2),
    daily_fats DECIMAL(5,2),
    plan_data JSON,  -- Estructura del plan semanal
    created_at TIMESTAMP
);

-- Photo Analyses History (optional)
CREATE TABLE photo_analyses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    image_url VARCHAR(500),
    analysis_result JSON,
    ai_model VARCHAR(20),
    confidence_score INTEGER,
    created_at TIMESTAMP
);
```

### Relaciones

```
users (1) ─────── (N) patients
  │                      │
  │                      │
  └─────── (N) consultations (N) ───┘
  │
  └─────── (N) meal_plans
  │
  └─────── (N) photo_analyses

foods (N) ─────── (N) recipes (via ingredients JSON)
```

---

## AI Vision Integration

### Arquitectura Híbrida

```
User uploads photo
       │
       ▼
┌──────────────────┐
│  FastAPI Router  │
│  /analyze-food   │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────┐
│  FoodVisionService          │
│  ┌───────────────────────┐  │
│  │  1. Validate image    │  │
│  │  2. Convert to bytes  │  │
│  │  3. Choose AI model   │  │
│  └───────────┬───────────┘  │
└──────────────┼──────────────┘
               │
       ┌───────┴────────┐
       │   Hybrid Mode  │
       └───────┬────────┘
               │
     ┌─────────▼─────────┐
     │  Gemini Vision    │ ← Primary
     │  (Fast & Cheap)   │
     └─────────┬─────────┘
               │
        Confidence?
         /        \
      ≥75%       <75%
       │           │
       ▼           ▼
    ┌──────┐   ┌────────────────┐
    │ Done │   │ Claude Vision  │ ← Fallback
    └──────┘   │ (Max Precision)│
               └────────┬───────┘
                        │
                        ▼
                   ┌──────┐
                   │ Done │
                   └──────┘
```

### Prompt Especializado

**Archivo**: `backend/services/ai/vision.py:43`

El prompt de 170 líneas está optimizado para:

1. **Platillo Mexicano**:
   - Nombre exacto del platillo
   - Región de origen
   - Si es tradicional o no
   - Categoría (antojito, platillo fuerte, postre, etc.)

2. **Ingredientes Detectados**:
   - Nombre del ingrediente
   - Cantidad estimada en gramos/piezas
   - Info nutricional por porción
   - Categoría SMAE equivalente

3. **Análisis NOM-051** (Sellos de advertencia):
   - Exceso de calorías
   - Exceso de azúcares
   - Exceso de grasas saturadas
   - Exceso de sodio
   - Contiene edulcorantes
   - Contiene cafeína

4. **Evaluación de Salubridad**:
   - Score 0-100
   - Nivel (Excelente/Bueno/Moderado/Pobre)
   - Color sugerido para UI
   - Factores positivos y negativos

5. **Recomendaciones Culturalmente Apropiadas**:
   - Tipo (reducción/sustitución/mejora/porción)
   - Título e impacto estimado

### Formato de Respuesta

```json
{
  "platillo": {
    "nombre": "Tacos al Pastor",
    "confianza": 92,
    "descripcion": "Tacos de cerdo marinado con piña",
    "region": "Ciudad de México",
    "categoria": "Antojito mexicano",
    "es_tradicional": true
  },
  "ingredientes": [
    {
      "nombre": "Tortilla de maíz",
      "cantidad_estimada": "3 piezas (90g)",
      "confianza": 95,
      "calorias": 192,
      "proteina": 4.5,
      "carbohidratos": 41.4,
      "grasas": 2.7,
      "fibra": 3.3,
      "sodio": 15,
      "categoria_smae": "Cereales sin grasa"
    }
  ],
  "totales": {
    "calorias": 650,
    "proteina": 35,
    "carbohidratos": 70,
    "grasas": 25,
    "fibra": 8,
    "sodio": 1200,
    "margen_error": 15
  },
  "sellos_nom051": {
    "exceso_calorias": false,
    "exceso_azucares": false,
    "exceso_grasas_saturadas": true,
    "exceso_sodio": true,
    "contiene_edulcorantes": false,
    "contiene_cafeina": false
  },
  "evaluacion": {
    "score": 68,
    "nivel": "Bueno",
    "color": "#FF9800",
    "factores_positivos": ["Alto en proteína", "Fibra adecuada"],
    "factores_negativos": ["Alto en sodio", "Grasas saturadas"]
  },
  "recomendaciones": [
    {
      "tipo": "reduccion",
      "titulo": "Reducir sal",
      "descripcion": "Pedir sin sal adicional",
      "impacto": "Reducir sodio en 30%"
    }
  ],
  "contexto_diario": {
    "porcentaje_calorias_diarias": 32.5,
    "momento_recomendado": "Comida principal (12-15h)",
    "requiere_ajuste": false,
    "mensaje": "Porción adecuada para comida fuerte"
  },
  "confidence_score": 92
}
```

---

## Flujo de Datos

### Flujo Completo - Análisis de Foto

```
1. Usuario captura/sube foto
   ↓
2. React component (AnalizadorFotosMejorado.js)
   - Valida formato (JPG/PNG/WEBP)
   - Crea FormData
   - Muestra loading state
   ↓
3. Axios POST → /api/v1/vision/analyze-food
   ↓
4. FastAPI Router (vision.py)
   - Valida content-type
   - Valida tamaño (max 10MB)
   - Lee image bytes
   ↓
5. FoodVisionService.analyze_food_image()
   ↓
6. Gemini Vision API
   - Procesa imagen
   - Ejecuta prompt especializado
   - Retorna JSON
   ↓
7. [Opcional] Claude Vision API
   - Si confianza < 75% en modo híbrido
   ↓
8. FastAPI Response → JSON
   ↓
9. React component
   - Actualiza state
   - Renderiza resultados:
     * Card con platillo
     * Lista de ingredientes
     * Gráfica de macronutrientes
     * Sellos NOM-051
     * Score de salubridad
     * Recomendaciones
   - Agrega a historial
```

### Flujo - Calculadora de Requerimientos

```
1. Usuario ingresa datos:
   - Edad, sexo, peso, altura
   - Nivel de actividad
   - Objetivo (perder/mantener/ganar)
   ↓
2. Frontend calcula TMB (Tasa Metabólica Basal)
   - Fórmula de Harris-Benedict
   ↓
3. Calcula TDEE (Total Daily Energy Expenditure)
   - TMB × Factor de actividad
   ↓
4. Ajusta según objetivo
   - Perder peso: -500 kcal
   - Ganar músculo: +300 kcal
   - Mantener: +0 kcal
   ↓
5. Distribuye macronutrientes
   - Proteína: 1.8-2.2g/kg
   - Grasas: 25-30% calorías
   - Carbohidratos: resto
   ↓
6. Muestra resultados
   - Calorías diarias
   - Distribución de macros
   - Recomendaciones
```

---

## Seguridad

### Autenticación

**JWT (JSON Web Tokens)**:

```python
# backend/api/routers/auth_simple.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Password Hashing

**bcrypt via passlib**:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### CORS Configuration

```python
# Restricción a orígenes conocidos
allow_origins=[
    "http://localhost:3005",
    "http://localhost:3000",
    "https://nutrition-intelligence.com"  # Production
]
```

### Input Validation

**Pydantic Models**:

```python
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)
    full_name: str
```

### API Key Protection

```python
# Never commit .env to git
GOOGLE_API_KEY=***
ANTHROPIC_API_KEY=***

# Load securely
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
```

---

## Escalabilidad

### Horizontal Scaling

**Backend**:
- Stateless API (puede replicarse)
- JWT tokens (no session storage)
- Load balancer compatible

**Sugerencia para producción**:
```
             ┌──────────────┐
Internet ──→ │ Load Balancer│
             └──────┬───────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    Backend 1   Backend 2   Backend 3
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
            PostgreSQL (Primary)
                    │
                    ▼
            PostgreSQL (Replica)
```

### Caching Strategy

**Recomendaciones**:

1. **Redis para sesiones**:
   ```python
   # Cache AI Vision results
   redis.setex(f"vision:{image_hash}", 3600, json.dumps(result))
   ```

2. **CDN para imágenes**:
   - CloudFlare
   - AWS CloudFront

3. **Database indexes**:
   ```sql
   CREATE INDEX idx_foods_category ON foods(category);
   CREATE INDEX idx_recipes_rating ON recipes(rating DESC);
   ```

### Performance Optimization

**Backend**:
- Async/await para I/O operations
- Connection pooling para database
- Image compression antes de procesar

**Frontend**:
- Code splitting (React.lazy)
- Image optimization
- Lazy loading de componentes

---

## Deployment

### Backend Deployment

**Opción 1: Docker**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Opción 2: Cloud Services**:
- AWS Elastic Beanstalk
- Google Cloud Run
- Heroku
- Railway

### Frontend Deployment

```bash
npm run build
# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
```

---

**Última actualización**: 2025-10-31
