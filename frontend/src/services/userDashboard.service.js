// frontend/src/services/userDashboard.service.js
import axios from 'axios';
import { API_BASE_URL } from '../config/index';
/*
// Use environment variable for API URL (DevSecOps best practice)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
*/

export const userDashboardService = {
  async getUserDashboardData() {
    try {
      // Use the /auth/me endpoint to get current user info (and any other dashboard data you want to include)
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        withCredentials: true
      });
      
      // Return the user data and any additional dashboard-specific data you want to include
      return {
        user: response.data,
        // you cand add more dashboard-specific data here in the future, e.g. stats, notifications, etc.
      };
    } catch (error) {
      console.error('User Dashboard service error:', error);
      throw error;
    }
  }
};