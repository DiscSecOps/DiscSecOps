// frontend/src/config/index.js
const getApiBaseUrl = () => {
  // Production: din .env.production standard '/api' 
  if (import.meta.env.PROD) {
    return '/api';
  }
  
  // Development: from .env.development
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
};

export const API_BASE_URL = getApiBaseUrl();