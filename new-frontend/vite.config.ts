import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// In dev, requests to /api are proxied to your backend so there are no CORS issues.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: { '/api': { target: env.VITE_BACKEND_URL || 'http://localhost:8000', changeOrigin: true } },
    },
  };
});
