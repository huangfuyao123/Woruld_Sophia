<template>
  <section class="detail-card account-card" @click="goToDetail">
    <div class="card-top">
      <h2>账户管理</h2>
      <span class="card-arrow">›</span>
    </div>
    <p class="card-hint">管理社团成员账号、身份与权限分配</p>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToDetail(): void {
  router.push('/profile/root/accounts')
}
</script>

<style scoped>
.account-card {
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

.account-card:hover .card-arrow {
  color: var(--accent);
  transform: translateX(2px);
}

.card-hint {
  margin: 8px 0 0;
  font-size: 13px;
  color: #64748b;
}
</style>
