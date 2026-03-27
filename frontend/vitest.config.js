// frontend/vitest.config.js
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.js'],
    include: ['**/*.{test,spec}.{js,jsx}'],
    exclude: ['**/node_modules/**', '**/tests/e2e/**'],
    
    maxWorkers: 4,        
    isolate: true,       
    // vmMemoryLimit: '300Mb', 
    
    testTimeout: 30000,
    hookTimeout: 30000,
    
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{js,jsx}'],
      exclude: ['src/main.jsx', 'src/**/*.test.{js,jsx}'],
    },
  }
})