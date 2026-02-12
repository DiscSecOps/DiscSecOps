// frontend/src/services/auth.service.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const authService = {
  /**
   * Login user with session-based auth
   * Sets HTTP-only cookie automatically
   */
  async login(email, password) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email,
        password
      }, {
        withCredentials: true  // ESSENTIAL for cookies!
      });
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Login failed';
      console.error('Login error:', errorMsg);
      throw new Error(errorMsg);
    }
  },

  /**
   * Register new user
   */
  async register(email, password, username = '', full_name = '') {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        email,
        password,
        username,
        full_name
      });
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Registration failed';
      console.error('Register error:', errorMsg);
      throw new Error(errorMsg);
    }
  },

  /**
   * Logout user (invalidates session)
   */
  async logout() {
    try {
      const response = await axios.post(`${API_URL}/auth/logout`, {}, {
        withCredentials: true
      });
      return response.data;
    } catch (err) {
      console.warn('Logout error (might be already logged out):', err.message);
      return { success: true }; // Still consider it successful
    }
  },

  /**
   * Check if user is authenticated
   * Tries to access a protected endpoint
   */
  async checkAuth() {
    try {
      // Try ANY protected endpoint - maybe dashboard or user profile
      const response = await axios.get(`${API_URL}/dashboard`, {
        withCredentials: true
      });

      // If we get user data in response, return it
      if (response.data.user) {
        return { authenticated: true, user: response.data.user };
      }

      return { authenticated: true };
    } catch (err) {
      // 401/403 means not authenticated
      if (err.response?.status === 401 || err.response?.status === 403) {
        return { authenticated: false };
      }

      // Other errors (network, server down)
      console.warn('Auth check failed:', err.message);
      return { authenticated: false };
    }
  }
};