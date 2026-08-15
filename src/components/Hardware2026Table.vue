<template>
  <section class="hw2026-board">
    <div class="board-header">
      <input v-if="canEditTableName" v-model="tableName" class="board-title-input" type="text" @keydown.enter.prevent="handleEnterSave" @blur="handleEnterSave" />
      <h2 v-else class="board-title">{{ tableName }}</h2>
      <div class="board-summary">
        <span class="summary-chip total">总报修 {{ totalCount }}</span>
        <span class="summary-chip solved">已解决 {{ solvedCount }}</span>
        <span class="summary-chip unsolved">未解决 {{ unsolvedCount }}</span>
        <span class="summary-chip second">二次维修 {{ hasSecondRepair }}</span>
      </div>
    </div>

    <div class="board-toolbar board-toolbar-inline">
      <div class="toolbar-left">
        <span class="schema-toolbar-label">月份选择</span>
        <select class="month-select" :value="selectedMonthId ?? ''" @change="onMonthChange">
          <option value="">请选择</option>
          <option v-for="m in monthList" :key="m.id" :value="m.id">{{ m.month }}</option>
        </select>
        <button v-if="canManageSchema" class="schema-reset-btn month-manage-btn" type="button" @click="openMonthManage">月份管理</button>
        <button v-if="canEditFieldSchema" class="schema-reset-btn" type="button" @click="toggleFieldEdit">{{ isFieldEditing ? '完成编辑' : '字段编辑' }}</button>
      </div>
      <div class="toolbar-right">
        <button v-if="canAddRow && selectedMonthId" class="add-row-btn" type="button" @click="addRow">+ 新增记录</button>
      </div>
    </div>

    <div v-if="!monthList.length" class="month-hint">当前还没有月份，请负责人/指导老师先新增月份</div>
    <div v-else class="month-current">当前：<span class="month-current-text">{{ activeMonth }} 月份表</span></div>

    <div v-if="canEditFieldSchema && isFieldEditing" class="schema-toolbar">
      <span class="schema-toolbar-label">字段结构编辑中（回车保存）</span>
      <button class="schema-reset-btn" type="button" @click="resetColumnLabels">恢复默认字段名</button>
    </div>

    <div class="table-scroll">
      <table class="repair-table">
        <thead>
          <tr class="group-row">
            <th rowspan="2" class="col-actions">操作</th>
            <th colspan="4" class="group-problem">问题信息</th>
            <th colspan="8" class="group-first">第一次维修</th>
            <th colspan="6" class="group-second">二次维修</th>
          </tr>
          <tr>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.problemDate" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.problemDate }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.classroom" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.classroom }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.repairPeriod" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.repairPeriod }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.problemDetail" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.problemDetail }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstRepairDate" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstRepairDate }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstRepairTimeRange" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstRepairTimeRange }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstRepairStatus" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstRepairStatus }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstSolved" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstSolved }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstRepairPerson" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstRepairPerson }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.firstRepairDuration" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.firstRepairDuration }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.remark" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.remark }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.faultPhoto" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.faultPhoto }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondRepairDate" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondRepairDate }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondRepairPerson" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondRepairPerson }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondRepairContent" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondRepairContent }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondSolved" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondSolved }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondRepairTimeRange" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondRepairTimeRange }}</template></th>
            <th><input v-if="canEditFieldSchema && isFieldEditing" v-model="columnLabels.secondRepairDuration" @blur="handleEnterSave" class="header-input" type="text" @keydown.enter.prevent="handleEnterSave" /><template v-else>{{ columnLabels.secondRepairDuration }}</template></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="records.length === 0">
            <td colspan="19" class="empty-row">暂无记录，点击「新增记录」开始填写</td>
          </tr>
          <tr v-for="row in records" :key="row.id">
            <td class="col-actions"><button v-if="canAddRow" class="delete-btn" type="button" @click="deleteRow(row.id)">删除</button></td>
            <td><input v-model="row.problemDate" type="date" class="date-input" :disabled="!canEditContent" /></td>
            <td><input v-model="row.classroom" type="text" class="text-input" placeholder="教室" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td><select v-model="row.repairPeriod" class="select-input" :disabled="!canEditContent" @change="saveRow(row)"><option value="">—</option><option v-for="opt in REPAIR_PERIODS" :key="opt" :value="opt">{{ opt }}</option></select></td>
            <td><input v-model="row.problemDetail" type="text" class="text-input" placeholder="问题描述" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td><input v-model="row.firstRepairDate" type="date" class="date-input" :disabled="!canEditContent" @change="saveRow(row)" /></td>
            <td class="time-range-cell"><div class="time-range"><input v-model="row.firstRepairStart" type="time" class="time-input" :disabled="!canEditContent" @change="saveRow(row)" /><span>~</span><input v-model="row.firstRepairEnd" type="time" class="time-input" :disabled="!canEditContent" @change="saveRow(row)" /></div></td>
            <td><input v-model="row.firstRepairStatus" type="text" class="text-input" placeholder="维修情况" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td><select v-model="row.firstSolved" class="select-input" :disabled="!canEditContent" :data-status="row.firstSolved" @change="saveRow(row)"><option value="">—</option><option v-for="opt in SOLVED_OPTIONS" :key="opt" :value="opt">{{ opt }}</option></select></td>
            <td><input v-model="row.firstRepairPerson" type="text" class="text-input" placeholder="维修人员" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td class="duration-cell">{{ calcDuration(row.firstRepairStart, row.firstRepairEnd) }}</td>
            <td><input v-model="row.remark" type="text" class="text-input" placeholder="备注" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td class="photo-cell">
              <div class="photo-area">
                <img v-if="row.faultPhoto" :src="row.faultPhoto" class="photo-preview" alt="故障照片" @click="previewPhoto(row.faultPhoto)" />
                <label v-if="canEditContent" class="photo-upload">
                  <input type="file" accept="image/*" class="photo-file" @change="(e) => onPhotoChange(e, row)" />
                  <span>{{ row.faultPhoto ? '更换' : '上传' }}</span>
                </label>
                <button v-if="row.faultPhoto && canEditContent" class="photo-clear" type="button" @click="clearPhoto(row)">清除</button>
              </div>
            </td>
            <td><input v-model="row.secondRepairDate" type="date" class="date-input" :disabled="!canEditContent" @change="saveRow(row)" /></td>
            <td><input v-model="row.secondRepairPerson" type="text" class="text-input" placeholder="维修人员" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td><input v-model="row.secondRepairContent" type="text" class="text-input" placeholder="维修内容" :disabled="!canEditContent" @keydown.enter.prevent="saveRow(row)" @blur="saveRow(row)" /></td>
            <td><select v-model="row.secondSolved" class="select-input" :disabled="!canEditContent" :data-status="row.secondSolved" @change="saveRow(row)"><option value="">—</option><option v-for="opt in SOLVED_OPTIONS" :key="opt" :value="opt">{{ opt }}</option></select></td>
            <td class="time-range-cell"><div class="time-range"><input v-model="row.secondRepairStart" type="time" class="time-input" :disabled="!canEditContent" @change="saveRow(row)" /><span>~</span><input v-model="row.secondRepairEnd" type="time" class="time-input" :disabled="!canEditContent" @change="saveRow(row)" /></div></td>
            <td class="duration-cell">{{ calcDuration(row.secondRepairStart, row.secondRepairEnd) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="previewUrl" class="photo-modal" @click="previewUrl = ''">
      <img :src="previewUrl" class="photo-modal-img" alt="预览" />
    </div>

    <div v-if="showMonthDialog" class="photo-modal month-modal" @click.self="closeMonthManage">
      <div class="month-modal-card">
        <div class="month-modal-head">
          <h3>月份管理</h3>
          <button class="close-btn" type="button" @click="closeMonthManage">×</button>
        </div>
        <div class="month-modal-body">
          <div class="month-form-row">
            <input v-model="monthDraft" class="month-input" type="text" placeholder="例如：2026-07" @keydown.enter.prevent="submitMonthDraft" />
            <button class="month-save-btn" type="button" @click="submitMonthDraft">新增</button>
          </div>
          <div class="month-list">
            <div v-for="m in monthList" :key="m.id" class="month-list-item">
              <input v-model="monthEditMap[m.id]" class="month-input month-inline-input" type="text" @keydown.enter.prevent="renameMonth(m.id)" />
              <button class="month-mini-btn" type="button" @click="renameMonth(m.id)">保存</button>
              <button class="month-mini-btn danger" type="button" @click="removeMonth(m.id)">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { calcDuration, useHardware2026Data, type RepairRecord } from '@/composables/useHardware2026Data'

const {
  records,
  tableName,
  columnLabels,
  monthList,
  activeMonth,
  selectedMonthId,
  canManageSchema,
  canEditTableName,
  canEditFieldSchema,
  canEditContent,
  canAddRow,
  totalCount,
  solvedCount,
  unsolvedCount,
  hasSecondRepair,
  addRow,
  deleteRow,
  addMonth,
  updateMonth,
  deleteMonth,
  setMonth,
  flushSave,
  resetColumnLabels: resetColumnLabelsRemote,
  renameTable,
  saveRecord,
} = useHardware2026Data()

const REPAIR_PERIODS = ['维修', '12节', '34节', '56节', '78节', '910节', '保障']
const SOLVED_OPTIONS = ['已解决', '未解决', '未完全解决']

const previewUrl = ref('')
const showMonthDialog = ref(false)
const monthDraft = ref('')
const monthEditMap = ref<Record<number, string>>({})
const isFieldEditing = ref(false)

watch(monthList, (list) => {
  const next: Record<number, string> = {}
  list.forEach((m) => {
    next[m.id] = m.month
  })
  monthEditMap.value = next
}, { immediate: true, deep: true })

function previewPhoto(url: string): void {
  previewUrl.value = url
}

async function handleEnterSave(): Promise<void> {
  await renameTable(tableName.value)
  await flushSave()
}

function openMonthManage(): void {
  showMonthDialog.value = true
}

function closeMonthManage(): void {
  showMonthDialog.value = false
  monthDraft.value = ''
}

async function submitMonthDraft(): Promise<void> {
  const month = monthDraft.value.trim()
  if (!month) return
  await addMonth(month)
  monthDraft.value = ''
}

async function renameMonth(id: number): Promise<void> {
  const month = (monthEditMap.value[id] || '').trim()
  if (!month) return
  await updateMonth(id, month)
}

async function removeMonth(id: number): Promise<void> {
  await deleteMonth(id)
}

function toggleFieldEdit(): void {
  isFieldEditing.value = !isFieldEditing.value
}

function onMonthChange(e: Event): void {
  const v = Number((e.target as HTMLSelectElement).value)
  if (v) setMonth(v)
}

async function resetColumnLabels(): Promise<void> {
  await resetColumnLabelsRemote()
}

async function saveRow(row: RepairRecord): Promise<void> {
  await saveRecord(row)
}

async function clearPhoto(row: RepairRecord): Promise<void> {
  row.faultPhoto = ''
  await saveRow(row)
}

function onPhotoChange(e: Event, row: RepairRecord): void {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = async () => {
    row.faultPhoto = reader.result as string
    await saveRow(row)
  }
  reader.readAsDataURL(file)
  target.value = ''
}
</script>

<style scoped>
.hw2026-board {
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  background: #fff;
  overflow: hidden;
}

.board-header {
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--card-border);
  background: linear-gradient(135deg, rgba(185, 28, 28, 0.04), transparent);
}

.board-title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 700;
  color: var(--accent);
}

