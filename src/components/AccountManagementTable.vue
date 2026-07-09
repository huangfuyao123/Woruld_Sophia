<template>
  <section class="acct-board">
    <div class="board-header">
      <h2 class="board-title">账户管理</h2>
      <button class="add-btn" type="button" @click="startAdd">+ 新增账户</button>
    </div>

    <div class="table-scroll">
      <table class="acct-table">
        <thead>
          <tr>
            <th>姓名</th>
            <th>身份</th>
            <th>负责的组</th>
            <th>用户名</th>
            <th>密码</th>
            <th>寰宇智域管理员</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="accounts.length === 0">
            <td colspan="7" class="empty-row">暂无账户</td>
          </tr>
          <tr v-for="acct in accounts" :key="acct.id">
            <td>{{ acct.displayName }}</td>
            <td>{{ formatRoles(acct.roles) }}</td>
            <td>{{ formatGroups(acct.roles) }}</td>
            <td class="mono">{{ acct.username }}</td>
            <td class="mono pwd-cell">
              <span class="pwd-hidden">••••••••</span>
              <button class="show-pwd-btn" type="button" @click="togglePwd(acct.id)">
                {{ shownPwds.has(acct.id) ? (acct.password || '—') : '显示' }}
              </button>
            </td>
            <td>
              <span :class="['badge', acct.isSophiaAdmin ? 'badge-yes' : 'badge-no']">
                {{ acct.isSophiaAdmin ? '是' : '否' }}
              </span>
            </td>
            <td>
              <button class="edit-btn" type="button" @click="startEdit(acct)">编辑</button>
              <button class="del-btn" type="button" @click="handleDelete(acct)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 新增/编辑弹窗 -->
    <div v-if="editing" class="dialog-backdrop" @click="cancelEdit">
      <div class="acct-dialog" @click.stop>
        <h3>{{ editing.id ? '编辑账户' : '新增账户' }}</h3>

        <div class="form-row">
          <label>姓名</label>
          <input v-model="editing.displayName" type="text" placeholder="输入中文姓名" @input="autoUsername" />
        </div>

        <div class="form-row">
          <label>身份</label>
          <select v-model="editing.roleType" @change="onRoleChange">
            <option value="">请选择</option>
            <option value="president">会长</option>
            <option value="vice_president">副会长</option>
            <option value="teacher">指导老师</option>
            <option value="group_leader">组长</option>
            <option value="vice_group_leader">副组长</option>
            <option value="member">组员</option>
          </select>
        </div>

        <div v-if="editing.roleType === 'teacher'" class="form-row">
          <label>负责的组</label>
          <div class="checkbox-group">
            <label v-for="g in GROUP_OPTIONS" :key="g.value" class="checkbox-item">
              <input
                type="checkbox"
                :value="g.value"
                :checked="editing.teacherGroups.includes(g.value)"
                @change="toggleTeacherGroup(g.value)"
              />
              <span>{{ g.label }}</span>
            </label>
          </div>
        </div>

        <div v-if="['group_leader', 'vice_group_leader', 'member'].includes(editing.roleType)" class="form-row">
          <label>所属分组</label>
          <select v-model="editing.groupId">
            <option value="">请选择</option>
            <option v-for="g in GROUP_OPTIONS" :key="g.value" :value="g.value">{{ g.label }}</option>
          </select>
        </div>

        <div class="form-row">
          <label>用户名</label>
          <input v-model="editing.username" type="text" placeholder="拼音用户名" />
        </div>

        <div class="form-row">
          <label>密码</label>
          <div class="pwd-row">
            <input v-model="editing.password" type="text" placeholder="留空则自动生成" />
            <button class="gen-pwd-btn" type="button" @click="genPassword">生成</button>
          </div>
        </div>

        <div v-if="editing.roleType !== 'teacher'" class="form-row">
          <label>寰宇智域管理员</label>
          <select v-model="editing.isSophiaAdmin">
            <option :value="false">否</option>
            <option :value="true">是</option>
          </select>
        </div>

        <p v-if="dialogError" class="error-msg">{{ dialogError }}</p>

        <div class="dialog-actions">
          <button class="dialog-btn secondary" type="button" @click="cancelEdit">取消</button>
          <button class="dialog-btn primary" type="button" :disabled="saving" @click="saveAccount">
            {{ saving ? '保存中…' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { pinyin } from 'pinyin-pro'
import { apiRequest } from '@/api/client'

interface AccountRow {
  id: number
  displayName: string
  username: string
  password: string
  roles: { role: string; scope: { type: string; groupId?: string; groupIds?: string[] } }[]
  isSophiaAdmin: boolean
}

interface EditingForm {
  id: number | null
  displayName: string
  roleType: string
  teacherGroups: string[]
  groupId: string
  username: string
  password: string
  isSophiaAdmin: boolean
}

const GROUP_OPTIONS = [
  { value: 'conference', label: '会议组' },
  { value: 'hardware', label: '硬件组' },
  { value: 'software', label: '软件组' },
  { value: 'network', label: '网络组' },
]

const ROLE_LABELS: Record<string, string> = {
  president: '会长',
  vice_president: '副会长',
  teacher: '指导老师',
  group_leader: '组长',
  vice_group_leader: '副组长',
  member: '组员',
}

const accounts = ref<AccountRow[]>([])
const shownPwds = ref<Set<number>>(new Set())
const editing = ref<EditingForm | null>(null)
const saving = ref(false)
const dialogError = ref('')

async function loadAccounts() {
  try {
    accounts.value = await apiRequest<AccountRow[]>('/api/accounts')
  } catch {
    /* ignore */
  }
}

onMounted(loadAccounts)

function togglePwd(id: number) {
  const next = new Set(shownPwds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  shownPwds.value = next
}

function formatRoles(roles: AccountRow['roles']): string {
  return roles
    .filter((r) => r.role !== 'sophia_admin')
    .map((r) => ROLE_LABELS[r.role] || r.role)
    .join('、') || '—'
}

function formatGroups(roles: AccountRow['roles']): string {
  for (const r of roles) {
    if (r.scope.type === 'group' && r.scope.groupId) return GROUP_OPTIONS.find((g) => g.value === r.scope.groupId)?.label || r.scope.groupId
    if (r.scope.type === 'groups' && r.scope.groupIds) {
      return r.scope.groupIds.map((gid) => GROUP_OPTIONS.find((g) => g.value === gid)?.label || gid).join('、')
    }
  }
  return '—'
}

function autoUsername() {
  if (!editing.value) return
  const name = editing.value.displayName.trim()
  if (name) {
    editing.value.username = pinyin(name, { toneType: 'none', type: 'array' }).join('')
  }
}

function onRoleChange() {
  if (!editing.value) return
  if (editing.value.roleType !== 'teacher') {
    editing.value.teacherGroups = []
  }
  if (!['group_leader', 'vice_group_leader', 'member'].includes(editing.value.roleType)) {
    editing.value.groupId = ''
  }
}

function toggleTeacherGroup(g: string) {
  if (!editing.value) return
  const idx = editing.value.teacherGroups.indexOf(g)
  if (idx >= 0) editing.value.teacherGroups.splice(idx, 1)
  else editing.value.teacherGroups.push(g)
}

async function genPassword() {
  try {
    const res = await apiRequest<{ password: string }>('/api/generate-password')
    if (editing.value) editing.value.password = res.password
  } catch {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    if (editing.value) editing.value.password = Array.from({ length: 8 }, () => chars[Math.floor(Math.random() * chars.length)]).join('')
  }
}

function startAdd() {
  editing.value = {
    id: null,
    displayName: '',
    roleType: '',
    teacherGroups: [],
    groupId: '',
    username: '',
    password: '',
    isSophiaAdmin: false,
  }
  dialogError.value = ''
}

function startEdit(acct: AccountRow) {
  const firstRole = acct.roles.find((r) => r.role !== 'sophia_admin')
  editing.value = {
    id: acct.id,
    displayName: acct.displayName,
    roleType: firstRole?.role || '',
    teacherGroups: firstRole?.scope.type === 'groups' ? [...(firstRole.scope.groupIds || [])] : [],
    groupId: firstRole?.scope.type === 'group' ? firstRole.scope.groupId || '' : '',
    username: acct.username,
    password: '',
    isSophiaAdmin: acct.isSophiaAdmin,
  }
  dialogError.value = ''
}

function cancelEdit() {
  editing.value = null
  dialogError.value = ''
}

function buildRolesPayload(form: EditingForm) {
  const roles: { role: string; scope: { type: string; groupId?: string; groupIds?: string[] } }[] = []
  if (form.roleType === 'president' || form.roleType === 'vice_president') {
    roles.push({ role: form.roleType, scope: { type: 'global' } })
  } else if (form.roleType === 'teacher') {
    roles.push({ role: 'teacher', scope: { type: 'groups', groupIds: form.teacherGroups } })
  } else if (form.roleType && form.groupId) {
    roles.push({ role: form.roleType, scope: { type: 'group', groupId: form.groupId } })
  }
  return roles
}

async function saveAccount() {
  if (!editing.value) return
  const f = editing.value
  dialogError.value = ''
  if (!f.displayName.trim()) {
    dialogError.value = '请填写姓名'
    return
  }
  if (!f.roleType) {
    dialogError.value = '请选择身份'
    return
  }
  if (f.roleType === 'teacher' && f.teacherGroups.length === 0) {
    dialogError.value = '指导老师需选择负责的组'
    return
  }
  if (['group_leader', 'vice_group_leader', 'member'].includes(f.roleType) && !f.groupId) {
    dialogError.value = '请选择所属分组'
    return
  }
  if (!f.username.trim()) {
    dialogError.value = '请填写用户名'
    return
  }

  saving.value = true
  try {
    const payload: Record<string, unknown> = {
      displayName: f.displayName,
      username: f.username,
      roles: buildRolesPayload(f),
      isSophiaAdmin: f.isSophiaAdmin,
    }
    if (f.password) payload.password = f.password

    if (f.id) {
      await apiRequest(`/api/accounts/${f.id}/update`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      })
    } else {
      const res = await apiRequest<{ password: string }>('/api/accounts/create', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      if (!f.password && res.password) {
        console.log(`新账户密码: ${res.password}`)
      }
    }
    editing.value = null
    await loadAccounts()
  } catch (e) {
    dialogError.value = (e as Error).message || '保存失败'
  } finally {
    saving.value = false
  }
}

async function handleDelete(acct: AccountRow) {
  if (!confirm(`确定删除账户「${acct.displayName}」吗？`)) return
  try {
    await apiRequest(`/api/accounts/${acct.id}/delete`, { method: 'DELETE' })
    await loadAccounts()
  } catch {
    /* ignore */
  }
}
</script>

<style scoped>
.acct-board {
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  background: #fff;
  overflow: hidden;
  max-width: 1200px;
  margin: 0 auto;
}

.board-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--card-border);
}

.board-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--accent);
}

