// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // host for container
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Forward API requests to backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
});