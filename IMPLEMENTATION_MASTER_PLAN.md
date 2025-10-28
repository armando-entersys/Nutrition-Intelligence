# 🚀 Plan Maestro de Implementación
## Nutrition Intelligence - Plataforma Multiplataforma Profesional

**Fecha:** Enero 2025
**Objetivo:** Crear una plataforma adictiva de nutrición con React Native + Web compartiendo backend

---

## 📊 Análisis Competitivo - Apps Líderes del Mercado

### **MyFitnessPal** (Líder en tracking)
- ✅ 14M+ alimentos en base de datos
- ✅ Escaneo de códigos de barras
- ✅ Integración con wearables (Fitbit, Apple Watch)
- ✅ Tracking de macros y micronutrientes
- 💰 Premium: $19.99/mes - $79.99/año

### **Noom** (Líder en psicología comportamental)
- ✅ Sistema de colores (verde/amarillo/rojo) para alimentos
- ✅ Coaching 1-on-1 con nutriólogos
- ✅ Lecciones diarias de psicología
- ✅ Grupos de apoyo con moderadores
- ✅ Estrategias de mindful eating
- 💰 Premium: $70/mes - $209/año

### **Lose It!** (Líder en simplicidad)
- ✅ Foto-tracking de comidas con IA
- ✅ Voz para logging rápido
- ✅ Desafíos semanales
- ✅ Reportes de progreso visuales
- ✅ Integración con fitness trackers
- 💰 Premium: $9.99/mes - $79.99/año

### **Tendencias 2025 - Gamificación en Salud**
- 🎮 15-20% mejora en resultados con gamificación
- 🏆 30% mayor retención con apps prescritas por profesionales
- 🤝 Comunidades y retos sociales aumentan motivación
- 🔔 Recordatorios inteligentes y notificaciones personalizadas
- 📈 Visualización de progreso con gráficos atractivos
- 🥇 Sistema de achievements, badges y recompensas

---

## 🎯 Nuestra Ventaja Competitiva

**"Nutrition Intelligence" será la primera app que combina:**

1. **Relación Directa Nutriólogo-Paciente** (vs. coaching genérico)
2. **Sistema de Equivalencias Mexicano** (único en el mercado)
3. **Gamificación Social Bidireccional** (nutriólogos y pacientes compiten/colaboran)
4. **Multiplataforma con Datos Sincronizados** (Web + iOS + Android)
5. **Comunidad Privada por Nutriólogo** (no solo comunidad global)
6. **IA para Recomendaciones Personalizadas**

---

## 🏗️ Arquitectura Técnica - Monorepo Compartido

```
nutrition-intelligence/
├── packages/
│   ├── mobile/              # React Native (Expo) - iOS + Android
│   ├── web/                 # React Web (código actual mejorado)
│   ├── shared/              # Código compartido entre plataformas
│   │   ├── components/      # Componentes UI universales
│   │   ├── hooks/           # Custom hooks compartidos
│   │   ├── utils/           # Funciones utilitarias
│   │   ├── api/             # Cliente API compartido (Axios)
│   │   ├── types/           # TypeScript types
│   │   └── constants/       # Constantes globales
│   └── backend/             # FastAPI actual (mejorado)
│       ├── auth/            # Sistema de autenticación
│       ├── gamification/    # Sistema de puntos/badges
│       ├── social/          # Features sociales
│       └── notifications/   # Push notifications
├── assets/                  # Imágenes, iconos compartidos
└── scripts/                 # Scripts de deployment
```

### **Stack Tecnológico**

#### Frontend
- **Mobile:** React Native + Expo (iOS/Android)
- **Web:** React 18+ (actual)
- **UI Shared:** React Native Paper / Tamagui (componentes multiplataforma)
- **Navigation:** React Navigation (mobile) + React Router (web)
- **State:** Zustand (ligero, fácil sincronización)
- **Forms:** React Hook Form
- **API Client:** Axios con interceptors compartidos

