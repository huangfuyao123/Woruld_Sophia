<template>
  <div v-if="show" class="dialog-backdrop" @click="$emit('cancel')">
    <div class="pwd-dialog" @click.stop>
      <h3>修改密码</h3>
      <div class="form-group">
        <label>原密码</label>
        <input v-model="form.oldPassword" type="password" placeholder="输入当前密码" />
      </div>
      <div class="form-group">
        <label>新密码</label>
        <input v-model="form.newPassword" type="password" placeholder="输入新密码" />
      </div>
      <div class="form-group">
        <label>确认新密码</label>
        <input v-model="form.confirmPassword" type="password" placeholder="再次输入新密码" />
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <p v-if="success" class="success-msg">{{ success }}</p>
      <div class="dialog-actions">
        <button class="dialog-btn secondary" type="button" @click="$emit('cancel')">取消</button>
        <button class="dialog-btn primary" type="button" :disabled="loading" @click="handleSubmit">
          {{ loading ? '提交中…' : '确认修改' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { apiRequest } from '@/api/client'

const props = defineProps<{ show: boolean }>()
const emit = defineEmits<{ cancel: []; success: [] }>()

const form = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)

watch(
  () => props.show,
  (v) => {
    if (v) {
      form.oldPassword = ''
      form.newPassword = ''
      form.confirmPassword = ''
      error.value = ''
      success.value = ''
    }
  },
)

async function handleSubmit() {
  error.value = ''
  success.value = ''
  if (!form.oldPassword || !form.newPassword) {
    error.value = '请填写原密码和新密码'
    return
  }
  if (form.newPassword !== form.confirmPassword) {
    error.value = '两次输入的新密码不一致'
    return
  }
  loading.value = true
  try {
    await apiRequest('/api/change-password', {
      method: 'POST',
      body: JSON.stringify({
        oldPassword: form.oldPassword,
        newPassword: form.newPassword,
      }),
    })
    success.value = '密码修改成功'
    setTimeout(() => emit('success'), 800)
  } catch (e) {
    error.value = (e as Error).message || '修改失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.42);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  z-index: 200;
}

.pwd-dialog {
  width: min(100%, 380px);
  padding: 24px;
  border-radius: 12px;
  background: #fff;
  color: #111827;
}

.pwd-dialog h3 {
  margin: 0 0 20px;
  font-size: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #1f2937;
}

.form-group input:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12);
}

.error-msg {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 6px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 13px;
}

.success-msg {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 6px;
  background: #f0fdf4;
  color: #15803d;
  font-size: 13px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.dialog-btn {
  min-width: 90px;
  padding: 9px 16px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.dialog-btn.secondary {
  background: #e5e7eb;
  color: #1f2937;
}

.dialog-btn.primary {
  background: #7c3aed;
  color: #fff;
}

.dialog-btn.primary:hover {
  background: #6d28d9;
}

.dialog-btn.secondary:hover {
  background: #d1d5db;
}
</style>
