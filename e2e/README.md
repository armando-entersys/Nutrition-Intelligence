# E2E Tests with Playwright

Pruebas end-to-end para Nutrition Intelligence Platform usando Playwright.

## Estructura

```
e2e/
├── tests/
│   ├── auth.spec.ts           # Tests de autenticación
│   ├── food-search.spec.ts    # Tests de búsqueda de alimentos
│   ├── product-scanner.spec.ts # Tests del escáner NOM-051
│   ├── ai-chat.spec.ts        # Tests del chat con IA
│   └── meal-plan.spec.ts      # Tests de planes de comida
├── fixtures/                  # Imágenes y datos de prueba
├── playwright.config.ts       # Configuración de Playwright
└── package.json
```

## Instalación

```bash
cd e2e
npm install
npx playwright install  # Instala navegadores
```

## Ejecutar Tests

### Todos los tests
```bash
npm test
```

### Con interfaz visual
```bash
npm run test:ui
```

### En modo headed (ver navegador)
```bash
npm run test:headed
```

### Solo un navegador
```bash
npm run test:chromium
npm run test:firefox
npm run test:webkit
```

### Tests móviles
```bash
npm run test:mobile
```

### Debug mode
```bash
npm run test:debug
```

### Test específico
```bash
npx playwright test auth.spec.ts
```

## Ver Reportes

```bash
npm run report
```

Abre un reporte HTML interactivo con:
- Resultados por test
- Screenshots de fallos
- Videos de ejecución
- Traces para debugging

## Generar Tests Automáticamente

```bash
npm run codegen
```

Esto abre el navegador y graba tus acciones para generar código de test.

## Tests Implementados

### 1. Authentication (auth.spec.ts)
- ✅ Registro de usuario
- ✅ Login
- ✅ Logout
- ✅ Recuperación de contraseña
- ✅ Validación de formularios
- ✅ Validación de password strength

### 2. Food Search (food-search.spec.ts)
- ✅ Búsqueda de alimentos
- ✅ Filtros por categoría SMAE
- ✅ Ver detalles nutricionales
- ✅ Búsqueda sin resultados
- ✅ Paginación
- ✅ Agregar a plan de comida
- ✅ Búsqueda de recetas
- ✅ Filtros de recetas

### 3. Product Scanner (product-scanner.spec.ts)
- ✅ Escaneo por código de barras
- ✅ Upload de imagen de producto
- ✅ Visualización de información NOM-051
- ✅ Sellos de advertencia
- ✅ Producto no encontrado
- ✅ Comparación de productos
- ✅ Historial de escaneos

### 4. AI Chat (ai-chat.spec.ts)
- ✅ Enviar y recibir mensajes
- ✅ Preguntas sobre nutrición
- ✅ Recomendaciones personalizadas
- ✅ Conversaciones largas
- ✅ Limpiar historial
- ✅ Manejo de errores
- ✅ Preguntas sugeridas
- ✅ Validación de mensajes vacíos

### 5. Meal Plans (meal-plan.spec.ts)
- ✅ Crear plan de comidas
- ✅ Agregar alimentos al plan
- ✅ Ver resumen nutricional
- ✅ Editar comidas
- ✅ Eliminar alimentos
- ✅ Copiar días
- ✅ Exportar a PDF
- ✅ Compartir con nutricionista
- ✅ Estado vacío

## Configuración

### Variables de Entorno

Crear archivo `.env` en `e2e/`:

```bash
BASE_URL=http://localhost:3000
TEST_USER_EMAIL=patient@example.com
TEST_USER_PASSWORD=password123
```

### Datos de Prueba

Los tests requieren:
- Usuario de prueba registrado
- Base de datos con alimentos SMAE
- Productos NOM-051 de ejemplo

## CI/CD

### GitHub Actions

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        working-directory: e2e
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        working-directory: e2e
        run: npm test

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: e2e/playwright-report/
```

## Best Practices

### 1. Use Test IDs
```tsx
<button data-testid="login-button">Login</button>
```

```typescript
await page.click('[data-testid="login-button"]');
```

### 2. Wait for Elements
```typescript
await expect(page.locator('[data-testid="result"]')).toBeVisible({ timeout: 10000 });
```

### 3. Independent Tests
Cada test debe ser independiente y poder ejecutarse en cualquier orden.

### 4. Clean Up
Tests deben limpiar los datos que crean.

### 5. Use Page Objects
Para tests complejos, usar Page Object Model:

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}
```

## Troubleshooting

### Tests fallan en CI pero pasan local

- Verificar timeouts (CI es más lento)
- Revisar variables de entorno
- Verificar que navegadores estén instalados

### Screenshots negros

- Aumentar timeout antes del screenshot
- Usar `await page.waitForLoadState('networkidle')`

### Tests intermitentes

- Agregar esperas explícitas
- No usar `page.waitForTimeout()` (usar condiciones)
- Verificar estado de la aplicación antes de actuar

## Recursos

- [Playwright Docs](https://playwright.dev/docs/intro)
- [Test Generator](https://playwright.dev/docs/codegen)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [Best Practices](https://playwright.dev/docs/best-practices)
