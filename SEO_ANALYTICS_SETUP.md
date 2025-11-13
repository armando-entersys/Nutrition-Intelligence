# SEO & Analytics Setup Guide

## Google Analytics 4 Setup

### 1. Create Google Analytics Property

1. Ir a [Google Analytics](https://analytics.google.com/)
2. Crear nueva propiedad
3. Configurar:
   - Nombre: "Nutrition Intelligence"
   - Zona horaria: "America/Mexico_City"
   - Moneda: "MXN"
4. Copiar el **Measurement ID** (formato: G-XXXXXXXXXX)

### 2. Configurar en Frontend

Agregar al archivo `.env.local`:

```bash
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### 3. Uso en la Aplicación

El archivo `frontend/src/utils/analytics.ts` ya está configurado con funciones para tracking:

```typescript
import { initGA, pageview, event, trackLogin, trackSearch } from '@/utils/analytics';

// Inicializar en _app.tsx
useEffect(() => {
  initGA();
}, []);

// Track page views en cambios de ruta
useEffect(() => {
  pageview(router.pathname);
}, [router.pathname]);

// Track eventos personalizados
trackLogin('email');
trackSearch('pollo', 'foods');
trackProductScan(true);
trackAIChat(5);
```

### 4. Eventos Pre-configurados

#### Autenticación
- `trackSignup(method)` - Usuario se registra
- `trackLogin(method)` - Usuario inicia sesión
- `trackLogout()` - Usuario cierra sesión

#### Búsquedas
- `trackSearch(term, category)` - Usuario busca alimentos/recetas

#### Features
- `trackProductScan(success)` - Escaneo de productos NOM-051
- `trackAIChat(messageCount)` - Interacciones con AI nutritionist
- `trackMealPlanCreate(days)` - Creación de planes de alimentación

#### Content
- `trackRecipeView(id, name)` - Ver receta
- `trackError(error)` - Errores en la aplicación

### 5. Métricas Clave a Monitorear

#### Engagement
- Usuarios activos diarios/semanales
- Sesiones por usuario
- Duración de sesión
- Tasa de rebote por página

#### Features Usage
- Escaneos de productos exitosos
- Mensajes de AI chat por sesión
- Planes de comida creados
- Recetas vistas

#### Conversión
- Registro de usuarios
- Activación (primera acción importante)
- Retención (usuarios que regresan)

## SEO Optimization

### 1. Robots.txt

Archivo: `frontend/public/robots.txt`

```txt
User-agent: *
Allow: /
Allow: /recipes
Allow: /foods

Disallow: /dashboard
Disallow: /admin
Disallow: /api/

Sitemap: https://nutrition-intelligence.com/sitemap.xml
```

### 2. Sitemap.xml

Archivo: `frontend/public/sitemap.xml`

Actualizar fechas y agregar nuevas páginas según se creen.

### 3. Meta Tags en Páginas

Agregar en cada página del frontend:

```tsx
import Head from 'next/head';

<Head>
  <title>Nutrition Intelligence - Tu nutricionista con IA</title>
  <meta name="description" content="Plataforma de nutrición inteligente con IA. Escanea productos, crea planes de comida y consulta con nutricionistas virtuales." />

  {/* Open Graph / Facebook */}
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://nutrition-intelligence.com/" />
  <meta property="og:title" content="Nutrition Intelligence - Tu nutricionista con IA" />
  <meta property="og:description" content="Plataforma de nutrición inteligente con IA" />
  <meta property="og:image" content="https://nutrition-intelligence.com/og-image.jpg" />

  {/* Twitter */}
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://nutrition-intelligence.com/" />
  <meta property="twitter:title" content="Nutrition Intelligence" />
  <meta property="twitter:description" content="Plataforma de nutrición inteligente con IA" />
  <meta property="twitter:image" content="https://nutrition-intelligence.com/og-image.jpg" />

  {/* Additional SEO */}
  <meta name="keywords" content="nutrición, IA, dieta, México, NOM-051, SMAE, nutricionista virtual" />
  <meta name="author" content="Nutrition Intelligence" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" content="https://nutrition-intelligence.com/" />
</Head>
```

### 4. Structured Data (Schema.org)

Agregar JSON-LD para ayudar a Google:

```tsx
<Head>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{
      __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Nutrition Intelligence",
        "description": "Plataforma de nutrición inteligente con IA",
        "url": "https://nutrition-intelligence.com",
        "applicationCategory": "HealthApplication",
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "MXN"
        },
        "featureList": [
          "Escaneo de productos NOM-051",
          "Planes de alimentación personalizados",
          "Chat con nutricionista virtual",
          "Base de datos SMAE"
        ]
      })
    }}
  />
