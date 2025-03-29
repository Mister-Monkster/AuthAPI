import { defineConfig } from 'vite'
import fs from 'fs';  // Импортируем модуль fs
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),
    tailwindcss(),
  ],

  // css: {
  //   postcss: {
  //     plugins: [tailwindcss()],
  //   }
  // }

})
