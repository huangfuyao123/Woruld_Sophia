<template>
  <header class="nav" :class="{ scrolled: isScrolled }">
    <div class="nav-inner">
      <img class="logo" src="@/assets/images/NetClub.png" alt="Logo" />

      <button
        class="burger"
        :class="{ open: menuOpen }"
        @click="menuOpen = !menuOpen"
        aria-label="菜单"
      >
        <span /><span /><span />
      </button>

      <ul class="menu" :class="{ open: menuOpen }">
        <li
          v-for="item in navItems"
          :key="item.to"
          class="nav-item"
          :class="{ 'has-children': item.children }"
        >
          <i class="iconfont" :class="item.icon"></i>
          <RouterLink
            v-if="!item.requiresAuth"
            class="link"
            :to="item.to"
            @click="menuOpen = false"
          >
            {{ item.label }}
          </RouterLink>
          <button v-else class="link nav-button" type="button" @click="handleProtectedNav(item.to)">
            {{ item.label }}
          </button>

          <div v-if="item.children" class="submenu">
            <RouterLink
              v-for="child in item.children"
              :key="child.to"
              class="submenu-link"
              :to="child.to"
              @click="menuOpen = false"
            >
              {{ child.label }}
            </RouterLink>
          </div>
        </li>
      </ul>

      <div class="auth-section">
        <button v-if="!auth.isAuthenticated" class="auth-btn signin-btn" @click="openLogin()">
          Sign In
        </button>

        <div v-else class="profile-entry">
          <button class="avatar-button" type="button" aria-label="打开用户菜单" @click="toggleProfileMenu">
            <img v-if="avatarUrl" class="avatar-image" :src="avatarUrl" alt="用户头像" />
            <span v-else class="avatar-circle">{{ userInitial }}</span>
          </button>

          <div v-if="profileMenuOpen" class="profile-menu">
            <button class="profile-menu-item" type="button" @click="openProfileCenter">
              个人中心
            </button>
            <button class="profile-menu-item danger" type="button" @click="requestLogout">
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>

  <div v-if="showLogoutConfirm" class="dialog-backdrop" @click="cancelLogout">
    <div class="logout-dialog" @click.stop>
      <h3>确认登出</h3>
      <p>确定要退出当前账号吗？</p>
      <div class="dialog-actions">
        <button class="dialog-btn secondary" type="button" @click="cancelLogout">取消</button>
        <button class="dialog-btn primary" type="button" @click="confirmLogout">确认登出</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { LOGIN_SUCCESS_MESSAGE } from '@/services/auth'
import { resolveProfileRoute } from '@/utils/profile'

const router = useRouter()
const auth = useAuthStore()

interface SubNavItem {
  label: string
  to: string
}

interface NavItem {
  label: string
  to: string
  icon: string
  requiresAuth: boolean
  groupId?: 'conference' | 'hardware' | 'software' | 'network'
  moduleId?: 'woruld_sophia'
  children?: SubNavItem[]
}

