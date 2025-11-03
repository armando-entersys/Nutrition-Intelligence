# 🔧 Guía de Configuración de APIs Externas

**Proyecto**: Nutrition Intelligence
**Última actualización**: Noviembre 2025

---

## 📋 Índice

1. [Google Gemini Vision API](#google-gemini-vision-api)
2. [Twilio WhatsApp API](#twilio-whatsapp-api)
3. [Anthropic Claude API](#anthropic-claude-api-opcional)
4. [Verificación de Configuración](#verificación-de-configuración)

---

## 🤖 Google Gemini Vision API

### ¿Qué hace?
Análisis inteligente de fotos de alimentos para identificar ingredientes, porciones y valores nutricionales.

### Paso 1: Obtener API Key (GRATIS)

1. **Visita Google AI Studio**:
   - URL: https://ai.google.dev/
   - O directo: https://makersuite.google.com/app/apikey

2. **Crea tu API Key**:
   - Click en "Get API Key"
   - Si es tu primera vez, acepta los términos
   - Click en "Create API Key"
   - Copia la key que empieza con `AIza...`

3. **Límites Gratuitos**:
   ```
   ✅ 60 requests por minuto
   ✅ Hasta 1,500 requests por día
   ✅ Gratis para desarrollo
   ```

### Paso 2: Configurar en el Proyecto

**Tu API Key actual**: `AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A`

**Problema detectado**: El modelo usado en el código está desactualizado.

#### Archivo a modificar: `backend/services/ai/vision.py`

Busca la línea que dice:
```python
model = genai.GenerativeModel('gemini-1.5-pro-latest')
```

Y cámbiala por:
```python
model = genai.GenerativeModel('gemini-pro-vision')
# O si quieres el más reciente:
# model = genai.GenerativeModel('gemini-1.5-flash')
```

**Modelos disponibles de Gemini**:
- `gemini-pro-vision` - Análisis de imágenes (RECOMENDADO)
- `gemini-1.5-flash` - Más rápido y económico
- `gemini-1.5-pro` - Máxima precisión (solo texto)

### Paso 3: Verificar Configuración

Tu archivo `.env` ya tiene:
```bash
GOOGLE_API_KEY=AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A
AI_VISION_MODEL=gemini
```

✅ **Configuración correcta**

---

## 📱 Twilio WhatsApp API

### ¿Qué hace?
Envío de mensajes WhatsApp a pacientes:
- Recordatorios de consulta
- Planes de alimentación
- Solicitud de fotos de platillos
- Seguimiento y motivación

### Paso 1: Crear Cuenta Twilio (GRATIS para probar)

1. **Regístrate en Twilio**:
   - URL: https://www.twilio.com/try-twilio
   - Completa el registro
   - Verifica tu email y teléfono

2. **Accede al Console**:
   - URL: https://www.twilio.com/console
   - Anota tus credenciales:
     - **Account SID**: ACxxxxxxxxxxxxxxxxxxxxx
     - **Auth Token**: [token secreto]

3. **Activa WhatsApp Sandbox**:
   - En Console, ve a "Messaging" → "Try it out" → "Send a WhatsApp message"
   - O directo: https://www.twilio.com/console/sms/whatsapp/sandbox
   - Verás un número como: `+1 415 523 8886`
   - Envía el código de activación desde tu WhatsApp

### Paso 2: Obtener Credenciales

En tu Twilio Console verás:

```
┌─────────────────────────────────────────┐
│  ACCOUNT SID                            │
│  ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     │
│                                         │
│  AUTH TOKEN                             │
│  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx      │
│  [Show]                                 │
└─────────────────────────────────────────┘
```

### Paso 3: Configurar en el Proyecto

Abre el archivo `backend/.env` y agrega/actualiza:

```bash
# Twilio - For WhatsApp messaging
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Notas importantes**:
- El número debe empezar con `whatsapp:+`
- En sandbox, el número es: `whatsapp:+14155238886`
- En producción, necesitas comprar un número propio

### Paso 4: Verificar WhatsApp Sandbox

Para usar el sandbox:

1. Desde tu WhatsApp personal, envía al número Twilio:
   ```
   join [código-sandbox]
   ```

2. Ejemplo:
   ```
   join shadow-clock
   ```

3. Recibirás confirmación:
   ```
   ✅ You are now connected to the Twilio Sandbox
   ```

### Límites de Sandbox (Gratis)

```yaml
Sandbox gratuito:
  ✅ Hasta 500 mensajes/mes
  ✅ Solo a números verificados
  ⚠️  Sandbox expira cada 72 horas de inactividad
  ⚠️  Prefijo "Twilio Sandbox" en mensajes

Para producción:
  📱 Compra número WhatsApp Business: ~$1.50/mes
  💬 Mensajes: $0.005 cada uno
```

---

## 💬 Anthropic Claude API (Opcional)

### ¿Qué hace?
Chat inteligente con pacientes y nutriólogos. Responde preguntas nutricionales.

### Paso 1: Obtener API Key

1. **Regístrate en Anthropic**:
   - URL: https://console.anthropic.com/
   - Crea cuenta gratuita

2. **Obtén tu API Key**:
   - Ve a Settings → API Keys
   - Click "Create Key"
   - Copia la key que empieza con `sk-ant-...`

3. **Añade créditos**:
   - Mínimo $5 USD
   - Pay-as-you-go: ~$3 por millón de tokens

### Paso 2: Configurar en el Proyecto

Actualiza tu `backend/.env`:

```bash
# Anthropic Claude API Key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Límites y Costos

```yaml
Claude Sonnet 3.5:
  💰 $3 por millón de tokens input
  💰 $15 por millón de tokens output
  📊 Contexto: 200k tokens

Uso estimado:
  💬 Chat promedio: ~$0.01 por conversación
  📸 Análisis de foto: ~$0.03 por imagen
```

---

## ✅ Verificación de Configuración

### 1. Verificar archivo .env

Tu archivo `backend/.env` debe tener:

```bash
# AI Vision Services
GOOGLE_API_KEY=AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
AI_VISION_MODEL=gemini

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 2. Reiniciar Backend

Después de modificar `.env`, reinicia el backend:

```bash
# Detener: Ctrl+C en la terminal del backend
# Iniciar:
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Probar Gemini Vision

**Test desde la terminal**:
```bash
cd backend
python -c "
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A')
model = genai.GenerativeModel('gemini-pro-vision')
print('✅ Gemini Vision configurado correctamente')
"
```

**Test desde la app**:
1. Abre: http://localhost:3002
2. Inicia sesión como nutriólogo o paciente
3. Ve a "Análisis de Fotos"
4. Sube una foto de comida
5. Debe analizar y devolver resultados

### 4. Probar Twilio WhatsApp

**Test desde Python**:
```python
from twilio.rest import Client

account_sid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='🇲🇽 ¡Hola! Este es un mensaje de prueba de Nutrition Intelligence',
    to='whatsapp:+52XXXXXXXXXX'  # Tu número verificado
)

print(f'✅ Mensaje enviado: {message.sid}')
```

### 5. Ver Logs del Backend

Revisa la terminal donde corre el backend. Deberías ver:

**✅ Configuración correcta**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
✅ Gemini Vision configured
✅ Twilio WhatsApp configured
```

**❌ Si ves errores**:
```
⚠️  Anthropic API key not configured. Claude Vision disabled.
⚠️  Twilio not configured. WhatsApp disabled.
```

---

## 🔧 Troubleshooting

### Error: "models/gemini-1.5-pro-latest is not found"

**Causa**: Modelo desactualizado en el código.

**Solución**:
1. Abre `backend/services/ai/vision.py`
2. Busca: `'gemini-1.5-pro-latest'`
3. Cambia por: `'gemini-pro-vision'`
4. Reinicia backend

### Error: "Unable to authenticate. Please check your Twilio credentials"

**Causa**: Account SID o Auth Token incorrectos.

**Solución**:
1. Verifica en https://www.twilio.com/console
2. Copia exactamente el SID y Token
3. Asegúrate de no tener espacios extras en `.env`
4. Reinicia backend

### Error: "Phone number not verified"

**Causa**: Intentas enviar a un número no verificado en Sandbox.

**Solución**:
1. El número destino debe enviar `join [código]` al sandbox
2. O compra un número WhatsApp Business para producción

### Gemini no responde / timeout

**Causa**: API key inválida o cuota excedida.

**Solución**:
1. Verifica tu API key en https://makersuite.google.com/app/apikey
2. Revisa límites en Google Cloud Console
3. Prueba con una API key nueva

---

## 💰 Costos Estimados

### Desarrollo (Gratis)

```yaml
Gemini Vision:
  ✅ Gratis hasta 60 req/min
  ✅ 1,500 req/día
  Costo: $0

Twilio Sandbox:
  ✅ 500 mensajes/mes gratis
  Costo: $0

Claude (opcional):
  ⚠️  Requiere $5 USD mínimo
  Costo: $5 inicial
```

### Producción (Pequeña escala)

```yaml
Supongamos 100 pacientes:

Gemini Vision:
  📸 500 análisis/mes
  💰 $0 (dentro del tier gratis)

Twilio WhatsApp:
  📱 Número: $1.50/mes
  💬 2,000 mensajes: $10/mes
  Total: $11.50/mes

Claude:
  💬 5,000 conversaciones: $50/mes

TOTAL: ~$61.50/mes para 100 pacientes
```

---

## 📞 Soporte

### Google Gemini
- Documentación: https://ai.google.dev/docs
- Foro: https://discuss.ai.google.dev/

### Twilio
- Documentación: https://www.twilio.com/docs/whatsapp
- Soporte: https://support.twilio.com/

### Anthropic Claude
- Documentación: https://docs.anthropic.com/
- Discord: https://discord.gg/anthropic

---

## ✅ Checklist de Configuración

Marca cuando completes cada paso:

```
Google Gemini Vision:
  ☐ Obtener API Key
  ☐ Agregar a .env
  ☐ Actualizar modelo en código
  ☐ Reiniciar backend
  ☐ Probar con foto de prueba

Twilio WhatsApp:
  ☐ Crear cuenta Twilio
  ☐ Obtener Account SID
  ☐ Obtener Auth Token
  ☐ Activar WhatsApp Sandbox
  ☐ Agregar credenciales a .env
  ☐ Verificar tu número con 'join'
  ☐ Reiniciar backend
  ☐ Enviar mensaje de prueba

Anthropic Claude (Opcional):
  ☐ Crear cuenta Anthropic
  ☐ Agregar $5 USD de crédito
  ☐ Obtener API Key
  ☐ Agregar a .env
  ☐ Reiniciar backend
  ☐ Probar chat IA
```

---

**🇲🇽 Nutrition Intelligence - Configuración de APIs Completada**
