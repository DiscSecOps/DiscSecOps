// frontend/src/services/circle.service.js
import api from './api';  

const BASE_URL = '/circles'; 

export const circleService = {
  getMyCircles: async () => {
    try {
      const response = await api.get(`${BASE_URL}/my`);
      return response.data;
    } catch (error) {
      console.error('Error fetching circles:', error);
      throw error;
    }
  },

  getCircle: async (circleId) => {
    try {
      const response = await api.get(`${BASE_URL}/${circleId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching circle:', error);
      throw error;
    }
  },

  createCircle: async (circleData) => {
    try {
      const response = await api.post(BASE_URL, circleData);
      return response.data;
    } catch (error) {
      console.error('Error creating circle:', error);
      throw error;
    }
  }
};