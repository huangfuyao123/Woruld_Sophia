/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_MOCK_USERS?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
