# Marketing Implementation Guide

Esta guía te ayudará a implementar la landing page y crear el video demo.

## Parte 1: Landing Page Implementation

### Opción A: Landing Page Separada (Recomendado)

Crear una landing page estática independiente para máximo performance y SEO.

#### Stack Recomendado
- **Framework**: Next.js (static export) o Astro
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Forms**: React Hook Form
- **Analytics**: Google Analytics 4
- **Hosting**: Vercel (gratis)

#### Estructura de Archivos
```
landing/
├── pages/
│   ├── index.tsx          # Home
│   ├── features.tsx       # Características detalladas
│   ├── pricing.tsx        # Planes
│   ├── for-professionals.tsx
│   └── blog/              # Blog posts para SEO
├── components/
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── HowItWorks.tsx
│   ├── Testimonials.tsx
│   ├── Pricing.tsx
│   ├── FAQ.tsx
│   └── CTA.tsx
├── public/
│   ├── images/
│   ├── videos/
│   └── demo.mp4
└── styles/
    └── globals.css
```

#### Quick Start
```bash
# Crear proyecto Next.js
npx create-next-app@latest landing --typescript --tailwind

cd landing

# Instalar dependencias
npm install framer-motion react-hook-form @headlessui/react

# Configurar para static export
# En next.config.js:
module.exports = {
  output: 'export',
  images: {
    unoptimized: true
  }
}
```

### Opción B: Integrar en Frontend Existente

Agregar ruta `/landing` o `/` en el frontend actual.

```typescript
// frontend/src/pages/index.tsx
import Hero from '@/components/landing/Hero'
import Features from '@/components/landing/Features'
// ... otros componentes

export default function LandingPage() {
  return (
    <>
      <Hero />
      <Features />
      <HowItWorks />
      <Testimonials />
      <Pricing />
      <FAQ />
      <CTASection />
    </>
  )
}
```

---

## Parte 2: Components Implementation

### Hero Component Example

```typescript
// components/Hero.tsx
import { motion } from 'framer-motion'
import { initGA, trackSignup } from '@/utils/analytics'

export default function Hero() {
  const handleCTA = () => {
    trackSignup('landing_hero')
    window.location.href = '/register'
  }

  return (
    <section className="relative min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Tu Nutricionista
              <span className="text-green-600"> Inteligente</span>
              <br />en México
            </h1>

            <p className="text-xl text-gray-600 mb-8">
              Escanea productos, crea planes de alimentación personalizados
              y consulta con IA. Todo basado en estándares mexicanos NOM-051 y SMAE.
            </p>

            <div className="flex gap-4">
              <button
                onClick={handleCTA}
                className="px-8 py-4 bg-green-600 text-white rounded-lg
                         hover:bg-green-700 transition font-semibold text-lg"
              >
                Empezar Gratis
              </button>

              <button
                className="px-8 py-4 border-2 border-green-600 text-green-600
                         rounded-lg hover:bg-green-50 transition font-semibold text-lg"
              >
                Ver Demo
              </button>
            </div>

            {/* Trust Indicators */}
            <div className="mt-8 flex gap-6 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-600">...</svg>
                <span>Gratis para siempre</span>
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-600">...</svg>
                <span>Sin tarjeta de crédito</span>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Hero Image/Animation */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="relative">
              {/* Mockup de la app aquí */}
              <img
                src="/images/hero-mockup.png"
                alt="App Screenshot"
                className="w-full h-auto"
              />

              {/* Elementos flotantes animados */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute top-10 -right-10"
              >
                <div className="bg-white rounded-lg shadow-xl p-4">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-red-500 rounded-full" />
                    <span className="font-semibold">Exceso Azúcares</span>
                  </div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
```

### Features Grid Component

```typescript
// components/Features.tsx
const features = [
  {
    icon: '🔍',
    title: 'Escáner Inteligente NOM-051',
    description: 'Escanea cualquier producto en segundos',
    points: [
      'Lee códigos de barras automáticamente',
      'Analiza sellos de advertencia',
      'Compara con alternativas saludables'
    ]
  },
  // ... más features
]

export default function Features() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">
          Todo lo que necesitas para mejorar tu nutrición
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-600 mb-4">{feature.description}</p>
              <ul className="space-y-2">
                {feature.points.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <svg className="w-5 h-5 text-green-600 flex-shrink-0">...</svg>
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## Parte 3: Video Demo Creation

### Herramientas Necesarias

#### Screen Recording
- **OBS Studio** (Gratis): Para grabar pantalla
- **Loom** (Gratis/Paid): Grabación rápida con edición básica
- **Camtasia** (Pago): Profesional con editing integrado

#### Video Editing
- **DaVinci Resolve** (Gratis): Professional grade
- **Adobe Premiere** (Pago): Industry standard
- **CapCut** (Gratis): Fácil para principiantes

#### Audio
- **Audacity** (Gratis): Edición de audio
- **Fiverr**: Contratar voiceover profesional ($50-100)

### Paso a Paso

#### 1. Preparación (1 hora)
```bash
# Preparar datos de prueba
- Crear usuario demo
- Agregar alimentos al plan
- Tener productos listos para escanear
- Preparar preguntas para IA
- Screenshots de alta calidad
```

#### 2. Grabación (2 horas)
```
OBS Studio Settings:
- Resolution: 1920x1080
- FPS: 60 (para animaciones suaves)
- Format: MP4
- Codec: H.264

