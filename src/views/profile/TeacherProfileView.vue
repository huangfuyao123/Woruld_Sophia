<template>
  <ProfileLayout
    title="指导老师工作台"
    subtitle="指导分组、审批与通知"
    role-label="指导老师"
    theme="teacher"
    :show-sophia-stats="false"
  >
    <section class="detail-card" style="--card-priority: 1">
      <h2>指导分组</h2>
      <p>暂无数据，后续在此展示你指导的分组列表。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card" style="--card-priority: 2">
      <h2>待审批事项</h2>
      <p>暂无待办，后续在此展示需要老师审批的事项。</p>
    </section>
    <section class="detail-card" style="--card-priority: 3">
      <h2>通知中心</h2>
      <p>暂无通知，后续在此展示来自各分组的通知。</p>
    </section>
    <section class="detail-card" style="--card-priority: 4">
      <h2>指导记录</h2>
      <p>暂无记录，后续在此展示历次指导记录。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
</script>
