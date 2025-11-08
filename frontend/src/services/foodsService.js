/**
 * Foods Service
 * Maneja las llamadas API para búsqueda y gestión de alimentos
 */

import { API_BASE_URL } from '../config/api';
import authService from './authService';

const foodsService = {
  /**
   * Buscar alimentos por nombre
   * @param {string} query - Término de búsqueda
   * @param {object} options - Opciones de búsqueda (limit, offset, status, category)
   * @returns {Promise<array>} - Lista de alimentos encontrados
   */
  async searchFoods(query, options = {}) {
    try {
      const { limit = 20, offset = 0, status = null, category = null } = options;

      const params = new URLSearchParams();
      if (query) params.append('search', query);
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      if (status) params.append('status', status);
      if (category) params.append('category', category);

      const response = await fetch(`${API_BASE_URL}/api/v1/foods?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        console.warn(`⚠️ Foods search returned status ${response.status}`);
        // Return empty array if search fails
        return [];
      }

      const data = await response.json();
      console.log(`✅ Found ${data.length} foods for query: "${query}"`);
      return data;

    } catch (error) {
      console.error('❌ Error searching foods:', error);
      // Return empty array on error instead of throwing
      return [];
    }
  },

  /**
   * Obtener detalles de un alimento específico
   * @param {number} foodId - ID del alimento
   * @returns {Promise<object>} - Datos del alimento
   */
  async getFood(foodId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/foods/${foodId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;

    } catch (error) {
      console.error('❌ Error loading food:', error);
      return null;
    }
  },

  /**
   * Crear un nuevo alimento (requiere autenticación)
   * @param {object} foodData - Datos del nuevo alimento
   * @returns {Promise<object>} - Alimento creado
   */
  async createFood(foodData) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/foods`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(foodData)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Food created:', data);
      return data;

    } catch (error) {
      console.error('❌ Error creating food:', error);
      throw error;
    }
  },

  /**
   * Obtener alimentos con filtros avanzados
   * @param {object} filters - Filtros de búsqueda
   * @returns {Promise<array>} - Lista de alimentos
   */
  async getFoods(filters = {}) {
    try {
      const {
        search = '',
        limit = 50,
        offset = 0,
        status = null,
        category = null
      } = filters;

      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      if (status) params.append('status', status);
      if (category) params.append('category', category);

      const response = await fetch(`${API_BASE_URL}/api/v1/foods?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        console.warn(`⚠️ Foods endpoint returned status ${response.status}`);
        return [];
      }

      const data = await response.json();
      return data;

    } catch (error) {
      console.error('❌ Error loading foods:', error);
      return [];
    }
  },

  /**
   * Datos por defecto cuando el backend no está disponible o no hay resultados
   * @param {string} query - Término de búsqueda
   * @returns {array} - Lista de alimentos por defecto
   */
  getDefaultFoods(query = '') {
    const defaultFoods = [
      {
        id: 1,
        name: 'Tortilla de maíz',
        serving_size: 30,
        calories_per_serving: 64,
        protein_g: 1.5,
        carbs_g: 13.8,
        fat_g: 0.9,
        fiber_g: 1.5,
        category: 'CEREALES',
        status: 'APPROVED'
      },
      {
        id: 2,
        name: 'Frijoles negros cocidos',
        serving_size: 90,
        calories_per_serving: 114,
        protein_g: 7.6,
        carbs_g: 20.4,
        fat_g: 0.5,
        fiber_g: 7.5,
        category: 'LEGUMINOSAS',
        status: 'APPROVED'
      },
      {
        id: 3,
        name: 'Aguacate hass',
        serving_size: 50,
        calories_per_serving: 80,
        protein_g: 1.0,
        carbs_g: 4.3,
        fat_g: 7.3,
        fiber_g: 3.4,
        category: 'GRASAS',
        status: 'APPROVED'
      },
      {
        id: 4,
        name: 'Pechuga de pollo sin piel',
        serving_size: 100,
        calories_per_serving: 165,
        protein_g: 31.0,
        carbs_g: 0,
        fat_g: 3.6,
        fiber_g: 0,
        category: 'CARNES',
        status: 'APPROVED'
      },
      {
        id: 5,
        name: 'Arroz integral cocido',
        serving_size: 150,
        calories_per_serving: 165,
        protein_g: 3.5,
        carbs_g: 34.2,
        fat_g: 1.5,
        fiber_g: 2.8,
        category: 'CEREALES',
        status: 'APPROVED'
      },
      {
        id: 6,
        name: 'Huevo entero',
        serving_size: 50,
        calories_per_serving: 72,
        protein_g: 6.3,
        carbs_g: 0.4,
        fat_g: 4.8,
        fiber_g: 0,
        category: 'CARNES',
        status: 'APPROVED'
      },
      {
        id: 7,
        name: 'Leche descremada',
        serving_size: 240,
        calories_per_serving: 83,
        protein_g: 8.3,
        carbs_g: 12.2,
        fat_g: 0.2,
        fiber_g: 0,
        category: 'LACTEOS',
        status: 'APPROVED'
      },
      {
        id: 8,
        name: 'Plátano tabasco',
        serving_size: 120,
        calories_per_serving: 107,
        protein_g: 1.3,
        carbs_g: 27.3,
        fat_g: 0.4,
        fiber_g: 3.1,
        category: 'FRUTAS',
        status: 'APPROVED'
      },
      {
        id: 9,
        name: 'Brócoli cocido',
        serving_size: 100,
        calories_per_serving: 35,
        protein_g: 2.4,
        carbs_g: 7.2,
        fat_g: 0.4,
        fiber_g: 3.3,
        category: 'VERDURAS',
        status: 'APPROVED'
      },
      {
        id: 10,
        name: 'Aceite de oliva',
        serving_size: 10,
        calories_per_serving: 88,
        protein_g: 0,
        carbs_g: 0,
        fat_g: 10.0,
        fiber_g: 0,
        category: 'GRASAS',
        status: 'APPROVED'
      }
    ];

    if (!query || query.length < 2) {
      return defaultFoods;
    }

    return defaultFoods.filter(food =>
      food.name.toLowerCase().includes(query.toLowerCase())
    );
  }
};

export default foodsService;
