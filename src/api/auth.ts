import type { AuthUser } from '@/types/auth'

export type LoginResponse = AuthUser

export async function loginAPI(username: string, password: string): Promise<LoginResponse> {
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.message || '登录失败')
  }
  const data = (await res.json()) as LoginResponse
  if (!data.roles) data.roles = []
  return data
}

export async function logoutAPI(refreshToken?: string): Promise<void> {
  try {
    await fetch('/api/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken: refreshToken ?? '' }),
    })
  } catch {
    /* 静默失败：登出时后端不可达不应阻塞前端清理 */
  }
}

export async function getMeAPI(): Promise<AuthUser | null> {
  const user = JSON.parse(
    localStorage.getItem('auth_user') || sessionStorage.getItem('auth_user') || 'null',
  ) as AuthUser | null
  if (!user?.token) return null

  const res = await fetch('/api/me', {
    headers: { Authorization: `Bearer ${user.token}` },
  })
  if (!res.ok) return null
  const data = (await res.json()) as AuthUser
  data.token = user.token
  data.refreshToken = user.refreshToken
  if (!data.roles) data.roles = []
  return data
}
