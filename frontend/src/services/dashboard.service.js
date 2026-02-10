// frontend/src/services/dashboard.service.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const dashboardService = {
  async getDashboardData() {
    try {
      const response = await axios.get(`${API_URL}/dashboard`, {
        withCredentials: true // 👈 Important for session cookies!
      });
      return response.data;
    } catch (error) {
      console.error('Dashboard service error:', error);
      throw error;
    }
  }
};