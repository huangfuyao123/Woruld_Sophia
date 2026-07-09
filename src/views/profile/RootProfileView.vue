<template>
  <ProfileLayout
    title="超级管理工作台"
    subtitle="账户管理与全局配置"
    role-label="超级管理员"
    theme="root"
    :show-sophia-stats="false"
    @change-password="showPwdDialog = true"
  >
    <AccountManagementCard />

    <section class="detail-card">
      <h2>系统概览</h2>
      <p>root 账号拥有最高权限，可管理所有账户与模块。</p>
    </section>
  </ProfileLayout>

  <ChangePasswordDialog
    :show="showPwdDialog"
    @cancel="showPwdDialog = false"
    @success="showPwdDialog = false"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProfileLayout from '@/layouts/ProfileLayout.vue'
import AccountManagementCard from '@/components/AccountManagementCard.vue'
import ChangePasswordDialog from '@/components/ChangePasswordDialog.vue'

const showPwdDialog = ref(false)
</script>
