import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginRequest, loadUser, persistUser, clearUser, type AuthUser } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  // ---------- 状态 ----------
  const user = ref<AuthUser | null>(loadUser())

  /** 已认证 = 存在完整用户（含 token）。真实 JWT 接入后在 loadUser 内校验 exp */
  const isAuthenticated = computed(() => user.value !== null)

  // ---------- 登录 ----------
  async function login(username: string, password: string) {
    const res = await loginRequest(username, password)
    if (res.success) {
      user.value = res.user
      persistUser(res.user)
      return { success: true as const }
    }
    return { success: false as const, error: res.error }
  }

  // ---------- 登出 ----------
  function logout() {
    user.value = null
    clearUser()
  }

  // ---------- 恢复登录态 ----------
  function checkAuth() {
    user.value = loadUser()
  }

  return { user, isAuthenticated, login, logout, checkAuth }
})
