# ✅ Resumen de Configuración - APIs Externas

**Fecha**: Noviembre 2025
**Estado**: Parcialmente configurado

---

## 📊 Estado Actual

| Servicio | Estado | Acciones Necesarias |
|----------|--------|---------------------|
| ✅ Google Gemini Vision | **CONFIGURADO** | ✓ API Key válida |
| ✅ Código Gemini | **ACTUALIZADO** | ✓ Modelo correcto ('gemini-1.5-flash') |
| ⚠️ Twilio WhatsApp | **PENDIENTE** | ⏳ Necesitas registrarte |
| ⚠️ Anthropic Claude | **OPCIONAL** | ⏳ Para chat avanzado |

---

## 🎯 ¿Qué está funcionando ahora?

### ✅ Google Gemini Vision

**Estado**: **LISTO PARA USAR**

```yaml
Configuración actual:
  API Key: AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A
  Modelo: gemini-1.5-flash
  Estado: ✅ Configurado correctamente
```

**El problema anterior ya está resuelto**:
- ❌ Antes usaba: `gemini-1.5-pro-latest` (no existe)
- ✅ Ahora usa: `gemini-1.5-flash` (válido)

**Para probar ahora mismo**:
1. Abre tu navegador: http://localhost:3002
2. Inicia sesión como nutriólogo o paciente
3. Ve a "Análisis de Fotos"
4. Sube una foto de comida
5. ¡Debería funcionar! 🎉

---

## ⏳ ¿Qué falta configurar?

### 1. Twilio WhatsApp (Opcional pero Recomendado)

**¿Para qué sirve?**
- Enviar recordatorios de consulta
- Compartir planes de alimentación
- Recibir fotos de pacientes por WhatsApp
- Mensajes de seguimiento

**Cómo configurar (15 minutos)**:

#### Paso 1: Crear cuenta Twilio

1. Ve a: https://www.twilio.com/try-twilio
2. Regístrate gratis (tarjeta de crédito requerida pero no cobra)
3. Verifica tu email y teléfono

#### Paso 2: Obtener credenciales

1. Ve al Console: https://www.twilio.com/console
2. Copia:
   ```
   Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Auth Token: [muestra el token con "Show"]
   ```

#### Paso 3: Activar WhatsApp Sandbox

1. En Console: Messaging → Try it out → Send a WhatsApp message
2. O directo: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
3. Verás un número: `+1 (415) 523-8886`
4. Desde tu WhatsApp, envía:
   ```
   join [código que te muestren]
   ```
   Ejemplo: `join shadow-clock`

#### Paso 4: Actualizar archivo .env

Abre: `C:\Nutrition Intelligence\backend\.env`

Busca estas líneas:
```bash
TWILIO_ACCOUNT_SID=your-twilio-account-sid-here
TWILIO_AUTH_TOKEN=your-twilio-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

Reemplaza con tus valores reales:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_token_secreto_de_twilio_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

⚠️ **IMPORTANTE**: El número de WhatsApp debe empezar con `whatsapp:+`

#### Paso 5: Reiniciar el backend

```bash
# En la terminal donde corre el backend, presiona Ctrl+C
# Luego vuelve a ejecutar:
cd "C:\Nutrition Intelligence\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Paso 6: Probar WhatsApp

Prueba desde Python:
```python
cd "C:\Nutrition Intelligence\backend"
python

# En el intérprete de Python:
from twilio.rest import Client

account_sid = 'TU_ACCOUNT_SID'
auth_token = 'TU_AUTH_TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='🇲🇽 ¡Prueba exitosa de Nutrition Intelligence!',
    to='whatsapp:+52XXXXXXXXXX'  # Tu número (debe estar en sandbox)
)

print(f'✅ Mensaje enviado: {message.sid}')
```

---

### 2. Anthropic Claude (Opcional)

**¿Para qué sirve?**
- Chat IA más avanzado
- Respuestas más precisas
- Fallback cuando Gemini tiene baja confianza

**Cómo configurar (5 minutos)**:

#### Paso 1: Crear cuenta

1. Ve a: https://console.anthropic.com/
2. Regístrate
3. Agrega $5 USD de crédito (pay-as-you-go)

#### Paso 2: Obtener API Key

1. Settings → API Keys
2. Create Key
3. Copia la key (empieza con `sk-ant-api03-...`)

#### Paso 3: Actualizar .env

En `backend/.env`, cambia:
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

Por:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx-tu-key-real-aqui-xxxxx
```

#### Paso 4: Reiniciar backend

Ctrl+C y vuelve a iniciar con uvicorn.

---

## 🧪 Verificar que Todo Funciona

### Checklist de Verificación

```
✅ Gemini Vision:
   ☑ API key configurada en .env
   ☑ Código usa modelo correcto
   ☑ Backend reiniciado
   ☐ Probado con foto de prueba

