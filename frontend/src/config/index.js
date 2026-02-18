// frontend/src/config/index.js
const getApiBaseUrl = () => {
  // Production: use versioned API path from environment or default
  if (import.meta.env.PROD) {
    return import.meta.env.VITE_API_BASE_URL || '/api/v1';
  }
  
  // Development: from .env or .env.development
  // Must match backend's API_V1_STR setting (default: /api/v1)
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
};

export const API_BASE_URL = getApiBaseUrl();