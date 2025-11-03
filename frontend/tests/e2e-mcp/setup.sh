#!/bin/bash

# ============================================================================
# Nutrition Intelligence - E2E Testing Setup Script
# ============================================================================
# This script sets up the chrome-devtools-mcp testing environment
# ============================================================================

set -e

echo ""
echo "=========================================================================="
echo "🧪 Nutrition Intelligence - E2E Testing Setup"
echo "   Chrome DevTools MCP Configuration"
echo "=========================================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Node.js version
echo "📋 Verificando requisitos previos..."
echo ""

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    echo "   Por favor instala Node.js v18+ desde https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${YELLOW}⚠️  Node.js v18+ recomendado (tienes v$NODE_VERSION)${NC}"
else
    echo -e "${GREEN}✅ Node.js $(node -v)${NC}"
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm no está instalado${NC}"
    exit 1
else
    echo -e "${GREEN}✅ npm $(npm -v)${NC}"
fi

echo ""

# Install dependencies
echo "📦 Instalando dependencias..."
echo ""

npm install

echo ""
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Install chrome-devtools-mcp globally if not installed
if ! npm list -g chrome-devtools-mcp &> /dev/null; then
    echo "🌐 Instalando chrome-devtools-mcp globalmente..."
    npm install -g chrome-devtools-mcp@latest
    echo -e "${GREEN}✅ chrome-devtools-mcp instalado${NC}"
else
    echo -e "${GREEN}✅ chrome-devtools-mcp ya está instalado${NC}"
fi

echo ""

# Install Playwright browsers
echo "🌐 Instalando navegadores de Playwright..."
npx playwright install chromium
npx playwright install-deps chromium || true
echo -e "${GREEN}✅ Navegadores instalados${NC}"

echo ""

# Create directories
echo "📁 Creando directorios de reportes..."
mkdir -p ../reports/html
mkdir -p ../reports/json
mkdir -p ../screenshots
mkdir -p ../videos
echo -e "${GREEN}✅ Directorios creados${NC}"

echo ""

# Check if services are running
echo "🔍 Verificando servicios..."
echo ""

FRONTEND_URL="http://localhost:3002"
BACKEND_URL="http://localhost:8000"

if curl -s "$FRONTEND_URL" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend corriendo en $FRONTEND_URL${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend NO está corriendo en $FRONTEND_URL${NC}"
    echo "   Ejecuta: cd frontend && npm start"
fi

if curl -s "$BACKEND_URL/docs" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend corriendo en $BACKEND_URL${NC}"
else
    echo -e "${YELLOW}⚠️  Backend NO está corriendo en $BACKEND_URL${NC}"
    echo "   Ejecuta: cd backend && python -m uvicorn main:app --reload"
fi

echo ""
echo "=========================================================================="
echo -e "${GREEN}✅ Setup completo!${NC}"
echo "=========================================================================="
echo ""
echo "Para ejecutar las pruebas:"
echo "  npm test                    # Ejecutar todos los tests"
echo "  npm run test:headless       # Ejecutar en modo headless"
echo "  npm run report              # Ver reporte HTML"
echo ""
echo "Documentación:"
echo "  cat README.md               # Ver documentación completa"
echo ""
echo "=========================================================================="
echo ""
