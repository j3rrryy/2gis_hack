import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite configuration for the house-score-react-final project.
// This configuration enables the React plugin and sets
// sensible defaults for development and production.

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: false
  },
  preview: {
    port: 4173
  },
  build: {
    outDir: 'dist'
  }
});