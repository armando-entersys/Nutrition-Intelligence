/**
 * Diagnostic Test: Inspect the actual page structure
 * This will help identify the correct selectors for form fields
 */

const { chromium } = require('playwright');
const fs = require('fs');

const BASE_URL = 'https://nutrition-intelligence.scram2k.com';

async function diagnosticTest() {
  console.log('╔══════════════════════════════════════════╗');
  console.log('║   PRUEBA DIAGNÓSTICA - INSPECCIÓN HTML  ║');
  console.log('║   Nutrition Intelligence Platform        ║');
  console.log('╚══════════════════════════════════════════╝\n');

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  // Log all console messages from the browser
  page.on('console', msg => {
    console.log(`   🖥️  BROWSER LOG [${msg.type()}]:`, msg.text());
  });

  // Log all network requests
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/api/v1/') || url.includes('nutrition-intelligence')) {
      console.log(`   → ${request.method()} ${url}`);
    }
  });

  // Log responses
  page.on('response', response => {
    const url = response.url();
    if (url.includes('/api/v1/')) {
      console.log(`   ← ${response.status()} ${url}`);
    }
  });

  try {
    console.log('========================================');
    console.log('1. NAVEGANDO A LA PÁGINA');
    console.log('========================================\n');

    await page.goto(BASE_URL, {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    console.log('✅ Página cargada\n');
    console.log('URL actual:', page.url());
    console.log('Título:', await page.title());

    // Take screenshot of initial page
    await page.screenshot({ path: './screenshots/01_initial_page.png', fullPage: true });
    console.log('📸 Screenshot guardado: ./screenshots/01_initial_page.png\n');

    console.log('========================================');
    console.log('2. INSPECCIONANDO ESTRUCTURA HTML');
    console.log('========================================\n');

    // Get all input fields
    const inputs = await page.$$('input');
    console.log(`Encontrados ${inputs.length} campos <input>\n`);

    for (let i = 0; i < inputs.length; i++) {
      const input = inputs[i];
      const type = await input.getAttribute('type');
      const name = await input.getAttribute('name');
      const id = await input.getAttribute('id');
      const placeholder = await input.getAttribute('placeholder');
      const className = await input.getAttribute('class');

      console.log(`Input ${i + 1}:`);
      console.log(`  - type: ${type}`);
      console.log(`  - name: ${name}`);
      console.log(`  - id: ${id}`);
      console.log(`  - placeholder: ${placeholder}`);
      console.log(`  - class: ${className ? className.substring(0, 50) + '...' : 'none'}`);
      console.log('');
    }

    // Get all buttons
    const buttons = await page.$$('button');
    console.log(`\nEncontrados ${buttons.length} botones <button>\n`);

    for (let i = 0; i < buttons.length; i++) {
      const button = buttons[i];
      const type = await button.getAttribute('type');
      const text = await button.textContent();
      const className = await button.getAttribute('class');

      console.log(`Button ${i + 1}:`);
      console.log(`  - type: ${type}`);
      console.log(`  - text: ${text?.trim()}`);
      console.log(`  - class: ${className ? className.substring(0, 50) + '...' : 'none'}`);
      console.log('');
    }

    // Check for Material-UI specific classes
    console.log('\n========================================');
    console.log('3. BUSCANDO COMPONENTES MATERIAL-UI');
    console.log('========================================\n');

    const muiTextFields = await page.$$('[class*="MuiTextField"]');
    console.log(`Encontrados ${muiTextFields.length} componentes MuiTextField`);

    const muiInputBase = await page.$$('[class*="MuiInputBase"]');
    console.log(`Encontrados ${muiInputBase.length} componentes MuiInputBase`);

    const muiButton = await page.$$('[class*="MuiButton"]');
    console.log(`Encontrados ${muiButton.length} componentes MuiButton`);

    // Get page HTML
    console.log('\n========================================');
    console.log('4. GUARDANDO HTML COMPLETO');
    console.log('========================================\n');

    const html = await page.content();
    fs.writeFileSync('./debug_page.html', html);
    console.log('📄 HTML guardado en: ./debug_page.html\n');

    // Check for specific text patterns
    console.log('\n========================================');
    console.log('5. BUSCANDO PATRONES DE TEXTO');
    console.log('========================================\n');

    const textPatterns = [
      'Registro',
      'Iniciar Sesión',
      'Login',
      'Email',
      'Correo',
      'Password',
      'Contraseña',
      'Usuario',
      'Username',
      'Entrar',
      'Ingresar'
    ];

    for (const pattern of textPatterns) {
      const found = html.includes(pattern);
      console.log(`"${pattern}": ${found ? '✅ Encontrado' : '❌ No encontrado'}`);
    }

    // Try to find links to login or register
    console.log('\n========================================');
    console.log('6. BUSCANDO ENLACES DE NAVEGACIÓN');
    console.log('========================================\n');

    const links = await page.$$('a');
    console.log(`Encontrados ${links.length} enlaces\n`);

    for (const link of links.slice(0, 10)) { // Show first 10 links
      const href = await link.getAttribute('href');
      const text = await link.textContent();
      if (href) {
        console.log(`Link: "${text?.trim()}" -> ${href}`);
      }
    }

    // Check if we're on login page or main app
    console.log('\n========================================');
    console.log('7. DIAGNÓSTICO FINAL');
    console.log('========================================\n');

    const currentUrl = page.url();
    console.log('URL actual:', currentUrl);

    if (currentUrl.includes('/login')) {
      console.log('✅ La aplicación redirigió a /login');
      console.log('💡 Necesitamos encontrar selectores para el formulario de login');
    } else if (currentUrl.includes('/register')) {
      console.log('✅ La aplicación redirigió a /register');
      console.log('💡 Necesitamos encontrar selectores para el formulario de registro');
    } else if (currentUrl === BASE_URL || currentUrl === BASE_URL + '/') {
      console.log('⚠️ La aplicación está en la página principal');
      console.log('💡 Puede que necesitemos navegar explícitamente a /login o /register');
    }

    // Try some common Material-UI selectors
    console.log('\n========================================');
    console.log('8. PROBANDO SELECTORES COMUNES');
    console.log('========================================\n');

    const commonSelectors = [
      'input[type="email"]',
      'input[name="email"]',
      'input[id="email"]',
      'input[placeholder*="email" i]',
      'input[placeholder*="correo" i]',
      '#email',
      '[name="email"]',
      '[aria-label*="email" i]',
      '[aria-label*="correo" i]',
      'input[type="text"]',
      '.MuiTextField-root input',
      '.MuiInputBase-input'
    ];

    for (const selector of commonSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          const visible = await element.isVisible();
          console.log(`✅ "${selector}" - ${visible ? 'VISIBLE' : 'NO VISIBLE'}`);
        } else {
          console.log(`❌ "${selector}" - NO ENCONTRADO`);
        }
      } catch (error) {
        console.log(`❌ "${selector}" - ERROR: ${error.message}`);
      }
    }

  } catch (error) {
    console.error('\n⚠️ ERROR EN DIAGNÓSTICO:');
    console.error(error.message);
    console.error(error.stack);

    await page.screenshot({ path: './screenshots/error.png', fullPage: true });
    console.log('\n📸 Screenshot de error guardado: ./screenshots/error.png');
  } finally {
    await browser.close();
  }

  console.log('\n\n╔══════════════════════════════════════════╗');
  console.log('║   DIAGNÓSTICO COMPLETADO                ║');
  console.log('╚══════════════════════════════════════════╝');
}

// Create screenshots directory
const fs2 = require('fs');
if (!fs2.existsSync('./screenshots')) {
  fs2.mkdirSync('./screenshots', { recursive: true });
}

diagnosticTest();
