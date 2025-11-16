/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

import axios from 'axios';
import { API_BASE_URL } from '../config/api';

const AUTH_ENDPOINT = `${API_BASE_URL}/api/v1/auth`;

// Token storage keys
const ACCESS_TOKEN_KEY = 'nutrition_access_token';
const REFRESH_TOKEN_KEY = 'nutrition_refresh_token';
const USER_DATA_KEY = 'nutrition_user';

class AuthService {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} - Registered user data
   */
  async register(userData) {
    try {
      // Clean up data: remove nutritionist_email if empty
      const cleanedData = { ...userData };
      if (!cleanedData.nutritionist_email || cleanedData.nutritionist_email.trim() === '') {
        delete cleanedData.nutritionist_email;
      }

      const response = await axios.post(`${AUTH_ENDPOINT}/register`, cleanedData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} - Login response with tokens
   */
  async login(email, password) {
    try {
      const response = await axios.post(`${AUTH_ENDPOINT}/login`, {
        email,
        password
      });

      const { access_token, refresh_token, user } = response.data;

      // Store tokens and user data
      this.setTokens(access_token, refresh_token);
      this.setUser(user);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      await axios.post(`${AUTH_ENDPOINT}/logout`, {}, {
        headers: this.getAuthHeaders()
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage regardless of API call result
      this.clearAuth();
    }
  }

  /**
   * Request password reset
   * @param {string} email - User email
   * @returns {Promise<Object>} - Reset request response
   */
  async forgotPassword(email) {
    try {
      const response = await axios.post(`${AUTH_ENDPOINT}/forgot-password`, {
        email
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Reset password with token
   * @param {string} token - Reset token
   * @param {string} newPassword - New password
   * @param {string} confirmPassword - Password confirmation
   * @returns {Promise<Object>} - Reset response
   */
  async resetPassword(token, newPassword, confirmPassword) {
    try {
      const response = await axios.post(`${AUTH_ENDPOINT}/reset-password`, {
        token,
        new_password: newPassword,
        confirm_password: confirmPassword
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get current user data
   * @returns {Object|null} - User data or null
   */
  getCurrentUser() {
    const userData = localStorage.getItem(USER_DATA_KEY);
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Get access token
   * @returns {string|null} - Access token or null
   */
  getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  /**
   * Get refresh token
   * @returns {string|null} - Refresh token or null
   */
  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  /**
   * Check if user is authenticated
   * @returns {boolean} - True if authenticated
   */
  isAuthenticated() {
    return !!this.getAccessToken();
  }

  /**
   * Set tokens in local storage
   * @param {string} accessToken - Access token
   * @param {string} refreshToken - Refresh token
   */
  setTokens(accessToken, refreshToken) {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }

  /**
   * Set user data in local storage
   * @param {Object} user - User data
   */
  setUser(user) {
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(user));
  }

  /**
   * Clear all authentication data
   */
  clearAuth() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_DATA_KEY);
  }

  /**
   * Get authorization headers
   * @returns {Object} - Headers with authorization
   */
  getAuthHeaders() {
    const token = this.getAccessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  /**
   * Handle API errors
   * @param {Error} error - Axios error
   * @returns {Error} - Formatted error
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.message || 'An error occurred';
      const errorObj = new Error(message);
      errorObj.status = error.response.status;
      errorObj.data = error.response.data;
      return errorObj;
    } else if (error.request) {
      // Request made but no response
      return new Error('No response from server. Please check your connection.');
    } else {
      // Error in request setup
      return new Error(error.message || 'An error occurred');
    }
  }

  /**
   * Validate email format
   * @param {string} email - Email to validate
   * @returns {boolean} - True if valid
   */
  validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  /**
   * Validate password strength
   * @param {string} password - Password to validate
   * @returns {Object} - Validation result
   */
  validatePassword(password) {
    const result = {
      isValid: true,
      errors: []
    };

    if (password.length < 8) {
      result.isValid = false;
      result.errors.push('Password must be at least 8 characters');
    }

    if (!/[A-Z]/.test(password)) {
      result.isValid = false;
      result.errors.push('Password must contain at least one uppercase letter');
    }

    if (!/[a-z]/.test(password)) {
      result.isValid = false;
      result.errors.push('Password must contain at least one lowercase letter');
    }

    if (!/\d/.test(password)) {
      result.isValid = false;
      result.errors.push('Password must contain at least one number');
    }

    return result;
  }

  /**
   * Get password strength
   * @param {string} password - Password to check
   * @returns {Object} - Strength info
   */
  getPasswordStrength(password) {
    let strength = 0;
    const checks = {
      length: password.length >= 8,
      lowercase: /[a-z]/.test(password),
      uppercase: /[A-Z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };

    strength = Object.values(checks).filter(Boolean).length;

    const levels = {
      0: { text: 'Very Weak', color: '#f44336', percent: 0 },
      1: { text: 'Weak', color: '#ff9800', percent: 20 },
      2: { text: 'Fair', color: '#ffeb3b', percent: 40 },
      3: { text: 'Good', color: '#8bc34a', percent: 60 },
      4: { text: 'Strong', color: '#4caf50', percent: 80 },
      5: { text: 'Very Strong', color: '#2196f3', percent: 100 }
    };

    return {
      ...levels[strength],
      checks
    };
  }
}

// Export singleton instance
const authService = new AuthService();
export default authService;