.add-btn {
  padding: 8px 16px;
  border: 1px solid var(--accent);
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.add-btn:hover { filter: brightness(1.1); }

.table-scroll { overflow-x: auto; }

.acct-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.acct-table thead th {
  padding: 10px 16px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  background: #f8fafc;
  border-bottom: 1px solid var(--card-border);
  white-space: nowrap;
}

.acct-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
}

.acct-table tbody tr:hover { background: #f8fafc; }

.acct-table td {
  padding: 8px 16px;
  color: #334155;
}

.empty-row {
  padding: 32px !important;
  text-align: center;
  color: #94a3b8;
}

.mono {
  font-family: 'JuliaMono Medium', sans-serif;
}

.pwd-cell { display: flex; align-items: center; gap: 8px; }

.pwd-hidden { color: #94a3b8; }

.show-pwd-btn {
  border: none;
  background: transparent;
  color: var(--accent);
  font-size: 12px;
  cursor: pointer;
  text-decoration: underline;
}

.badge {
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge-yes { background: #f5f3ff; color: #7c3aed; }
.badge-no { background: #f1f5f9; color: #94a3b8; }

.edit-btn, .del-btn {
  padding: 4px 10px;
  border: 1px solid var(--card-border);
  border-radius: 4px;
  background: #fff;
  font-size: 12px;
  cursor: pointer;
  margin-right: 4px;
  transition: 0.15s;
}

.edit-btn:hover { border-color: var(--accent); color: var(--accent); }
.del-btn:hover { border-color: #f87171; color: #b91c1c; background: #fef2f2; }

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

.acct-dialog {
  width: min(100%, 480px);
  padding: 28px 24px;
  border-radius: 12px;
  background: #fff;
  color: #111827;
  max-height: 90vh;
  overflow-y: auto;
}

.acct-dialog h3 {
  margin: 0 0 20px;
  font-size: 20px;
}

.form-row {
  margin-bottom: 16px;
}

.form-row > label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-row input, .form-row select {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #1f2937;
}

.form-row input:focus, .form-row select:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  cursor: pointer;
}

.pwd-row {
  display: flex;
  gap: 8px;
}

.pwd-row input { flex: 1; }

.gen-pwd-btn {
  padding: 9px 14px;
  border: 1px solid #7c3aed;
  border-radius: 8px;
  background: #f5f3ff;
  color: #7c3aed;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}

.gen-pwd-btn:hover { background: #ede9fe; }

.error-msg {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 6px;
  background: #fef2f2;
  color: #b91c1c;
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

.dialog-btn.secondary { background: #e5e7eb; color: #1f2937; }
.dialog-btn.primary { background: #7c3aed; color: #fff; }
.dialog-btn.primary:hover { background: #6d28d9; }
.dialog-btn.secondary:hover { background: #d1d5db; }
</style>
