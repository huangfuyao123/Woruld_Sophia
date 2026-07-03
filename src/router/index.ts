import { createRouter, createWebHistory } from 'vue-router'
import HomeSection from '@/components/HomeSection.vue'
import { useAuthStore } from '@/stores/auth'

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
      meta: { title: '会议组', requiresAuth: true },
    },
    {
      path: '/hardware',
      name: 'hardware',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '硬件组', requiresAuth: true },
    },
    {
      path: '/software',
      name: 'software',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '软件组', requiresAuth: true },
    },
    {
      path: '/network',
      name: 'network',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '网络组', requiresAuth: true },
    },
    {
      path: '/woruld-sophia',
      name: 'woruld-sophia',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '寰宇智域', requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) {
      return { name: 'login', query: { redirect: to.fullPath } }
    }
  }
})

export default router
