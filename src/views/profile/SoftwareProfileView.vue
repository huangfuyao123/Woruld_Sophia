<template>
  <ProfileLayout
    title="软件组工作台"
    subtitle="代码仓库、任务与进度"
    role-label="软件组"
    theme="software"
  >
    <section class="detail-card" style="--card-priority: 1">
      <h2>代码仓库</h2>
      <p>暂无仓库，后续在此展示软件组的代码仓库列表。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card" style="--card-priority: 2">
      <h2>我的任务</h2>
      <p>暂无任务，后续在此展示分配给你的开发任务。</p>
    </section>
    <section class="detail-card" style="--card-priority: 3">
      <h2>迭代进度</h2>
      <p>暂无数据，后续在此展示软件组的迭代与进度。</p>
    </section>
    <section class="detail-card" style="--card-priority: 4">
      <h2>组内成员</h2>
      <p>暂无数据，后续在此展示软件组成员列表。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
</script>
