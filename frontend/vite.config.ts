import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths'
import dotenv from 'dotenv';

dotenv.config({ path: __dirname + '../../.envs/dev/react.env' });

const hostVal = process.env.HOST ? process.env.HOST.toString() : '0.0.0.0'
const portVal = process.env.PORT ? Number(process.env.PORT) : 3000

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    watch: {
      usePolling: true,
    },
    host: hostVal,
    strictPort: true,
    port: portVal,
  },
  define: {
    'process.env': process.env
  }
});
