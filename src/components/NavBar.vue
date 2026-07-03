<template>
  <header class="nav" :class="{ scrolled: isScrolled }">
    <div class="nav-inner">
      <img class="logo" src="@/assets/images/NetClub.png" alt="Logo" />

      <!-- 汉堡按钮 -->
      <button
        class="burger"
        :class="{ open: menuOpen }"
        @click="menuOpen = !menuOpen"
        aria-label="菜单"
      >
        <span /><span /><span />
      </button>

      <!-- 导航菜单 -->
      <ul class="menu" :class="{ open: menuOpen }">
        <li v-for="item in navItems" :key="item.to">
          <i class="iconfont" :class="item.icon"></i>
          <RouterLink class="link" :to="item.to" @click="menuOpen = false">{{
            item.label
          }}</RouterLink>
        </li>
      </ul>

      <!-- ===== 右侧登录 / 登出 ===== -->
      <div class="auth-section">
        <!-- 未登录：点击打开新窗口 -->
        <button v-if="!auth.isAuthenticated" class="auth-btn signin-btn" @click="openLogin">
          Sign In
        </button>

        <!-- 已登录：用户名 + Sign Out -->
        <div v-else class="user-area">
          <span class="user-name">Hi, {{ auth.user?.username }}</span>
          <button class="auth-btn signout-btn" @click="handleLogout">Sign Out</button>
        </div>
      </div>
      <!-- ============================ -->
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { LOGIN_SUCCESS_MESSAGE } from '@/services/auth'

const router = useRouter()
const auth = useAuthStore()

interface NavItem {
  label: string
  to: string
  icon: string
}

const navItems: NavItem[] = [
  { label: '首页', to: '/', icon: 'icon-xialajiantou' },
  { label: '会议组', to: '/conference', icon: 'icon-xialajiantou' },
  { label: '硬件组', to: '/hardware', icon: 'icon-xialajiantou' },
  { label: '软件组', to: '/software', icon: 'icon-xialajiantou' },
  { label: '网络组', to: '/network', icon: 'icon-xialajiantou' },
  { label: '寰宇智域', to: '/woruld-sophia', icon: 'icon-xialajiantou' },
]

const isScrolled = ref(false)
const menuOpen = ref(false)

// 登录窗口引用
let loginWindow: Window | null = null

function onScroll(): void {
  isScrolled.value = window.scrollY > 50
}

function onMessage(e: MessageEvent): void {
  if (e.origin !== window.location.origin) return
  if (e.data === LOGIN_SUCCESS_MESSAGE) {
    auth.checkAuth()
    if (loginWindow && !loginWindow.closed) loginWindow.close()
    loginWindow = null
  }
}

/** 在新窗口打开登录页 */
function openLogin(): void {
  menuOpen.value = false

  // 如果已有登录窗口开着，聚焦它
  if (loginWindow && !loginWindow.closed) {
    loginWindow.focus()
    return
  }

  const w = 480
  const h = 640
  const left = (screen.width - w) / 2
  const top = (screen.height - h) / 2

  loginWindow = window.open(
    '/login',
    'netclub-login',
    `width=${w},height=${h},left=${left},top=${top},resizable=no,scrollbars=no`,
  )
}

function handleLogout(): void {
  auth.logout()
  menuOpen.value = false
  router.push('/')
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('message', onMessage)
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('message', onMessage)
})
</script>

<style scoped>
/* ========================================
   导航栏 — 桌面（>900px）
   ======================================== */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
  z-index: 100;
  background: rgb(40, 70, 150);
  transition:
    background 0.4s,
    box-shadow 0.4s;
}

.nav.scrolled {
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-inner {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0 4px;
  color: #fff;
}

.nav.scrolled .nav-inner {
  color: #333;
}

.logo {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.menu {
  display: flex;
  list-style: none;
  align-items: center;
  height: 50px;
  flex: 1;
}

.menu li {
  font-size: clamp(12px, 1.5vw, 24px);
  margin-right: 2px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  height: 50px;
}

.menu li i {
  font-size: 20px;
  margin-right: 2px;
}

.link {
  font-size: clamp(16px, 1.8vw, 36px);
  font-family: '寒蝉正楷体';
  text-decoration: none;
  color: inherit;
  white-space: nowrap;
}

.burger {
  display: none;
}

/* ========================================
   auth 区域
   ======================================== */
.auth-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  margin-right: 24px;
  flex-shrink: 0;
}

.auth-btn {
  padding: 7px 18px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  font-family: 'JuliaMono BlackItalic';
}

.signin-btn {
  background: transparent;
  border: 2px solid currentColor;
  color: inherit;
}

.signin-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.nav.scrolled .signin-btn {
  color: #333;
  border-color: #333;
}

.nav.scrolled .signin-btn:hover {
  background: rgba(0, 0, 0, 0.06);
}

.user-area {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-name {
  font-size: 24px;
  font-weight: 500;
  color: inherit;
  white-space: nowrap;
  font-family: 'JuliaMono Medium';
  font-style: italic;
}

.signout-btn {
  background: #2b2a669c;
  color: #fff;
  border: none;
}

.signout-btn:hover {
  background: #e33d3f;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.3);
}

/* ========================================
   手机 / 窄屏（≤900px）
   ======================================== */
@media (max-width: 900px) {
  .burger {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 6px;
    color: inherit;
    order: 3;
  }

  .burger span {
    display: block;
    width: 24px;
    height: 2.5px;
    background: currentColor;
    border-radius: 2px;
    transition: 0.25s;
  }

  .burger.open span:nth-child(1) {
    transform: translateY(7.5px) rotate(45deg);
  }
  .burger.open span:nth-child(2) {
    opacity: 0;
  }
  .burger.open span:nth-child(3) {
    transform: translateY(-7.5px) rotate(-45deg);
  }

  .menu {
    display: none;
    position: absolute;
    top: 50px;
    left: 0;
    width: 100%;
    flex-direction: column;
    height: auto;
    background: rgb(40, 70, 150);
    z-index: 99;
  }

  .nav.scrolled .menu {
    background: #fff;
  }

  .menu.open {
    display: flex;
  }

  .menu li {
    width: 100%;
    height: auto;
    padding: 8px 20px;
  }

  .link {
    font-size: clamp(14px, 3.5vw, 18px);
  }

  .auth-section {
    order: 2;
    margin-left: auto;
    margin-right: 8px;
  }

  .user-name {
    display: none;
  }

  .auth-btn {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
