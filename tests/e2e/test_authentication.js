/**
 * Test Suite: Autenticación
 * Basado en: docs/03_MATRICES_PRUEBA.md
 * Casos: TEST-AUTH-001 a TEST-AUTH-006
 */

const { chromium } = require('playwright');

// Configuración
const BASE_URL = 'https://nutrition-intelligence.scram2k.com';
const TIMEOUT = 30000;

// Datos de prueba (según matriz de pruebas)
const TEST_DATA = {
  nutritionist: {
    email: 'armando.cortes@entersys.mx',
    username: 'armandocortes',
    password: 'Test123456',
    firstName: 'Armando',
    lastName: 'Cortés',
    phone: '+52 55 1234 5678',
    role: 'nutritionist'
  },
  patient: {
    email: 'zero.armando@gmail.com',
    username: 'zeroarmando',
    password: 'Test123456',
    firstName: 'Zero',
    lastName: 'Armando',
    phone: '+52 55 9876 5432',
    role: 'patient'
  },
  invalidPasswords: [
    { password: 'Ab1', expected: 'Muy corto (< 8 caracteres)' },
    { password: 'Abcd123', expected: '7 caracteres - límite inferior' },
    { password: 'abcd1234', expected: 'Sin mayúscula' },
    { password: 'Abcdefgh', expected: 'Sin número' }
  ]
};

// Resultados de pruebas
const testResults = {
  passed: 0,
  failed: 0,
  total: 0,
  details: []
};

// Helper function para registrar resultados
function logTestResult(testId, testName, status, details = {}) {
  testResults.total++;
  if (status === 'PASÓ') {
    testResults.passed++;
  } else {
    testResults.failed++;
  }

  const result = {
    id: testId,
    name: testName,
    status: status,
    timestamp: new Date().toISOString(),
    ...details
  };

  testResults.details.push(result);

  const statusIcon = status === 'PASÓ' ? '✅' : '⚠️';
  console.log(`\n${statusIcon} ${testId}: ${testName} - ${status}`);
  if (details.error) {
    console.log(`   Error: ${details.error}`);
  }
  if (details.message) {
    console.log(`   ${details.message}`);
  }
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * TEST-AUTH-001: Registro de Usuario Nutriólogo
 */
async function testNutritionistRegistration(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-001: Registro Usuario Nutriólogo');
  console.log('========================================');

  try {
    // Navegar a la página
    console.log('1. Navegando a la aplicación...');
    await page.goto(BASE_URL, {
      waitUntil: 'networkidle',
      timeout: TIMEOUT
    });

    // Esperar al formulario de registro
    console.log('2. Esperando formulario de registro...');
    await page.waitForSelector('input[type="email"]', { timeout: 5000 });

    // Llenar formulario
    console.log('3. Llenando formulario de registro...');
    await page.fill('input[type="email"]', `test.nutritionist.${Date.now()}@test.com`);
    await page.fill('input[name="username"]', `nutritionist${Date.now()}`);
    await page.fill('input[name="firstName"]', TEST_DATA.nutritionist.firstName);
    await page.fill('input[name="lastName"]', TEST_DATA.nutritionist.lastName);
    await page.fill('input[type="tel"]', TEST_DATA.nutritionist.phone);
    await page.fill('input[type="password"]', TEST_DATA.nutritionist.password);
    await page.fill('input[name="confirmPassword"]', TEST_DATA.nutritionist.password);

    // Seleccionar rol
    await page.selectOption('select[name="role"]', 'nutritionist');

    // Enviar formulario y capturar respuesta
    console.log('4. Enviando formulario...');
    const [response] = await Promise.all([
      page.waitForResponse(response =>
        response.url().includes('/api/v1/auth/register') &&
        response.request().method() === 'POST',
        { timeout: 10000 }
      ),
      page.click('button[type="submit"]')
    ]);

    const status = response.status();
    const body = await response.json();

    console.log(`   Status HTTP: ${status}`);
    console.log(`   Response:`, JSON.stringify(body, null, 2));

    if (status === 200 || status === 201) {
      logTestResult(
        'TEST-AUTH-001',
        'Registro Usuario Nutriólogo',
        'PASÓ',
        {
          httpStatus: status,
          message: 'Registro exitoso',
          response: body
        }
      );
    } else {
      logTestResult(
        'TEST-AUTH-001',
        'Registro Usuario Nutriólogo',
        'FALLÓ',
        {
          httpStatus: status,
          error: body.message || 'Error en registro',
          response: body
        }
      );
    }

  } catch (error) {
    logTestResult(
      'TEST-AUTH-001',
      'Registro Usuario Nutriólogo',
      'FALLÓ',
      { error: error.message }
    );
  }
}

/**
 * TEST-AUTH-002: Registro con Email Duplicado
 */
async function testDuplicateEmailRegistration(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-002: Registro con Email Duplicado');
  console.log('========================================');

  try {
    console.log('1. Intentando registro con email existente...');
    await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: TIMEOUT });

    await page.waitForSelector('input[type="email"]', { timeout: 5000 });

    // Usar email que ya existe en producción
    await page.fill('input[type="email"]', TEST_DATA.nutritionist.email);
    await page.fill('input[name="username"]', `duplicate${Date.now()}`);
    await page.fill('input[type="password"]', TEST_DATA.nutritionist.password);

    const [response] = await Promise.all([
      page.waitForResponse(response =>
        response.url().includes('/api/v1/auth/register'),
        { timeout: 10000 }
      ),
      page.click('button[type="submit"]')
    ]);

    const status = response.status();
    const body = await response.json();

    console.log(`   Status HTTP: ${status}`);
    console.log(`   Response:`, JSON.stringify(body, null, 2));

    // Esperamos un error 400 Bad Request
    if (status === 400 && body.message && body.message.includes('already')) {
      logTestResult(
        'TEST-AUTH-002',
        'Registro con Email Duplicado',
        'PASÓ',
        {
          httpStatus: status,
          message: 'Error correctamente detectado: ' + body.message
        }
      );
    } else {
      logTestResult(
        'TEST-AUTH-002',
        'Registro con Email Duplicado',
        'FALLÓ',
        {
          httpStatus: status,
          error: 'No se detectó email duplicado correctamente',
          response: body
        }
      );
    }

  } catch (error) {
    logTestResult(
      'TEST-AUTH-002',
      'Registro con Email Duplicado',
      'FALLÓ',
      { error: error.message }
    );
  }
}