#### Backend (Mejoras)
- **Framework:** FastAPI (actual)
- **Auth:** JWT + Refresh Tokens + OAuth2
- **Database:** PostgreSQL (actual) + Redis (sessions/cache)
- **Storage:** MinIO (actual) + Cloudinary (imágenes optimizadas)
- **Real-time:** WebSockets (Socket.io o FastAPI WebSocket)
- **Notifications:** Firebase Cloud Messaging (FCM)
- **Email:** SendGrid / Mailgun (recuperación contraseñas)
- **Social:** API de Facebook, Instagram, Twitter para compartir

#### DevOps
- **Monorepo:** Nx o Turborepo
- **CI/CD:** GitHub Actions
- **Mobile Deploy:** EAS (Expo Application Services)
- **Web Deploy:** Vercel o Netlify
- **Backend Deploy:** Docker + AWS/DigitalOcean

---

## 🔐 Sistema de Autenticación Completo

### **Funcionalidades**

#### 1. Registro de Usuarios
```
Nutriólogos:
- Email + Contraseña
- Cédula profesional
- Foto de perfil
- Información profesional
- Verificación manual por admin

Pacientes:
- Método 1: Creado automáticamente por nutriólogo
- Método 2: Registro directo con código de invitación
- Email + Contraseña
- Foto de perfil (opcional)
- Datos básicos (edad, peso, altura, objetivo)
```

#### 2. Login
```
- Email/Username + Contraseña
- OAuth2: Google, Facebook, Apple Sign-In
- Biometría (Touch ID / Face ID) en mobile
- Remember me (30 días con refresh token)
- Detección de dispositivo sospechoso
```

#### 3. Recuperación de Contraseña
```
Flujo completo:
1. Usuario ingresa email
2. Backend envía código de 6 dígitos (válido 15 min)
3. Usuario ingresa código
4. Usuario crea nueva contraseña
5. Todas las sesiones se cierran (excepto la actual)
6. Email de notificación de cambio
```

#### 4. Sesiones y Seguridad
```
- JWT Access Token (15 min)
- Refresh Token (30 días, rotación automática)
- Lista de dispositivos activos (web + mobile)
- Cerrar sesión remota
- Notificaciones de login en nuevo dispositivo
- 2FA opcional (Google Authenticator)
```

---

## 👥 Sistema de Gestión de Pacientes

### **Creación Automática de Usuario Paciente**

Cuando un nutriólogo agrega un paciente:

```python
# Backend - Pseudo-código
def create_patient(nutritionist_id, patient_data):
    # 1. Crear usuario en auth system
    temp_password = generate_secure_password()
    user = create_user(
        email=patient_data.email,
        password=temp_password,
        role="patient",
        is_temp_password=True
    )

    # 2. Crear perfil de paciente
    patient = create_patient_profile(
        user_id=user.id,
        nutritionist_id=nutritionist_id,
        name=patient_data.name,
        age=patient_data.age,
        initial_weight=patient_data.weight,
        goal=patient_data.goal
    )

    # 3. Enviar email de bienvenida con credenciales
    send_welcome_email(
        email=patient_data.email,
        temp_password=temp_password,
        nutritionist_name=nutritionist.name,
        app_download_links={
            "ios": "https://apps.apple.com/...",
            "android": "https://play.google.com/...",
            "web": "https://nutritionintelligence.com"
        }
    )

    # 4. Crear objetivos iniciales y plan básico
    create_initial_goals(patient.id)

    return patient
```

### **Email de Bienvenida al Paciente**

```html
¡Hola [Nombre Paciente]!

Tu nutriólogo(a) [Nombre Nutriólogo] te ha registrado en Nutrition Intelligence 🎉

Tus credenciales de acceso son:
📧 Email: [email]
🔑 Contraseña temporal: [temp_password]

⚠️ Por seguridad, te pediremos cambiar tu contraseña en el primer inicio de sesión.

Descarga la app:
📱 iOS: [link]
🤖 Android: [link]
💻 Web: [link]

¡Comienza tu viaje hacia una vida más saludable! 🥗

---
Equipo Nutrition Intelligence
```

