# API Documentation - Nutrition Intelligence

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URLs](#base-urls)
- [Rate Limiting](#rate-limiting)
- [Response Format](#response-format)
- [Error Codes](#error-codes)
- [Endpoints](#endpoints)
  - [Authentication](#authentication-endpoints)
  - [Foods (SMAE)](#foods-endpoints)
  - [Products (NOM-051)](#products-endpoints)
  - [Recipes](#recipes-endpoints)
  - [Meal Plans](#meal-plans-endpoints)
  - [Nutrition Calculator](#nutrition-calculator-endpoints)
  - [Vision AI](#vision-ai-endpoints)
  - [RAG Chat](#rag-chat-endpoints)
  - [Nutritionist](#nutritionist-endpoints)
  - [Weekly Planning](#weekly-planning-endpoints)
- [Examples](#examples)

## Overview

The Nutrition Intelligence API is a RESTful API built with FastAPI that provides comprehensive nutrition management capabilities specialized for the Mexican context.

**Version**: 1.0.0
**Base URL Production**: `https://nutrition-intelligence.scram2k.com`
**Base URL Development**: `http://localhost:8000`

## Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### Getting a Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Juan Pérez",
    "primary_role": "patient"
  }
}
```

### Using the Token

Include the token in the `Authorization` header for all authenticated requests:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- Access tokens expire after **30 minutes**
- Refresh tokens can be implemented for longer sessions
- On expiration, the API returns `401 Unauthorized`

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Production  | `https://nutrition-intelligence.scram2k.com` |
| Development | `http://localhost:8000` |

All endpoints use the prefix `/api/v1/` unless otherwise specified.

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Global limits**:
  - 60 requests per minute
  - 1000 requests per hour
- **Per-endpoint limits**: Vary by endpoint complexity

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
```

When rate limit is exceeded:

```json
{
  "detail": "Too many requests. Please try again later.",
  "retry_after": 45
}
```

## Response Format

### Success Response

```json
{
  "data": { /* response data */ },
  "message": "Operation successful",
  "status": 200
}
```

### Error Response

```json
{
  "detail": "Error description",
  "status_code": 400,
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid data format |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Endpoints

### Authentication Endpoints

#### Register User

Create a new user account.

```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "Juan Pérez",
  "primary_role": "patient"
}
```

**Roles**: `patient`, `nutritionist`, `admin`

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Juan Pérez",
  "primary_role": "patient",
  "created_at": "2025-11-11T10:00:00"
}
```

#### Login

Authenticate and receive access token.

```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Juan Pérez",
    "primary_role": "patient"
  }
}
```

#### Get Current User

Get authenticated user's profile.

```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Juan Pérez",
  "primary_role": "patient",
  "created_at": "2025-11-11T10:00:00"
}
```

---

### Foods Endpoints

#### List Foods (SMAE)

Get list of foods from Sistema Mexicano de Alimentos Equivalentes.

```http
GET /api/v1/foods
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (int, default: 0) - Pagination offset
- `limit` (int, default: 100) - Number of items
- `search` (string) - Search by name
- `grupo_smae` (string) - Filter by SMAE group

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Tortilla de maíz",
      "nombre_comun": "Tortilla",
      "grupo_smae": "Cereales",
      "subgrupo": "Sin grasa",
      "porcion": 30,
      "unidad_porcion": "g",
      "peso_neto_g": 30,
      "calorias": 64,
      "proteinas": 1.7,
      "carbohidratos": 13.4,
      "grasas": 0.9,
      "fibra": 1.5,
      "sodio_mg": 3,
      "es_mexicano": true,
      "verificado": true
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 100
}
```

#### Get Food by ID

```http
GET /api/v1/foods/{food_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": 1,
  "nombre": "Tortilla de maíz",
  "grupo_smae": "Cereales",
  "calorias": 64,
  "proteinas": 1.7,
  "carbohidratos": 13.4,
  "grasas": 0.9,
  "fibra": 1.5,
  "sodio_mg": 3
}
```

#### Search Foods

Search foods by name with fuzzy matching.

```http
GET /api/v1/foods/search?q=tortilla
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "results": [
    {
      "id": 1,
      "nombre": "Tortilla de maíz",
      "similarity": 0.95
    },
    {
      "id": 2,
      "nombre": "Tortilla de harina",
      "similarity": 0.92
    }
  ]
}
```

---

### Products Endpoints

#### List Products (NOM-051)

Get list of products with NOM-051 labeling information.

```http
GET /api/v1/products
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (int) - Pagination offset
- `limit` (int) - Number of items
- `search` (string) - Search by name or brand
- `is_global` (bool) - Filter global products
- `verified` (bool) - Filter verified products
- `has_excesos` (bool) - Filter products with NOM-051 warnings

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "codigo_barras": "7501055300891",
      "nombre": "Coca-Cola Original",
      "marca": "Coca-Cola",
      "porcion_gramos": 100,
      "calorias": 42,
      "proteinas": 0,
      "carbohidratos": 10.6,
      "azucares": 10.6,
      "grasas_totales": 0,
      "grasas_saturadas": 0,
      "sodio": 11,
      "exceso_azucares": true,
      "exceso_calorias": false,
      "exceso_grasas_saturadas": false,
      "exceso_sodio": false,
      "is_global": true,
      "verified": true,
      "scan_count": 1543
    }
  ],
  "total": 3,
  "skip": 0,
  "limit": 100
}
```

#### Get Product by Barcode

```http
GET /api/v1/products/barcode/{barcode}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": 1,
  "codigo_barras": "7501055300891",
  "nombre": "Coca-Cola Original",
  "marca": "Coca-Cola",
  "exceso_azucares": true,
  "is_global": true,
  "verified": true
}
```

#### Create Product

Add a new product (or increment scan count if exists).

```http
POST /api/v1/products
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "codigo_barras": "7501234567890",
  "nombre": "Nuevo Producto",
  "marca": "Marca",
  "porcion_gramos": 100,
  "calorias": 150,
  "proteinas": 5.0,
  "carbohidratos": 20.0,
  "azucares": 10.0,
  "grasas_totales": 5.0,
  "grasas_saturadas": 2.0,
  "sodio": 200
}
```

**Response (201):**
```json
{
  "id": 4,
  "codigo_barras": "7501234567890",
  "nombre": "Nuevo Producto",
  "is_global": true,
  "scan_count": 1
}
```

#### Get Global Products Stats

Get statistics about global products.

```http
GET /api/v1/products/stats/global
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "total_products": 1543,
  "verified_products": 892,
  "total_scans": 45234,
  "products_with_excesos": 678,
  "most_scanned": [
    {
      "nombre": "Coca-Cola Original",
      "scan_count": 1543
    }
  ]
}
```

---

### Recipes Endpoints

#### List Recipes

```http
GET /api/v1/recipes
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (int) - Pagination offset
- `limit` (int) - Number of items
- `category` (string) - Filter by category
- `difficulty` (string) - easy, medium, hard

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Tacos de Pescado",
      "description": "Tacos saludables con pescado a la plancha",
      "category": "Plato Principal",
      "difficulty": "medium",
      "prep_time_minutes": 30,
      "servings": 4,
      "calories_per_serving": 320,
      "protein": 25,
      "carbs": 35,
      "fats": 10,
      "average_rating": 4.5,
      "total_ratings": 128
    }
  ],
  "total": 45,
  "skip": 0,
  "limit": 20
}
```

#### Get Recipe by ID

```http
GET /api/v1/recipes/{recipe_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Tacos de Pescado",
  "ingredients": [
    {
      "name": "Pescado blanco",
      "quantity": 400,
      "unit": "g"
    },
    {
      "name": "Tortillas de maíz",
      "quantity": 8,
      "unit": "piezas"
    }
  ],
  "instructions": [
    "Marinar el pescado con limón y especias",
    "Cocinar a la plancha 5 minutos por lado",
    "Servir en tortillas con col y salsa"
  ],
  "nutrition_info": {
    "calories": 320,
    "protein": 25,
    "carbs": 35,
    "fats": 10,
    "fiber": 5
  }
}
```

#### Rate Recipe

```http
POST /api/v1/recipes/{recipe_id}/rate
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "rating": 5,
  "comment": "Deliciosa receta!"
}
```

**Response (200):**
```json
{
  "recipe_id": 1,
  "average_rating": 4.6,
  "total_ratings": 129
}
```

---

### Meal Plans Endpoints

#### Create Meal Plan

Generate personalized meal plan.

```http
POST /api/v1/meal-plans
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "goal": "weight_loss",
  "daily_calories": 1800,
  "days": 7,
  "meals_per_day": 5,
  "dietary_restrictions": ["gluten_free"],
  "preferences": {
    "include_snacks": true,
    "meal_prep_friendly": false
  }
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "goal": "weight_loss",
  "daily_calories": 1800,
  "start_date": "2025-11-11",
  "end_date": "2025-11-18",
  "days": [
    {
      "day": 1,
      "date": "2025-11-11",
      "meals": [
        {
          "meal_type": "breakfast",
          "recipe_id": 5,
          "recipe_name": "Avena con Fruta",
          "calories": 350,
          "protein": 12,
          "carbs": 60,
          "fats": 8
        }
      ],
      "total_calories": 1785,
      "total_protein": 95,
      "total_carbs": 220,
      "total_fats": 55
    }
  ]
}
```

#### Get Meal Plan

```http
GET /api/v1/meal-plans/{plan_id}
Authorization: Bearer {token}
```

#### List User's Meal Plans

```http
GET /api/v1/meal-plans/me
Authorization: Bearer {token}
```

---

### Nutrition Calculator Endpoints

#### Calculate Requirements

Calculate nutritional requirements based on user data.

```http
POST /api/v1/nutrition-calculator/requirements
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "age": 30,
  "gender": "male",
  "weight_kg": 75,
  "height_cm": 175,
  "activity_level": "moderately_active",
  "goal": "weight_loss"
}
```

**Activity Levels**: `sedentary`, `lightly_active`, `moderately_active`, `very_active`, `extremely_active`

**Goals**: `weight_loss`, `maintenance`, `muscle_gain`

**Response (200):**
```json
{
  "bmr": 1725,
  "tdee": 2380,
  "target_calories": 1880,
  "macros": {
    "protein_g": 140,
    "protein_calories": 560,
    "protein_percentage": 30,
    "carbs_g": 188,
    "carbs_calories": 752,
    "carbs_percentage": 40,
    "fats_g": 63,
    "fats_calories": 567,
    "fats_percentage": 30
  },
  "recommendations": [
    "Déficit calórico moderado de 500 calorías para pérdida de peso saludable",
    "Proteína alta para preservar masa muscular"
  ]
}
```

#### Calculate Meal Nutrition

```http
POST /api/v1/nutrition-calculator/meal
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "foods": [
    {
      "food_id": 1,
      "quantity": 2,
      "unit": "porciones"
    },
    {
      "food_id": 5,
      "quantity": 100,
      "unit": "g"
    }
  ]
}
```

**Response (200):**
```json
{
  "total_calories": 425,
  "total_protein": 15.5,
  "total_carbs": 55.2,
  "total_fats": 12.8,
  "total_fiber": 8.5,
  "foods_breakdown": [
    {
      "food_name": "Tortilla de maíz",
      "quantity": 2,
      "calories": 128
    }
  ]
}
```

---

### Vision AI Endpoints

#### Analyze Food Photo

Analyze a food photo using AI vision.

```http
POST /api/v1/vision/analyze-food
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request:**
```
image: [binary file]
```

