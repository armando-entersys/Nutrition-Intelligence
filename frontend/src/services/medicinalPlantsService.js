/**
 * Medicinal Plants Service
 * API calls for Mexican Medicinal Plants module
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const medicinalPlantsService = {
  /**
   * Get all medicinal plants with filters and pagination
   */
  async getPlants(params = {}) {
    try {
      const response = await axios.get(`${API_BASE_URL}/medicinal-plants/`, {
        params: {
          category: params.category,
          evidence_level: params.evidenceLevel,
          safety_level: params.safetyLevel,
          search: params.search,
          page: params.page || 1,
          page_size: params.pageSize || 20
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching medicinal plants:', error);
      throw error;
    }
  },

  /**
   * Get a specific plant by ID
   */
  async getPlantById(plantId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/medicinal-plants/${plantId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching plant ${plantId}:`, error);
      throw error;
    }
  },

  /**
   * Search plants by health condition
   */
  async searchByCondition(condition) {
    try {
      const response = await axios.get(`${API_BASE_URL}/medicinal-plants/search/by-condition`, {
        params: { condition }
      });
      return response.data;
    } catch (error) {
      console.error('Error searching plants by condition:', error);
      throw error;
    }
  },

  /**
   * Get plant categories for filters
   */
  getCategories() {
    return [
      { value: 'DIGESTIVE', label: 'Digestivas' },
      { value: 'RESPIRATORY', label: 'Respiratorias' },
      { value: 'CALMING', label: 'Calmantes' },
      { value: 'METABOLIC', label: 'Metabólicas' },
      { value: 'ANTI_INFLAMMATORY', label: 'Antiinflamatorias' },
      { value: 'SKIN_HAIR', label: 'Piel y Cabello' },
      { value: 'PAIN_RELIEF', label: 'Alivio del Dolor' },
      { value: 'IMMUNE_SUPPORT', label: 'Apoyo Inmune' },
      { value: 'FEMALE_HEALTH', label: 'Salud Femenina' },
      { value: 'MEMORY_COGNITION', label: 'Memoria y Cognición' },
      { value: 'URINARY', label: 'Urinarias' },
      { value: 'OTHER', label: 'Otras' }
    ];
  },

  /**
   * Get evidence levels for filters
   */
  getEvidenceLevels() {
    return [
      { value: 'STRONG_EVIDENCE', label: 'Evidencia Fuerte' },
      { value: 'MODERATE_EVIDENCE', label: 'Evidencia Moderada' },
      { value: 'TRADITIONAL_ONLY', label: 'Solo Tradicional' }
    ];
  },

  /**
   * Get safety levels for filters
   */
  getSafetyLevels() {
    return [
      { value: 'VERY_SAFE', label: 'Muy Segura' },
      { value: 'SAFE', label: 'Segura' },
      { value: 'MODERATE', label: 'Precaución Moderada' }
    ];
  }
};

export default medicinalPlantsService;
