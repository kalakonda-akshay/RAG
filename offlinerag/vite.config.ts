import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// IMPORTANT: When deploying to GitHub Pages at
// https://YOUR_USERNAME.github.io/OfflineRAG/
// set `base` below to "/OfflineRAG/". If you deploy to a custom domain
// or to the root of your Pages site, leave it as "/".
export default defineConfig({
  base: "/",
  plugins: [react()],
});