---

## 🎮 Sistema de Gamificación - "Adicción Positiva"

### **Para Pacientes**

#### **Sistema de Puntos (XP)**
```
Acciones diarias:
- Registrar comida: +10 XP
- Completar comida saludable: +15 XP
- Cumplir objetivo de agua: +20 XP
- Hacer ejercicio: +25 XP
- Foto de comida aprobada por nutriólogo: +30 XP
- Racha diaria: +5 XP por día consecutivo

Acciones semanales:
- Cumplir plan semanal: +100 XP
- Perder peso según objetivo: +150 XP
- Completar desafío semanal: +75 XP

Acciones sociales:
- Compartir receta: +10 XP
- Recibir like en receta: +5 XP
- Comentar en comunidad: +3 XP
- Ayudar a otro paciente: +15 XP
```

#### **Sistema de Niveles**
```
Nivel 1: Principiante (0-100 XP) 🌱
Nivel 2: Aprendiz (101-300 XP) 🌿
Nivel 3: Comprometido (301-600 XP) 🌳
Nivel 4: Experto (601-1000 XP) 🏆
Nivel 5: Maestro (1001-2000 XP) 👑
Nivel 6: Leyenda (2000+) ⭐

Cada nivel desbloquea:
- Avatares especiales
- Marcos de foto personalizados
- Acceso a recetas premium
- Badges exclusivos
```

#### **Badges y Logros**
```
Constancia:
🔥 "Racha de Fuego" - 7 días consecutivos registrando comidas
⚡ "Imparable" - 30 días consecutivos
💎 "Disciplina Diamante" - 90 días consecutivos

Salud:
🥗 "Come Verde" - 50 comidas saludables registradas
💧 "Hidratación Perfecta" - 7 días cumpliendo objetivo de agua
🏃 "Activo" - 20 sesiones de ejercicio

Social:
👨‍🍳 "Chef Comunitario" - 10 recetas compartidas con 5+ likes
🤝 "Mentor" - Ayudar a 5 personas nuevas
❤️ "Inspiración" - 100 likes en tus publicaciones

Especiales:
🎯 "Objetivo Cumplido" - Alcanzar peso meta
📸 "Fotógrafo Pro" - 100 fotos de comida compartidas
🌟 "All-Star" - Completar todos los badges de un mes
```

#### **Rachas (Streaks)**
```
Visual atractivo: 🔥 5 días

Rachas importantes:
- Registro diario: 🥗
- Ejercicio: 🏃
- Agua: 💧
- Cumplimiento de plan: ✅

Protección de racha:
- "Freeze" (1 vez al mes): Puedes fallar un día sin perder racha
```

### **Para Nutriólogos**

#### **Sistema de Reputación**
```
Puntos por:
- Paciente activo por 7 días: +50 pts
- Paciente alcanza objetivo: +100 pts
- Review positiva (5⭐): +75 pts
- Receta popular (50+ likes): +40 pts
- Certificación adicional completada: +200 pts

Niveles profesionales:
⭐ Nutriólogo Junior (0-500)
⭐⭐ Nutriólogo Certificado (501-1500)
⭐⭐⭐ Nutriólogo Experto (1501-3000)
⭐⭐⭐⭐ Nutriólogo Elite (3001-6000)
⭐⭐⭐⭐⭐ Nutriólogo Legend (6000+)
```

#### **Badges Profesionales**
```
🏆 "Top Motivador" - 90% pacientes activos
📈 "Resultados Comprobados" - 20 pacientes en objetivo
🌟 "5 Estrellas" - Rating promedio 4.8+
👥 "Comunidad Grande" - 50+ pacientes activos
📚 "Educador" - 50 artículos/tips publicados
```

---

## 🤝 Features Sociales - Comunidad Adictiva

### **1. Feed de Comunidad (Estilo Instagram)**

