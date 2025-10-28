import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    headers: {
      'Content-Security-Policy': "script-src 'self' 'unsafe-inline' blob:; worker-src 'self' blob:"
    }
  },
  build: {
    // Disable eval in production
    target: 'esnext',
    sourcemap: false
  },
  define: {
    // Prevent eval usage
    'process.env.NODE_ENV': '"production"'
  }
})