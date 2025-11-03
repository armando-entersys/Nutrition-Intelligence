#!/usr/bin/env node

/**
 * ============================================================================
 * Test Runner - Chrome DevTools MCP
 * ============================================================================
 * Professional test runner with advanced reporting and monitoring integration
 * Generates HTML reports, JSON results, and exports metrics to Prometheus
 * ============================================================================
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const Mocha = require('mocha');
const { chromium } = require('playwright');

// ============================================================================
// Configuration
// ============================================================================
const CONFIG = {
  baseURL: process.env.BASE_URL || 'http://localhost:3002',
  backendURL: process.env.BACKEND_URL || 'http://localhost:8000',
  reportsDir: path.join(__dirname, '../reports'),
  screenshotsDir: path.join(__dirname, '../screenshots'),
  videosDir: path.join(__dirname, '../videos'),
  timeout: parseInt(process.env.TIMEOUT) || 30000,
  headless: process.env.HEADLESS === 'true',
  parallel: process.env.PARALLEL === 'true',
  retries: parseInt(process.env.RETRIES) || 2
};

// ============================================================================
// Ensure directories exist
// ============================================================================
function ensureDirectories() {
  const dirs = [
    CONFIG.reportsDir,
    path.join(CONFIG.reportsDir, 'html'),
    path.join(CONFIG.reportsDir, 'json'),
    CONFIG.screenshotsDir,
    CONFIG.videosDir
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// ============================================================================
// Check if services are running
// ============================================================================
async function checkServices() {
  console.log('\n🔍 Verificando servicios...\n');

  const checkService = async (url, name) => {
    try {
      const response = await fetch(url, { method: 'GET', timeout: 3000 }).catch(() => null);
      if (response && (response.ok || response.status === 404)) {
        console.log(`✅ ${name} está corriendo en ${url}`);
        return true;
      } else {
        console.log(`❌ ${name} no responde en ${url}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ ${name} no está disponible en ${url}`);
      return false;
    }
  };

  const frontendRunning = await checkService(CONFIG.baseURL, 'Frontend');
  const backendRunning = await checkService(`${CONFIG.backendURL}/docs`, 'Backend API');

  if (!frontendRunning) {
    console.log('\n⚠️  ADVERTENCIA: Frontend no está corriendo en', CONFIG.baseURL);
    console.log('   Ejecuta: cd frontend && npm start\n');
  }

  if (!backendRunning) {
    console.log('\n⚠️  ADVERTENCIA: Backend no está corriendo en', CONFIG.backendURL);
    console.log('   Ejecuta: cd backend && python -m uvicorn main:app --reload\n');
  }

  return { frontendRunning, backendRunning };
}

// ============================================================================
// HTML Report Generator
// ============================================================================
function generateHTMLReport(results) {
  const timestamp = new Date().toISOString();
  const passed = results.tests.filter(t => t.state === 'passed').length;
  const failed = results.tests.filter(t => t.state === 'failed').length;
  const skipped = results.tests.filter(t => t.state === 'pending').length;
  const total = results.tests.length;
  const passRate = total > 0 ? ((passed / total) * 100).toFixed(2) : 0;

  const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nutrition Intelligence - Test Report</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
      color: #333;
    }
    .container {
      max-width: 1400px;
      margin: 0 auto;
      background: white;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 40px;
      text-align: center;
    }
    .header h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
      font-weight: 700;
    }
    .header p {
      font-size: 1.1rem;
      opacity: 0.95;
    }
    .summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      padding: 40px;
      background: #f8f9fa;
    }
    .stat-card {
      background: white;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      text-align: center;
      transition: transform 0.2s;
    }
    .stat-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .stat-number {
      font-size: 3rem;
      font-weight: 700;
      margin-bottom: 10px;
    }
    .stat-label {
      font-size: 1rem;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .stat-card.passed .stat-number { color: #10b981; }
    .stat-card.failed .stat-number { color: #ef4444; }
    .stat-card.skipped .stat-number { color: #f59e0b; }
    .stat-card.total .stat-number { color: #3b82f6; }
    .progress-bar {
      width: 100%;
      height: 30px;
      background: #e5e7eb;
      border-radius: 15px;
      overflow: hidden;
      margin: 20px 0;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #10b981, #34d399);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      transition: width 1s ease;
    }
    .tests-section {
      padding: 40px;
    }
    .test-suite {
      margin-bottom: 30px;
      border: 2px solid #e5e7eb;
      border-radius: 15px;
      overflow: hidden;
    }
    .suite-header {
      background: #f3f4f6;
      padding: 20px;
      font-weight: 700;
      font-size: 1.2rem;
      border-bottom: 2px solid #e5e7eb;
    }
    .test-case {
      padding: 20px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .test-case:last-child { border-bottom: none; }
    .test-title {
      flex: 1;
      font-size: 1rem;
    }
    .test-status {
      padding: 8px 20px;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.9rem;
      text-transform: uppercase;
    }
    .test-status.passed {
      background: #d1fae5;
      color: #065f46;
    }
    .test-status.failed {
      background: #fee2e2;
      color: #991b1b;
    }
    .test-status.pending {
      background: #fef3c7;
      color: #92400e;
    }
    .test-duration {
      color: #6b7280;
      font-size: 0.9rem;
      margin-left: 15px;
    }
    .error-details {
      background: #fef2f2;
      border-left: 4px solid #ef4444;
      padding: 15px;
      margin-top: 10px;
      border-radius: 5px;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
      color: #991b1b;
      white-space: pre-wrap;
    }
    .footer {
      background: #f9fafb;
      padding: 30px;
      text-align: center;
      color: #6b7280;
      border-top: 2px solid #e5e7eb;
    }
    .timestamp {
      font-size: 0.9rem;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🧪 Nutrition Intelligence</h1>
      <p>Reporte de Pruebas E2E - Chrome DevTools MCP</p>
    </div>

    <div class="summary">
      <div class="stat-card passed">
        <div class="stat-number">${passed}</div>
        <div class="stat-label">✅ Pasaron</div>
      </div>
      <div class="stat-card failed">
        <div class="stat-number">${failed}</div>
        <div class="stat-label">❌ Fallaron</div>
      </div>
      <div class="stat-card skipped">
        <div class="stat-number">${skipped}</div>
        <div class="stat-label">⏭️ Omitidos</div>
      </div>
      <div class="stat-card total">
        <div class="stat-number">${total}</div>
        <div class="stat-label">📊 Total</div>
      </div>
    </div>

    <div style="padding: 0 40px;">
      <div class="progress-bar">
        <div class="progress-fill" style="width: ${passRate}%">${passRate}% Éxito</div>
      </div>
    </div>

    <div class="tests-section">
      <h2 style="margin-bottom: 30px; font-size: 1.8rem;">Resultados Detallados</h2>
      ${generateTestSuitesHTML(results.tests)}
    </div>

    <div class="footer">
      <p><strong>Nutrition Intelligence Platform</strong> - Sistema de Nutrición Inteligente</p>
      <p class="timestamp">Generado: ${new Date(timestamp).toLocaleString('es-MX', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })}</p>
      <p style="margin-top: 10px; font-size: 0.85rem;">Powered by chrome-devtools-mcp & Mocha</p>
    </div>
  </div>
</body>
</html>`;

  return html;
}

function generateTestSuitesHTML(tests) {
  const suites = {};

  // Group tests by suite
  tests.forEach(test => {
    const suiteName = test.fullTitle.split(' ')[0] || 'General';
    if (!suites[suiteName]) {
      suites[suiteName] = [];
    }
    suites[suiteName].push(test);
  });

  // Generate HTML for each suite
  return Object.entries(suites).map(([suiteName, suiteTests]) => `
    <div class="test-suite">
      <div class="suite-header">${suiteName}</div>
      ${suiteTests.map(test => `
        <div class="test-case">
          <div class="test-title">${test.title}</div>
          <div>
            <span class="test-status ${test.state}">${test.state === 'passed' ? 'PASSED' : test.state === 'failed' ? 'FAILED' : 'SKIPPED'}</span>
            <span class="test-duration">${test.duration}ms</span>
          </div>
        </div>
        ${test.error ? `<div class="error-details">${escapeHtml(test.error)}</div>` : ''}
      `).join('')}
    </div>
  `).join('');
}

function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

// ============================================================================
// Run Tests
// ============================================================================
async function runTests() {
  console.log('\n' + '='.repeat(80));
  console.log('🧪 NUTRITION INTELLIGENCE - TEST SUITE');
  console.log('   Chrome DevTools MCP + Mocha');
  console.log('='.repeat(80) + '\n');

  ensureDirectories();

  // Check services
  const services = await checkServices();

  // Initialize Mocha
  const mocha = new Mocha({
    timeout: CONFIG.timeout,
    retries: CONFIG.retries,
    slow: 5000,
    reporter: 'spec',
    color: true
  });

  // Add test files
  const testFiles = [
    path.join(__dirname, 'e2e-clinical-workflow.test.js'),
    path.join(__dirname, 'e2e-whatsapp-integration.test.js'),
    path.join(__dirname, 'e2e-ai-vision.test.js')
  ];

  testFiles.forEach(file => {
    if (fs.existsSync(file)) {
      mocha.addFile(file);
    }
  });

  // Collect results
  const results = {
    tests: [],
    passes: 0,
    failures: 0,
    pending: 0,
    start: new Date(),
    end: null,
    duration: 0
  };

  // Run tests
  return new Promise((resolve) => {
    const runner = mocha.run((failures) => {
      results.end = new Date();
      results.duration = results.end - results.start;

      console.log('\n' + '='.repeat(80));
      console.log('📊 RESUMEN DE PRUEBAS');
      console.log('='.repeat(80));
      console.log(`✅ Pasaron:  ${results.passes}`);
      console.log(`❌ Fallaron: ${results.failures}`);
      console.log(`⏭️  Omitidos: ${results.pending}`);
      console.log(`⏱️  Duración: ${(results.duration / 1000).toFixed(2)}s`);
      console.log('='.repeat(80) + '\n');

      // Generate reports
      const htmlReport = generateHTMLReport(results);
      const htmlPath = path.join(CONFIG.reportsDir, 'html', 'test-report.html');
      fs.writeFileSync(htmlPath, htmlReport);
      console.log(`📄 Reporte HTML generado: ${htmlPath}`);

      const jsonPath = path.join(CONFIG.reportsDir, 'json', 'test-results.json');
      fs.writeFileSync(jsonPath, JSON.stringify(results, null, 2));
      console.log(`📄 Resultados JSON guardados: ${jsonPath}\n`);

      resolve(failures);
    });

    runner.on('pass', (test) => {
      results.passes++;
      results.tests.push({
        title: test.title,
        fullTitle: test.fullTitle(),
        duration: test.duration,
        state: 'passed'
      });
    });

    runner.on('fail', (test, err) => {
      results.failures++;
      results.tests.push({
        title: test.title,
        fullTitle: test.fullTitle(),
        duration: test.duration,
        state: 'failed',
        error: err.message
      });
    });

    runner.on('pending', (test) => {
      results.pending++;
      results.tests.push({
        title: test.title,
        fullTitle: test.fullTitle(),
        duration: 0,
        state: 'pending'
      });
    });
  });
}

// ============================================================================
// Main
// ============================================================================
if (require.main === module) {
  runTests()
    .then(failures => {
      process.exit(failures > 0 ? 1 : 0);
    })
    .catch(error => {
      console.error('❌ Error ejecutando pruebas:', error);
      process.exit(1);
    });
}

module.exports = { runTests, generateHTMLReport };