```
Posts pueden incluir:
- 📸 Fotos de comidas con descripción
- 📊 Progreso semanal (gráficos)
- 🎯 Logros desbloqueados
- 💪 Fotos de transformación (antes/después)
- 📝 Tips y reflexiones
- 🍽️ Recetas creadas

Interacciones:
- ❤️ Like
- 💬 Comentarios
- 🔗 Compartir (interno o redes externas)
- 🏆 Reacciones: 💪 👏 🔥 🙌

Privacidad:
- Público (toda la comunidad)
- Solo mi nutriólogo
- Privado
```

### **2. Grupos y Desafíos**

```
Tipos de grupos:
- 👥 Grupo de Nutriólogo (pacientes del mismo nutriólogo)
- 🎯 Grupos por Objetivo (pérdida peso, masa muscular, etc.)
- 🌎 Grupos Regionales
- 🏆 Grupos de Desafío

Desafíos semanales:
- "Semana Verde" - Solo comida plant-based
- "Hidratación Hero" - 3L agua diario
- "Sugar Detox" - 7 días sin azúcar añadida
- "10K Steps" - 10,000 pasos diarios

Premios de desafío:
- Badge exclusivo
- +200 XP bonus
- Aparición en hall of fame
- Descuentos en renovación premium
```

### **3. Leaderboards (Ranking)**

```
Rankings globales:
- 🏆 Top XP del mes
- 🔥 Mayor racha activa
- 📸 Fotos más populares
- 🥗 Más comidas saludables

Rankings por nutriólogo:
- Competencia sana entre pacientes del mismo nutriólogo
- Reward para top 3: Video felicitación del nutriólogo

Rankings de nutriólogos:
- Más pacientes activos
- Mejor rating promedio
- Más transformaciones exitosas
```

### **4. Compartir en Redes Sociales**

```
Integración con:
- Facebook: Compartir logros, fotos, progreso
- Instagram: Stories automáticas con progreso semanal
- Twitter: Tweets de logros
- WhatsApp: Compartir directamente con amigos

Plantillas atractivas:
- "¡Alcancé mi meta de peso! 🎯"
- "7 días seguidos cumpliendo mi plan 🔥"
- "Mi transformación en 30 días 💪"
- "Nueva receta favorita 🍽️"

Watermark opcional: "Powered by Nutrition Intelligence"
```

---

## 📱 Experiencia de Usuario - UI/UX Adictiva

### **Onboarding Mágico**

```
Paciente nuevo:
1. Splash screen animado (logo + tagline)
2. Welcome: "¡Bienvenido! Tu nutriólogo te ha invitado"
3. Cambio de contraseña obligatorio
4. Quiz personalización (5 preguntas):
   - ¿Cuál es tu objetivo principal?
   - ¿Qué te motiva más?
   - ¿Cuánto tiempo puedes dedicar diariamente?
   - ¿Tienes restricciones alimentarias?
   - ¿Prefieres notificaciones por la mañana o noche?
5. Tour interactivo (5 pasos)
6. Primera misión: "Registra tu primera comida"
```

### **Dashboard Intuitivo**

```
Vista Paciente:
┌─────────────────────────────────────┐
│ 👋 Hola Sara! Día 23 🔥             │
│ Nivel 4: Experto 🏆                 │
│ 850/1000 XP  [████████░░] ➜ Nivel 5│
├─────────────────────────────────────┤
│ 📊 HOY (Círculos de progreso)       │
│ Calorías: 1450/2000 kcal [73%] ✅  │
│ Agua: 2.1/3L [70%] 💧              │
│ Ejercicio: 30/45 min [67%] 🏃       │
├─────────────────────────────────────┤
│ 🎯 MIS OBJETIVOS                    │
│ Peso actual: 68 kg → Meta: 63 kg   │
│ Progreso: ████░░░░░ 5/10 kg (50%)  │
├─────────────────────────────────────┤
│ ⚡ ACCIONES RÁPIDAS                 │
│ [+ Registrar Comida] [📸 Foto]     │
│ [💧 Agua] [🏃 Ejercicio]            │
├─────────────────────────────────────┤
│ 🏆 DESAFÍO ACTIVO                   │
│ "Semana Verde" 🥗                   │
│ Día 3/7 - ¡Vas genial! 💪          │
├─────────────────────────────────────┤
│ 📣 FEED COMUNITARIO                 │
│ [Posts más recientes...]            │
└─────────────────────────────────────┘

Bottom Navigation:
🏠 Inicio | 🍽️ Comidas | 📊 Progreso | 👥 Comunidad | 👤 Perfil
```

