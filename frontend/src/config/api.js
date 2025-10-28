// API Configuration
// Force the correct URL since environment variables might not be loading properly
export const API_BASE_URL = 'http://localhost:8001';

export const API_ENDPOINTS = {
  HEALTH: `${API_BASE_URL}/health`,
  FOODS: `${API_BASE_URL}/api/v1/foods`,
  RECIPES: `${API_BASE_URL}/api/v1/recipes`,
  EQUIVALENCES: `${API_BASE_URL}/api/v1/equivalences`,
  NUTRITION_CALCULATOR: `${API_BASE_URL}/api/v1/nutrition-calculator`,
  DOCS: `${API_BASE_URL}/docs`
};

export default {
  API_BASE_URL,
  API_ENDPOINTS
};