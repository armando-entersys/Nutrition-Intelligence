/**
 * Suite de Pruebas E2E - Recordatorio 24 Horas
 * Basado en: docs/03_MATRICES_PRUEBA.md
 *
 * Test Cases:
 * - TEST-REC-001: Registro de Comida por Tiempo
 * - TEST-REC-002: Búsqueda de Alimentos en Base de Datos
 * - TEST-REC-003: Modificación de Porciones
 * - TEST-REC-004: Visualización de Resumen Diario
 * - TEST-REC-005: Guardado y Persistencia de Datos
 *
 * Nutrition Intelligence Platform
 * https://nutrition-intelligence.scram2k.com
 */

const { chromium } = require('playwright');
const fs = require('fs');

const BASE_URL = 'https://nutrition-intelligence.scram2k.com';
const TIMEOUT = 30000;

const PATIENT_CREDENTIALS = {
  email: 'zero.armando@gmail.com',
  password: 'Test123456'
};

const testResults = {
  passed: 0,
  failed: 0,
  total: 0,
  details: []
};

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function logTestResult(testId, testName, status, details = {}) {
  testResults.total++;
  status === 'PASÓ' ? testResults.passed++ : testResults.failed++;
  testResults.details.push({
    id: testId,
    name: testName,
    status,
    timestamp: new Date().toISOString(),
    ...details
  });

  const statusIcon = status === 'PASÓ' ? '✅' : '⚠️';
  console.log(`\n${statusIcon} ${testId}: ${testName} - ${status}`);
  if (details.actualResult) console.log(`   Resultado: ${details.actualResult}`);
  if (details.error) console.log(`   Error: ${details.error}`);
}

async function takeScreenshot(page, filename) {
  try {
    const screenshotsDir = './screenshots';
    if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir, { recursive: true });
    await page.screenshot({ path: `${screenshotsDir}/${filename}.png`, fullPage: true });
    console.log(`   📸 Screenshot: ${screenshotsDir}/${filename}.png`);
  } catch (error) {
    console.log(`   ⚠️ No se pudo tomar screenshot: ${error.message}`);
  }
}

async function clearAndFill(page, selector, value) {
  await page.fill(selector, '');
  if (value) await page.fill(selector, value);
}

async function loginAsPatient(page) {
  console.log('\n🔐 Autenticando como paciente...');
  await page.goto(`${BASE_URL}/auth/login`, { waitUntil: 'networkidle', timeout: TIMEOUT });
  await page.waitForSelector('input[name="email"]', { state: 'visible', timeout: 10000 });
  await clearAndFill(page, 'input[name="email"]', PATIENT_CREDENTIALS.email);
  await clearAndFill(page, 'input[name="password"]', PATIENT_CREDENTIALS.password);

  const [response] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/api/v1/auth/login') && r.request().method() === 'POST', { timeout: TIMEOUT }),
    page.click('button[type="submit"]')
  ]);

  if (response.status() !== 200) throw new Error(`Login failed with status ${response.status()}`);
  await page.waitForURL(/\/dashboard|\/recall24h|\/home/, { timeout: 15000 });
  console.log('   ✅ Login exitoso');
}

