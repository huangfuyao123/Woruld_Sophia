import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import { getStoredRefreshToken, updatePersistedUser } from '@/services/auth'

let isRefreshed = false

async function refreshAccessToken(): Promise<string | null> {
  const refresh = getStoredRefreshToken()
  if (!refresh) return null

  try {
    const res = await fetch('/api/token/refresh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    })
    if (!res.ok) return null
    const data = (await res.json()) as { access?: string }
    if (!data.access) return null

    updatePersistedUser({ token: data.access })
    isRefreshed = true
    return data.access
  } catch {
    return null
  }
}

export async function apiRequest<T>(
  input: RequestInfo | URL,
  init: RequestInit = {},
): Promise<T> {
  const auth = useAuthStore()
  const headers = new Headers(init.headers ?? {})

  if (!headers.has('Content-Type') && init.body) {
    headers.set('Content-Type', 'application/json')
  }

  if (auth.user?.token) {
    headers.set('Authorization', `Bearer ${auth.user.token}`)
  }

  let response = await fetch(input, { ...init, headers })

  if (response.status === 401 && auth.user?.token) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      headers.set('Authorization', `Bearer ${newToken}`)
      response = await fetch(input, { ...init, headers })
    } else {
      auth.logoutLocal()
      router.push({ name: 'login' })
      throw new Error('登录已过期，请重新登录')
    }
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      if (body.message) message = body.message
    } catch {
      const text = await response.text().catch(() => '')
      if (text) message = text
    }
    throw new Error(message)
  }

  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

export function consumeRefreshedFlag(): boolean {
  const v = isRefreshed
  isRefreshed = false
  return v
}
