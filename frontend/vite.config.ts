import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import electron from 'vite-plugin-electron/simple'
import path from "path"

// https://vite.dev/config/
export default defineConfig({
  base: "./",
  plugins: [
    react(), 
    tailwindcss(),
    electron({
      main: {
        entry: path.resolve(__dirname, '../electron-app/main.ts'),
      },
      preload: {
        input: path.resolve(__dirname, '../electron-app/preload.ts'),
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