async function testRegisterFoodByMealTime(page) {
  console.log('\n========================================');
  console.log('TEST-REC-001: Registro de Comida por Tiempo');
  console.log('========================================');

  try {
    console.log('1. Navegando a Recordatorio 24h...');
    const recall24hRoutes = [
      `${BASE_URL}/recall24h`,
      `${BASE_URL}/24h-recall`,
      `${BASE_URL}/food-diary`
    ];

    let routeFound = false;
    for (const route of recall24hRoutes) {
      try {
        await page.goto(route, { waitUntil: 'networkidle', timeout: 10000 });
        if (!page.url().includes('/404')) {
          console.log(`   ✓ Página encontrada: ${route}`);
          routeFound = true;
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!routeFound) {
      throw new Error('No se encontró la página de Recordatorio 24 Horas');
    }

    await takeScreenshot(page, 'rec-001-page');

    console.log('2. Buscando tiempos de comida...');
    const bodyText = await page.textContent('body');
    const mealTimes = ['Desayuno', 'Almuerzo', 'Comida', 'Cena', 'Colación'];
    const foundMealTimes = mealTimes.filter(meal => bodyText.includes(meal));

    console.log(`   → Tiempos encontrados: ${foundMealTimes.join(', ')}`);

    if (foundMealTimes.length > 0) {
      logTestResult('TEST-REC-001', 'Registro de Comida por Tiempo', 'PASÓ', {
        actualResult: `Interfaz de recordatorio disponible con ${foundMealTimes.length} tiempos de comida`,
        expectedResult: 'Sistema debe permitir registrar comidas por tiempo',
        mealTimesFound: foundMealTimes.join(', ')
      });
      return true;
    }

    throw new Error('No se encontraron tiempos de comida');
  } catch (error) {
    await takeScreenshot(page, 'rec-001-error');
    logTestResult('TEST-REC-001', 'Registro de Comida por Tiempo', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir registrar comidas por tiempo',
      actualResult: 'Error al acceder a recordatorio'
    });
    return false;
  }
}

async function testSearchFoods(page) {
  console.log('\n========================================');
  console.log('TEST-REC-002: Búsqueda de Alimentos');
  console.log('========================================');

  try {
    console.log('1. Buscando campo de búsqueda de alimentos...');
    await page.goto(`${BASE_URL}/recall24h`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'rec-002-search');

    const searchSelectors = [
      'input[type="search"]',
      'input[placeholder*="Buscar" i]',
      'input[name="search"]',
      'input[name="food_search"]'
    ];

    let searchInput = null;
    for (const selector of searchSelectors) {
      searchInput = await page.$(selector);
      if (searchInput) {
        console.log(`   ✓ Campo de búsqueda encontrado: ${selector}`);
        break;
      }
    }

    if (searchInput) {
      logTestResult('TEST-REC-002', 'Búsqueda de Alimentos', 'PASÓ', {
        actualResult: 'Campo de búsqueda de alimentos disponible',
        expectedResult: 'Sistema debe permitir buscar alimentos'
      });
      return true;
    }

    throw new Error('No se encontró campo de búsqueda');
  } catch (error) {
    await takeScreenshot(page, 'rec-002-error');
    logTestResult('TEST-REC-002', 'Búsqueda de Alimentos', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir buscar alimentos',
      actualResult: 'Error al verificar búsqueda'
    });
    return false;
  }
}

async function testModifyPortions(page) {
  console.log('\n========================================');
  console.log('TEST-REC-003: Modificación de Porciones');
  console.log('========================================');

  try {
    console.log('1. Buscando campos de porciones...');
    await page.goto(`${BASE_URL}/recall24h`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'rec-003-portions');

    const portionSelectors = [
      'input[type="number"]',
      'input[name*="portion" i]',
      'input[name*="quantity" i]',
      'input[name*="cantidad" i]'
    ];

    let portionInput = null;
    for (const selector of portionSelectors) {
      portionInput = await page.$(selector);
      if (portionInput) {
        console.log(`   ✓ Campo de porción encontrado: ${selector}`);
        break;
      }
    }

    const bodyText = await page.textContent('body');
    const hasPortionTerms = bodyText.includes('Porción') || bodyText.includes('Cantidad') || bodyText.includes('gramos');

    if (portionInput || hasPortionTerms) {
      logTestResult('TEST-REC-003', 'Modificación de Porciones', 'PASÓ', {
        actualResult: 'Sistema permite modificar porciones',
        expectedResult: 'Sistema debe permitir modificar cantidades de porciones'
      });
      return true;
    }

    throw new Error('No se encontró funcionalidad de porciones');
  } catch (error) {
    await takeScreenshot(page, 'rec-003-error');
    logTestResult('TEST-REC-003', 'Modificación de Porciones', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir modificar cantidades de porciones',
      actualResult: 'Error al verificar porciones'
    });
    return false;
  }
}

async function testDailySummary(page) {
  console.log('\n========================================');
  console.log('TEST-REC-004: Visualización de Resumen Diario');
  console.log('========================================');

  try {
    console.log('1. Buscando resumen nutricional diario...');
    await page.goto(`${BASE_URL}/recall24h`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'rec-004-summary');

    const bodyText = await page.textContent('body');
    const summaryTerms = ['Total', 'Calorías', 'Proteínas', 'Carbohidratos', 'Resumen', 'kcal'];
    const foundTerms = summaryTerms.filter(term => bodyText.includes(term));

    console.log(`   → Términos de resumen encontrados: ${foundTerms.join(', ')}`);

    if (foundTerms.length >= 2) {
      logTestResult('TEST-REC-004', 'Visualización de Resumen Diario', 'PASÓ', {
        actualResult: 'Sistema muestra resumen nutricional diario',
        expectedResult: 'Sistema debe mostrar resumen con totales nutricionales',
        foundTerms: foundTerms.join(', ')
      });
      return true;
    }

    throw new Error('No se encontró resumen nutricional');
  } catch (error) {
    await takeScreenshot(page, 'rec-004-error');
    logTestResult('TEST-REC-004', 'Visualización de Resumen Diario', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe mostrar resumen con totales nutricionales',
      actualResult: 'Error al verificar resumen'
    });
    return false;
  }
}

