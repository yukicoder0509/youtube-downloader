import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "../backend/backend/frontend-dist",
  },
  server: {},
  preview: {
    fallback: true,
  },
});
