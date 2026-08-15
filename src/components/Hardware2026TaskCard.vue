<template>
  <section class="detail-card task-card" style="--card-priority: 2" @click="goToDetail">
    <div class="card-top">
      <h2>{{ tableName }}</h2>
      <span class="card-arrow">›</span>
    </div>

    <div class="card-stats">
      <div class="stat">
        <span class="stat-num">{{ totalCount }}</span>
        <span class="stat-label">总报修</span>
      </div>
      <div class="stat">
        <span class="stat-num done">{{ solvedCount }}</span>
        <span class="stat-label">已解决</span>
      </div>
      <div class="stat">
        <span class="stat-num pending">{{ unsolvedCount }}</span>
        <span class="stat-label">未解决</span>
      </div>
      <div class="stat">
        <span class="stat-num second">{{ hasSecondRepair }}</span>
        <span class="stat-label">二次维修</span>
      </div>
    </div>

    <p class="card-hint">点击查看完整维修记录</p>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useHardware2026Data } from '@/composables/useHardware2026Data'

const router = useRouter()
const { tableName, totalCount, solvedCount, unsolvedCount, hasSecondRepair } = useHardware2026Data()

function goToDetail(): void {
  router.push('/profile/hardware/hardware2026')
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
  gap: 16px;
  margin: 14px 0 8px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  font-family: 'JuliaMono Medium', sans-serif;
}

.stat-num.done { color: #15803d; }
.stat-num.pending { color: #b91c1c; }
.stat-num.second { color: #b45309; }

.stat-label {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
}

.card-hint {
  margin: 10px 0 0;
  font-size: 12px;
  color: #cbd5e1;
}
</style>
