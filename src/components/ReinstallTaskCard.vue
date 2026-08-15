<template>
  <section class="detail-card task-card" :class="{ 'has-progress': true }" style="--card-priority: 1" @click="goToDetail">
    <div class="card-top">
      <h2>多媒体教室主机系统重装</h2>
      <span class="card-arrow">›</span>
    </div>

    <div class="card-stats">
      <div class="stat">
        <span class="stat-num">{{ totalCount }}</span>
        <span class="stat-label">总教室</span>
      </div>
      <div class="stat">
        <span class="stat-num done">{{ reinstalledCount + newHostCount }}</span>
        <span class="stat-label">已填写</span>
      </div>
      <div class="stat">
        <span class="stat-num pending">{{ pendingCount }}</span>
        <span class="stat-label">未填写</span>
      </div>
    </div>

    <div class="card-progress">
      <div class="card-progress-bar">
        <div class="card-progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <span class="card-progress-text">{{ progressPercent }}%</span>
    </div>

    <p class="card-hint">点击查看完整表格</p>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useReinstallData } from '@/composables/useReinstallData'

const router = useRouter()
const { totalCount, reinstalledCount, newHostCount, pendingCount, progressPercent } =
  useReinstallData()

function goToDetail(): void {
  router.push('/profile/hardware/reinstall')
}
</script>

<style scoped>
.task-card {
  cursor: pointer;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-arrow {
  font-size: 22px;
  color: #94a3b8;
  transition: 0.2s;
}

.task-card:hover .card-arrow {
  color: var(--accent);
  transform: translateX(2px);
}

.card-stats {
  display: flex;
  gap: 20px;
  margin: 14px 0 12px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  font-family: 'JuliaMono Medium', sans-serif;
}

.stat-num.done {
  color: #15803d;
}

.stat-num.pending {
  color: #b91c1c;
}

.stat-label {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
}

.card-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-progress-bar {
  flex: 1;
  height: 5px;
  border-radius: 3px;
  background: #f1f5f9;
  overflow: hidden;
}

.card-progress-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--accent);
  transition: width 0.3s ease;
}

.card-progress-text {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  white-space: nowrap;
}

.card-hint {
  margin: 10px 0 0;
  font-size: 12px;
  color: #cbd5e1;
}
</style>
