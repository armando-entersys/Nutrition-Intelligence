# Configuración de AI Vision (Gemini & Claude)

Este documento explica cómo configurar las APIs de visión de IA para el análisis de fotos de comida.

## Modelos Disponibles

### 1. **Gemini 1.5 Pro** (Recomendado para empezar) ⭐
- **Ventajas**: Económico, buena precisión, contexto largo
- **Costo**: ~$0.35 USD / 1M tokens con imágenes
- **Velocidad**: Rápido
- **API**: Google AI Studio (GRATIS para desarrollo)

### 2. **Claude 3.5 Sonnet** (Mejor precisión)
- **Ventajas**: Máxima precisión en análisis nutricional
- **Costo**: ~$3 USD / 1M tokens con imágenes
- **Velocidad**: Rápido
- **API**: Anthropic Console (Pay-as-you-go)

### 3. **Modo Híbrido** (Mejor balance) 🎯
- Usa Gemini como principal
- Fallback a Claude si confianza < 75%
- Optimiza costos y mantiene calidad

---

## Guía de Configuración

### Opción 1: Gemini Vision (GRATIS para empezar)

#### Paso 1: Obtener API Key

1. Ve a [Google AI Studio](https://ai.google.dev/)
2. Inicia sesión con tu cuenta de Google Workspace
3. Click en "Get API Key"
4. Crea un nuevo proyecto o selecciona uno existente
5. Copia la API key generada

#### Paso 2: Configurar en el Backend

Edita el archivo `backend/.env`:

```env
# AI Vision Services
GOOGLE_API_KEY=tu-api-key-de-google-aqui
AI_VISION_MODEL=gemini
```

#### Paso 3: Verificar Instalación

```bash
cd backend
python -c "import google.generativeai as genai; print('Gemini SDK instalado correctamente')"
```

---

### Opción 2: Claude Vision (Máxima Precisión)

#### Paso 1: Obtener API Key

1. Ve a [Anthropic Console](https://console.anthropic.com/settings/keys)
2. Inicia sesión con tu cuenta de Anthropic
3. Click en "Create Key"
4. Copia la API key generada

#### Paso 2: Configurar en el Backend

Edita el archivo `backend/.env`:

```env
# AI Vision Services
ANTHROPIC_API_KEY=sk-ant-tu-api-key-de-anthropic-aqui
AI_VISION_MODEL=claude
```

#### Paso 3: Verificar Instalación

```bash
cd backend
python -c "import anthropic; print('Anthropic SDK instalado correctamente')"
```

---

### Opción 3: Modo Híbrido (Recomendado para Producción) 🎯

#### Configuración

Edita el archivo `backend/.env`:

```env
# AI Vision Services
GOOGLE_API_KEY=tu-api-key-de-google-aqui
ANTHROPIC_API_KEY=sk-ant-tu-api-key-de-anthropic-aqui
AI_VISION_MODEL=hybrid
AI_VISION_CONFIDENCE_THRESHOLD=75
```

#### ¿Cómo funciona?

1. Gemini analiza la imagen primero (económico)
2. Si confianza >= 75% → usa resultado de Gemini ✅
3. Si confianza < 75% → llama a Claude para análisis detallado 🔄
4. Resultado: **~85% ahorro** vs usar solo Claude

---

## Configuración de Variables

En `backend/.env`:

```env
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
```

---

## Verificar Configuración

### 1. Verificar Health del Servicio

```bash
curl http://localhost:8000/api/v1/vision/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "ai-vision",
  "models": {
    "gemini": {
      "available": true,
      "model": "gemini-1.5-pro-latest"
    },
    "claude": {
      "available": false,
      "model": null
    }
  },
  "mode": "gemini"
}
```

### 2. Verificar Configuración

```bash
curl http://localhost:8000/api/v1/vision/config
```

### 3. Probar Análisis de Imagen

```bash
curl -X POST "http://localhost:8000/api/v1/vision/analyze-food" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/taco-image.jpg"
```

---

## Límites y Costos

### Google AI Studio (Desarrollo - GRATIS)
- **Requests**: 15 requests/minuto
- **Límite diario**: Generoso para desarrollo
- **Costo**: GRATIS
- **Ideal para**: Desarrollo y pruebas

### Vertex AI (Producción)
- **Costo**: $0.35 / 1M tokens input (con imágenes)
- **Límite**: Escalable según plan
- **Ideal para**: Producción

### Anthropic API
- **Costo**: $3.00 / 1M tokens input (con imágenes)
- **Límite**: Según créditos
- **Ideal para**: Análisis de máxima precisión

---

## Comparación de Modelos

| Característica | Gemini 1.5 Pro | Claude 3.5 Sonnet | Híbrido |
|----------------|----------------|-------------------|---------|
| **Precisión Nutricional** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Costo (por 1M tokens)** | $0.35 | $3.00 | ~$0.80 |
| **Velocidad** | Rápido | Rápido | Rápido |
| **Comida Mexicana** | Muy bueno | Excelente | Excelente |
| **Gratis para Dev** | ✅ Sí | ❌ No | ⚠️ Parcial |
| **Contexto Largo** | 1M tokens | 200K tokens | 1M tokens |

---

## Solución de Problemas

### Error: "API key not configured"

```python
# Verifica que la variable esté en .env
GOOGLE_API_KEY=tu-api-key-aqui

# NO uses comillas ni espacios
✅ GOOGLE_API_KEY=AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A
❌ GOOGLE_API_KEY="AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A"
❌ GOOGLE_API_KEY = AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A
```

### Error: "Module not found"

```bash
# Reinstala las dependencias
cd backend
pip install -r requirements.txt
```

### Error: "Rate limit exceeded"

- **Gemini**: Estás haciendo más de 15 requests/minuto en dev
  - Solución: Espera 1 minuto o actualiza a Vertex AI
- **Claude**: Agotaste tus créditos
  - Solución: Agrega créditos en Anthropic Console

### Error: "Invalid JSON response"

El modelo respondió en formato incorrecto:
- Revisa los logs del backend para ver la respuesta raw
- Puede suceder si la imagen es de mala calidad
- Solución: Usa imagen de mejor calidad o prueba con modo híbrido

---

## Recomendaciones

### Para Desarrollo 🔨
```env
AI_VISION_MODEL=gemini
GOOGLE_API_KEY=tu-key-de-google-ai-studio
```

### Para Producción (Balance) ⚖️
```env
AI_VISION_MODEL=hybrid
GOOGLE_API_KEY=tu-key-de-google
ANTHROPIC_API_KEY=tu-key-de-claude
AI_VISION_CONFIDENCE_THRESHOLD=75
```

### Para Máxima Precisión 🎯
```env
AI_VISION_MODEL=claude
ANTHROPIC_API_KEY=tu-key-de-claude
```

---

## Prompt Especializado

El sistema usa un prompt especializado para comida mexicana que incluye:

- ✅ Identificación de platillos tradicionales mexicanos
- ✅ Análisis NOM-051 (sellos de advertencia)
- ✅ Categorización SMAE
- ✅ Estimación de porciones
- ✅ Recomendaciones culturalmente apropiadas

Ver código en: `backend/services/ai/vision.py:40-170`

---

## Siguiente Paso

Una vez configurado:

1. Reinicia el backend
2. Abre el frontend en http://localhost:3005
3. Ve a "Análisis de Fotos IA"
4. Sube una foto de comida
5. ¡Disfruta del análisis con IA! 🎉

---

## Soporte

- **Google AI Studio**: https://ai.google.dev/
- **Anthropic Console**: https://console.anthropic.com/
- **Documentación Gemini**: https://ai.google.dev/docs
- **Documentación Claude**: https://docs.anthropic.com/

---

**Última actualización**: 2025-10-31