</Head>
```

### 5. Optimización de Imágenes

```tsx
import Image from 'next/image';

<Image
  src="/images/food.jpg"
  alt="Descripción detallada del alimento"
  width={600}
  height={400}
  loading="lazy"
  quality={85}
/>
```

### 6. Performance

#### Next.js Config Optimizations

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['nutrition-intelligence.com'],
    formats: ['image/webp', 'image/avif'],
  },
  compress: true,
  swcMinify: true,
  reactStrictMode: true,

  // Generate static pages for SEO
  experimental: {
    optimizeCss: true,
  },
};
```

### 7. Google Search Console

1. Verificar propiedad en [Search Console](https://search.google.com/search-console)
2. Subir sitemap.xml
3. Monitorear:
   - Errores de rastreo
   - Cobertura del índice
   - Rendimiento de búsqueda
   - Core Web Vitals

### 8. Lighthouse Score

Objetivos:
- **Performance**: >90
- **Accessibility**: >95
- **Best Practices**: >95
- **SEO**: 100

```bash
# Ejecutar Lighthouse
npm run build
npm run start
lighthouse http://localhost:3000 --view
```

## Content Strategy

### 1. Blog Posts (SEO-Optimized)

Crear contenido sobre:
- "Cómo leer etiquetas NOM-051"
- "Guía SMAE: Sistema Mexicano de Alimentos Equivalentes"
- "10 recetas saludables mexicanas"
- "Nutrición con IA: El futuro de la alimentación"

### 2. Landing Pages

Crear páginas específicas:
- `/para-nutricionistas` - SEO: "software para nutricionistas México"
- `/para-pacientes` - SEO: "app de nutrición México"
- `/escanear-productos` - SEO: "escanear etiquetas NOM-051"
- `/chat-nutricionista` - SEO: "nutricionista virtual IA"

### 3. Keywords Research

Keywords principales:
- "nutricionista virtual" (1,200 búsquedas/mes)
- "app nutrición México" (800 búsquedas/mes)
- "NOM-051 escáner" (600 búsquedas/mes)
- "dieta personalizada" (2,400 búsquedas/mes)
- "SMAE alimentos" (400 búsquedas/mes)

## Monitoring Dashboard

### Google Analytics Reports

1. **Realtime** - Usuarios activos ahora
2. **Acquisition** - De dónde vienen los usuarios
3. **Engagement** - Qué hacen en el sitio
4. **Monetization** - Conversiones (registros, planes premium)
5. **Retention** - Usuarios que regresan

### Custom Reports

Crear informes para:
- Feature adoption (escaneos, chats AI, planes)
- User journey (desde landing hasta conversión)
- Content performance (recetas más vistas)
- Error tracking (errores reportados)

## Integración con Backend

Configurar eventos de servidor en backend:

```python
# backend/core/analytics.py
import httpx
from core.config import get_settings

async def track_server_event(event_name: str, user_id: str, properties: dict):
    """Track server-side events to Google Analytics"""
    settings = get_settings()

    if not settings.ga_measurement_id or not settings.ga_api_secret:
        return

    url = f"https://www.google-analytics.com/mp/collect"
    params = {
        "measurement_id": settings.ga_measurement_id,
        "api_secret": settings.ga_api_secret,
    }

    payload = {
        "client_id": user_id,
        "events": [{
            "name": event_name,
            "params": properties
        }]
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, params=params, json=payload)
```

## Checklist de Lanzamiento

### Pre-Lanzamiento
- [ ] Google Analytics configurado
- [ ] robots.txt actualizado
- [ ] sitemap.xml creado
- [ ] Meta tags en todas las páginas
- [ ] Structured data agregado
- [ ] Lighthouse score >90
- [ ] Search Console verificado

### Post-Lanzamiento
- [ ] Monitorear métricas diarias
- [ ] Ajustar tracking según comportamiento
- [ ] Crear informes semanales
- [ ] A/B testing de landing pages
- [ ] Optimizar keywords según rendimiento

## Referencias

- [Google Analytics 4 Docs](https://developers.google.com/analytics/devguides/collection/ga4)
- [Next.js SEO Guide](https://nextjs.org/learn/seo/introduction-to-seo)
- [Schema.org Markup](https://schema.org/)
- [Google Search Console](https://search.google.com/search-console/about)
