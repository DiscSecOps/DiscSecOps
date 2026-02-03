// frontend/src/services/auth.service.js
import axios from 'axios';
 
const API_URL = 'http://localhost:5000/api/auth';
 
// Service for authentication-related API calls
export const authService = {
  async login(username, password) {
    try {
      const response = await axios.post(`${API_URL}/login`, {
        username,
        password
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Login failed' };
    }
  },
 
  // Register a new user
  async register(username, password) {
    try {
      const response = await axios.post(`${API_URL}/register`, {
        username,
        password
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Registration failed' };
    }
  }
};