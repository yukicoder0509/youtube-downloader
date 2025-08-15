import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "dist",
  },
  server: {},
  preview: {
    fallback: true,
  },
});