const navItems: NavItem[] = [
  { label: '首页', to: '/', icon: 'icon-xialajiantou', requiresAuth: false, children: [
      { label: '协会简介', to: '/about' },
      { label: '活动', to: '/events' },
    ] },
  {
    label: '会议组',
    to: '/conference',
    icon: 'icon-xialajiantou',
    requiresAuth: true,
    groupId: 'conference',
    children: [
      { label: '分组简介', to: '/conference/about' },
      { label: '成果展示', to: '/conference/showcase' },
      { label: '成员名单', to: '/conference/members' },
    ],
  },
  {
    label: '硬件组',
    to: '/hardware',
    icon: 'icon-xialajiantou',
    requiresAuth: true,
    groupId: 'hardware',
    children: [
      { label: '分组简介', to: '/hardware/about' },
      { label: '成果展示', to: '/hardware/showcase' },
      { label: '成员名单', to: '/hardware/members' },
    ],
  },
  {
    label: '软件组',
    to: '/software',
    icon: 'icon-xialajiantou',
    requiresAuth: true,
    groupId: 'software',
    children: [
      { label: '分组简介', to: '/software/about' },
      { label: '成果展示', to: '/software/showcase' },
      { label: '成员名单', to: '/software/members' },
    ],
  },
  {
    label: '网络组',
    to: '/network',
    icon: 'icon-xialajiantou',
    requiresAuth: true,
    groupId: 'network',
    children: [
      { label: '分组简介', to: '/network/about' },
      { label: '成果展示', to: '/network/showcase' },
      { label: '成员名单', to: '/network/members' },
    ],
  },
  {
    label: '寰宇智域',
    to: '/woruld-sophia',
    icon: 'icon-xialajiantou',
    requiresAuth: true,
    moduleId: 'woruld_sophia',
    children: [
      { label: '资料库', to: '/materials' },
      { label: '训练平台', to: '/training' },
      { label: 'CTF靶场', to: '/ctf' },
    ],
  },
]

const isScrolled = ref(false)
const menuOpen = ref(false)
const profileMenuOpen = ref(false)
const showLogoutConfirm = ref(false)

let loginWindow: Window | null = null

const avatarUrl = computed(() => auth.user?.avatarUrl?.trim() || '')
const userInitial = computed(() => {
  const source = auth.user?.displayName?.trim() || auth.user?.username?.trim() || 'U'
  return source.charAt(0).toUpperCase()
})

function onScroll(): void {
  isScrolled.value = window.scrollY > 50
}

function onMessage(e: MessageEvent): void {
  if (e.origin !== window.location.origin) return
  if (e.data === LOGIN_SUCCESS_MESSAGE) {
    auth.checkAuth()
    if (loginWindow && !loginWindow.closed) loginWindow.close()
    loginWindow = null
    profileMenuOpen.value = false
    showLogoutConfirm.value = false
    router.push(resolveProfileRoute(auth.user))
  }
}

function openLogin(): void {
  menuOpen.value = false

  if (loginWindow && !loginWindow.closed) {
    loginWindow.focus()
    return
  }

  if (window.matchMedia('(max-width: 768px)').matches) {
    router.push('/login')
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

function handleProtectedNav(to: string): void {
  menuOpen.value = false

  if (!auth.isAuthenticated) {
    openLogin()
    return
  }

  router.push(to)
}

function toggleProfileMenu(): void {
  profileMenuOpen.value = !profileMenuOpen.value
}

function openProfileCenter(): void {
  profileMenuOpen.value = false
  menuOpen.value = false
  router.push(resolveProfileRoute(auth.user))
}

function requestLogout(): void {
  profileMenuOpen.value = false
  showLogoutConfirm.value = true
}

function cancelLogout(): void {
  showLogoutConfirm.value = false
}

function confirmLogout(): void {
  auth.logout()
  menuOpen.value = false
  profileMenuOpen.value = false
  showLogoutConfirm.value = false
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
  position: relative;
}

.nav-item .submenu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 160px;
  flex-direction: column;
  padding: 6px 0;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
  z-index: 120;
}

.nav-item:hover > .submenu,
.nav-item .submenu:hover {
  display: flex;
}

.submenu-link {
  display: block;
  padding: 8px 16px;
  font-size: 14px;
  font-family: '寒蝉正楷体';
  color: #1f2937;
  text-decoration: none;
  white-space: nowrap;
}

.submenu-link:hover {
  background: #eff6ff;
  color: #1e40af;
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

.nav-button {
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.burger {
  display: none;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  margin-right: 24px;
  flex-shrink: 0;
  position: relative;
}

.profile-entry {
  position: relative;
}

.avatar-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
}

.avatar-circle,
.avatar-image {
  width: 42px;
  height: 42px;
  border-radius: 50%;
}

.avatar-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.22);
  border: 2px solid rgba(255, 255, 255, 0.7);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  font-family: 'JuliaMono Medium';
}

