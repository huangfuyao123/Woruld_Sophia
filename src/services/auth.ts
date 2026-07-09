// ============================================================
//  认证服务层（纯后端，无 mock）
// ============================================================

import type { AuthUser } from '@/types/auth'

export type { AuthUser } from '@/types/auth'

export type LoginResult = { success: true; user: AuthUser } | { success: false; error: string }

const STORAGE_KEY = 'auth_user'

type StorageMode = 'local' | 'session'

function getStorage(mode: StorageMode): Storage {
  return mode === 'session' ? window.sessionStorage : window.localStorage
}

function parseStoredUser(raw: string | null): AuthUser | null {
  if (!raw) return null
  try {
    const data = JSON.parse(raw) as Partial<AuthUser>
    if (data.id && data.username && data.token && Array.isArray(data.roles)) {
      return data as AuthUser
    }
  } catch {
    /* fallthrough */
  }
  return null
}

function clearInvalidStoredUser(mode: StorageMode): void {
  getStorage(mode).removeItem(STORAGE_KEY)
}

async function loginWithBackend(username: string, password: string): Promise<LoginResult> {
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { message?: string }
      return { success: false, error: body.message ?? '登录失败' }
    }
    const data = (await res.json()) as AuthUser
    if (!data.roles) data.roles = []
    return { success: true, user: data }
  } catch {
    return { success: false, error: '登录服务暂不可用，请检查后端是否启动' }
  }
}

export async function loginRequest(username: string, password: string): Promise<LoginResult> {
  return loginWithBackend(username, password)
}

export function loadUser(): AuthUser | null {
  const localUser = parseStoredUser(window.localStorage.getItem(STORAGE_KEY))
  if (localUser) return localUser
  if (window.localStorage.getItem(STORAGE_KEY)) clearInvalidStoredUser('local')

  const sessionUser = parseStoredUser(window.sessionStorage.getItem(STORAGE_KEY))
  if (sessionUser) return sessionUser
  if (window.sessionStorage.getItem(STORAGE_KEY)) clearInvalidStoredUser('session')

  return null
}

export function persistUser(user: AuthUser, rememberMe = true): void {
  const targetMode: StorageMode = rememberMe ? 'local' : 'session'
  const otherMode: StorageMode = rememberMe ? 'session' : 'local'

  getStorage(targetMode).setItem(STORAGE_KEY, JSON.stringify(user))
  getStorage(otherMode).removeItem(STORAGE_KEY)
}

export function clearUser(): void {
  window.localStorage.removeItem(STORAGE_KEY)
  window.sessionStorage.removeItem(STORAGE_KEY)
}

export function updatePersistedUser(patch: Partial<AuthUser>): AuthUser | null {
  const localUser = parseStoredUser(window.localStorage.getItem(STORAGE_KEY))
  if (localUser) {
    const nextUser: AuthUser = { ...localUser, ...patch }
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser))
    return nextUser
  }

  const sessionUser = parseStoredUser(window.sessionStorage.getItem(STORAGE_KEY))
  if (sessionUser) {
    const nextUser: AuthUser = { ...sessionUser, ...patch }
    window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser))
    return nextUser
  }

  return null
}

export function getStoredRefreshToken(): string | null {
  return loadUser()?.refreshToken ?? null
}

export const AUTH_STORAGE_KEY = STORAGE_KEY
export const LOGIN_SUCCESS_MESSAGE = 'netclub:login-success'
