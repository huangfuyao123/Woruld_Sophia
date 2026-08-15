<template>
  <div class="hardware-overview theme-hardware">
    <button class="back-fab" type="button" aria-label="返回工作台" @click="goBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7" /></svg>
    </button>
    <section class="overview-card">
      <div class="card-head">
        <div>
          <h1>硬件组概览</h1>
          <p>维护教室数据、组内成员与巡检表模板</p>
        </div>
        <button v-if="canManage" class="save-btn" type="button" @click="saveAll">保存概览</button>
      </div>

      <div class="overview-section">
        <div class="section-title-row">
          <h2>教室数据</h2>
          <button v-if="canManage" class="mini-btn" type="button" @click="addRoom">新增教室</button>
        </div>
        <div class="grid-table room-grid">
          <div class="grid-head">教室</div>
          <div class="grid-head">排序</div>
          <div class="grid-head">状态</div>
          <div v-if="canManage" class="grid-head">操作</div>
          <template v-for="room in rooms" :key="room.localKey">
            <input v-model="room.name" class="grid-input" :disabled="!canManage" />
            <input v-model.number="room.sort_order" type="number" class="grid-input small" :disabled="!canManage" />
            <select v-model="room.is_active" class="grid-input" :disabled="!canManage">
              <option :value="true">启用</option>
              <option :value="false">停用</option>
            </select>
            <button v-if="canManage" class="danger-btn" type="button" @click="removeRoom(room.localKey)">删除</button>
          </template>
        </div>
      </div>

      <div class="overview-section">
        <div class="section-title-row">
          <h2>组内成员</h2>
          <button v-if="canManage" class="mini-btn" type="button" @click="addMember">新增成员</button>
        </div>
        <div class="grid-table member-grid">
          <div class="grid-head">姓名</div>
          <div class="grid-head">年级</div>
          <div class="grid-head">在组内身份</div>
          <div v-if="canManage" class="grid-head">操作</div>
          <template v-for="member in members" :key="member.localKey">
            <input v-model="member.name" class="grid-input" :disabled="!canManage" />
            <input v-model="member.grade" class="grid-input" :disabled="!canManage" />
            <select v-model="member.role" class="grid-input" :disabled="!canManage">
              <option value="leader">组长</option>
              <option value="vice_leader">副组长</option>
              <option value="member">成员</option>
            </select>
            <button v-if="canManage" class="danger-btn" type="button" @click="removeMember(member.localKey)">删除</button>
          </template>
        </div>
      </div>

      <div class="overview-section">
        <div class="section-title-row">
          <h2>巡检表模板</h2>
          <span class="template-tag">引用教室数据 · 仿照重装表布局</span>
        </div>
        <div class="template-fields">
          <span v-for="field in inspectionTemplate.fields" :key="field.key" class="field-chip">{{ field.label }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { canEditGroup } from '@/utils/permissions'
import { generateUuid } from '@/utils/generateUuid'

const router = useRouter()
const auth = useAuthStore()
const canManage = computed(() => canEditGroup(auth.user, 'hardware') || auth.user?.roles.some((role) => role.role === 'teacher') || false)
const rooms = ref<any[]>([])
const members = ref<any[]>([])
const inspectionTemplate = ref<{ fields: Array<{ key: string; label: string }> }>({ fields: [] })

async function load() {
  const data = await apiRequest<any>('/api/hardware/overview')
  rooms.value = (data.rooms || []).map((item: any) => ({ ...item, localKey: item.id || generateUuid() }))
  members.value = (data.members || []).map((item: any) => ({ ...item, localKey: item.id || generateUuid() }))
  inspectionTemplate.value = data.inspection_template || { fields: [] }
}

function addRoom() {
  rooms.value.push({ localKey: generateUuid(), name: '', sort_order: rooms.value.length + 1, is_active: true })
}
function removeRoom(localKey: string) {
  rooms.value = rooms.value.filter((item) => item.localKey !== localKey)
}
function addMember() {
  members.value.push({ localKey: generateUuid(), name: '', grade: '', role: 'member', sort_order: members.value.length + 1, is_active: true })
}
function removeMember(localKey: string) {
  members.value = members.value.filter((item) => item.localKey !== localKey)
}
async function saveAll() {
  await apiRequest('/api/hardware/overview', {
    method: 'PUT',
    body: JSON.stringify({
      rooms: rooms.value.map(({ localKey, ...rest }) => rest),
      members: members.value.map(({ localKey, ...rest }) => rest),
    }),
  })
  await load()
}
function goBack() { router.push('/profile/hardware') }
onMounted(load)
</script>

<style scoped>
.hardware-overview{--accent:#b91c1c;--accent-soft:#fef2f2;--accent-border:rgba(185,28,28,.15);--card-radius:4px;--card-border:#e2e8f0;min-height:100vh;padding:80px 16px 64px;background:linear-gradient(180deg,var(--accent-soft) 0%,#f1f5f9 45%,#f8fafc 100%);color:#1e293b}.overview-card{max-width:1200px;margin:0 auto;background:#fff;border:1px solid var(--card-border);border-radius:var(--card-radius);overflow:hidden}.card-head{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;border-bottom:1px solid var(--card-border)}.card-head h1{margin:0 0 6px;color:var(--accent);font-size:22px}.card-head p{margin:0;color:#64748b;font-size:13px}.overview-section{padding:20px 24px;border-bottom:1px solid var(--card-border)}.overview-section:last-child{border-bottom:none}.section-title-row{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}.section-title-row h2{margin:0;font-size:16px;color:#1e293b}.grid-table{display:grid;gap:10px;align-items:center}.room-grid{grid-template-columns:2fr 100px 120px 80px}.member-grid{grid-template-columns:1.4fr 1fr 1.2fr 80px}.grid-head{font-size:12px;font-weight:700;color:#64748b}.grid-input{padding:8px 10px;border:1px solid var(--card-border);border-radius:6px;background:#fff;color:#1e293b}.grid-input.small{width:100%}.mini-btn,.save-btn{height:32px;padding:0 14px;border-radius:6px;border:1px solid var(--accent);cursor:pointer;font-size:12px;font-weight:600}.mini-btn{background:#fff;color:var(--accent)}.save-btn{background:var(--accent);color:#fff}.danger-btn{height:32px;border:1px solid #fca5a5;background:#fef2f2;color:#b91c1c;border-radius:6px;cursor:pointer}.template-fields{display:flex;flex-wrap:wrap;gap:8px}.field-chip,.template-tag{display:inline-flex;align-items:center;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600}.field-chip{background:#f8fafc;color:#475569;border:1px solid #e2e8f0}.template-tag{background:#eff6ff;color:#1d4ed8}.back-fab{position:fixed;left:24px;top:20px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border:none;border-radius:50%;cursor:pointer;background:#fff;color:var(--accent);box-shadow:0 4px 14px var(--accent-border);z-index:50}.back-fab svg{width:22px;height:22px}
</style>