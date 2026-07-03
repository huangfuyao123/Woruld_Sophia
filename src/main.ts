import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// 应用启动时恢复登录态（仅一次，避免组件内重复调用）
useAuthStore(pinia).checkAuth()

app.use(router)
app.mount('#app')
