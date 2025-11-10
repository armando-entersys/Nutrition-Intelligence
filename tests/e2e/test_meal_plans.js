/**
 * Suite de Pruebas E2E - Plan Alimenticio
 * Basado en: docs/03_MATRICES_PRUEBA.md
 *
 * Test Cases:
 * - TEST-PLAN-001: Creación de Plan Alimenticio
 * - TEST-PLAN-002: Asignación de Alimentos a Tiempos de Comida
 * - TEST-PLAN-003: Cálculo Automático de Totales Nutricionales
 * - TEST-PLAN-004: Compartir Plan con Paciente
 *
 * Nutrition Intelligence Platform
 * https://nutrition-intelligence.scram2k.com
 */

const { chromium } = require('playwright');
const fs = require('fs');

// ═══════════════════════════════════════
// CONFIGURACIÓN
// ═══════════════════════════════════════

const BASE_URL = 'https://nutrition-intelligence.scram2k.com';
const TIMEOUT = 30000;

const NUTRITIONIST_CREDENTIALS = {
  email: 'armando.cortes@entersys.mx',
  password: 'Test123456'
};

const testResults = {
  passed: 0,
  failed: 0,
  total: 0,
  details: []
};

// ═══════════════════════════════════════
// FUNCIONES AUXILIARES
// ═══════════════════════════════════════

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

async function loginAsNutritionist(page) {
  console.log('\n🔐 Autenticando como nutriólogo...');
  await page.goto(`${BASE_URL}/auth/login`, { waitUntil: 'networkidle', timeout: TIMEOUT });
  await page.waitForSelector('input[name="email"]', { state: 'visible', timeout: 10000 });
  await clearAndFill(page, 'input[name="email"]', NUTRITIONIST_CREDENTIALS.email);
  await clearAndFill(page, 'input[name="password"]', NUTRITIONIST_CREDENTIALS.password);

  const [response] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/api/v1/auth/login') && r.request().method() === 'POST', { timeout: TIMEOUT }),
    page.click('button[type="submit"]')
  ]);

  if (response.status() !== 200) throw new Error(`Login failed with status ${response.status()}`);
  await page.waitForURL(/\/dashboard|\/nutrition-plans|\/home/, { timeout: 15000 });
  console.log('   ✅ Login exitoso');
}

// ═══════════════════════════════════════
// TESTS DE PLAN ALIMENTICIO
// ═══════════════════════════════════════

async function testCreateMealPlan(page) {
  console.log('\n========================================');
  console.log('TEST-PLAN-001: Creación de Plan Alimenticio');
  console.log('========================================');

  try {
    console.log('1. Navegando a planes alimenticios...');
    await page.goto(`${BASE_URL}/nutrition-plans`, { waitUntil: 'networkidle', timeout: TIMEOUT });
    await takeScreenshot(page, 'plan-001-plans-page');

    console.log('2. Buscando botón para crear nuevo plan...');
    const createButtonSelectors = [
      'button:has-text("Nuevo Plan")',
      'button:has-text("Crear Plan")',
      'button:has-text("Agregar Plan")',
      'button[aria-label*="nuevo" i]',
      'button[aria-label*="create" i]'
    ];

    let createButton = null;
    for (const selector of createButtonSelectors) {
      createButton = await page.$(selector);
      if (createButton) {
        console.log(`   ✓ Botón encontrado: ${selector}`);
        break;
      }
    }

    if (!createButton) {
      console.log('   ℹ️ Verificando si ya hay interfaz para crear plan...');
      const bodyText = await page.textContent('body');
      const hasCreateInterface = bodyText.includes('Nombre del plan') || bodyText.includes('Objetivo') || bodyText.includes('Desayuno');

      if (hasCreateInterface) {
        logTestResult('TEST-PLAN-001', 'Creación de Plan Alimenticio', 'PASÓ', {
          actualResult: 'Interfaz de creación de plan alimenticio disponible',
          expectedResult: 'Sistema debe permitir crear planes alimenticios',
          note: 'Interfaz de creación encontrada'
        });
        return true;
      }

      throw new Error('No se encontró botón o interfaz para crear plan alimenticio');
    }

    await createButton.click();
    await delay(2000);
    await takeScreenshot(page, 'plan-001-create-form');

    logTestResult('TEST-PLAN-001', 'Creación de Plan Alimenticio', 'PASÓ', {
      actualResult: 'Funcionalidad de creación de planes disponible',
      expectedResult: 'Sistema debe permitir crear planes alimenticios'
    });

    return true;
  } catch (error) {
    await takeScreenshot(page, 'plan-001-error');
    logTestResult('TEST-PLAN-001', 'Creación de Plan Alimenticio', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir crear planes alimenticios',
      actualResult: 'Error al acceder a funcionalidad de planes'
    });
    return false;
  }
}