Scenes a grabar:
1. Home/Dashboard
2. Escaneo de producto (Coca-Cola)
3. Comparación de productos
4. Chat con IA (3-4 preguntas)
5. Crear plan de comidas
6. Ver plan semanal
7. Dashboard de progreso
8. Exportar PDF
```

#### 3. Edición (3-4 horas)
```
DaVinci Resolve Timeline:
- Import todos los clips
- Cortar partes lentas
- Agregar text overlays
- Sincronizar con narración
- Agregar música de fondo
- Color grading básico
- Render 1080p 30fps
```

#### 4. Exportación
```
Settings:
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Frame Rate: 30fps
- Bitrate: 10 Mbps (buena calidad, tamaño razonable)
- Audio: AAC 320kbps
```

---

## Parte 4: Screenshots & Assets

### Screenshots Necesarios

```bash
screenshots/
├── hero-mockup.png         # iPhone con app abierta
├── scanner-demo.png        # Escaneo de producto
├── chat-demo.png           # Chat con IA
├── meal-plan-demo.png      # Plan semanal
├── dashboard-demo.png      # Dashboard de progreso
├── comparison-demo.png     # Comparación de productos
└── mobile/
    ├── ios-scanner.png
    └── android-scanner.png
```

### Crear Mockups Profesionales

**Herramientas Gratis:**
- **Screely**: screely.com (Browser mockups)
- **Mockuphone**: mockuphone.com (Mobile mockups)
- **Smartmockups**: smartmockups.com (Multi-device)

**Proceso:**
1. Capturar screenshots limpias de la app
2. Subir a herramienta de mockups
3. Seleccionar device (iPhone 14, MacBook, etc.)
4. Descargar PNG de alta resolución

---

## Parte 5: Hosting & Deployment

### Landing Page Hosting

#### Opción 1: Vercel (Recomendado)
```bash
# Deploy automático con GitHub
npm install -g vercel
vercel login
vercel --prod

# Configurar dominio custom
vercel domains add nutrition-intelligence.com
```

#### Opción 2: Netlify
```bash
# Similar a Vercel
npm install -g netlify-cli
netlify deploy --prod
```

### Video Hosting

#### YouTube (Recomendado)
- Gratis, ilimitado
- SEO benefits
- Analytics incluidos
- Embed fácil

```html
<!-- Embed en landing page -->
<iframe
  width="100%"
  height="600"
  src="https://www.youtube.com/embed/VIDEO_ID"
  frameborder="0"
  allow="accelerometer; autoplay; encrypted-media"
  allowfullscreen
></iframe>
```

#### Alternativas
- **Vimeo**: Más profesional, sin ads
- **Wistia**: Analytics avanzados (pago)
- **Self-hosted**: Usar Mux o Cloudflare Stream

---

## Parte 6: SEO & Performance

### Optimización

```typescript
// pages/_app.tsx - Meta tags
import Head from 'next/head'

export default function LandingApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Nutrition Intelligence - Tu Nutricionista con IA</title>
        <meta name="description" content="Plataforma de nutrición inteligente..." />

        {/* Open Graph */}
        <meta property="og:image" content="/og-image.jpg" />
        <meta property="og:title" content="Nutrition Intelligence" />

        {/* Structured Data */}
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Nutrition Intelligence",
            // ... resto del schema
          })}
        </script>
      </Head>

      <Component {...pageProps} />
    </>
  )
}
```

### Performance Checklist
- [ ] Lazy load images
- [ ] Optimize images (WebP format)
- [ ] Minify CSS/JS
- [ ] Enable compression
- [ ] Use CDN
- [ ] Preload critical resources
- [ ] Defer non-critical JS

---

## Parte 7: Launch Checklist

### Pre-Launch
- [ ] Landing page diseñada
- [ ] Video demo grabado y editado
- [ ] Screenshots profesionales
- [ ] Copy revisado (ortografía, gramática)
- [ ] Forms funcionando
- [ ] Analytics configurado
- [ ] SEO optimizado
- [ ] Mobile responsive
- [ ] Performance >90 (Lighthouse)

### Launch Day
- [ ] Deploy a producción
- [ ] DNS configurado
- [ ] SSL certificate
- [ ] Google Search Console submitted
- [ ] Social media posts
- [ ] Email announcement
- [ ] Press release (opcional)

### Post-Launch
- [ ] Monitor analytics diariamente
- [ ] A/B test CTAs
- [ ] Collect user feedback
- [ ] Iterate based on data

---

## Recursos Adicionales

### Design Inspiration
- https://land-book.com/
- https://www.landingfolio.com/
- https://saaslandingpage.com/

### Stock Images
- https://unsplash.com/
- https://www.pexels.com/
- https://pixabay.com/

### Icons
- https://heroicons.com/
- https://fontawesome.com/
- https://www.flaticon.com/

### Colors & Fonts
- https://coolors.co/
- https://fonts.google.com/

### Video Tutorials
- "How to create a landing page" - YouTube
- "Screen recording with OBS" - YouTube
- "DaVinci Resolve basics" - YouTube
