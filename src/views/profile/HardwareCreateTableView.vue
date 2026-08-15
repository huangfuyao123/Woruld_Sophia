<template>
  <div class="hardware-create theme-hardware">
    <button class="back-fab" type="button" aria-label="返回工作台" @click="goBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7" /></svg>
    </button>
    <section class="create-card">
      <div class="card-head">
        <div>
          <h1>新增表</h1>
          <p>负责人和指导老师可创建引用模板或自定义字段的表</p>
        </div>
        <button class="create-btn" type="button" @click="createTable">创建表</button>
      </div>

      <div class="form-section">
        <label class="label">表名</label>
        <input v-model="tableName" class="text-input" placeholder="例如：巡检表" />
      </div>

      <div class="form-section split-row">
        <div>
          <label class="label">模板</label>
          <select v-model="templateCode" class="text-input">
            <option value="">不引用模板</option>
            <option value="inspection_template">巡检表模板</option>
          </select>
        </div>
        <label class="check-item"><input v-model="useRoomSource" type="checkbox" /> 引用全部教室数据</label>
      </div>

      <div class="form-section">
        <div class="section-title-row">
          <h2>字段</h2>
          <button class="mini-btn" type="button" @click="addField">新增字段</button>
        </div>
        <div class="field-grid">
          <div class="grid-head">字段名</div>
          <div class="grid-head">字段类型</div>
          <div class="grid-head">选项（逗号分隔）</div>
          <div class="grid-head">操作</div>
          <template v-for="field in fields" :key="field.localKey">
            <input v-model="field.label" class="text-input" />
            <select v-model="field.field_type" class="text-input">
              <option value="text">文本</option>
              <option value="date">日期</option>
              <option value="select">下拉</option>
              <option value="image">图片</option>
            </select>
            <input v-model="field.optionText" class="text-input" :disabled="field.field_type !== 'select'" />
            <button class="danger-btn" type="button" @click="removeField(field.localKey)">删除</button>
          </template>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/api/client'
import { generateUuid } from '@/utils/generateUuid'

const router = useRouter()
const tableName = ref('')
const templateCode = ref('')
const useRoomSource = ref(false)
const fields = ref<any[]>([])

watch(templateCode, (value) => {
  if (value === 'inspection_template') {
    useRoomSource.value = true
    fields.value = []
  }
})

function addField() {
  fields.value.push({ localKey: generateUuid(), label: '', field_type: 'text', optionText: '' })
}
function removeField(localKey: string) {
  fields.value = fields.value.filter((field) => field.localKey !== localKey)
}
async function createTable() {
  await apiRequest('/api/hardware/tables', {
    method: 'POST',
    body: JSON.stringify({
      name: tableName.value,
      template_code: templateCode.value,
      use_room_source: useRoomSource.value,
      fields: fields.value.map((field, index) => ({
        key: `custom_${index + 1}`,
        label: field.label,
        field_type: field.field_type,
        options_json: field.field_type === 'select' ? field.optionText.split(',').map((item: string) => item.trim()).filter(Boolean) : [],
        order: index,
      })),
    }),
  })
  router.push('/profile/hardware')
}
function goBack() { router.push('/profile/hardware') }
</script>

<style scoped>
.hardware-create{--accent:#b91c1c;--accent-soft:#fef2f2;--accent-border:rgba(185,28,28,.15);--card-radius:4px;--card-border:#e2e8f0;min-height:100vh;padding:80px 16px 64px;background:linear-gradient(180deg,var(--accent-soft) 0%,#f1f5f9 45%,#f8fafc 100%);color:#1e293b}.create-card{max-width:1100px;margin:0 auto;background:#fff;border:1px solid var(--card-border);border-radius:var(--card-radius);overflow:hidden}.card-head{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;border-bottom:1px solid var(--card-border)}.card-head h1{margin:0 0 6px;color:var(--accent);font-size:22px}.card-head p{margin:0;color:#64748b;font-size:13px}.form-section{padding:20px 24px;border-bottom:1px solid var(--card-border)}.form-section:last-child{border-bottom:none}.label{display:block;margin-bottom:8px;font-size:12px;font-weight:700;color:#64748b}.text-input{width:100%;height:38px;padding:0 12px;border:1px solid var(--card-border);border-radius:6px;background:#fff;color:#1e293b}.split-row{display:flex;align-items:end;justify-content:space-between;gap:20px}.split-row>div{flex:1}.check-item{display:flex;align-items:center;gap:8px;height:38px;color:#475569;font-size:13px}.section-title-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}.section-title-row h2{margin:0;font-size:16px}.field-grid{display:grid;grid-template-columns:1.2fr 140px 1.4fr 80px;gap:10px;align-items:center}.grid-head{font-size:12px;font-weight:700;color:#64748b}.mini-btn,.create-btn{height:32px;padding:0 14px;border-radius:6px;border:1px solid var(--accent);cursor:pointer;font-size:12px;font-weight:600}.mini-btn{background:#fff;color:var(--accent)}.create-btn{background:var(--accent);color:#fff}.danger-btn{height:32px;border:1px solid #fca5a5;background:#fef2f2;color:#b91c1c;border-radius:6px;cursor:pointer}.back-fab{position:fixed;left:24px;top:20px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border:none;border-radius:50%;cursor:pointer;background:#fff;color:var(--accent);box-shadow:0 4px 14px var(--accent-border);z-index:50}.back-fab svg{width:22px;height:22px}
</style>