### **Animaciones y Micro-interacciones**

```
Efectos que generan adicción:
- 🎉 Confetti cuando subes de nivel
- ⭐ Particles cuando desbloqueas badge
- 🔥 Llama que crece con racha
- 📈 Gráficas animadas (Chart.js / Victory Native)
- 💚 Corazón late cuando das like
- ✅ Checkmark animado al completar objetivo
- 🏆 Badge aparece con "shine" effect
```

### **Notificaciones Inteligentes**

```
Push notifications personalizadas:
Morning:
- "☀️ Buenos días! Registra tu desayuno" (8am)
- "💧 Momento de hidratarte" (10am)

Afternoon:
- "🍽️ ¿Ya registraste tu comida?" (2pm)
- "🏃 Hora de moverte un poco" (4pm)

Evening:
- "📊 Revisa tu progreso del día" (7pm)
- "🌙 Prepara tu cena saludable" (8pm)

Social:
- "❤️ @usuario le gustó tu foto"
- "💬 Tienes 3 comentarios nuevos"
- "🏆 ¡Subiste al top 10 del leaderboard!"
- "🎯 Tu nutriólogo actualizó tu plan"

Smart timing:
- Análisis de comportamiento: Aprende cuándo el usuario es más receptivo
- No molestar: Respeta horarios de sueño
- Frecuencia adaptativa: Reduce si el usuario las ignora
```

---

## 🔄 Sincronización Web ↔ Mobile

### **Arquitectura de Sincronización**