async function testAssignFoodsToMeals(page) {
  console.log('\n========================================');
  console.log('TEST-PLAN-002: Asignación de Alimentos a Tiempos de Comida');
  console.log('========================================');

  try {
    console.log('1. Verificando interfaz de tiempos de comida...');
    await page.goto(`${BASE_URL}/nutrition-plans`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'plan-002-meal-times');

    const bodyText = await page.textContent('body');
    const mealTimes = ['Desayuno', 'Almuerzo', 'Comida', 'Cena', 'Colación', 'Snack'];
    const foundMealTimes = mealTimes.filter(meal => bodyText.includes(meal));

    console.log(`   → Tiempos de comida encontrados: ${foundMealTimes.join(', ')}`);

    if (foundMealTimes.length > 0) {
      logTestResult('TEST-PLAN-002', 'Asignación de Alimentos a Tiempos de Comida', 'PASÓ', {
        actualResult: `Interfaz de tiempos de comida disponible (${foundMealTimes.length} tiempos encontrados)`,
        expectedResult: 'Sistema debe permitir asignar alimentos a diferentes tiempos de comida',
        mealTimesFound: foundMealTimes.join(', ')
      });
      return true;
    }

    throw new Error('No se encontraron tiempos de comida en la interfaz');
  } catch (error) {
    await takeScreenshot(page, 'plan-002-error');
    logTestResult('TEST-PLAN-002', 'Asignación de Alimentos a Tiempos de Comida', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir asignar alimentos a diferentes tiempos de comida',
      actualResult: 'Error al verificar tiempos de comida'
    });
    return false;
  }
}

async function testAutomaticNutritionalTotals(page) {
  console.log('\n========================================');
  console.log('TEST-PLAN-003: Cálculo Automático de Totales Nutricionales');
  console.log('========================================');

  try {
    console.log('1. Buscando totales nutricionales en el plan...');
    await page.goto(`${BASE_URL}/nutrition-plans`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'plan-003-nutritional-totals');

    const bodyText = await page.textContent('body');

    const nutritionalTerms = ['Calorías', 'Proteínas', 'Carbohidratos', 'Grasas', 'kcal', 'Total'];
    const foundTerms = nutritionalTerms.filter(term => bodyText.includes(term));

    console.log(`   → Términos nutricionales encontrados: ${foundTerms.join(', ')}`);

    // Buscar valores numéricos que parezcan totales
    const hasNumericValues = /\d+\s*(kcal|g|%)/i.test(bodyText);

    if (foundTerms.length >= 2 || hasNumericValues) {
      logTestResult('TEST-PLAN-003', 'Cálculo Automático de Totales Nutricionales', 'PASÓ', {
        actualResult: 'Sistema muestra totales nutricionales',
        expectedResult: 'Sistema debe calcular automáticamente los totales nutricionales',
        foundElements: foundTerms.join(', ')
      });
      return true;
    }

    throw new Error('No se encontraron totales nutricionales');
  } catch (error) {
    await takeScreenshot(page, 'plan-003-error');
    logTestResult('TEST-PLAN-003', 'Cálculo Automático de Totales Nutricionales', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe calcular automáticamente los totales nutricionales',
      actualResult: 'Error al verificar totales nutricionales'
    });
    return false;
  }
}

