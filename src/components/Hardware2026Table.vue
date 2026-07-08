<template>
  <section class="hw2026-board">
    <!-- 表名（负责人/指导老师可编辑） -->
    <div class="board-header">
      <input
        v-if="canEditTableName"
        v-model="tableName.value"
        class="board-title-input"
        type="text"
      />
      <h2 v-else class="board-title">{{ tableName.value }}</h2>

      <div class="board-summary">
        <span class="summary-chip total">总报修 {{ totalCount }}</span>
        <span class="summary-chip solved">已解决 {{ solvedCount }}</span>
        <span class="summary-chip unsolved">未解决 {{ unsolvedCount }}</span>
        <span class="summary-chip second">二次维修 {{ hasSecondRepair }}</span>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="board-toolbar">
      <button v-if="canAddRow" class="add-row-btn" type="button" @click="addRow">+ 新增记录</button>
    </div>

    <!-- 表格 -->
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
            <th>问题时间</th>
            <th>教室</th>
            <th>报修节数</th>
            <th>具体问题</th>
            <th>维修日期</th>
            <th>维修时间段</th>
            <th>维修情况</th>
            <th>是否解决</th>
            <th>维修人员</th>
            <th>维修时长</th>
            <th>备注</th>
            <th>故障照片</th>
            <th>二次维修时间</th>
            <th>维修人员</th>
            <th>维修内容</th>
            <th>是否解决</th>
            <th>维修时间段</th>
            <th>维修时长</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="records.length === 0">
            <td colspan="19" class="empty-row">暂无记录，点击「新增记录」开始填写</td>
          </tr>
          <tr v-for="row in records" :key="row.id">
            <td class="col-actions">
              <button
                v-if="canAddRow"
                class="delete-btn"
                type="button"
                @click="deleteRow(row.id)"
              >删除</button>
            </td>

            <td><input v-model="row.problemDate" type="date" class="date-input" :disabled="!canEditContent" /></td>
            <td><input v-model="row.classroom" type="text" class="text-input" placeholder="教室" :disabled="!canEditContent" /></td>
            <td>
              <select v-model="row.repairPeriod" class="select-input" :disabled="!canEditContent">
                <option value="">—</option>
                <option v-for="opt in REPAIR_PERIODS" :key="opt" :value="opt">{{ opt }}</option>
              </select>
            </td>
            <td><input v-model="row.problemDetail" type="text" class="text-input" placeholder="问题描述" :disabled="!canEditContent" /></td>

            <td><input v-model="row.firstRepairDate" type="date" class="date-input" :disabled="!canEditContent" /></td>
            <td class="time-range-cell">
              <div class="time-range">
                <input v-model="row.firstRepairStart" type="time" class="time-input" :disabled="!canEditContent" />
                <span>~</span>
                <input v-model="row.firstRepairEnd" type="time" class="time-input" :disabled="!canEditContent" />
              </div>
            </td>
            <td><input v-model="row.firstRepairStatus" type="text" class="text-input" placeholder="维修情况" :disabled="!canEditContent" /></td>
            <td>
              <select v-model="row.firstSolved" class="select-input" :disabled="!canEditContent" :data-status="row.firstSolved">
                <option value="">—</option>
                <option v-for="opt in SOLVED_OPTIONS" :key="opt" :value="opt">{{ opt }}</option>
              </select>
            </td>
            <td><input v-model="row.firstRepairPerson" type="text" class="text-input" placeholder="维修人员" :disabled="!canEditContent" /></td>
            <td class="duration-cell">{{ calcDuration(row.firstRepairStart, row.firstRepairEnd) }}</td>
            <td><input v-model="row.remark" type="text" class="text-input" placeholder="备注" :disabled="!canEditContent" /></td>
            <td class="photo-cell">
              <div class="photo-area">
                <img v-if="row.faultPhoto" :src="row.faultPhoto" class="photo-preview" alt="故障照片" @click="previewPhoto(row.faultPhoto)" />
                <label v-if="canEditContent" class="photo-upload">
                  <input type="file" accept="image/*" class="photo-file" @change="(e) => onPhotoChange(e, row)" />
                  <span>{{ row.faultPhoto ? '更换' : '上传' }}</span>
                </label>
                <button v-if="row.faultPhoto && canEditContent" class="photo-clear" type="button" @click="row.faultPhoto = ''">清除</button>
              </div>
            </td>

            <td><input v-model="row.secondRepairDate" type="date" class="date-input" :disabled="!canEditContent" /></td>
            <td><input v-model="row.secondRepairPerson" type="text" class="text-input" placeholder="维修人员" :disabled="!canEditContent" /></td>
            <td><input v-model="row.secondRepairContent" type="text" class="text-input" placeholder="维修内容" :disabled="!canEditContent" /></td>
            <td>
              <select v-model="row.secondSolved" class="select-input" :disabled="!canEditContent" :data-status="row.secondSolved">
                <option value="">—</option>
                <option v-for="opt in SOLVED_OPTIONS" :key="opt" :value="opt">{{ opt }}</option>
              </select>
            </td>
            <td class="time-range-cell">
              <div class="time-range">
                <input v-model="row.secondRepairStart" type="time" class="time-input" :disabled="!canEditContent" />
                <span>~</span>
                <input v-model="row.secondRepairEnd" type="time" class="time-input" :disabled="!canEditContent" />
              </div>
            </td>
            <td class="duration-cell">{{ calcDuration(row.secondRepairStart, row.secondRepairEnd) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 照片预览弹窗 -->
    <div v-if="previewUrl" class="photo-modal" @click="previewUrl = ''">
      <img :src="previewUrl" class="photo-modal-img" alt="预览" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { calcDuration, useHardware2026Data, type RepairRecord } from '@/composables/useHardware2026Data'

const {
  records,
  tableName,
  canEditTableName,
  canEditContent,
  canAddRow,
  totalCount,
  solvedCount,
  unsolvedCount,
  hasSecondRepair,
  addRow,
  deleteRow,
} = useHardware2026Data()

const REPAIR_PERIODS = ['维修', '12节', '34节', '56节', '78节', '910节', '保障']
const SOLVED_OPTIONS = ['已解决', '未解决', '未完全解决']

const previewUrl = ref('')

function previewPhoto(url: string): void {
  previewUrl.value = url
}

function onPhotoChange(e: Event, row: RepairRecord): void {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    const reader = new FileReader()
    reader.onload = () => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const maxW = 600
        const scale = img.width > maxW ? maxW / img.width : 1
        canvas.width = img.width * scale
        canvas.height = img.height * scale
        const ctx = canvas.getContext('2d')
        if (ctx) {
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          row.faultPhoto = canvas.toDataURL('image/jpeg', 0.7)
        }
      }
      img.src = reader.result as string
    }
    reader.readAsDataURL(file)
  } else {
    const reader = new FileReader()
    reader.onload = () => {
      row.faultPhoto = reader.result as string
    }
    reader.readAsDataURL(file)
  }
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

.board-toolbar {
  padding: 12px 24px;
  border-bottom: 1px solid var(--card-border);
}

.add-row-btn {
  padding: 6px 16px;
  border: 1px solid var(--accent);
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.15s;
}

.add-row-btn:hover {
  filter: brightness(1.1);
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
</style>
