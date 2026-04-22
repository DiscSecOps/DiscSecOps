// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/frontend/',
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000, // force Vite dev server to run on port 3000
    strictPort: true,
    watch: { usePolling: true },
    open: true, // Automatically open browser on startup
  },
});