import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Crucial for Docker
    port: 3000,      // Force port 3000
    watch: {
      usePolling: true // Helps with file changes in Docker on Windows
    }
  }
})