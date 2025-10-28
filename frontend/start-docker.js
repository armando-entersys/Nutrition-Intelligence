#!/usr/bin/env node

// Simple start script para evitar conflictos
const { execSync } = require('child_process');

console.log('🚀 Iniciando frontend de Nutrition Intelligence...');

try {
  // Set environment variables
  process.env.HOST = '0.0.0.0';
  process.env.PORT = '3000';
  process.env.GENERATE_SOURCEMAP = 'false';
  process.env.REACT_APP_API_URL = 'http://localhost:8001';
  
  console.log('✅ Variables de entorno configuradas');
  
  // Start React dev server
  execSync('npx react-scripts start', { 
    stdio: 'inherit',
    cwd: process.cwd()
  });
} catch (error) {
  console.error('❌ Error iniciando el servidor:', error);
  process.exit(1);
}