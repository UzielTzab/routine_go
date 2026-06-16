import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true
      },
      includeAssets: ['favicon.ico', 'images/routine_go_logo.png'],
      manifestFilename: 'manifest.json',
      manifest: {
        name: 'Uziel OS',
        short_name: 'UzielOS',
        description: 'Gestor personal de rutinas y alto rendimiento',
        theme_color: '#B8B7FF',
        background_color: '#E9E9FB',
        display: 'standalone',
        icons: [
          {
            src: '/images/routine_go_logo.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/images/routine_go_logo.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
})
