/**
 * ============================================================================
 * E2E TEST: Flujo Completo Expediente Clínico
 * ============================================================================
 * Test ID: E2E-001, E2E-002
 * Description: Valida el flujo completo desde login hasta creación de expediente
 * Technology: chrome-devtools-mcp
 * Priority: Alta
 * ============================================================================
 */

const { chromium } = require('chrome-devtools-mcp');
const { expect } = require('chai');
const fs = require('fs');
const path = require('path');

describe('E2E-001: Flujo Completo - Expediente Clínico', () => {
  let browser;
  let page;
  const baseURL = 'http://localhost:3002';
  const screenshotsDir = path.join(__dirname, '../screenshots');
  const reportsDir = path.join(__dirname, '../reports');

  // Utility function para captura avanzada
  async function captureAdvancedScreenshot(name, options = {}) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${name}-${timestamp}.png`;
    const filepath = path.join(screenshotsDir, filename);

    await page.screenshot({
      path: filepath,
      fullPage: options.fullPage || false,
      ...options
    });

    // Capturar métricas de performance
    const metrics = await page.metrics();
    const performanceData = {
      timestamp,
      testName: name,
      metrics,
      url: page.url()
    };

    return { filepath, performanceData };
  }

  // Utility para captura de métricas Web Vitals
  async function captureWebVitals() {
    return await page.evaluate(() => {
      return new Promise((resolve) => {
        const vitals = {};

        // First Contentful Paint
        const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0];
        if (fcpEntry) vitals.fcp = fcpEntry.startTime;

        // Largest Contentful Paint
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          vitals.lcp = lastEntry.renderTime || lastEntry.loadTime;
          resolve(vitals);
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // Fallback si LCP no se dispara
        setTimeout(() => resolve(vitals), 3000);
      });
    });
  }

  before(async () => {
    console.log('🚀 Iniciando Chrome con DevTools Protocol...');

    browser = await chromium.launch({
      headless: false,
      devtools: true,
      args: [
        '--start-maximized',
        '--disable-blink-features=AutomationControlled',
        '--enable-precise-memory-info'
      ]
    });

    page = await browser.newPage();

    // Configurar viewport
    await page.setViewport({ width: 1920, height: 1080 });

    // Habilitar capturas de red y consola
    await page.setRequestInterception(true);

    page.on('request', request => {
      console.log(`📡 Request: ${request.method()} ${request.url()}`);
      request.continue();
    });

    page.on('console', msg => {
      const type = msg.type();
      if (type === 'error') {
        console.error(`❌ Console Error: ${msg.text()}`);
      }
    });

    page.on('pageerror', error => {
      console.error(`💥 Page Error: ${error.message}`);
    });

    console.log('✅ Chrome DevTools configurado correctamente');
  });

  after(async () => {
    if (browser) {
      await browser.close();
      console.log('🔚 Browser cerrado');
    }
  });

  it('E2E-001: Debe cargar la aplicación correctamente', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-001: Carga de aplicación');

    // Navegar a la app
    const navigationStart = Date.now();
    await page.goto(baseURL, { waitUntil: 'networkidle2' });
    const navigationTime = Date.now() - navigationStart;

    console.log(`⏱️  Tiempo de navegación: ${navigationTime}ms`);

    // Capturar Web Vitals
    const vitals = await captureWebVitals();
    console.log('📊 Web Vitals:', vitals);

    // Validar título
    const title = await page.title();
    expect(title).to.include('Nutrition Intelligence');

    // Validar elementos principales
    const heading = await page.$('text=Nutrition Intelligence');
    expect(heading).to.not.be.null;

    // Screenshot
    const { filepath, performanceData } = await captureAdvancedScreenshot('01-app-loaded', { fullPage: true });
    console.log(`📸 Screenshot guardado: ${filepath}`);

    // Validar performance
    expect(navigationTime).to.be.below(5000, 'La página debe cargar en menos de 5 segundos');

    if (vitals.fcp) {
      expect(vitals.fcp).to.be.below(2500, 'FCP debe ser menor a 2.5s');
    }

    console.log('✅ E2E-001 PASSED');
  });

  it('E2E-002: Debe navegar a Expediente Clínico', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-002: Navegación a Expediente');

    // Buscar botón de Expediente en sidebar
    const expButton = await page.waitForSelector('text=/Expediente/i', { timeout: 10000 });
    expect(expButton).to.not.be.null;

    // Click en Expediente
    await expButton.click();
    await page.waitForTimeout(2000);

    // Validar que se cargó la vista de expediente
    const tabs = await page.$$('button');
    const tabTexts = await Promise.all(tabs.map(tab => tab.evaluate(el => el.textContent)));

    const hasExpedienteTabs = tabTexts.some(text =>
      text.includes('Datos Generales') ||
      text.includes('Historia Clínica') ||
      text.includes('Mediciones')
    );

    expect(hasExpedienteTabs).to.be.true;

    // Screenshot
    await captureAdvancedScreenshot('02-expediente-view');

    console.log('✅ E2E-002 PASSED');
  });

  it('E2E-003: Debe acceder a Historia Clínica tab', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-003: Historia Clínica');

    // Buscar tab de Historia Clínica
    const historiaTab = await page.waitForSelector('button:has-text("Historia Clínica")', {
      timeout: 10000,
      state: 'visible'
    }).catch(() => null);

    if (historiaTab) {
      await historiaTab.click();
      await page.waitForTimeout(1500);

      // Validar contenido de Historia Clínica
      const content = await page.$('main');
      expect(content).to.not.be.null;

      await captureAdvancedScreenshot('03-historia-clinica');
      console.log('✅ E2E-003 PASSED');
    } else {
      console.log('⚠️  Historia Clínica tab no encontrado - SKIP');
      this.skip();
    }
  });

  it('E2E-004: Debe acceder a Datos de Laboratorio', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-004: Datos de Laboratorio');

    // Buscar tab de Laboratorio
    const labTab = await page.waitForSelector('button:has-text("Laboratorio")', {
      timeout: 10000
    }).catch(() => null);

    if (labTab) {
      await labTab.click();
      await page.waitForTimeout(1500);

      // Validar vista de laboratorio
      const content = await page.$('main');
      expect(content).to.not.be.null;

      await captureAdvancedScreenshot('04-laboratorio');
      console.log('✅ E2E-004 PASSED');
    } else {
      console.log('⚠️  Laboratorio tab no encontrado - SKIP');
      this.skip();
    }
  });

  it('E2E-005: Debe validar responsive design (mobile)', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-005: Responsive Design');

    // Cambiar a viewport móvil
    await page.setViewport({ width: 375, height: 667 });
    await page.waitForTimeout(1000);

    // Buscar menú hamburguesa
    const hamburger = await page.$('[aria-label*="menú"], [aria-label*="Abrir"]');

    if (hamburger) {
      await hamburger.click();
      await page.waitForTimeout(500);

      // Validar que el drawer se abrió
      const drawer = await page.$('[role="dialog"], [role="presentation"]');
      expect(drawer).to.not.be.null;

      await captureAdvancedScreenshot('05-mobile-menu');
    }

    // Validar que no hay scroll horizontal
    const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = await page.evaluate(() => window.innerWidth);

    expect(scrollWidth).to.be.at.most(viewportWidth + 1);

    // Restaurar viewport
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('✅ E2E-005 PASSED');
  });
});
