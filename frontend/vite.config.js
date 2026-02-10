// vite.config.js - version corrected - use that
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
 
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // host for container
    port: 3000, // force Vite dev server to run on port 3000
    strictPort: true,  // exit if port is already in use
    hmr: {
      port: 3001, // 👈 FIX port for HMR
    },
    watch: {
      usePolling: true // For dev containers
    },
    open: true, // Automatically open browser on startup
    // 👇 PROXY ADDED by feature/test-env-setup (GOOD!)
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Forward API requests to backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
})