import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "path"; // Ensure path is imported properly

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"), // Creates @ alias for src/
    },
  },
});
