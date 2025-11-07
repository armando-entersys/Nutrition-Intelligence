/**
 * Dashboard Service
 * Maneja las llamadas API para obtener estadísticas y datos del dashboard
 * por rol (admin, nutritionist, patient)
 */

import { API_BASE_URL } from '../config/api';
import authService from './authService';

const dashboardService = {
  /**
   * Obtener estadísticas del dashboard según el rol del usuario
   * @param {string} role - El rol del usuario ('admin', 'nutritionist', 'patient')
   * @returns {Promise<object>} - Datos del dashboard específicos del rol
   */
  async getDashboardStats(role) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/dashboard/${role}/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        // Si el endpoint no existe aún, retornar datos por defecto
        console.warn(`⚠️ Dashboard stats endpoint not implemented yet for role: ${role}`);
        return this.getDefaultStats(role);
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Dashboard stats loaded:', data);
      return data;

    } catch (error) {
      console.error('❌ Error loading dashboard stats:', error);

      // En caso de error, retornar datos por defecto como fallback
      console.warn(`⚠️ Using fallback data for role: ${role}`);
      return this.getDefaultStats(role);
    }
  },

  /**
   * Obtener próximas citas (para nutricionistas)
   * @returns {Promise<array>} - Lista de próximas citas
   */
  async getUpcomingAppointments() {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/appointments/upcoming`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Appointments endpoint not implemented yet');
        return [];
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.appointments || data || [];

    } catch (error) {
      console.error('❌ Error loading appointments:', error);
      return [];
    }
  },

  /**
   * Obtener alertas de pacientes (para nutricionistas)
   * @returns {Promise<array>} - Lista de alertas
   */
  async getPatientAlerts() {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients/alerts`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Patient alerts endpoint not implemented yet');
        return [];
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.alerts || data || [];

    } catch (error) {
      console.error('❌ Error loading patient alerts:', error);
      return [];
    }
  },

  /**
   * Datos por defecto cuando el backend no está disponible
   * Esto permite que el frontend funcione mientras se implementan los endpoints
   * @param {string} role - El rol del usuario
   * @returns {object} - Datos por defecto del dashboard
   */
  getDefaultStats(role) {
    const defaults = {
      admin: {
        totalUsers: 0,
        activeNutritionists: 0,
        activePatients: 0,
        totalPatients: 0,
        systemHealth: "Inicializando...",
        monthlyCalculations: 0,
        monthlyPlans: 0,
        aiQueries: 0,
        dailyLogins: 0,
        _isDefault: true
      },
      nutritionist: {
        activePatients: 0,
        weeklyPlansCreated: 0,
        pendingReviews: 0,
        avgPatientSatisfaction: 0,
        thisWeekConsultations: 0,
        completedPlans: 0,
        todayAppointments: 0,
        pending24hRecalls: 0,
        pendingPhotoAnalysis: 0,
        unreadMessages: 0,
        _isDefault: true
      },
      patient: {
        currentPlan: "Sin plan asignado",
        todayProgress: 0,
        weeklyAdherence: 0,
        favoriteRecipes: 0,
        nextAppointment: null,
        totalEquivalentsToday: 0,
        todayCalories: 0,
        weekProgress: 0,
        _isDefault: true
      }
    };

    return defaults[role] || {};
  }
};

export default dashboardService;
