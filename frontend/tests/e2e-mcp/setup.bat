@echo off
REM ============================================================================
REM Nutrition Intelligence - E2E Testing Setup Script (Windows)
REM ============================================================================
REM This script sets up the chrome-devtools-mcp testing environment
REM ============================================================================

echo.
echo ==========================================================================
echo 🧪 Nutrition Intelligence - E2E Testing Setup
echo    Chrome DevTools MCP Configuration
echo ==========================================================================
echo.

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js no está instalado
    echo    Por favor instala Node.js v18+ desde https://nodejs.org/
    exit /b 1
)

echo ✅ Node.js detectado
node -v

REM Check npm
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm no está instalado
    exit /b 1
)

echo ✅ npm detectado
npm -v
echo.

REM Install dependencies
echo 📦 Instalando dependencias...
echo.

call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error instalando dependencias
    exit /b 1
)

echo.
echo ✅ Dependencias instaladas
echo.

REM Install chrome-devtools-mcp globally
echo 🌐 Instalando chrome-devtools-mcp globalmente...
call npm install -g chrome-devtools-mcp@latest

if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Error instalando chrome-devtools-mcp (puede que ya esté instalado)
) else (
    echo ✅ chrome-devtools-mcp instalado
)

echo.

REM Install Playwright browsers
echo 🌐 Instalando navegadores de Playwright...
call npx playwright install chromium

if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Error instalando navegadores Playwright
) else (
    echo ✅ Navegadores instalados
)

echo.

REM Create directories
echo 📁 Creando directorios de reportes...
if not exist "..\reports\html" mkdir "..\reports\html"
if not exist "..\reports\json" mkdir "..\reports\json"
if not exist "..\screenshots" mkdir "..\screenshots"
if not exist "..\videos" mkdir "..\videos"
echo ✅ Directorios creados

echo.

REM Check if services are running
echo 🔍 Verificando servicios...
echo.

curl -s http://localhost:3002 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Frontend corriendo en http://localhost:3002
) else (
    echo ⚠️  Frontend NO está corriendo en http://localhost:3002
    echo    Ejecuta: cd frontend ^&^& npm start
)

curl -s http://localhost:8000/docs >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Backend corriendo en http://localhost:8000
) else (
    echo ⚠️  Backend NO está corriendo en http://localhost:8000
    echo    Ejecuta: cd backend ^&^& python -m uvicorn main:app --reload
)

echo.
echo ==========================================================================
echo ✅ Setup completo!
echo ==========================================================================
echo.
echo Para ejecutar las pruebas:
echo   npm test                    # Ejecutar todos los tests
echo   npm run test:headless       # Ejecutar en modo headless
echo   npm run report              # Ver reporte HTML
echo.
echo Documentación:
echo   type README.md              # Ver documentación completa
echo.
echo ==========================================================================
echo.

pause
