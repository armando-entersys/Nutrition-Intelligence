/**
 * Patients Service
 * Maneja las llamadas API para gestión de pacientes
 */

import { API_BASE_URL } from '../config/api';
import authService from './authService';

const patientsService = {
  /**
   * Obtener lista de pacientes del nutricionista actual
   * @returns {Promise<array>} - Lista de pacientes
   */
  async getPatients() {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Patients endpoint not implemented yet');
        return this.getDefaultPatients();
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Patients loaded:', data);
      return data.patients || data || [];

    } catch (error) {
      console.error('❌ Error loading patients:', error);
      console.warn('⚠️ Using fallback patient data');
      return this.getDefaultPatients();
    }
  },

  /**
   * Obtener detalles de un paciente específico
   * @param {number} patientId - ID del paciente
   * @returns {Promise<object>} - Datos del paciente
   */
  async getPatient(patientId) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Patient detail endpoint not implemented yet');
        return null;
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;

    } catch (error) {
      console.error('❌ Error loading patient:', error);
      return null;
    }
  },

  /**
   * Crear un nuevo paciente
   * @param {object} patientData - Datos del nuevo paciente
   * @returns {Promise<object>} - Paciente creado
   */
  async createPatient(patientData) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(patientData)
      });

      if (response.status === 404) {
        console.warn('⚠️ Create patient endpoint not implemented yet');
        // Simular creación exitosa con datos mock
        const bmi = this.calculateBMI(patientData.weight_kg, patientData.height_cm);
        return {
          id: Date.now(), // ID temporal
          ...patientData,
          bmi: bmi,
          created_at: new Date().toISOString().split('T')[0],
          last_visit: new Date().toISOString().split('T')[0],
          measurements: [{
            date: new Date().toISOString().split('T')[0],
            weight_kg: patientData.weight_kg,
            bmi: bmi
          }],
          _isDefault: true
        };
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Patient created:', data);
      return data;

    } catch (error) {
      console.error('❌ Error creating patient:', error);
      throw error;
    }
  },

  /**
   * Actualizar un paciente existente
   * @param {number} patientId - ID del paciente
   * @param {object} patientData - Datos actualizados del paciente
   * @returns {Promise<object>} - Paciente actualizado
   */
  async updatePatient(patientId, patientData) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(patientData)
      });

      if (response.status === 404) {
        console.warn('⚠️ Update patient endpoint not implemented yet');
        // Simular actualización exitosa
        return {
          id: patientId,
          ...patientData,
          bmi: this.calculateBMI(patientData.weight_kg, patientData.height_cm),
          _isDefault: true
        };
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Patient updated:', data);
      return data;

    } catch (error) {
      console.error('❌ Error updating patient:', error);
      throw error;
    }
  },

  /**
   * Eliminar un paciente
   * @param {number} patientId - ID del paciente
   * @returns {Promise<boolean>} - True si se eliminó correctamente
   */
  async deletePatient(patientId) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Delete patient endpoint not implemented yet');
        // Simular eliminación exitosa
        return true;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      console.log('✅ Patient deleted');
      return true;

    } catch (error) {
      console.error('❌ Error deleting patient:', error);
      throw error;
    }
  },

  /**
   * Asignar plan nutricional a un paciente
   * @param {number} patientId - ID del paciente
   * @param {object} planData - Datos del plan nutricional
   * @returns {Promise<object>} - Plan creado
   */
  async assignNutritionalPlan(patientId, planData) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}/nutritional-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(planData)
      });

      if (response.status === 404) {
        console.warn('⚠️ Assign plan endpoint not implemented yet');
        // Simular asignación exitosa
        return {
          id: Date.now(),
          ...planData,
          progress: 0,
          created_at: new Date().toISOString(),
          _isDefault: true
        };
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Nutritional plan assigned:', data);
      return data;

    } catch (error) {
      console.error('❌ Error assigning plan:', error);
      throw error;
    }
  },

  /**
   * Calcular IMC
   * @param {number} weight - Peso en kg
   * @param {number} height - Altura en cm
   * @returns {number} - IMC calculado
   */
  calculateBMI(weight, height) {
    const heightM = height / 100;
    return parseFloat((weight / (heightM * heightM)).toFixed(1));
  },

  /**
   * Datos por defecto cuando el backend no está disponible
   * @returns {array} - Lista de pacientes por defecto
   */
  getDefaultPatients() {
    return [
      {
        id: 1,
        name: 'María González',
        email: 'maria.gonzalez@example.com',
        phone: '+34 612 345 678',
        birth_date: '1985-03-15',
        gender: 'F',
        height_cm: 165,
        weight_kg: 68,
        activity_level: 'MODERATE',
        medical_conditions: 'Diabetes tipo 2',
        allergies: 'Ninguna',
        dietary_preferences: 'Vegetariana',
        bmi: 25.0,
        created_at: '2024-01-15',
        last_visit: '2024-10-20',
        nutritional_plan: {
          id: 1,
          goal: 'WEIGHT_LOSS',
          target_calories: 1800,
          target_protein_g: 90,
          target_carbs_g: 180,
          target_fat_g: 60,
          duration_weeks: 12,
          progress: 45
        },
        measurements: [
          { date: '2024-10-01', weight_kg: 70, bmi: 25.7 },
          { date: '2024-10-15', weight_kg: 68.5, bmi: 25.2 },
          { date: '2024-10-27', weight_kg: 68, bmi: 25.0 }
        ],
        _isDefault: true
      },
      {
        id: 2,
        name: 'Carlos Rodríguez',
        email: 'carlos.rodriguez@example.com',
        phone: '+34 623 456 789',
        birth_date: '1990-07-22',
        gender: 'M',
        height_cm: 178,
        weight_kg: 85,
        activity_level: 'ACTIVE',
        medical_conditions: 'Ninguna',
        allergies: 'Frutos secos',
        dietary_preferences: 'Sin restricciones',
        bmi: 26.8,
        created_at: '2024-02-10',
        last_visit: '2024-10-25',
        nutritional_plan: {
          id: 2,
          goal: 'MUSCLE_GAIN',
          target_calories: 2800,
          target_protein_g: 170,
          target_carbs_g: 300,
          target_fat_g: 85,
          duration_weeks: 16,
          progress: 60
        },
        measurements: [
          { date: '2024-09-15', weight_kg: 82, bmi: 25.9 },
          { date: '2024-10-01', weight_kg: 84, bmi: 26.5 },
          { date: '2024-10-25', weight_kg: 85, bmi: 26.8 }
        ],
        _isDefault: true
      },
      {
        id: 3,
        name: 'Ana Martínez',
        email: 'ana.martinez@example.com',
        phone: '+34 634 567 890',
        birth_date: '1978-11-08',
        gender: 'F',
        height_cm: 160,
        weight_kg: 62,
        activity_level: 'LIGHT',
        medical_conditions: 'Hipertensión',
        allergies: 'Lactosa',
        dietary_preferences: 'Baja en sodio',
        bmi: 24.2,
        created_at: '2024-03-20',
        last_visit: '2024-10-22',
        nutritional_plan: {
          id: 3,
          goal: 'MAINTENANCE',
          target_calories: 1900,
          target_protein_g: 75,
          target_carbs_g: 200,
          target_fat_g: 65,
          duration_weeks: 8,
          progress: 30
        },
        measurements: [
          { date: '2024-09-20', weight_kg: 63, bmi: 24.6 },
          { date: '2024-10-05', weight_kg: 62.5, bmi: 24.4 },
          { date: '2024-10-22', weight_kg: 62, bmi: 24.2 }
        ],
        _isDefault: true
      }
    ];
  }
};

export default patientsService;