.board-title-input {
  display: block;
  width: 100%;
  max-width: 300px;
  margin: 0 0 12px;
  padding: 6px 10px;
  border: 1px solid var(--accent);
  border-radius: 6px;
  font-size: 17px;
  font-weight: 700;
  color: var(--accent);
  font-family: inherit;
}

.board-title-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--accent-border);
}

.board-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.summary-chip {
  padding: 3px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.summary-chip.total { background: #f1f5f9; color: #475569; }
.summary-chip.solved { background: #f0fdf4; color: #15803d; }
.summary-chip.unsolved { background: #fef2f2; color: #b91c1c; }
.summary-chip.second { background: #fffbeb; color: #b45309; }

.schema-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--card-border);
  background: #fff7ed;
}

.schema-toolbar-label {
  font-size: 12px;
  font-weight: 600;
  color: #9a3412;
}

.board-toolbar {
  padding: 12px 24px;
  border-bottom: 1px solid var(--card-border);
}

.board-toolbar-inline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.month-select {
  min-width: 120px;
  height: 32px;
  padding: 0 10px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
}

.month-hint {
  padding: 10px 24px 0;
  color: #b45309;
  font-size: 12px;
  font-weight: 600;
}

.month-current {
  padding: 8px 24px 0;
  color: #64748b;
  font-size: 12px;
}

.month-current-text {
  color: #b91c1c;
  font-weight: 700;
}

.add-row-btn,
.schema-reset-btn,
.month-save-btn {
  width: 96px;
  height: 32px;
  padding: 0 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.15s;
}

.add-row-btn {
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #fff;
}

.add-row-btn:hover {
  filter: brightness(1.08);
}

.schema-reset-btn {
  border: 1px solid #cbd5e1;
  background: #fff;
  color: #475569;
}

.schema-reset-btn:hover {
  background: #f8fafc;
}

.month-manage-btn {
  color: #9a3412;
  border-color: #fdba74;
  background: #fff7ed;
}

.month-manage-btn:hover {
  background: #ffedd5;
}

.table-scroll {
  overflow-x: auto;
}

.repair-table {
  border-collapse: collapse;
  font-size: 12px;
  white-space: nowrap;
}

.repair-table thead th {
  padding: 8px 10px;
  text-align: center;
  font-weight: 600;
  color: #475569;
  background: #f8fafc;
  border-bottom: 1px solid var(--card-border);
  border-left: 1px solid #f1f5f9;
  position: sticky;
  top: 0;
  z-index: 1;
}

.repair-table thead th:first-child {
  border-left: none;
}

.header-input {
  width: 100%;
  min-width: 72px;
  padding: 4px 6px;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  background: #fff;
  color: #334155;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
}

.header-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-border);
}

.group-row th {
  font-size: 13px;
  color: #1e293b;
}

.group-problem { background: #eff6ff !important; }
.group-first { background: #f0fdf4 !important; }
.group-second { background: #fffbeb !important; }

.col-actions {
  min-width: 60px;
  position: sticky;
  left: 0;
  z-index: 2;
  background: #f8fafc !important;
}

.repair-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
}

.repair-table tbody tr:hover {
  background: #f8fafc;
}

.repair-table td {
  padding: 6px 8px;
  color: #334155;
  border-left: 1px solid #f1f5f9;
  text-align: center;
}

.repair-table td:first-child {
  border-left: none;
}

.empty-row {
  padding: 32px !important;
  text-align: center;
  color: #94a3b8;
}

.text-input,
.date-input,
.select-input {
  width: 100%;
  min-width: 80px;
  max-width: 140px;
  padding: 4px 6px;
  border: 1px solid transparent;
  border-radius: 4px;
  font-size: 12px;
  color: #334155;
  background: transparent;
  transition: 0.15s;
}

.date-input {
  min-width: 130px;
}

.select-input {
  min-width: 90px;
  cursor: pointer;
  background: #fff;
  border: 1px solid var(--card-border);
}

.text-input:focus,
.date-input:focus,
.select-input:focus {
  outline: none;
  border-color: var(--accent);
  background: #fff;
}

.text-input::placeholder {
  color: #cbd5e1;
}

.text-input:disabled,
.date-input:disabled,
.select-input:disabled {
  opacity: 0.7;
  cursor: default;
}

.select-input[data-status='已解决'] {
  color: #15803d;
  font-weight: 600;
}

.select-input[data-status='未解决'] {
  color: #b91c1c;
  font-weight: 600;
}

.select-input[data-status='未完全解决'] {
  color: #b45309;
  font-weight: 600;
}

.time-range-cell {
  min-width: 160px;
}

.time-range {
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: center;
}

.time-range span {
  color: #94a3b8;
  font-size: 11px;
}

.time-input {
  width: 70px;
  padding: 4px 4px;
  border: 1px solid transparent;
  border-radius: 4px;
  font-size: 12px;
  color: #334155;
  background: transparent;
  text-align: center;
}

.time-input:focus {
  outline: none;
  border-color: var(--accent);
  background: #fff;
}

.time-input:disabled {
  opacity: 0.7;
}

.duration-cell {
  font-family: 'JuliaMono Medium', sans-serif;
  font-weight: 600;
  color: var(--accent);
  min-width: 70px;
}

.photo-cell {
  min-width: 90px;
}

.photo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.photo-preview {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid var(--card-border);
  cursor: pointer;
}

.photo-upload {
  cursor: pointer;
  font-size: 11px;
  color: var(--accent);
  text-decoration: underline;
}

.photo-upload input {
  display: none;
}

.photo-clear {
  border: none;
  background: transparent;
  color: #b91c1c;
  font-size: 11px;
  cursor: pointer;
  text-decoration: underline;
}

.delete-btn {
  padding: 4px 10px;
  border: 1px solid #fca5a5;
  border-radius: 4px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 11px;
  cursor: pointer;
  transition: 0.15s;
}

.delete-btn:hover {
  background: #fee2e2;
  border-color: #f87171;
}

.photo-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 24px;
}

.photo-modal-img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 8px;
}

.month-modal-card {
  width: 100%;
  max-width: 520px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid var(--card-border);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.2);
}

.month-modal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  border-bottom: 1px solid var(--card-border);
}

.month-modal-head h3 {
  margin: 0;
  font-size: 16px;
  color: #0f172a;
}

.close-btn {
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 22px;
  cursor: pointer;
}

.month-modal-body {
  padding: 18px;
}

.month-form-row,
.month-list-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.month-form-row {
  margin-bottom: 14px;
}

.month-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.month-input {
  flex: 1;
  height: 36px;
  padding: 0 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 13px;
}

.month-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-border);
}

.month-save-btn {
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #fff;
}

.month-mini-btn {
  min-width: 56px;
  height: 36px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #fff;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.month-mini-btn.danger {
  border-color: #fca5a5;
  background: #fef2f2;
  color: #b91c1c;
}
</style>