```typescript
// Shared API Client
class NutritionAPI {
  private token: string;
  private baseURL: string;

  // Auto-sync con WebSocket
  connectRealtime() {
    const ws = new WebSocket(`wss://${this.baseURL}/ws`);

    ws.on('meal_updated', (data) => {
      // Actualizar store local (Zustand)
      useMealStore.getState().updateMeal(data);
    });

    ws.on('badge_earned', (badge) => {
      // Mostrar notificación in-app
      showBadgeNotification(badge);
    });
  }

  // Offline-first con cola de sincronización
  async addMeal(mealData, options = { offline: true }) {
    if (isOffline() && options.offline) {
      // Guardar en cola local
      await offlineQueue.add('meal', mealData);
      // Sync cuando haya conexión
      return { id: tempId, synced: false };
    }

    return await this.post('/meals', mealData);
  }
}
```

### **Estado Compartido (Zustand)**

```typescript
// packages/shared/store/authStore.ts
import create from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const { user, token } = await api.login(email, password);
        set({ user, token, isAuthenticated: true });
      },

      logout: () => {
        api.logout();
        set({ user: null, token: null, isAuthenticated: false });
      },

      updateProfile: async (data) => {
        const updated = await api.updateProfile(data);
        set({ user: updated });
      }
    }),
    {
      name: 'auth-storage',
      // En mobile usa AsyncStorage, en web localStorage
      getStorage: () => (
        Platform.OS === 'web'
          ? localStorage
          : require('@react-native-async-storage/async-storage').default
      )
    }
  )
);
```

---

## 📅 Plan de Implementación - 12 Semanas

### **Fase 1: Fundación (Semanas 1-3)**

**Semana 1: Setup y Arquitectura**
- ✅ Crear monorepo con Nx/Turborepo
- ✅ Configurar packages/shared
- ✅ Setup React Native + Expo
- ✅ Migrar componentes web a compartidos
- ✅ Setup Zustand stores compartidos

**Semana 2: Backend - Auth System**
- ✅ Implementar JWT + Refresh Tokens
- ✅ Endpoints de registro (nutriólogo/paciente)
- ✅ Login con email/password
- ✅ Recuperación de contraseña (email con código)
- ✅ OAuth2: Google, Facebook
- ✅ Sistema de sesiones y dispositivos

**Semana 3: Mobile - Pantallas Auth**
- ✅ Splash Screen
- ✅ Onboarding (quiz + tour)
- ✅ Login screen
- ✅ Registro nutriólogo
- ✅ Recuperación contraseña
- ✅ Cambio de contraseña
- ✅ Biometría (Touch ID / Face ID)

### **Fase 2: Core Features (Semanas 4-6)**

**Semana 4: Dashboard y Navegación**
- ✅ Bottom Tab Navigation (mobile)
- ✅ Dashboard paciente (mobile + web sync)
- ✅ Dashboard nutriólogo
- ✅ Sidebar mejorado (web)
- ✅ Sincronización real-time (WebSocket)

**Semana 5: Gestión de Pacientes**
- ✅ CRUD pacientes (nutriólogo)
- ✅ Auto-creación de usuario paciente
- ✅ Envío de email de bienvenida
- ✅ Sistema de invitación con código
- ✅ Lista de pacientes con filtros
- ✅ Perfil detallado de paciente

**Semana 6: Tracking de Comidas**
- ✅ Registro de comida (mobile + web)
- ✅ Búsqueda de alimentos
- ✅ Cálculo de macros
- ✅ Foto de comida con upload
- ✅ Historial de comidas
- ✅ Gráficas de progreso

### **Fase 3: Gamificación (Semanas 7-8)**

**Semana 7: Sistema de Puntos y Niveles**
- ✅ Backend: Sistema XP
- ✅ Cálculo de nivel
- ✅ Triggers de puntos (comida, ejercicio, etc.)
- ✅ UI: Barra de progreso XP
- ✅ Animaciones de subida de nivel

**Semana 8: Badges y Achievements**
- ✅ Backend: Sistema de badges
- ✅ 30+ badges diferentes
- ✅ Detección automática de logros
- ✅ UI: Colección de badges
- ✅ Notificaciones de badge desbloqueado
- ✅ Rachas (streaks) visuales

### **Fase 4: Social (Semanas 9-10)**

**Semana 9: Feed Comunitario**
- ✅ Backend: Posts system
- ✅ CRUD posts (crear, editar, eliminar)
- ✅ Likes y comentarios
- ✅ Feed infinito con paginación
- ✅ Subida de imágenes optimizada
- ✅ UI: Feed estilo Instagram

**Semana 10: Desafíos y Leaderboards**
- ✅ Backend: Sistema de desafíos
- ✅ Inscripción a desafíos
- ✅ Tracking de progreso
- ✅ Leaderboards (global, por nutriólogo)
- ✅ Rankings en tiempo real
- ✅ UI: Pantallas de desafíos y rankings

### **Fase 5: Integración Social (Semana 11)**

**Semana 11: Compartir en Redes**
- ✅ Share API (mobile)
- ✅ Templates para compartir
- ✅ Facebook SDK integration
- ✅ Instagram Stories integration
- ✅ Twitter share
- ✅ WhatsApp direct share
- ✅ Generación de imágenes con progreso

### **Fase 6: Polish y Deploy (Semana 12)**

**Semana 12: Testing, Optimización y Release**
- ✅ Testing E2E (Detox mobile, Playwright web)
- ✅ Performance optimization
- ✅ Offline mode testing
- ✅ Push notifications setup (FCM)
- ✅ App Store setup (iOS)
- ✅ Google Play setup (Android)
- ✅ Web production deploy
- ✅ Documentación usuario final

---

## 💰 Modelo de Negocio

### **Planes de Suscripción**

#### Para Nutriólogos
```
🆓 FREE (Siempre gratis)
- 5 pacientes máximo
- Features básicos
- Sin badge profesional
- Anuncios en la app

