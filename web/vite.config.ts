import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// BASE_PATH permite publicar em subpasta (ex.: GitHub Pages: /AprenderIngl-schunks/).
export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  plugins: [react()],
});
