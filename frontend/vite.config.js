import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/app/",
  build: {
    outDir: "../static/react",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: {
      // Así en desarrollo puedes usar fetch("/api/...") igual que en producción
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