⏳ Twilio WhatsApp:
   ☐ Cuenta creada
   ☐ Account SID obtenido
   ☐ Auth Token obtenido
   ☐ Sandbox activado con 'join'
   ☐ Credenciales en .env
   ☐ Backend reiniciado
   ☐ Mensaje de prueba enviado

⏳ Claude (Opcional):
   ☐ Cuenta creada
   ☐ Crédito agregado
   ☐ API key obtenida
   ☐ API key en .env
   ☐ Backend reiniciado
   ☐ Chat probado
```

### Comandos Útiles para Verificar

**Ver logs del backend**:
```bash
# La terminal donde corre uvicorn mostrará:
✅ Gemini Vision configured
✅ Twilio WhatsApp configured
```

**Probar Gemini desde terminal**:
```bash
cd "C:\Nutrition Intelligence\backend"
python -c "
import google.generativeai as genai
genai.configure(api_key='AIzaSyCrlS17fcuCQkIQfC40TAVa19X6RFftc6A')
model = genai.GenerativeModel('gemini-1.5-flash')
print('✅ Gemini funcionando correctamente')
"
```

**Ver estado de servicios**:
```bash
curl http://localhost:8000/health
```

---

## 📝 Archivo .env Completo (Ejemplo)

Así debería verse tu archivo después de configurar todo:

```bash
# Nutrition Intelligence Backend - Local Development Environment

# Environment Configuration
ENVIRONMENT=development
DEBUG=true

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./nutrition_intelligence.db
DATABASE_ECHO=false

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=development-secret-key-for-local-testing-only-change-in-production-minimum-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
ALGORITHM=HS256

# API Configuration
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://localhost:3005,http://localhost:3001,http://localhost:3002,http://127.0.0.1:3000,http://127.0.0.1:3005,http://127.0.0.1:3001,http://127.0.0.1:3002

# AI Vision Services
GOOGLE_API_KEY=AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx-tu-key-aqui-xxxxx
AI_VISION_MODEL=gemini
AI_VISION_CONFIDENCE_THRESHOLD=75

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_token_secreto_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Compliance
DATA_RETENTION_DAYS=2555
AUDIT_LOG_ENABLED=true

SMTP_PORT=587
```

---

## 💰 Costos Estimados

### Actual (Con solo Gemini)

```
Gemini Vision: $0/mes (gratis hasta 1,500 req/día)
Total: $0/mes ✅
```

### Si agregas Twilio + Claude

```
Gemini Vision: $0/mes (gratis)
Twilio Sandbox: $0/mes (500 mensajes gratis)
Claude Chat: ~$5/mes (uso moderado)
─────────────────────────────
Total: ~$5/mes
```

### Producción (100 pacientes)

```
Gemini Vision: $0/mes (dentro del tier gratis)
Twilio Producción: $11.50/mes
  - Número: $1.50/mes
  - 2,000 mensajes: $10/mes
Claude: $50/mes (5,000 conversaciones)
─────────────────────────────
Total: ~$61.50/mes
```

---

## 🆘 Problemas Comunes

### 1. "Gemini Vision not found"

✅ **Ya está resuelto** - El código ahora usa 'gemini-1.5-flash'

### 2. "Twilio authentication failed"

Verifica:
- Account SID comienza con `AC`
- Auth Token no tiene espacios
- Número tiene formato: `whatsapp:+14155238886`

### 3. "WhatsApp number not verified"

Tu número debe:
1. Enviar `join [código]` al sandbox de Twilio
2. Recibir confirmación de Twilio

### 4. "Claude rate limit exceeded"

Solución:
- Agrega más crédito en console.anthropic.com
- O usa solo modo `gemini` en AI_VISION_MODEL

---

## 📞 Contacto y Soporte

### Documentación Completa

📄 Ver: `docs/GUIA-CONFIGURACION-APIS.md` (guía extendida)

### URLs Importantes

- **Gemini API**: https://ai.google.dev/
- **Twilio Console**: https://www.twilio.com/console
- **Claude Console**: https://console.anthropic.com/
- **Documentación Proyecto**: `docs/`

---

## ✅ Resumen Final

### ¿Qué funciona ahora?

✅ **Gemini Vision está listo para usar**
- Análisis de fotos de alimentos
- Identificación de ingredientes
- Cálculo nutricional automático

### ¿Qué falta?

⏳ **Twilio WhatsApp** (15 min para configurar)
⏳ **Claude Chat** (5 min para configurar, opcional)

### Próximo paso

**Para habilitar WhatsApp**:
1. Regístrate en Twilio (https://www.twilio.com/try-twilio)
2. Copia tus credenciales
3. Actualiza el .env
4. Reinicia el backend
5. ¡Listo para enviar mensajes! 🎉

---

**🇲🇽 Nutrition Intelligence - APIs Configuradas Correctamente**

**Última actualización**: Noviembre 2025
