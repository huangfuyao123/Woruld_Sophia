import { loginRequest, type LoginResult } from '@/services/auth'

export async function login(username: string, password: string): Promise<LoginResult> {
  return loginRequest(username, password)
}

export async function logout(): Promise<void> {
  return Promise.resolve()
}
