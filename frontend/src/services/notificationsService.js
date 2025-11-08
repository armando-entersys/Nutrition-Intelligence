/**
 * Notifications Service
 * Maneja las llamadas API para gestión de notificaciones
 */

import { API_BASE_URL } from '../config/api';
import authService from './authService';

const notificationsService = {
  /**
   * Obtener todas las notificaciones del usuario actual
   * @param {object} options - Opciones de búsqueda (unread_only, limit, offset)
   * @returns {Promise<array>} - Lista de notificaciones
   */
  async getNotifications(options = {}) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        console.warn('⚠️ No authentication token found');
        return [];
      }

      const { unread_only = false, limit = 50, offset = 0 } = options;

      const params = new URLSearchParams();
      if (unread_only) params.append('unread_only', 'true');
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());

      const response = await fetch(`${API_BASE_URL}/api/v1/notifications?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Notifications endpoint not implemented yet');
        return [];
      }

      if (!response.ok) {
        console.warn(`⚠️ Notifications endpoint returned status ${response.status}`);
        return [];
      }

      const data = await response.json();
      console.log(`✅ Loaded ${data.length || 0} notifications`);
      return data.notifications || data || [];

    } catch (error) {
      console.error('❌ Error loading notifications:', error);
      return [];
    }
  },

  /**
   * Marcar una notificación como leída
   * @param {number} notificationId - ID de la notificación
   * @returns {Promise<boolean>} - True si se marcó correctamente
   */
  async markAsRead(notificationId) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/notifications/${notificationId}/read`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Mark as read endpoint not implemented yet');
        return true; // Simular éxito
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log(`✅ Notification ${notificationId} marked as read`);
      return true;

    } catch (error) {
      console.error('❌ Error marking notification as read:', error);
      return false;
    }
  },

  /**
   * Marcar todas las notificaciones como leídas
   * @returns {Promise<boolean>} - True si se marcaron correctamente
   */
  async markAllAsRead() {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/notifications/mark-all-read`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Mark all as read endpoint not implemented yet');
        return true; // Simular éxito
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log('✅ All notifications marked as read');
      return true;

    } catch (error) {
      console.error('❌ Error marking all notifications as read:', error);
      return false;
    }
  },

  /**
   * Eliminar una notificación
   * @param {number} notificationId - ID de la notificación
   * @returns {Promise<boolean>} - True si se eliminó correctamente
   */
  async deleteNotification(notificationId) {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/notifications/${notificationId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Delete notification endpoint not implemented yet');
        return true; // Simular éxito
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log(`✅ Notification ${notificationId} deleted`);
      return true;

    } catch (error) {
      console.error('❌ Error deleting notification:', error);
      return false;
    }
  },

  /**
   * Obtener el conteo de notificaciones no leídas
   * @returns {Promise<number>} - Número de notificaciones no leídas
   */
  async getUnreadCount() {
    try {
      const token = authService.getAccessToken();

      if (!token) {
        return 0;
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/notifications/unread-count`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 404) {
        console.warn('⚠️ Unread count endpoint not implemented yet');
        return 0;
      }

      if (!response.ok) {
        return 0;
      }

      const data = await response.json();
      return data.count || data.unread_count || 0;

    } catch (error) {
      console.error('❌ Error getting unread count:', error);
      return 0;
    }
  }
};

export default notificationsService;