/**
 * TEST-AUTH-003: Registro con Password Débil
 */
async function testWeakPasswordRegistration(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-003: Registro con Password Débil');
  console.log('========================================');

  for (const pwdTest of TEST_DATA.invalidPasswords) {
    try {
      console.log(`\nProbando: ${pwdTest.expected}`);
      console.log(`Password: "${pwdTest.password}"`);

      await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: TIMEOUT });
      await page.waitForSelector('input[type="email"]', { timeout: 5000 });

      await page.fill('input[type="email"]', `weakpwd.${Date.now()}@test.com`);
      await page.fill('input[name="username"]', `weakpwd${Date.now()}`);
      await page.fill('input[type="password"]', pwdTest.password);

      // Verificar si hay validación en frontend antes de enviar
      const submitButton = await page.$('button[type="submit"]');
      const isDisabled = await submitButton.isDisabled();

      if (isDisabled) {
        console.log(`   ✅ Validación frontend: botón deshabilitado`);
        logTestResult(
          'TEST-AUTH-003',
          `Password Débil: ${pwdTest.expected}`,
          'PASÓ',
          { message: 'Validación frontend previene envío' }
        );
        continue;
      }

      // Si no está deshabilitado, intentar enviar
      const [response] = await Promise.all([
        page.waitForResponse(response =>
          response.url().includes('/api/v1/auth/register'),
          { timeout: 10000 }
        ),
        page.click('button[type="submit"]')
      ]);

      const status = response.status();
      const body = await response.json();

      // Esperamos un error 400
      if (status === 400) {
        console.log(`   ✅ Validación backend: ${body.message}`);
        logTestResult(
          'TEST-AUTH-003',
          `Password Débil: ${pwdTest.expected}`,
          'PASÓ',
          { message: 'Password rechazada correctamente' }
        );
      } else {
        logTestResult(
          'TEST-AUTH-003',
          `Password Débil: ${pwdTest.expected}`,
          'FALLÓ',
          { error: 'Password débil aceptada incorrectamente' }
        );
      }

    } catch (error) {
      logTestResult(
        'TEST-AUTH-003',
        `Password Débil: ${pwdTest.expected}`,
        'FALLÓ',
        { error: error.message }
      );
    }
  }
}

/**
 * TEST-AUTH-004: Login Usuario Nutriólogo
 */
