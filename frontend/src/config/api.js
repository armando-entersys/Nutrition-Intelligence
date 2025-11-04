// API Configuration for Nutrition Intelligence Platform
// Supports environment variable override or defaults to relative URLs for production

// Use environment variable if available, otherwise:
// - Development: use localhost:8000
// - Production: use empty string (relative URLs) to let Nginx proxy handle routing
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : '');

// API Endpoints
export const API_ENDPOINTS = {
  // Health & System
  HEALTH: `${API_BASE_URL}/health`,

  // Core Data
  FOODS: `${API_BASE_URL}/api/v1/foods`,
  RECIPES: `${API_BASE_URL}/api/v1/recipes`,
  EQUIVALENCES: `${API_BASE_URL}/api/v1/equivalences`,
  PATIENTS: `${API_BASE_URL}/api/v1/patients`,

  // Calculations & Planning
  NUTRITION_CALCULATOR: `${API_BASE_URL}/api/v1/nutrition-calculator`,
  MEAL_PLANS: `${API_BASE_URL}/api/v1/meal-plans`,
  WEEKLY_PLANNING: `${API_BASE_URL}/api/v1/weekly-planning`,

  // AI Services
  VISION: `${API_BASE_URL}/api/v1/vision`,

  // Authentication
  AUTH: `${API_BASE_URL}/api/v1/auth`,

  // Documentation
  DOCS: `${API_BASE_URL}/docs`,
  REDOC: `${API_BASE_URL}/redoc`,
};

// Development helper - log API configuration in console
if (process.env.NODE_ENV === 'development') {
  console.log('🌐 API Configuration:', {
    baseUrl: API_BASE_URL,
    environment: process.env.NODE_ENV,
    fromEnvVar: !!process.env.REACT_APP_API_BASE_URL
  });
}

export default {
  API_BASE_URL,
  API_ENDPOINTS
};