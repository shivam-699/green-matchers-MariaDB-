import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173, // Changed to default Vite port
    headers: {
      'Content-Security-Policy': "script-src 'self' 'unsafe-inline' blob:; worker-src 'self' blob:"
    }
  },
  build: {
    target: 'esnext',
    sourcemap: false
  },
  define: {
    'process.env.NODE_ENV': '"production"'
  },
  css: {
    postcss: './postcss.config.js' // Ensure this points to your PostCSS config
  }
})