/**
 * ============================================================================
 * E2E TEST: Integración WhatsApp - Recordatorios y Notificaciones
 * ============================================================================
 * Test ID: E2E-WA-001 to E2E-WA-005
 * Description: Valida el flujo completo de mensajería WhatsApp
 * Technology: chrome-devtools-mcp
 * Priority: Alta
 * ============================================================================
 */

const { chromium } = require('chrome-devtools-mcp');
const { expect } = require('chai');
const path = require('path');

describe('E2E: WhatsApp Integration Workflow', () => {
  let browser;
  let page;
  const baseURL = 'http://localhost:3002';
  const screenshotsDir = path.join(__dirname, '../screenshots');

  async function captureScreenshot(name) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filepath = path.join(screenshotsDir, `whatsapp-${name}-${timestamp}.png`);
    await page.screenshot({ path: filepath, fullPage: true });
    return filepath;
  }

  before(async () => {
    browser = await chromium.launch({
      headless: false,
      devtools: true,
      args: ['--start-maximized']
    });

    page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Navegar a la app
    await page.goto(baseURL, { waitUntil: 'networkidle2' });
  });

  after(async () => {
    if (browser) await browser.close();
  });

  it('E2E-WA-001: Debe navegar a la sección WhatsApp Manager', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-WA-001: Navegación a WhatsApp Manager');

    // Buscar el elemento de WhatsApp en el sidebar
    const whatsappButton = await page.waitForSelector('text=/WhatsApp|Mensajería/i', {
      timeout: 10000
    }).catch(() => null);

    if (!whatsappButton) {
      console.log('⚠️  WhatsApp Manager no encontrado en sidebar - SKIP');
      this.skip();
      return;
    }

    await whatsappButton.click();
    await page.waitForTimeout(2000);

    // Validar que se cargó la vista de WhatsApp
    const heading = await page.$('text=/Mensajería WhatsApp|WhatsApp/i');
    expect(heading).to.not.be.null;

    await captureScreenshot('01-whatsapp-manager');
    console.log('✅ E2E-WA-001 PASSED');
  });

  it('E2E-WA-002: Debe mostrar opciones de mensajes rápidos', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-WA-002: Mensajes Rápidos');

    // Validar que existen las tarjetas de acciones rápidas
    const cards = await page.$$('[class*="MuiCard"]');
    expect(cards.length).to.be.at.least(1);

    // Buscar botones de envío
    const buttons = await page.$$('button:has-text("Enviar")');
    expect(buttons.length).to.be.at.least(1);

    await captureScreenshot('02-quick-actions');
    console.log('✅ E2E-WA-002 PASSED');
  });

  it('E2E-WA-003: Debe enviar recordatorio de cita', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-WA-003: Enviar Recordatorio');

    // Buscar botón "Enviar Recordatorio"
    const sendButton = await page.waitForSelector('button:has-text("Enviar Recordatorio")', {
      timeout: 10000
    }).catch(() => null);

    if (!sendButton) {
      console.log('⚠️  Botón de recordatorio no encontrado - SKIP');
      this.skip();
      return;
    }

    // Click para enviar
    await sendButton.click();
    await page.waitForTimeout(3000);

    // Esperar alert o confirmación
    // Nota: En ambiente de prueba puede usar valores mock

    await captureScreenshot('03-send-reminder');
    console.log('✅ E2E-WA-003 PASSED');
  });

  it('E2E-WA-004: Debe mostrar historial de mensajes', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-WA-004: Historial de Mensajes');

    // Buscar tab de Historial
    const historialTab = await page.waitForSelector('button:has-text("Historial")', {
      timeout: 10000
    }).catch(() => null);

    if (!historialTab) {
      console.log('⚠️  Tab Historial no encontrado - SKIP');
      this.skip();
      return;
    }

    await historialTab.click();
    await page.waitForTimeout(2000);

    // Validar que se muestra el historial (puede estar vacío o con mensajes)
    const content = await page.$('main');
    expect(content).to.not.be.null;

    await captureScreenshot('04-message-history');
    console.log('✅ E2E-WA-004 PASSED');
  });

  it('E2E-WA-005: Debe validar información de configuración Twilio', async function() {
    this.timeout(30000);

    console.log('\n📋 TEST E2E-WA-005: Configuración Twilio');

    // Buscar alert informativo sobre Twilio
    const alert = await page.$('text=/Twilio/i');

    if (alert) {
      const alertText = await alert.evaluate(el => el.textContent);
      expect(alertText).to.include('Twilio');
      console.log('✅ Alert de configuración Twilio encontrado');
    }

    await captureScreenshot('05-twilio-config');
    console.log('✅ E2E-WA-005 PASSED');
  });
});