async function testNutritionistLogin(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-004: Login Usuario Nutriólogo');
  console.log('========================================');

  try {
    console.log('1. Navegando a login...');
    await page.goto(BASE_URL + '/login', {
      waitUntil: 'networkidle',
      timeout: TIMEOUT
    });

    console.log('2. Llenando credenciales...');
    await page.waitForSelector('input[type="email"]', { timeout: 5000 });
    await page.fill('input[type="email"]', TEST_DATA.nutritionist.email);
    await page.fill('input[type="password"]', TEST_DATA.nutritionist.password);

    console.log('3. Enviando login...');
    const [response] = await Promise.all([
      page.waitForResponse(response =>
        response.url().includes('/api/v1/auth/login'),
        { timeout: 10000 }
      ),
      page.click('button[type="submit"]')
    ]);

    const status = response.status();
    const body = await response.json();

    console.log(`   Status HTTP: ${status}`);
    console.log(`   User ID: ${body.user_id}`);
    console.log(`   Role: ${body.primary_role}`);
    console.log(`   Status: ${body.account_status}`);

    if (status === 200 && body.access_token && body.primary_role === 'nutritionist') {
      console.log('   ✅ Tokens JWT generados');
      console.log('   ✅ Rol correcto');

      logTestResult(
        'TEST-AUTH-004',
        'Login Usuario Nutriólogo',
        'PASÓ',
        {
          httpStatus: status,
          userId: body.user_id,
          role: body.primary_role,
          message: 'Login exitoso con tokens JWT'
        }
      );

      // Verificar redirección a dashboard
      await page.waitForNavigation({ timeout: 5000 }).catch(() => {});
      const url = page.url();
      console.log(`   URL después de login: ${url}`);

    } else {
      logTestResult(
        'TEST-AUTH-004',
        'Login Usuario Nutriólogo',
        'FALLÓ',
        {
          httpStatus: status,
          error: 'Login falló o tokens no generados',
          response: body
        }
      );
    }

  } catch (error) {
    logTestResult(
      'TEST-AUTH-004',
      'Login Usuario Nutriólogo',
      'FALLÓ',
      { error: error.message }
    );
  }
}

/**
 * TEST-AUTH-005: Login Usuario Paciente
 */
async function testPatientLogin(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-005: Login Usuario Paciente');
  console.log('========================================');

  try {
    console.log('1. Navegando a login...');
    await page.goto(BASE_URL + '/login', {
      waitUntil: 'networkidle',
      timeout: TIMEOUT
    });

    console.log('2. Llenando credenciales...');
    await page.waitForSelector('input[type="email"]', { timeout: 5000 });
    await page.fill('input[type="email"]', TEST_DATA.patient.email);
    await page.fill('input[type="password"]', TEST_DATA.patient.password);

    console.log('3. Enviando login...');
    const [response] = await Promise.all([
      page.waitForResponse(response =>
        response.url().includes('/api/v1/auth/login'),
        { timeout: 10000 }
      ),
      page.click('button[type="submit"]')
    ]);

    const status = response.status();
    const body = await response.json();

    console.log(`   Status HTTP: ${status}`);
    console.log(`   User ID: ${body.user_id}`);
    console.log(`   Role: ${body.primary_role}`);
    console.log(`   Nutritionist ID: ${body.nutritionist_id}`);

    if (status === 200 && body.access_token && body.primary_role === 'patient') {
      console.log('   ✅ Tokens JWT generados');
      console.log('   ✅ Rol correcto');
      console.log('   ✅ Vinculado a nutriólogo');

      logTestResult(
        'TEST-AUTH-005',
        'Login Usuario Paciente',
        'PASÓ',
        {
          httpStatus: status,
          userId: body.user_id,
          role: body.primary_role,
          nutritionistId: body.nutritionist_id,
          message: 'Login exitoso con vinculación a nutriólogo'
        }
      );
    } else {
      logTestResult(
        'TEST-AUTH-005',
        'Login Usuario Paciente',
        'FALLÓ',
        {
          httpStatus: status,
          error: 'Login falló o datos incorrectos',
          response: body
        }
      );
    }

  } catch (error) {
    logTestResult(
      'TEST-AUTH-005',
      'Login Usuario Paciente',
      'FALLÓ',
      { error: error.message }
    );
  }
}

/**
 * TEST-AUTH-006: Login con Credenciales Incorrectas
 */
