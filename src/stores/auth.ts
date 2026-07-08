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

  function logout() {
    user.value = null
    clearUser()
  }

  function checkAuth() {
    user.value = loadUser()
  }

  function updateProfile(patch: Partial<AuthUser>) {
    const nextUser = updatePersistedUser(patch)
    if (nextUser) {
      user.value = nextUser
    }
  }

  return { user, isAuthenticated, login, logout, checkAuth, updateProfile }
})
