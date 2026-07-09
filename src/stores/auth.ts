import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  loginRequest,
  loadUser,
  persistUser,
  clearUser,
  updatePersistedUser,
  type AuthUser,
} from '@/services/auth'
import { logoutAPI, getMeAPI } from '@/api/auth'
import { updateProfileAPI } from '@/api/profile'

type LoginPayload = {
  username: string
  password: string
  rememberMe?: boolean
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(loadUser())

  const isAuthenticated = computed(() => user.value !== null)

  async function login({ username, password, rememberMe = true }: LoginPayload) {
    const res = await loginRequest(username, password)
    if (res.success) {
      user.value = res.user
      persistUser(res.user, rememberMe)
      return { success: true as const }
    }
    return { success: false as const, error: res.error }
  }

  async function logout() {
    if (user.value?.refreshToken) {
      await logoutAPI(user.value.refreshToken)
    }
    logoutLocal()
  }

  function logoutLocal() {
    user.value = null
    clearUser()
  }

  async function checkAuth() {
    user.value = loadUser()
    if (!user.value?.token) {
      logoutLocal()
      return
    }
    const fresh = await getMeAPI()
    if (fresh) {
      user.value = fresh
      persistUser(fresh, !!localStorage.getItem('auth_user'))
    } else {
      logoutLocal()
    }
  }

  async function updateProfile(patch: Partial<AuthUser>) {
    const next = await updateProfileAPI(patch)
    const merged: AuthUser = {
      ...(user.value ?? next),
      ...next,
      token: user.value?.token ?? next.token,
      refreshToken: user.value?.refreshToken ?? next.refreshToken,
    }
    user.value = merged
    updatePersistedUser(merged)
  }

  return { user, isAuthenticated, login, logout, logoutLocal, checkAuth, updateProfile }
})