**Response (200):**
```json
{
  "analysis": {
    "dish_name": "Tacos al Pastor",
    "region": "Ciudad de México",
    "confidence": 0.95,
    "ingredients": [
      {
        "name": "Carne de cerdo marinada",
        "quantity": "150g",
        "calories": 285
      },
      {
        "name": "Tortillas de maíz",
        "quantity": "3 piezas",
        "calories": 192
      },
      {
        "name": "Piña",
        "quantity": "30g",
        "calories": 15
      }
    ],
    "nutrition": {
      "total_calories": 492,
      "protein": 28,
      "carbs": 45,
      "fats": 22,
      "fiber": 6,
      "sodium": 650
    },
    "nom051_warnings": {
      "exceso_calorias": false,
      "exceso_azucares": false,
      "exceso_grasas_saturadas": true,
      "exceso_sodio": true
    },
    "health_score": 72,
    "recommendations": [
      "Moderada cantidad de sodio debido a la marinada",
      "Buena fuente de proteínas",
      "Considera reducir la porción de carne para menos grasas saturadas"
    ]
  },
  "model_used": "gemini-1.5-pro",
  "processing_time_ms": 2341
}
```

#### Check Vision Service Health

```http
GET /api/v1/vision/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "models_available": {
    "gemini": true,
    "claude": true
  },
  "current_model": "gemini",
  "api_keys_configured": {
    "gemini": true,
    "claude": false
  }
}
```

