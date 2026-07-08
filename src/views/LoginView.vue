<template>
  <div class="login-container">
    <img class="deco deco-tl" src="@/assets/images/sjs.png" alt="" />
    <img class="deco deco-br" src="@/assets/images/露西亚.png" alt="" />

    <div class="login-card">
      <h2 class="login-title">Sign In to NetClub</h2>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model.trim="form.username"
            type="text"
            placeholder="Enter your username"
            autocomplete="username"
            :class="{ error: errors.username }"
          />
          <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            autocomplete="current-password"
            :class="{ error: errors.password }"
          />
          <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
        </div>

        <label class="remember-row" for="remember-me">
          <input id="remember-me" v-model="rememberMe" type="checkbox" />
          <span>记住我</span>
        </label>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign In' }}
        </button>

        <p v-if="serverError" class="server-error">{{ serverError }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { LOGIN_SUCCESS_MESSAGE } from '@/services/auth'
import { resolveProfileRoute } from '@/utils/profile'

const auth = useAuthStore()
const router = useRouter()

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '' })
const serverError = ref('')
const loading = ref(false)
const rememberMe = ref(true)

function validate(): boolean {
  errors.username = ''
  errors.password = ''
  let ok = true
  if (!form.username) {
    errors.username = '用户名不能为空'
    ok = false
  }
  if (!form.password) {
    errors.password = '密码不能为空'
    ok = false
  }
  return ok
}

async function handleLogin() {
  if (!validate()) return
  serverError.value = ''
  loading.value = true

  const res = await auth.login({
    username: form.username,
    password: form.password,
    rememberMe: rememberMe.value,
  })
  loading.value = false

  if (res.success) {
    if (window.opener && !window.opener.closed) {
      window.opener.postMessage(LOGIN_SUCCESS_MESSAGE, window.location.origin)
      window.close()
      return
    }

    await router.replace(resolveProfileRoute(auth.user))
    return
  }

  serverError.value = res.error ?? '登录失败，请重试'
}
</script>

<style scoped>
.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.deco {
  position: absolute;
  pointer-events: none;
  opacity: 0.18;
}

.deco-tl {
  top: 30px;
  left: -15px;
  width: 140px;
  height: 140px;
}

.deco-br {
  bottom: 0;
  right: 0;
  width: 120px;
  height: 180px;
}

.login-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 40px 36px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  color: #fff;
  z-index: 1;
}

.login-title {
  font-size: 26px;
  font-family: '寒蝉正楷体', sans-serif;
  text-align: center;
  color: #333;
  margin-bottom: 28px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #555;
  font-size: 18px;
  font-weight: 500;
  font-family: '寒蝉正楷体', sans-serif;
}

.form-group input {
  width: 100%;
  padding: 14px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  transition: 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-group input.error {
  border-color: #ff4d4f;
}

.field-error {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.remember-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 4px 0 20px;
  color: #333;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

.remember-row input {
  width: 16px;
  height: 16px;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.submit-btn:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35);
}

.submit-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.server-error {
  margin-top: 16px;
  padding: 10px;
  text-align: center;
  color: #ff4d4f;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 6px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }

  .login-card {
    padding: 32px 28px;
    border-radius: 14px;
  }

  .login-title {
    font-size: 22px;
    margin-bottom: 24px;
  }

  .form-group label {
    font-size: 16px;
  }

  .form-group input {
    padding: 12px;
    font-size: 15px;
  }

  .submit-btn {
    padding: 14px;
    font-size: 15px;
  }

  .deco-tl {
    width: 100px;
    height: 100px;
    opacity: 0.12;
  }

  .deco-br {
    width: 80px;
    height: 120px;
    opacity: 0.12;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 24px 20px;
    border-radius: 12px;
  }

  .login-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    font-size: 15px;
  }

  .form-group input {
    padding: 11px;
    font-size: 14px;
  }

  .submit-btn {
    padding: 12px;
    font-size: 14px;
    letter-spacing: 0.5px;
  }

  .deco-tl {
    display: none;
  }

  .deco-br {
    display: none;
  }
}
</style>
