import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

// Chemins vers vos certificats SSL/TLS
const sslCertPath = path.resolve(__dirname, '/cert/cert.pem')
const sslKeyPath = path.resolve(__dirname, '/cert/key.pem')

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 4000,
    https: {
      key: fs.readFileSync(sslKeyPath),
      cert: fs.readFileSync(sslCertPath)
    },
    wss: true,
    origin: 'https://localhost:4000/',
  }
})



