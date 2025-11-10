# AI Services - Gemini Integration

Este módulo proporciona integración con Google Gemini AI para el sistema de chat nutricional context-aware.

## Configuración

### 1. Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API key
4. Copia la API key generada

### 2. Configurar Variables de Entorno

Agrega la siguiente variable a tu archivo `.env` en el directorio `backend`:

```bash
# AI Services
GEMINI_API_KEY=tu_api_key_aqui
DEFAULT_AI_MODEL=gemini-pro
```

**Opcional**: Si planeas usar Claude en el futuro:
```bash
ANTHROPIC_API_KEY=tu_api_key_de_claude
```

### 3. Reiniciar el Servidor

Después de agregar la API key, reinicia el servidor backend:

```bash
# Desarrollo
cd backend
uvicorn main:app --reload

# Docker
docker compose restart backend
```

## Uso

### Endpoint Principal: `/api/v1/rag/chat`

```bash
POST /api/v1/rag/chat
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "¿Qué alimentos puedo comer si tengo diabetes?",
  "include_context": true,
  "include_search_results": true
}
```

**Respuesta**:
```json
{
  "message": "¿Qué alimentos puedo comer si tengo diabetes?",
  "user_id": 123,
  "context_included": true,
  "search_included": true,
  "ai_response": "Como nutriólogo experto...",
  "model": "gemini-pro",
  "usage": {
    "prompt_tokens": 1500,
    "completion_tokens": 400,
    "total_tokens": 1900
  },
  "user_context_summary": {
    "scan_count": 45,
    "favorite_foods_count": 12
  }
}
```

## Características

### 1. Chat Context-Aware
- Acceso automático al historial de escaneos del usuario
- Incluye productos favoritos y estadísticas
- Respuestas personalizadas basadas en el perfil

### 2. Análisis Nutricional
```python
from backend.services.ai.gemini_service import GeminiService

gemini = GeminiService()
result = await gemini.nutritional_analysis(product_data)
```

### 3. Sugerencias de Planes de Comida
```python
result = await gemini.meal_plan_suggestions(
    user_profile={
        "edad": 35,
        "peso_kg": 75,
        "altura_cm": 170,
        "objetivo_nutricional": "bajar de peso"
    }
)
```

## Prompts del Sistema

### Contexto Nutricional Mexicano

El servicio está optimizado para:
- **NOM-051-SCFI/SSA1-2010**: Etiquetado frontal mexicano
- **SMAE**: Sistema Mexicano de Alimentos Equivalentes
- **Sellos de Advertencia**: Explicación automática
- **Alimentos Tradicionales**: Contexto cultural mexicano

### Sellos de Advertencia

El sistema explica automáticamente:
- 🔴 **Exceso calorías**: >275 kcal/100g
- 🔴 **Exceso azúcares**: >10g/100g
- 🔴 **Exceso grasas saturadas**: >4g/100g
- 🔴 **Exceso grasas trans**: >0.5g/100g
- 🔴 **Exceso sodio**: >300mg/100g

## Seguridad

### Filtros de Contenido

El servicio incluye filtros de seguridad para:
- ✅ Hate speech: BLOCK_MEDIUM_AND_ABOVE
- ✅ Dangerous content: BLOCK_MEDIUM_AND_ABOVE
- ✅ Sexually explicit: BLOCK_MEDIUM_AND_ABOVE
- ✅ Harassment: BLOCK_MEDIUM_AND_ABOVE

### Limitaciones Éticas

La IA **NUNCA**:
- ❌ Diagnostica enfermedades
- ❌ Proporciona tratamientos médicos
- ❌ Reemplaza consultas profesionales
- ❌ Juzga las decisiones alimentarias

La IA **SIEMPRE**:
- ✅ Refiere a profesionales de salud cuando es necesario
- ✅ Basa respuestas en evidencia científica
- ✅ Es empática y motivadora
- ✅ Respeta el contexto cultural

## Configuración Avanzada

### Ajustar Parámetros de Generación

En `gemini_service.py`, método `_get_generation_config()`:

```python
{
    "temperature": 0.7,      # Creatividad (0.0-1.0)
    "top_p": 0.95,           # Nucleus sampling
    "top_k": 40,             # Top-k sampling
    "max_output_tokens": 2048 # Tokens máximos
}
```

### Cambiar Modelo

Modelos disponibles:
- `gemini-pro` (recomendado)
- `gemini-pro-vision` (para imágenes)
- `gemini-ultra` (próximamente)

Cambiar en `.env`:
```bash
DEFAULT_AI_MODEL=gemini-pro-vision
```

## Monitoreo y Logs

El servicio genera logs automáticos:

```python
logger.info(f"Sending request to Gemini API (message length: {len(user_message)})")
logger.info(f"Gemini response received (length: {len(response.text)})")
logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
```

### Verificar Estado

```bash
GET /api/v1/rag/health
```

Respuesta:
```json
{
  "status": "healthy",
  "service": "RAG (Retrieval Augmented Generation)",
  "version": "1.0.0",
  "endpoints": {
    "chat": ["/rag/chat"],
    "search": [...],
    "context": [...]
  }
}
```

## Costos y Límites

### Google Gemini Pro

- **Free tier**: 60 requests/minute
- **Paid tier**: Mayor throughput
- **Costo**: $0.00025/1K tokens (prompt) + $0.0005/1K tokens (completion)

### Optimización de Costos

1. **Cache de Contexto**: Reutiliza contexto cuando sea posible
2. **Límite de Tokens**: Configurado a 2048 tokens máximo
3. **Contexto Selectivo**: Usa `include_context=false` si no necesitas historial

## Troubleshooting

### Error: "Gemini API key not configured"

**Solución**: Verifica que `GEMINI_API_KEY` esté en tu archivo `.env`

```bash
# Verificar en Docker
docker compose exec backend env | grep GEMINI_API_KEY

# Verificar localmente
echo $GEMINI_API_KEY
```

### Error: "Response blocked by safety filters"

**Solución**: El contenido fue bloqueado por filtros de seguridad. Revisa:
- El mensaje del usuario no contiene contenido inapropiado
- El contexto proporcionado es relevante al tema nutricional

### Error: "Rate limit exceeded"

**Solución**:
- Espera 1 minuto y reintentar
- Considera upgrade a plan pagado
- Implementa cache/retry logic

## Próximos Pasos

- [ ] Implementar frontend de chat
- [ ] Agregar soporte para streaming responses
- [ ] Implementar cache de respuestas
- [ ] Agregar soporte para Claude AI
- [ ] Implementar analytics de uso

## Recursos

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [NOM-051 Information](https://www.gob.mx/cofepris/documentos/nom-051)
- [SMAE Documentation](https://www.smae.nutricion.org/)
