/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly API_BACKEND_URL: string;
  readonly HOST: string;
  readonly PORT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
