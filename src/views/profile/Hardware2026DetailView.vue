<template>
  <div class="hw2026-detail theme-hardware">
    <button class="back-fab" type="button" aria-label="返回工作台" @click="goBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5M12 19l-7-7 7-7" />
      </svg>
    </button>

    <button class="home-fab" type="button" aria-label="返回首页" @click="goHome">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1V9.5z" />
      </svg>
    </button>

    <Hardware2026Table />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Hardware2026Table from '@/components/Hardware2026Table.vue'

const router = useRouter()

function goBack(): void {
  router.push('/profile/hardware')
}

function goHome(): void {
  router.push('/')
}
</script>

<style scoped>
.hw2026-detail {
  --accent: #b91c1c;
  --accent-soft: #fef2f2;
  --accent-border: rgba(185, 28, 28, 0.15);
  --card-radius: 4px;
  --card-border: #e2e8f0;
  min-height: 100vh;
  padding: 80px 16px 64px;
  background: linear-gradient(180deg, var(--accent-soft) 0%, #f1f5f9 45%, #f8fafc 100%);
  color: #1e293b;
  font-family: '寒蝉正楷体', 'JuliaMono Medium', sans-serif;
}

.hw2026-detail :deep(.hw2026-board) {
  max-width: 1400px;
  margin: 0 auto;
}

.back-fab,
.home-fab {
  position: fixed;
  top: 20px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 14px var(--accent-border);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 50;
}

.back-fab {
  left: 24px;
  background: #fff;
  color: var(--accent);
}

.home-fab {
  right: 24px;
  background: var(--accent);
  color: #fff;
}

.back-fab svg,
.home-fab svg {
  width: 22px;
  height: 22px;
}

.back-fab:hover,
.home-fab:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .hw2026-detail {
    padding: 24px 8px 48px;
  }

  .back-fab,
  .home-fab {
    top: 14px;
    width: 40px;
    height: 40px;
  }

  .back-fab { left: 14px; }
  .home-fab { right: 14px; }

  .back-fab svg,
  .home-fab svg {
    width: 20px;
    height: 20px;
  }
}
</style>