---

### RAG Chat Endpoints

#### Chat with AI Assistant

Send a message to the RAG-powered AI assistant.

```http
POST /api/v1/rag/chat
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "message": "¿Cuántas calorías tiene una tortilla de maíz?",
  "context_type": "foods",
  "conversation_id": "optional-conversation-id"
}
```

**Context Types**: `foods`, `products`, `recipes`, `all`

**Response (200):**
```json
{
  "response": "Una tortilla de maíz (30g) tiene aproximadamente 64 calorías. También aporta 1.7g de proteína, 13.4g de carbohidratos y 0.9g de grasas. Es una excelente fuente de fibra (1.5g) y tiene muy poco sodio (3mg).",
  "sources": [
    {
      "type": "food",
      "id": 1,
      "name": "Tortilla de maíz",
      "relevance": 0.98
    }
  ],
  "conversation_id": "conv-123-456",
  "model": "gemini-1.5-flash",
  "cached": false,
  "response_time_ms": 845
}
```

#### Get Chat History

```http
GET /api/v1/rag/history/{conversation_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "conversation_id": "conv-123-456",
  "messages": [
    {
      "role": "user",
      "content": "¿Cuántas calorías tiene una tortilla?",
      "timestamp": "2025-11-11T10:00:00"
    },
    {
      "role": "assistant",
      "content": "Una tortilla de maíz tiene 64 calorías...",
      "timestamp": "2025-11-11T10:00:02"
    }
  ]
}
```

