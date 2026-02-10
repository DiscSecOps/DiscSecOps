// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
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
  },
});