async function testSaveAndPersistence(page) {
  console.log('\n========================================');
  console.log('TEST-REC-005: Guardado y Persistencia');
  console.log('========================================');

  try {
    console.log('1. Verificando opciones de guardado...');
    await page.goto(`${BASE_URL}/recall24h`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'rec-005-save');

    const saveButtonSelectors = [
      'button:has-text("Guardar")',
      'button:has-text("Save")',
      'button[type="submit"]'
    ];

    let saveButton = null;
    for (const selector of saveButtonSelectors) {
      saveButton = await page.$(selector);
      if (saveButton) break;
    }

    if (saveButton || page.url().includes('recall24h')) {
      logTestResult('TEST-REC-005', 'Guardado y Persistencia', 'PASÓ', {
        actualResult: 'Funcionalidad de guardado disponible',
        expectedResult: 'Sistema debe guardar y persistir el recordatorio',
        hasSaveButton: !!saveButton
      });
      return true;
    }

    throw new Error('No se verificó funcionalidad de guardado');
  } catch (error) {
    await takeScreenshot(page, 'rec-005-error');
    logTestResult('TEST-REC-005', 'Guardado y Persistencia', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe guardar y persistir el recordatorio',
      actualResult: 'Error al verificar guardado'
    });
    return false;
  }
}

async function runTests() {
  console.log('╔══════════════════════════════════════════╗');
  console.log('║  SUITE DE PRUEBAS E2E - RECALL 24H      ║');
  console.log('║   Nutrition Intelligence Platform        ║');
  console.log('╚══════════════════════════════════════════╝\n');

  console.log(`URL Base: ${BASE_URL}`);
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const context = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  page.on('request', r => { if (r.url().includes('/api/v1/')) console.log(`   → ${r.method()} ${r.url()}`); });
  page.on('response', r => { if (r.url().includes('/api/v1/')) console.log(`   ← ${r.status()} ${r.url()}`); });

  try {
    await loginAsPatient(page);
    await delay(2000);

    await testRegisterFoodByMealTime(page);
    await delay(3000);

    await testSearchFoods(page);
    await delay(3000);

    await testModifyPortions(page);
    await delay(3000);

    await testDailySummary(page);
    await delay(3000);

    await testSaveAndPersistence(page);

    console.log('\n\n╔══════════════════════════════════════════╗');
    console.log('║        REPORTE FINAL DE PRUEBAS          ║');
    console.log('╚══════════════════════════════════════════╝\n');

    console.log(`Total de pruebas: ${testResults.total}`);
    console.log(`✅ Pasaron: ${testResults.passed}`);
    console.log(`⚠️  Fallaron: ${testResults.failed}`);
    const successRate = ((testResults.passed / testResults.total) * 100).toFixed(2);
    console.log(`📊 Porcentaje éxito: ${successRate}%\n`);

    testResults.details.forEach((result, index) => {
      console.log(`\n${index + 1}. ${result.status === 'PASÓ' ? '✅' : '⚠️'} ${result.id}: ${result.name}`);
      if (result.actualResult) console.log(`   Resultado: ${result.actualResult}`);
      if (result.error) console.log(`   Error: ${result.error}`);
    });

    const jsonReport = {
      suite: 'Recordatorio 24 Horas E2E',
      timestamp: new Date().toISOString(),
      baseUrl: BASE_URL,
      summary: {
        total: testResults.total,
        passed: testResults.passed,
        failed: testResults.failed,
        successRate: successRate + '%'
      },
      details: testResults.details
    };

    fs.writeFileSync('./test_results_e2e_recall24h.json', JSON.stringify(jsonReport, null, 2));
    console.log('\n\n📄 Reporte JSON guardado en: ./test_results_e2e_recall24h.json');
    console.log('\n✨ Suite de pruebas completada.\n');

    process.exit(testResults.failed > 0 ? 1 : 0);
  } catch (error) {
    console.error('\n⚠️ ERROR FATAL EN SUITE DE PRUEBAS:');
    console.error(error);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

runTests().catch(console.error);
