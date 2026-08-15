import { createRouter, createWebHistory } from 'vue-router'
import HomeSection from '@/components/HomeSection.vue'
import { useAuthStore } from '@/stores/auth'
import type { GroupId, ModuleId, ProfileType } from '@/types/auth'
import { canManageSophia } from '@/utils/permissions'
import { canAccessProfileType, resolveProfileRoute } from '@/utils/profile'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    implemented?: boolean
    groupId?: GroupId
    moduleId?: ModuleId
    profileType?: ProfileType
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeSection },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/conference',
      name: 'conference',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '会议组', requiresAuth: false, implemented: false, groupId: 'conference' },
    },
    {
      path: '/hardware',
      name: 'hardware',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '硬件组', requiresAuth: false, implemented: false, groupId: 'hardware' },
    },
    {
      path: '/software',
      name: 'software',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '软件组', requiresAuth: false, implemented: false, groupId: 'software' },
    },
    {
      path: '/network',
      name: 'network',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '网络组', requiresAuth: false, implemented: false, groupId: 'network' },
    },
    {
      path: '/woruld-sophia',
      name: 'woruld-sophia',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: {
        title: '寰宇智域',
        requiresAuth: true,
        implemented: false,
        moduleId: 'woruld_sophia',
      },
    },
    {
      path: '/conference/about',
      name: 'conference-about',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '会议组简介', requiresAuth: false, implemented: false },
    },
    {
      path: '/conference/showcase',
      name: 'conference-showcase',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '会议组成果展示', requiresAuth: false, implemented: false },
    },
    {
      path: '/conference/members',
      name: 'conference-members',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '会议组成员名单', requiresAuth: false, implemented: false },
    },
    {
      path: '/hardware/about',
      name: 'hardware-about',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '硬件组简介', requiresAuth: false, implemented: false },
    },
    {
      path: '/hardware/showcase',
      name: 'hardware-showcase',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '硬件组成果展示', requiresAuth: false, implemented: false },
    },
    {
      path: '/hardware/members',
      name: 'hardware-members',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '硬件组成员名单', requiresAuth: false, implemented: false },
    },
    {
      path: '/software/about',
      name: 'software-about',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '软件组简介', requiresAuth: false, implemented: false },
    },
    {
      path: '/software/showcase',
      name: 'software-showcase',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '软件组成果展示', requiresAuth: false, implemented: false },
    },
    {
      path: '/software/members',
      name: 'software-members',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '软件组成员名单', requiresAuth: false, implemented: false },
    },
    {
      path: '/network/about',
      name: 'network-about',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '网络组简介', requiresAuth: false, implemented: false },
    },
    {
      path: '/network/showcase',
      name: 'network-showcase',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '网络组成果展示', requiresAuth: false, implemented: false },
    },
    {
      path: '/network/members',
      name: 'network-members',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '网络组成员名单', requiresAuth: false, implemented: false },
    },
    {
      path: '/profile/conference',
      name: 'profile-conference',
      component: () => import('@/views/profile/ConferenceProfileView.vue'),
      meta: { title: '会议组个人信息页', requiresAuth: true, profileType: 'conference' },
    },
    {
      path: '/profile/hardware',
      name: 'profile-hardware',
      component: () => import('@/views/profile/HardwareProfileView.vue'),
      meta: { title: '硬件组个人信息页', requiresAuth: true, profileType: 'hardware' },
    },
    {
      path: '/profile/hardware/reinstall',
      name: 'profile-hardware-reinstall',
      component: () => import('@/views/profile/ReinstallDetailView.vue'),
      meta: { title: '多媒体教室主机系统重装', requiresAuth: true, profileType: 'hardware' },
    },
    {
      path: '/profile/hardware/hardware2026',
      name: 'profile-hardware-hardware2026',
      component: () => import('@/views/profile/Hardware2026DetailView.vue'),
      meta: { title: '硬件组2026', requiresAuth: true, profileType: 'hardware' },
    },
    {
      path: '/profile/hardware/overview',
      name: 'profile-hardware-overview',
      component: () => import('@/views/profile/HardwareOverviewDetailView.vue'),
      meta: { title: '硬件组概览', requiresAuth: true, profileType: 'hardware' },
    },
    {
      path: '/profile/hardware/create-table',
      name: 'profile-hardware-create-table',
      component: () => import('@/views/profile/HardwareCreateTableView.vue'),
      meta: { title: '新增表', requiresAuth: true, profileType: 'hardware' },
    },
    {
      path: '/profile/software',
      name: 'profile-software',
      component: () => import('@/views/profile/SoftwareProfileView.vue'),
      meta: { title: '软件组个人信息页', requiresAuth: true, profileType: 'software' },
    },
    {
      path: '/profile/network',
      name: 'profile-network',
      component: () => import('@/views/profile/NetworkProfileView.vue'),
      meta: { title: '网络组个人信息页', requiresAuth: true, profileType: 'network' },
    },
    {
      path: '/profile/teacher',
      name: 'profile-teacher',
      component: () => import('@/views/profile/TeacherProfileView.vue'),
      meta: { title: '指导老师个人信息页', requiresAuth: true, profileType: 'teacher' },
    },
    {
      path: '/profile/president',
      name: 'profile-president',
      component: () => import('@/views/profile/PresidentProfileView.vue'),
      meta: { title: '会长个人信息页', requiresAuth: true, profileType: 'president' },
    },
    {
      path: '/profile/root',
      name: 'profile-root',
      component: () => import('@/views/profile/RootProfileView.vue'),
      meta: { title: '超级管理工作台', requiresAuth: true, profileType: 'root' },
    },
    {
      path: '/profile/root/accounts',
      name: 'profile-root-accounts',
      component: () => import('@/views/profile/AccountManagementDetailView.vue'),
      meta: { title: '账户管理', requiresAuth: true, profileType: 'root' },
    },
    {
      path: '/materials',
      name: 'materials',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '资料库', requiresAuth: true, implemented: false },
    },
    {
      path: '/training',
      name: 'training',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '训练平台', requiresAuth: true, implemented: false },
    },
    {
      path: '/ctf',
      name: 'ctf',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: 'CTF靶场', requiresAuth: true, implemented: false },
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '协会简介', requiresAuth: false, implemented: false },
    },
    {
      path: '/events',
      name: 'events',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '活动', requiresAuth: false, implemented: false },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && auth.isAuthenticated) {
    return resolveProfileRoute(auth.user)
  }

  if (to.meta.profileType && !canAccessProfileType(auth.user, to.meta.profileType)) {
    return { name: 'not-found' }
  }

  if (to.meta.moduleId === 'woruld_sophia' && !canManageSophia(auth.user)) {
    return { name: 'not-found' }
  }
})

export default router