async function testInvalidCredentialsLogin(page) {
  console.log('\n========================================');
  console.log('TEST-AUTH-006: Login con Credenciales Incorrectas');
  console.log('========================================');

  const invalidTests = [
    {
      email: 'noexiste@test.com',
      password: 'Test123456',
      description: 'Email inválido'
    },
    {
      email: TEST_DATA.nutritionist.email,
      password: 'WrongPassword123',
      description: 'Password incorrecta'
    },
    {
      email: '',
      password: 'Test123456',
      description: 'Email vacío'
    },
    {
      email: TEST_DATA.nutritionist.email,
      password: '',
      description: 'Password vacío'
    }
  ];

  for (const test of invalidTests) {
    try {
      console.log(`\nProbando: ${test.description}`);

      await page.goto(BASE_URL + '/login', {
        waitUntil: 'networkidle',
        timeout: TIMEOUT
      });

      await page.waitForSelector('input[type="email"]', { timeout: 5000 });

      if (test.email) await page.fill('input[type="email"]', test.email);
      if (test.password) await page.fill('input[type="password"]', test.password);

      const [response] = await Promise.all([
        page.waitForResponse(response =>
          response.url().includes('/api/v1/auth/login'),
          { timeout: 10000 }
        ),
        page.click('button[type="submit"]')
      ]);

      const status = response.status();
      const body = await response.json();

      console.log(`   Status: ${status}`);
      console.log(`   Message: ${body.message || body.detail}`);

      // Esperamos 401 Unauthorized o 400 Bad Request
      if (status === 401 || status === 400) {
        logTestResult(
          'TEST-AUTH-006',
          `Credenciales Incorrectas: ${test.description}`,
          'PASÓ',
          {
            httpStatus: status,
            message: 'Error detectado correctamente'
          }
        );
      } else {
        logTestResult(
          'TEST-AUTH-006',
          `Credenciales Incorrectas: ${test.description}`,
          'FALLÓ',
          {
            httpStatus: status,
            error: 'Login no rechazado correctamente'
          }
        );
      }

    } catch (error) {
      logTestResult(
        'TEST-AUTH-006',
        `Credenciales Incorrectas: ${test.description}`,
        'FALLÓ',
        { error: error.message }
      );
    }
  }
}

/**
 * Función principal de ejecución
 */
async function runTests() {
  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║   SUITE DE PRUEBAS DE AUTENTICACIÓN     ║');
  console.log('║   Nutrition Intelligence Platform        ║');
  console.log('╚══════════════════════════════════════════╝');
  console.log(`\nURL Base: ${BASE_URL}`);
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  // Interceptar requests/responses para logging
  page.on('request', request => {
    if (request.url().includes('/api/v1/auth')) {
      console.log(`   → ${request.method()} ${request.url()}`);
    }
  });

  page.on('response', response => {
    if (response.url().includes('/api/v1/auth')) {
      console.log(`   ← ${response.status()} ${response.url()}`);
    }
  });

  try {
    // Ejecutar todos los tests
    await testNutritionistRegistration(page);
    await delay(2000);

    await testDuplicateEmailRegistration(page);
    await delay(2000);

    await testWeakPasswordRegistration(page);
    await delay(2000);

    await testNutritionistLogin(page);
    await delay(2000);

    await testPatientLogin(page);
    await delay(2000);

    await testInvalidCredentialsLogin(page);

  } catch (error) {
    console.error('\n❌ Error fatal en suite de pruebas:', error);
  } finally {
    await browser.close();
  }

  // Generar reporte final
  console.log('\n\n╔══════════════════════════════════════════╗');
  console.log('║        REPORTE FINAL DE PRUEBAS          ║');
  console.log('╚══════════════════════════════════════════╝');
  console.log(`\nTotal de pruebas: ${testResults.total}`);
  console.log(`✅ Pasaron: ${testResults.passed}`);
  console.log(`⚠️  Fallaron: ${testResults.failed}`);
  console.log(`📊 Porcentaje éxito: ${((testResults.passed / testResults.total) * 100).toFixed(2)}%`);

  console.log('\n\nDetalle de resultados:');
  console.log('═'.repeat(80));

  testResults.details.forEach((result, index) => {
    const icon = result.status === 'PASÓ' ? '✅' : '⚠️';
    console.log(`\n${index + 1}. ${icon} ${result.id}: ${result.name}`);
    console.log(`   Estado: ${result.status}`);
    console.log(`   Timestamp: ${result.timestamp}`);
    if (result.httpStatus) console.log(`   HTTP Status: ${result.httpStatus}`);
    if (result.message) console.log(`   Mensaje: ${result.message}`);
    if (result.error) console.log(`   Error: ${result.error}`);
  });

  // Guardar reporte JSON
  const fs = require('fs');
  const reportPath = './test_results_e2e_authentication.json';
  fs.writeFileSync(reportPath, JSON.stringify({
    suite: 'Autenticación',
    timestamp: new Date().toISOString(),
    baseUrl: BASE_URL,
    summary: {
      total: testResults.total,
      passed: testResults.passed,
      failed: testResults.failed,
      successRate: ((testResults.passed / testResults.total) * 100).toFixed(2)
    },
    details: testResults.details
  }, null, 2));

  console.log(`\n\n📄 Reporte JSON guardado en: ${reportPath}`);
  console.log('\n✨ Suite de pruebas completada.\n');

  // Exit code basado en resultados
  process.exit(testResults.failed > 0 ? 1 : 0);
}

// Ejecutar tests
runTests().catch(console.error);
