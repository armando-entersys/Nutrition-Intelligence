# Architecture Documentation - Nutrition Intelligence

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Principles](#architecture-principles)
- [Technology Stack](#technology-stack)
- [System Components](#system-components)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [API Design](#api-design)
- [Security Architecture](#security-architecture)
- [Performance Optimizations](#performance-optimizations)
- [Scalability](#scalability)

## System Overview

Nutrition Intelligence is a full-stack web application designed to provide intelligent nutrition management services specialized for the Mexican context. The system integrates AI-powered features with traditional nutrition tracking tools.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         Web Browser (React + Material-UI)                   │ │
│  │  • Responsive UI  • Progressive Web App  • Offline Support  │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS (JWT Auth)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REVERSE PROXY LAYER                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Traefik                                 │ │
│  │  • SSL Termination  • Load Balancing  • Request Routing    │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌─────────────┐
│   FRONTEND   │   │     BACKEND      │   │ MONITORING  │
│    LAYER     │   │      LAYER       │   │    LAYER    │
└──────────────┘   └────────┬─────────┘   └─────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│     DATA     │   │    CACHE     │   │   AI/ML      │
│    LAYER     │   │    LAYER     │   │   LAYER      │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Architecture Principles

### 1. Separation of Concerns
- **Frontend**: Presentation logic and user interaction
- **Backend**: Business logic and data management
- **Database**: Data persistence
- **Cache**: Performance optimization
- **AI Services**: Intelligent features

### 2. Scalability
- Horizontal scaling capability through Docker containers
- Stateless backend design
- Centralized cache with Redis
- Database connection pooling

### 3. Security
- JWT-based authentication
- Role-based access control (RBAC)
- HTTPS everywhere
- Input validation and sanitization
- Rate limiting

### 4. Performance
- Multi-layer caching strategy
- Database query optimization with indexes
- Lazy loading and code splitting
- Asset compression and CDN-ready
- Connection pooling

### 5. Maintainability
- Modular architecture
- Clear separation of layers
- Comprehensive documentation
- Type hints and validation
- Automated testing

## Technology Stack

### Frontend Stack

```
React 18.2
├── UI Framework: Material-UI v6
├── State Management: React Hooks + Context API
├── Routing: React Router DOM v6
├── HTTP Client: Axios
├── Forms: React Hook Form
├── Charts: Recharts
├── Animations: Framer Motion
└── Build Tool: Create React App (Webpack)
```

### Backend Stack

```
FastAPI 0.104
├── ORM: SQLAlchemy 2.0 + SQLModel
├── Validation: Pydantic V2
├── Authentication: python-jose (JWT)
├── Password Hashing: passlib + bcrypt
├── ASGI Server: Uvicorn
├── Database Driver: asyncpg (PostgreSQL)
├── Cache Driver: redis.asyncio
├── AI/ML:
│   ├── google-generativeai (Gemini)
│   └── anthropic (Claude)
└── Image Processing: Pillow
```

### Infrastructure Stack

```
Docker + Docker Compose
├── Reverse Proxy: Traefik v2.10
├── Web Server: Nginx Alpine
├── Database: PostgreSQL 15
│   ├── Extensions: pg_trgm, btree_gin
│   └── Encoding: UTF-8
├── Cache: Redis 7
├── Monitoring:
│   ├── Prometheus
│   ├── Grafana
│   ├── Loki
│   └── Promtail
└── SSL: Let's Encrypt (via Traefik)
```

## System Components

### 1. Frontend Layer

#### Component Architecture

```
src/
├── components/
│   ├── analisis-fotos/        # AI Photo Analysis
│   │   ├── AnalisisFotos.js
│   │   ├── CameraCapture.js
│   │   └── ResultsDisplay.js
│   ├── nutritionist/          # Nutritionist Portal
│   │   ├── NutritionistChat.js
│   │   ├── PatientManagement.js
│   │   └── ConsultationHistory.js
│   ├── recipes/               # Recipe Management
│   ├── recall/                # 24-Hour Recall
│   ├── requirements/          # Nutrition Calculator
│   └── products/              # Product Scanner
├── config/
│   └── api.js                 # API Configuration
├── theme/
│   └── theme.js               # Material-UI Theme
├── utils/
│   ├── auth.js                # Authentication Utils
│   └── validators.js          # Form Validation
└── App.js                      # Main Application
```

#### State Management

```javascript
// Context-based state management
UserContext
├── Authentication state
├── User profile
└── Permissions

NutritionContext
├── Meal plans
├── Food diary
└── Nutrition goals

AIContext
├── Photo analysis results
├── Chat history
└── RAG responses
```

### 2. Backend Layer

#### Layered Architecture

```
backend/
├── api/                        # API Layer
│   ├── routers/               # Route handlers
│   │   ├── auth_simple.py     # Authentication
│   │   ├── foods.py           # SMAE Foods
│   │   ├── products.py        # NOM-051 Products
│   │   ├── rag.py             # RAG Chat
│   │   └── vision.py          # AI Vision
│   └── deps.py                # Dependencies
├── core/                       # Core Layer
│   ├── config.py              # Configuration
│   ├── cache.py               # Cache Manager
│   ├── rate_limit.py          # Rate Limiting
│   └── security.py            # Security Utils
├── domain/                     # Domain Layer
│   ├── foods/                 # Food Domain
│   │   ├── smae_models.py
│   │   └── nom051_models.py
│   ├── users/                 # User Domain
│   └── recipes/               # Recipe Domain
├── services/                   # Service Layer
│   ├── ai/                    # AI Services
│   │   ├── vision.py
│   │   └── rag_service.py
│   ├── deduplication.py
│   └── search.py
└── main.py                     # Application Entry
```

#### Request Flow

```
HTTP Request
    │
    ▼
Middleware Stack
├── CORS Middleware
├── Rate Limit Middleware
└── Error Handler
    │
    ▼
Route Handler
├── Authentication (JWT)
├── Authorization (RBAC)
└── Input Validation (Pydantic)
    │
    ▼
Service Layer
├── Business Logic
├── Data Transformation
└── External API Calls
    │
    ▼
Data Layer
├── Cache Check (Redis)
├── Database Query (PostgreSQL)
└── Cache Update
    │
    ▼
Response
├── Serialization (Pydantic)
├── Response Headers
└── HTTP Status Code
```

### 3. Data Layer

#### Database Architecture

**PostgreSQL 15** with extensions:
- `pg_trgm`: Fuzzy text search
- `btree_gin`: Multi-column indexes

**Schema Design**:

```
┌─────────────────┐
│   auth_users    │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  patients    │  │ nutritionists│
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                │
         ┌──────┴──────┬──────────────┐
         ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐
│ meal_plans   │ │ favorites│ │ history  │
└──────┬───────┘ └──────────┘ └──────────┘
       │
       ▼
┌──────────────┐
│  meal_items  │
└──────┬───────┘
       │
       └───────────┬──────────────┐
                   │              │
            ┌──────▼──────┐ ┌─────▼──────┐
            │alimentos_   │ │productos_  │
            │smae         │ │nom051      │
            └─────────────┘ └────────────┘
```

#### Entity Relationships

**User System**:
```sql
auth_users (base users)
├── 1:1 → patients (patient profile)
├── 1:1 → nutritionists (nutritionist profile)
├── 1:N → meal_plans (created meal plans)
├── 1:N → favorite_foods (favorites)
└── 1:N → productos_nom051 (scanned products)
```

**Food System**:
```sql
alimentos_smae (SMAE foods)
├── 1:N → meal_items
├── 1:N → recipe_ingredients
└── 1:N → favorite_foods

productos_nom051 (NOM-051 products)
├── 1:N → meal_items
├── 1:N → favorite_foods
└── M:1 → auth_users (created_by)
```

**Nutrition System**:
```sql
meal_plans
├── 1:N → meal_days
└── M:1 → auth_users (user)

meal_days
└── 1:N → meal_items

meal_items
├── M:1 → alimentos_smae
└── M:1 → productos_nom051
```

### 4. Cache Layer

#### Redis Cache Strategy

```
┌──────────────────────────────────────┐
│          Cache Hierarchy              │
├──────────────────────────────────────┤
│  L1: In-Memory (Python dict)         │
│  • Session data                       │
│  • User context                       │
│  • TTL: Request scope                 │
├──────────────────────────────────────┤
│  L2: Redis (Distributed)              │
│  • API responses                      │
│  • Database queries                   │
│  • RAG searches                       │
│  • TTL: 5-30 minutes                  │
├──────────────────────────────────────┤
│  L3: Database (Persistent)            │
│  • Master data                        │
│  • User data                          │
│  • Historical data                    │
│  • TTL: Permanent                     │
└──────────────────────────────────────┘
```

#### Cache Keys Structure

```python
# Pattern: {prefix}:{id_or_hash}
user:{user_id}                      # User profile
product:{barcode}                   # Product by barcode
foods:search:{query_hash}           # Food search results
rag:chat:{message_hash}             # RAG responses
ratelimit:minute:{client}:{window}  # Rate limiting
ratelimit:hour:{client}:{window}    # Rate limiting
```

#### Cache Expiration

```python
CACHE_EXPIRATION = {
    "user": 600,           # 10 minutes
    "product": 1800,       # 30 minutes
    "food": 1800,          # 30 minutes
    "rag_search": 300,     # 5 minutes
    "nutritionist": 900,   # 15 minutes
    "patient": 300,        # 5 minutes
    "recipe": 1800,        # 30 minutes
    "meal_plan": 600,      # 10 minutes
}
```

### 5. AI/ML Layer

#### RAG (Retrieval Augmented Generation)

```
User Question
    │
    ▼
┌────────────────────┐
│ Vector Search      │
│ • Query embedding  │
│ • Similarity match │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Context Retrieval  │
│ • SMAE foods       │
│ • NOM-051 products │
│ • Recipes          │
│ • User history     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Prompt Engineering │
│ • System prompt    │
│ • Context injection│
│ • User query       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Gemini 1.5 Flash   │
│ • Max tokens: 5000 │
│ • Temperature: 0.7 │
└─────────┬──────────┘
          │
          ▼
   Contextual Response
```

#### Vision AI

```
Food Photo
    │
    ▼
┌────────────────────┐
│ Image Processing   │
│ • Resize           │
│ • Format conversion│
│ • Compression      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Gemini Vision 1.5  │
│ • Dish recognition │
│ • Ingredient ID    │
│ • Portion estimate │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Nutrition Analysis │
│ • Calorie calc     │
│ • Macro breakdown  │
│ • NOM-051 warnings │
└─────────┬──────────┘
          │
          ▼
  Structured Result
```

## Data Flow

### Authentication Flow

```
1. User Login Request
   POST /api/v1/auth/login
   {email, password}
        │
        ▼
2. Validate Credentials
   • Check email exists
   • Verify password hash
        │
        ▼
3. Generate JWT Token
   • User ID claim
   • Role claim
   • Expiration (30min)
        │
        ▼
4. Return Token
   {access_token, user}
        │
        ▼
5. Subsequent Requests
   Authorization: Bearer {token}
        │
        ▼
6. Token Validation
   • Verify signature
   • Check expiration
   • Extract claims
        │
        ▼
7. Request Processing
   with user context
```

### Food Search Flow

```
1. User Search Query
   GET /api/v1/foods/search?q=tortilla
        │
        ▼
2. Check Redis Cache
   Key: foods:search:{hash("tortilla")}
        │
   ┌────┴────┐
   │ Hit?    │
   └────┬────┘
        │
    Yes │ No
        │    │
        ▼    ▼
    Return  3. Database Query
            SELECT * FROM alimentos_smae
            WHERE nombre % 'tortilla'
            ORDER BY similarity DESC
            LIMIT 10
                 │
                 ▼
            4. Cache Result
               TTL: 30 minutes
                 │
                 ▼
            5. Return Results
```

### RAG Chat Flow

```
1. User Message
   POST /api/v1/rag/chat
   {message: "¿Cuántas calorías tiene una tortilla?"}
        │
        ▼
2. Check Cache
   Key: rag:chat:{message_hash}
        │
   ┌────┴────┐
   │ Hit?    │
   └────┬────┘
        │
    Yes │ No
        │    │
        ▼    ▼
    Return  3. Search Knowledge Base
            • Find relevant foods
            • Find relevant products
            • Get user context
                 │
                 ▼
            4. Build Prompt
               System: You are a nutrition expert...
               Context: [knowledge base results]
               User: {message}
                 │
                 ▼
            5. Call Gemini API
               model: gemini-1.5-flash
               temperature: 0.7
                 │
                 ▼
            6. Parse Response
               • Extract answer
               • Extract sources
                 │
                 ▼
            7. Cache Result
               TTL: 5 minutes
                 │
                 ▼
            8. Return Response
```

### Product Deduplication Flow

```
1. User Scans Product
   POST /api/v1/products
   {codigo_barras: "7501055300891", ...}
        │
        ▼
2. Search Exact Match
   SELECT * FROM productos_nom051
   WHERE codigo_barras = '7501055300891'
        │
   ┌────┴────┐
   │ Exists? │
   └────┬────┘
        │
    Yes │ No
        │    │
        ▼    ▼
    3a. Increment  3b. Search Similar
        scan_count     • Fuzzy name match
        Update stats   • Brand match
        Return         • Nutrition similarity
                           │
                      ┌────┴────┐
                      │Similar? │
                      └────┬────┘
                           │
                       Yes │ No
                           │    │
                           ▼    ▼
                      4a. Link   4b. Create New
                          to      • Set is_global=true
                          global  • scan_count=1
                                  • created_by=user
                           │    │
                           └────┴────┐
                                     ▼
                              5. Return Product
```

## Database Schema

### Core Tables

#### auth_users

```sql
CREATE TABLE auth_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    primary_role VARCHAR(50) NOT NULL,  -- patient, nutritionist, admin
    account_status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_auth_users_email_lower ON auth_users (LOWER(email));
CREATE INDEX idx_auth_users_role_status ON auth_users (primary_role, account_status);
```

#### alimentos_smae

```sql
CREATE TABLE alimentos_smae (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    nombre_comun VARCHAR(255),
    grupo_smae VARCHAR(100),       -- Cereales, Verduras, Frutas, etc.
    subgrupo VARCHAR(100),
    porcion DECIMAL(10,2),
    unidad_porcion VARCHAR(50),
    peso_neto_g DECIMAL(10,2),

    -- Nutrition per portion
    calorias DECIMAL(10,2),
    proteinas DECIMAL(10,2),
    carbohidratos DECIMAL(10,2),
    grasas DECIMAL(10,2),
    fibra DECIMAL(10,2),
    sodio_mg DECIMAL(10,2),

    -- Metadata
    es_mexicano BOOLEAN DEFAULT false,
    fuente VARCHAR(100),
    verificado BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alimentos_smae_nombre_trgm ON alimentos_smae USING gin (nombre gin_trgm_ops);
CREATE INDEX idx_alimentos_smae_grupo_nombre ON alimentos_smae (grupo_smae, nombre);
CREATE INDEX idx_alimentos_smae_mexicano ON alimentos_smae (es_mexicano) WHERE es_mexicano = true;
```

#### productos_nom051

```sql
CREATE TABLE productos_nom051 (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    marca VARCHAR(255),
    categoria VARCHAR(100),

    -- Nutrition per 100g
    porcion_gramos DECIMAL(10,2),
    calorias DECIMAL(10,2),
    proteinas DECIMAL(10,2),
    carbohidratos DECIMAL(10,2),
    azucares DECIMAL(10,2),
    grasas_totales DECIMAL(10,2),
    grasas_saturadas DECIMAL(10,2),
    grasas_trans DECIMAL(10,2),
    fibra DECIMAL(10,2),
    sodio DECIMAL(10,2),

    -- NOM-051 Seals
    exceso_calorias BOOLEAN DEFAULT false,
    exceso_azucares BOOLEAN DEFAULT false,
    exceso_grasas_saturadas BOOLEAN DEFAULT false,
    exceso_grasas_trans BOOLEAN DEFAULT false,
    exceso_sodio BOOLEAN DEFAULT false,
    contiene_edulcorantes BOOLEAN DEFAULT false,
    contiene_cafeina BOOLEAN DEFAULT false,

    -- Global product system
    created_by_user_id INTEGER REFERENCES auth_users(id),
    scan_count INTEGER DEFAULT 1,
    verified BOOLEAN DEFAULT false,
    is_global BOOLEAN DEFAULT true,

    fuente VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_productos_nom051_nombre_trgm ON productos_nom051 USING gin (nombre gin_trgm_ops);
CREATE INDEX idx_productos_nom051_marca_trgm ON productos_nom051 USING gin (marca gin_trgm_ops);
CREATE INDEX idx_productos_nom051_global_verified ON productos_nom051 (is_global, verified) WHERE is_global = true;
CREATE INDEX idx_productos_nom051_user_created ON productos_nom051 (created_by_user_id, created_at DESC);
CREATE INDEX idx_productos_nom051_excesos ON productos_nom051 (exceso_calorias, exceso_azucares, exceso_grasas_saturadas, exceso_sodio) WHERE exceso_calorias = true OR exceso_azucares = true OR exceso_grasas_saturadas = true OR exceso_sodio = true;
```

### Indexes Strategy

**GIN Indexes** for full-text search:
- `nombre gin_trgm_ops`: Fuzzy search on food/product names
- Enables queries like: `SELECT * FROM alimentos_smae WHERE nombre % 'tortilla'`

**Compound Indexes** for common filters:
- `(grupo_smae, nombre)`: Group + name lookups
- `(created_by_user_id, created_at DESC)`: User's recent products

**Partial Indexes** for specific queries:
- `WHERE is_global = true`: Only index global products
- `WHERE es_mexicano = true`: Only index Mexican foods
- `WHERE has_excesos = true`: Only index products with NOM-051 warnings

## API Design

### RESTful Principles

```
Resource-oriented URLs:
GET    /api/v1/foods           - List foods
GET    /api/v1/foods/{id}      - Get food
POST   /api/v1/foods           - Create food
PUT    /api/v1/foods/{id}      - Update food
DELETE /api/v1/foods/{id}      - Delete food

Collection filters:
GET /api/v1/foods?grupo_smae=Cereales&limit=20

Search endpoints:
GET /api/v1/foods/search?q=tortilla

Actions as sub-resources:
POST /api/v1/recipes/{id}/rate
POST /api/v1/products/{id}/verify
```

### Request/Response Format

**Request**:
```json
{
  "field": "value",
  "nested": {
    "field": "value"
  }
}
```

**Success Response**:
```json
{
  "data": { /* actual data */ },
  "message": "Success",
  "status": 200
}
```

**Error Response**:
```json
{
  "detail": "Error message",
  "status_code": 400,
  "errors": [
    {"field": "email", "message": "Invalid format"}
  ]
}
```

### Pagination

```json
{
  "items": [...],
  "total": 150,
  "skip": 0,
  "limit": 20
}
```

## Security Architecture

### Authentication

```
JWT Token Structure:
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "role": "patient",
    "exp": 1699876543
  },
  "signature": "..."
}
```

### Authorization (RBAC)

```python
Roles Hierarchy:
admin
├── Can manage all resources
├── Can manage users
└── Can access analytics

nutritionist
├── Can manage own patients
├── Can create meal plans for patients
├── Can view patient history
└── Can use RAG chat

patient
├── Can manage own profile
├── Can track own meals
├── Can use AI features
└── Cannot access other users' data
```

### Security Layers

```
1. Network Layer
   • HTTPS only
   • Firewall rules
   • DDoS protection

2. Application Layer
   • JWT authentication
   • RBAC authorization
   • CORS policy
   • Rate limiting

3. Data Layer
   • SQL injection prevention (ORM)
   • Input validation (Pydantic)
   • Password hashing (bcrypt)
   • Sensitive data encryption

4. Infrastructure Layer
   • Container isolation
   • Secret management
   • Log anonymization
   • Regular updates
```

## Performance Optimizations

### 1. Database Optimizations

- **19 Indexes**: GIN, compound, partial
- **pg_trgm Extension**: Fuzzy text search
- **Connection Pooling**: Reuse connections
- **Query Optimization**: EXPLAIN ANALYZE
- **VACUUM ANALYZE**: Regular maintenance

### 2. Cache Optimizations

- **Multi-layer Cache**: Memory + Redis
- **Smart TTLs**: Based on data volatility
- **Cache Invalidation**: On data updates
- **Cache Warming**: Pre-populate common queries

### 3. API Optimizations

- **Rate Limiting**: Prevent abuse
- **Response Compression**: Gzip level 6
- **Pagination**: Limit result sets
- **Field Selection**: Only return needed fields
- **Batch Endpoints**: Reduce round trips

### 4. Frontend Optimizations

- **Code Splitting**: Load on demand
- **Lazy Loading**: Defer non-critical resources
- **Asset Compression**: Minify JS/CSS
- **Image Optimization**: WebP, responsive images
- **CDN**: Static asset delivery

## Scalability

### Horizontal Scaling

```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
   ┌───┴───┬───────┬───────┐
   ▼       ▼       ▼       ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│App1 │ │App2 │ │App3 │ │App4 │
└──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
   │       │       │       │
   └───┬───┴───┬───┴───┬───┘
       ▼       ▼       ▼
   ┌─────┐ ┌─────┐ ┌─────┐
   │ DB  │ │Redis│ │ AI  │
   │Pool │ │Cache│ │ API │
   └─────┘ └─────┘ └─────┘
```

### Vertical Scaling

- CPU: 2 → 4 → 8 vCPUs
- RAM: 8GB → 16GB → 32GB
- Storage: SSD for database

### Database Scaling

- **Read Replicas**: Scale read operations
- **Partitioning**: Split large tables by date/region
- **Sharding**: Distribute data across servers

### Cache Scaling

- **Redis Cluster**: Distributed cache
- **Sentinel**: High availability
- **Replication**: Data redundancy

---

**Last Updated**: 2025-11-11
**Architecture Version**: 1.0.0