.avatar-image {
  display: block;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.7);
}

.nav.scrolled .avatar-circle {
  background: rgba(40, 70, 150, 0.12);
  border-color: rgba(40, 70, 150, 0.35);
  color: #284696;
}

.nav.scrolled .avatar-image {
  border-color: rgba(40, 70, 150, 0.35);
}

.profile-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 144px;
  padding: 8px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 120;
}

.profile-menu-item {
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #1f2937;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
}

.profile-menu-item:hover {
  background: #f3f4f6;
}

.profile-menu-item.danger {
  color: #c62828;
}

.profile-menu-item.danger:hover {
  background: #fdecec;
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

.dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.42);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  z-index: 140;
}

.logout-dialog {
  width: min(100%, 360px);
  padding: 24px;
  border-radius: 8px;
  background: #fff;
  color: #111827;
  box-shadow: 0 18px 48px rgba(15, 23, 42, 0.24);
}

.logout-dialog h3 {
  font-size: 20px;
  margin-bottom: 8px;
}

.logout-dialog p {
  font-size: 14px;
  line-height: 1.5;
  color: #4b5563;
}

@media (max-width: 480px) {
  .logout-dialog {
    padding: 20px 16px;
  }

  .logout-dialog h3 {
    font-size: 17px;
  }

  .logout-dialog p {
    font-size: 13px;
  }
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.dialog-btn {
  min-width: 96px;
  padding: 10px 14px;
  border-radius: 6px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.dialog-btn.secondary {
  background: #e5e7eb;
  color: #1f2937;
}

.dialog-btn.primary {
  background: #c62828;
  color: #fff;
}

.dialog-btn.primary:hover {
  background: #b71c1c;
}

.dialog-btn.secondary:hover {
  background: #d1d5db;
}

@media (max-width: 1100px) {
  .menu li {
    padding: 0 8px;
  }

  .menu li i {
    font-size: 16px;
  }

  .link {
    font-size: clamp(14px, 1.5vw, 28px);
  }
}

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
    max-height: calc(100vh - 50px);
    overflow-y: auto;
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

  .nav-item .submenu {
    position: static;
    box-shadow: none;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 0;
    padding: 0;
  }

  .nav-item.has-children {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-item.has-children > .link,
  .nav-item.has-children > .nav-button {
    width: 100%;
  }

  .nav-item:hover > .submenu,
  .nav-item .submenu:hover {
    display: none;
  }

  .nav-item.has-children .submenu {
    display: flex;
    position: static;
    width: 100%;
    margin-top: 4px;
  }

  .submenu-link {
    padding: 6px 24px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.85);
  }

  .nav.scrolled .submenu-link {
    color: #475569;
  }

  .submenu-link:hover {
    background: transparent;
    color: #fff;
  }

  .nav.scrolled .submenu-link:hover {
    color: #1e40af;
  }

  .menu li {
    width: 100%;
    height: auto;
    padding: 8px 20px;
  }

  .link {
    font-size: clamp(15px, 3.5vw, 18px);
  }

  .auth-section {
    order: 2;
    margin-left: auto;
    margin-right: 8px;
  }

  .auth-btn {
    font-size: 12px;
    padding: 6px 12px;
  }

  .profile-menu {
    min-width: 132px;
  }

  .avatar-button,
  .avatar-circle,
  .avatar-image {
    width: 36px;
    height: 36px;
  }

  .avatar-circle {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .logo {
    width: 32px;
    height: 32px;
  }

  .auth-section {
    margin-right: 4px;
    gap: 8px;
  }

  .auth-btn {
    font-size: 11px;
    padding: 5px 10px;
  }

  .burger span {
    width: 20px;
    height: 2px;
  }

  .submenu-link {
    padding: 6px 20px;
    font-size: 12px;
  }
}
</style>
