// ============================================================
//  认证服务层
//  ----------------------------------------------------------------
//  目前为开发阶段的 mock 实现：凭据从 .env.local 的 VITE_MOCK_USERS 读取，
//  生产构建（import.meta.env.PROD）下不提供 mock，登录直接返回错误。
//
//  后端就绪后，把 loginRequest 内的 mock 逻辑替换为 fetch('/api/login')，
//  store 与组件无需改动。
// ============================================================

/** 已认证用户（状态层与持久化共用同一结构） */
export interface AuthUser {
  id: string
  username: string
  email: string
  token: string
}

export type LoginResult = { success: true; user: AuthUser } | { success: false; error: string }

interface MockUser {
  id: string
  username: string
  email: string
  password: string
}

const STORAGE_KEY = 'auth_user'

/** 解析 .env.local 中的模拟用户表（仅开发环境） */
function loadMockUsers(): Record<string, MockUser> {
  if (!import.meta.env.DEV) return {}
  const raw = import.meta.env.VITE_MOCK_USERS
  if (!raw) return {}
  try {
    const parsed = JSON.parse(raw) as Record<string, MockUser>
    return parsed ?? {}
  } catch {
    console.warn('[auth] VITE_MOCK_USERS 不是合法 JSON，mock 登录将被禁用')
    return {}
  }
}

const MOCK_USERS = loadMockUsers()

/** 生成不透明的 mock token（不内嵌用户 id 等敏感信息） */
function generateToken(): string {
  const buf = new Uint8Array(32)
  crypto.getRandomValues(buf)
  return Array.from(buf, (b) => b.toString(16).padStart(2, '0')).join('')
}

/**
 * 登录请求。
 * TODO（后端接入）：替换为
 *   const res = await fetch('/api/login', {
 *     method: 'POST',
 *     headers: { 'Content-Type': 'application/json' },
 *     body: JSON.stringify({ username, password }),
 *   })
 *   if (!res.ok) throw new Error((await res.json()).message)
 *   return { success: true, user: (await res.json()) as AuthUser }
 */
export async function loginRequest(username: string, password: string): Promise<LoginResult> {
  if (import.meta.env.PROD) {
    return { success: false, error: '登录服务尚未接入（后端未配置）' }
  }

  const matched = MOCK_USERS[username]
  if (!matched) return { success: false, error: '用户名不存在' }
  if (matched.password !== password) return { success: false, error: '密码错误' }

  return {
    success: true,
    user: {
      id: matched.id,
      username: matched.username,
      email: matched.email,
      token: generateToken(),
    },
  }
}

/** 从 localStorage 恢复用户；结构不合法则清除并返回 null */
export function loadUser(): AuthUser | null {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return null
  try {
    const data = JSON.parse(raw) as Partial<AuthUser>
    // TODO（真实 JWT）：在此解析 token 的 exp，过期则 logout。
    if (data.id && data.username && data.email && data.token) {
      return data as AuthUser
    }
  } catch {
    /* fallthrough */
  }
  localStorage.removeItem(STORAGE_KEY)
  return null
}

export function persistUser(user: AuthUser): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
}

export function clearUser(): void {
  localStorage.removeItem(STORAGE_KEY)
}

export const AUTH_STORAGE_KEY = STORAGE_KEY
export const LOGIN_SUCCESS_MESSAGE = 'netclub:login-success'
