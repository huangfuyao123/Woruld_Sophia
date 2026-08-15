<template>
  <ProfileLayout
    title="硬件组工作台"
    subtitle="项目、设备与任务状态"
    role-label="硬件组"
    theme="hardware"
  >
    <Hardware2026TaskCard />
    <ReinstallTaskCard />

    <section class="detail-card" style="--card-priority: 3" @click="goOverview">
      <h2>概览</h2>
      <p>管理教室数据、组内成员与巡检表模板。</p>
      <span class="gh-placeholder-hint">点击进入</span>
    </section>
    <section class="detail-card" style="--card-priority: 4" @click="goCreateTable">
      <h2>新增表</h2>
      <p>创建引用模板或自定义字段的新表。</p>
      <span class="gh-placeholder-hint">点击创建</span>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import ProfileLayout from '@/layouts/ProfileLayout.vue'
import ReinstallTaskCard from '@/components/ReinstallTaskCard.vue'
import Hardware2026TaskCard from '@/components/Hardware2026TaskCard.vue'

const router = useRouter()
function goOverview(): void { router.push('/profile/hardware/overview') }
function goCreateTable(): void { router.push('/profile/hardware/create-table') }
</script>