#### RAG Health Check

```http
GET /api/v1/rag/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "gemini_api": true,
  "database_connection": true,
  "vector_search": true,
  "cache_available": true
}
```

---

### Nutritionist Endpoints

#### List Patients

Get list of patients assigned to nutritionist.

```http
GET /api/v1/nutritionist/patients
Authorization: Bearer {token}
```

**Requires**: `nutritionist` role

**Response (200):**
```json
{
  "patients": [
    {
      "id": 10,
      "full_name": "María González",
      "email": "maria@example.com",
      "age": 28,
      "last_consultation": "2025-11-10",
      "active_meal_plan": true,
      "progress": {
        "weight_change_kg": -3.5,
        "adherence_percentage": 85
      }
    }
  ],
  "total": 15
}
```

#### Get Patient Details

```http
GET /api/v1/nutritionist/patients/{patient_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": 10,
  "full_name": "María González",
  "consultations": [
    {
      "id": 1,
      "date": "2025-11-10",
      "notes": "Primera consulta, objetivo pérdida de peso",
      "weight_kg": 75,
      "height_cm": 165
    }
  ],
  "meal_plans": [
    {
      "id": 5,
      "start_date": "2025-11-10",
      "daily_calories": 1600
    }
  ],
  "progress_data": {
    "weight_history": [75, 74.5, 73.8, 71.5],
    "adherence_rate": 85
  }
}
```

#### Create Consultation Note

```http
POST /api/v1/nutritionist/consultations
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "patient_id": 10,
  "weight_kg": 73.5,
  "height_cm": 165,
  "notes": "Progreso excelente, mantener plan actual",
  "recommendations": [
    "Continuar con plan de 1600 calorías",
    "Agregar 30 min de ejercicio diario"
  ]
}
```

---

### Weekly Planning Endpoints

#### Create Weekly Plan

```http
POST /api/v1/weekly-planning
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "start_date": "2025-11-11",
  "meal_plan_id": 1,
  "generate_shopping_list": true
}
```