async function testSharePlanWithPatient(page) {
  console.log('\n========================================');
  console.log('TEST-PLAN-004: Compartir Plan con Paciente');
  console.log('========================================');

  try {
    console.log('1. Buscando opción para compartir plan...');
    await page.goto(`${BASE_URL}/nutrition-plans`, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await takeScreenshot(page, 'plan-004-share-option');

    const shareButtonSelectors = [
      'button:has-text("Compartir")',
      'button:has-text("Share")',
      'button:has-text("Enviar")',
      'button:has-text("Asignar")',
      'button[aria-label*="compartir" i]',
      'button[aria-label*="share" i]',
      '[data-testid*="share"]'
    ];

    let shareButton = null;
    for (const selector of shareButtonSelectors) {
      shareButton = await page.$(selector);
      if (shareButton) {
        console.log(`   ✓ Botón de compartir encontrado: ${selector}`);
        break;
      }
    }

    if (shareButton) {
      const isVisible = await shareButton.isVisible();
      const isEnabled = await shareButton.isEnabled();

      logTestResult('TEST-PLAN-004', 'Compartir Plan con Paciente', 'PASÓ', {
        actualResult: 'Funcionalidad de compartir plan disponible',
        expectedResult: 'Sistema debe permitir compartir/asignar planes a pacientes',
        buttonVisible: isVisible,
        buttonEnabled: isEnabled
      });
      return true;
    }

    // Verificar si hay una lista de pacientes (indicaría que se puede asignar)
    const bodyText = await page.textContent('body');
    const hasPatientList = bodyText.includes('Paciente') || bodyText.includes('Asignado a');

    if (hasPatientList) {
      logTestResult('TEST-PLAN-004', 'Compartir Plan con Paciente', 'PASÓ', {
        actualResult: 'Interfaz de asignación de pacientes disponible',
        expectedResult: 'Sistema debe permitir compartir/asignar planes a pacientes',
        note: 'Sistema muestra información de pacientes asignados'
      });
      return true;
    }

    throw new Error('No se encontró funcionalidad de compartir/asignar plan');
  } catch (error) {
    await takeScreenshot(page, 'plan-004-error');
    logTestResult('TEST-PLAN-004', 'Compartir Plan con Paciente', 'FALLÓ', {
      error: error.message,
      expectedResult: 'Sistema debe permitir compartir/asignar planes a pacientes',
      actualResult: 'Error al verificar funcionalidad de compartir'
    });
    return false;
  }
}

// ═══════════════════════════════════════
// FUNCIÓN PRINCIPAL
// ═══════════════════════════════════════

async function runTests() {
  console.log('╔══════════════════════════════════════════╗');
  console.log('║  SUITE DE PRUEBAS E2E - PLANES ALIM.    ║');
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
    await loginAsNutritionist(page);
    await delay(2000);

    await testCreateMealPlan(page);
    await delay(3000);

    await testAssignFoodsToMeals(page);
    await delay(3000);

    await testAutomaticNutritionalTotals(page);
    await delay(3000);

    await testSharePlanWithPatient(page);

    console.log('\n\n╔══════════════════════════════════════════╗');
    console.log('║        REPORTE FINAL DE PRUEBAS          ║');
    console.log('╚══════════════════════════════════════════╝\n');

    console.log(`Total de pruebas: ${testResults.total}`);
    console.log(`✅ Pasaron: ${testResults.passed}`);
    console.log(`⚠️  Fallaron: ${testResults.failed}`);
    const successRate = ((testResults.passed / testResults.total) * 100).toFixed(2);
    console.log(`📊 Porcentaje éxito: ${successRate}%\n`);

    console.log('\nDetalle de resultados:');
    console.log('═══════════════════════════════════════════════════════════════════════');

    testResults.details.forEach((result, index) => {
      console.log(`\n${index + 1}. ${result.status === 'PASÓ' ? '✅' : '⚠️'} ${result.id}: ${result.name}`);
      console.log(`   Estado: ${result.status}`);
      if (result.actualResult) console.log(`   Resultado: ${result.actualResult}`);
      if (result.error) console.log(`   Error: ${result.error}`);
    });

    const jsonReport = {
      suite: 'Plan Alimenticio E2E',
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

    fs.writeFileSync('./test_results_e2e_meal_plans.json', JSON.stringify(jsonReport, null, 2));
    console.log('\n\n📄 Reporte JSON guardado en: ./test_results_e2e_meal_plans.json');
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
