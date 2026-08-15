<template>
  <ProfileLayout
    title="会长工作台"
    subtitle="全局总览、审批与管理入口"
    role-label="会长"
    theme="president"
  >
    <section class="detail-card" style="--card-priority: 1">
      <h2>全局概览</h2>
      <p>暂无数据，后续在此展示各分组的整体运行状况。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card" style="--card-priority: 2">
      <h2>待审批事项</h2>
      <p>暂无待办，后续在此展示需要会长审批的事项。</p>
    </section>
    <section class="detail-card" style="--card-priority: 3">
      <h2>成员管理</h2>
      <p>暂无数据，后续在此提供成员管理入口。</p>
    </section>
    <section class="detail-card" style="--card-priority: 4">
      <h2>公告发布</h2>
      <p>暂无内容，后续在此提供社团公告发布功能。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
</script>
