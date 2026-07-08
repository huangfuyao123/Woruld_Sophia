<template>
  <ProfileLayout
    title="会议组工作台"
    subtitle="组内信息、任务与成果展示"
    role-label="会议组"
    theme="conference"
  >
    <section class="detail-card">
      <h2>组内公告</h2>
      <p>暂无公告，后续在此展示会议组的最新通知与安排。</p>
    </section>
    <section class="detail-card">
      <h2>我的任务</h2>
      <p>暂无任务，后续在此展示分配给你的会议组任务。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card">
      <h2>成果展示</h2>
      <p>暂无内容，后续在此展示会议组的成果与文档。</p>
    </section>
    <section class="detail-card">
      <h2>组内成员</h2>
      <p>暂无数据，后续在此展示会议组成员列表。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
</script>