💎 PRO ($29/mes o $290/año)
- Pacientes ilimitados
- Badge "Nutriólogo Certificado"
- Analytics avanzados
- Sin anuncios
- Prioridad en soporte
- Video consultas integradas

🏆 ELITE ($79/mes o $790/año)
- Todo de PRO +
- Badge "Nutriólogo Elite"
- IA para recomendaciones
- White-label (tu branding)
- API access
- Multi-usuario (equipo)
```

#### Para Pacientes
```
🆓 FREE (Siempre gratis)
- Todas las features básicas
- Tracking ilimitado
- Comunidad
- Gamificación básica

✨ PREMIUM ($9.99/mes o $79.99/año)
- Sin anuncios
- Badges exclusivos
- Recetas premium (500+)
- Análisis IA de fotos de comida
- Descarga de reportes PDF
- Gráficas avanzadas
- Challenges premium
```

### **Otros Ingresos**
```
- Marketplace de planes (nutriólogos venden planes)
- Comisión por referir nutriólogos (20%)
- Publicidad para marcas saludables
- API para clínicas y hospitales
```

---

## 🎨 Guía de Diseño Visual

### **Paleta de Colores**

```
Primarios:
- Verde Nutrición: #27AE60 (éxito, saludable)
- Azul Confianza: #3498DB (profesional, confiable)

Secundarios:
- Naranja Energía: #F39C12 (advertencia, motivación)
- Morado Premium: #9B59B6 (premium, especial)
- Rojo Alerta: #E74C3C (peligro, límite)

Neutros:
- Gris Oscuro: #2C3E50 (texto principal)
- Gris Medio: #7F8C8D (texto secundario)
- Gris Claro: #ECF0F1 (backgrounds)
- Blanco: #FFFFFF

Gamificación:
- Oro: #FFD700 (nivel alto, premium)
- Plata: #C0C0C0 (nivel medio)
- Bronce: #CD7F32 (nivel bajo)
```

### **Tipografía**

```
Primaria: Inter (San-serif moderna, legible)
- Headings: Inter Bold (700)
- Body: Inter Regular (400)
- Captions: Inter Medium (500)

Secundaria (números, stats): Roboto Mono
- Para datos numéricos: calorías, peso, etc.
```

### **Iconografía**

```
Sistema de íconos:
- Emoji nativos (universal, colorido)
- Lucide Icons / Feather (outline, simple)
- Custom icons para features únicos
```

---

## 🚀 Próximos Pasos Inmediatos

### **Lo que voy a hacer AHORA:**

1. ✅ **Crear estructura de monorepo**
2. ✅ **Setup backend mejorado con auth**
3. ✅ **Crear pantallas de login/registro (mobile)**
4. ✅ **Implementar recuperación de contraseña**
5. ✅ **Sistema de creación automática de pacientes**

### **¿Comenzamos?**

**Orden de implementación sugerido:**
```
1. Backend: Auth completo (JWT, recuperación, OAuth)
2. Mobile: Pantallas de auth + onboarding
3. Web: Mejorar pantallas de auth actuales
4. Backend: Sistema de pacientes con auto-registro
5. Mobile: Dashboard inicial
6. Gamificación básica (XP + niveles)
7. Social: Feed y posts
8. ...continuar con el roadmap
```

---

## 📝 Notas Importantes

- **Desarrollo iterativo:** Lanzar MVP en 4 semanas (auth + dashboard + tracking básico)
- **Testing continuo:** Con usuarios reales desde la semana 4
- **Feedback loop:** Ajustar gamificación según engagement real
- **Escalabilidad:** Arquitectura preparada para 10K+ usuarios concurrentes

---

**¿Estás listo para empezar? 🚀**

Propongo comenzar con:
1. **Backend Auth System** (Semana 1-2)
2. **Mobile Onboarding** (Semana 2-3)

Dime y empiezo a implementar! 💪
