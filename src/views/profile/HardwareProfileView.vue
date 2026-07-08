<template>
  <ProfileLayout
    title="硬件组工作台"
    subtitle="项目、设备与任务状态"
    role-label="硬件组"
    theme="hardware"
  >
    <ReinstallTaskCard />
    <Hardware2026TaskCard />

    <section class="detail-card">
      <h2>设备清单</h2>
      <p>暂无数据，后续在此展示硬件组管理的设备列表与状态。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card">
      <h2>组内成员</h2>
      <p>暂无数据，后续在此展示硬件组成员列表。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
import ReinstallTaskCard from '@/components/ReinstallTaskCard.vue'
import Hardware2026TaskCard from '@/components/Hardware2026TaskCard.vue'
</script>