**Response (201):**
```json
{
  "id": 1,
  "start_date": "2025-11-11",
  "end_date": "2025-11-18",
  "shopping_list": [
    {
      "item": "Pescado blanco",
      "quantity": 1.2,
      "unit": "kg",
      "category": "Proteínas"
    },
    {
      "item": "Tortillas de maíz",
      "quantity": 56,
      "unit": "piezas",
      "category": "Cereales"
    }
  ],
  "estimated_cost": 850.50
}
```

---

## Examples

### Complete User Flow Example

#### 1. Register and Login

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "SecurePass123!",
    "full_name": "Juan Pérez",
    "primary_role": "patient"
  }'

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "SecurePass123!"
  }' | jq -r '.access_token')
```

#### 2. Calculate Nutritional Requirements

```bash
curl -X POST http://localhost:8000/api/v1/nutrition-calculator/requirements \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "gender": "male",
    "weight_kg": 75,
    "height_cm": 175,
    "activity_level": "moderately_active",
    "goal": "weight_loss"
  }'
```

#### 3. Create Meal Plan

```bash
curl -X POST http://localhost:8000/api/v1/meal-plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "weight_loss",
    "daily_calories": 1880,
    "days": 7,
    "meals_per_day": 5
  }'
```

#### 4. Chat with AI for Food Questions

```bash
curl -X POST http://localhost:8000/api/v1/rag/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué alimentos puedo sustituir por tortilla?",
    "context_type": "foods"
  }'
```

#### 5. Analyze Food Photo

```bash
curl -X POST http://localhost:8000/api/v1/vision/analyze-food \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@taco.jpg"
```

### Python SDK Example

```python
import requests

class NutritionAPI:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.token = self._login(email, password)

    def _login(self, email, password):
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()["access_token"]

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def search_foods(self, query):
        response = requests.get(
            f"{self.base_url}/api/v1/foods/search",
            params={"q": query},
            headers=self._headers()
        )
        return response.json()

    def chat(self, message, context_type="all"):
        response = requests.post(
            f"{self.base_url}/api/v1/rag/chat",
            json={"message": message, "context_type": context_type},
            headers=self._headers()
        )
        return response.json()

# Usage
api = NutritionAPI("http://localhost:8000", "user@example.com", "password")
foods = api.search_foods("tortilla")
response = api.chat("¿Cuántas calorías tiene una tortilla?")
print(response["response"])
```

### JavaScript/TypeScript SDK Example

```typescript
class NutritionAPI {
  private baseUrl: string;
  private token: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async login(email: string, password: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    this.token = data.access_token;
  }

  private headers(): HeadersInit {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
  }

  async searchFoods(query: string) {
    const response = await fetch(
      `${this.baseUrl}/api/v1/foods/search?q=${encodeURIComponent(query)}`,
      { headers: this.headers() }
    );
    return await response.json();
  }

  async chat(message: string, contextType: string = 'all') {
    const response = await fetch(`${this.baseUrl}/api/v1/rag/chat`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ message, context_type: contextType })
    });
    return await response.json();
  }

  async analyzePhoto(imageFile: File) {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${this.baseUrl}/api/v1/vision/analyze-food`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${this.token}` },
      body: formData
    });
    return await response.json();
  }
}

// Usage
const api = new NutritionAPI('http://localhost:8000');
await api.login('user@example.com', 'password');
const foods = await api.searchFoods('tortilla');
const chatResponse = await api.chat('¿Cuántas calorías tiene una tortilla?');
console.log(chatResponse.response);
```

---

## API Versioning

The API uses URI versioning with the prefix `/api/v1/`.

Future versions will be available at `/api/v2/`, etc., with backward compatibility maintained for at least one major version.

## Pagination

List endpoints support pagination with `skip` and `limit` parameters:

```http
GET /api/v1/foods?skip=20&limit=10
```

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 150,
  "skip": 20,
  "limit": 10
}
```

## Filtering and Sorting

Many endpoints support filtering and sorting:

```http
GET /api/v1/recipes?category=breakfast&difficulty=easy&sort=rating&order=desc
```

## Webhooks

Future feature - webhook support for real-time notifications.

## Support

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Issues**: GitHub Issues
- **Email**: api-support@ejemplo.com

---

**Last Updated**: 2025-11-11
**API Version**: 1.0.0
