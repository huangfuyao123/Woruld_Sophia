<template>
  <ProfileLayout
    title="网络组工作台"
    subtitle="运维、网络状态与值班信息"
    role-label="网络组"
    theme="network"
  >
    <section class="detail-card">
      <h2>网络拓扑</h2>
      <p>暂无数据，后续在此展示网络拓扑与设备状态。</p>
      <span class="gh-placeholder-hint">待后端接入</span>
    </section>
    <section class="detail-card">
      <h2>值班表</h2>
      <p>暂无数据，后续在此展示网络组值班安排。</p>
    </section>
    <section class="detail-card">
      <h2>我的任务</h2>
      <p>暂无任务，后续在此展示分配给你的网络运维任务。</p>
    </section>
    <section class="detail-card">
      <h2>组内成员</h2>
      <p>暂无数据，后续在此展示网络组成员列表。</p>
    </section>
  </ProfileLayout>
</template>

<script setup lang="ts">
import ProfileLayout from '@/layouts/ProfileLayout.vue'
</script>
