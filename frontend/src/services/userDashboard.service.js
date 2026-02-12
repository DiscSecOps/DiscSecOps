// frontend/src/services/userDashboard.service.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const userDashboardService = {
  async getUserDashboardData() {
    try {
      const response = await axios.get(`${API_URL}/user-dashboard`, {
        withCredentials: true // 👈 Important for session cookies!
      });
      return response.data;
    } catch (error) {
      console.error('User Dashboard service error:', error);
      throw error;
    }
  }
};