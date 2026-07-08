<template>
  <section class="task-board">
    <div class="board-header">
      <h2 class="board-title">多媒体教室主机系统重装</h2>
      <div class="board-summary">
        <span class="summary-chip total">总计 {{ totalCount }}</span>
        <span class="summary-chip new-host">新主机 {{ newHostCount }}</span>
        <span class="summary-chip reinstalled">已重装 {{ reinstalledCount }}</span>
        <span class="summary-chip pending">未填写 {{ pendingCount }}</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
    </div>

    <div class="board-toolbar">
      <input v-model.trim="searchQuery" type="text" class="search-input" placeholder="搜索教室编号..." />
      <button class="toggle-all-btn" type="button" @click="toggleAllAreas">
        {{ allCollapsed ? '全部展开' : '全部收起' }}
      </button>
    </div>

    <div v-for="area in filteredAreas" :key="area.name" class="area-section">
      <button class="area-header" type="button" @click="toggleArea(area.name)">
        <span class="area-arrow" :class="{ collapsed: isCollapsed(area.name) }">▾</span>
        <span class="area-name">{{ area.name }}</span>
        <span class="area-meta">{{ area.classrooms.length }} 间 · {{ areaDoneCount(area) }} 已完成</span>
      </button>

      <div v-show="!isCollapsed(area.name)" class="table-wrapper">
        <table class="reinstall-table">
          <thead>
            <tr>
              <th class="col-room">教室</th>
              <th class="col-status">是否重装</th>
              <th class="col-operator">重装人员</th>
              <th class="col-remark">备注</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="room in area.classrooms"
              :key="room"
              :class="{ filled: getRecord(room).reinstallStatus }"
            >
              <td class="room-cell">{{ room }}</td>
              <td>
                <select
                  v-model="getRecord(room).reinstallStatus"
                  class="status-select"
                  :data-status="getRecord(room).reinstallStatus"
                >
                  <option value="">—</option>
                  <option value="新主机">新主机</option>
                  <option value="已重装">已重装</option>
                </select>
              </td>
              <td>
                <input
                  v-model="getRecord(room).operator"
                  type="text"
                  class="text-input"
                  placeholder="填写人员"
                />
              </td>
              <td>
                <input
                  v-model="getRecord(room).remark"
                  type="text"
                  class="text-input"
                  placeholder="备注"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <p v-if="filteredAreas.length === 0" class="no-result">未找到匹配的教室</p>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { REINSTALL_AREAS, useReinstallData } from '@/composables/useReinstallData'

const {
  getRecord,
  totalCount,
  reinstalledCount,
  newHostCount,
  pendingCount,
  progressPercent,
  areaDoneCount,
} = useReinstallData()

const searchQuery = ref('')
const collapsedAreas = ref<Set<string>>(new Set())

const allCollapsed = computed(() => collapsedAreas.value.size === REINSTALL_AREAS.length)

const filteredAreas = computed(() => {
  if (!searchQuery.value) return REINSTALL_AREAS
  const q = searchQuery.value.toLowerCase()
  return REINSTALL_AREAS.map((area) => ({
    ...area,
    classrooms: area.classrooms.filter((r) => r.toLowerCase().includes(q)),
  })).filter((area) => area.classrooms.length > 0)
})

function isCollapsed(name: string): boolean {
  return collapsedAreas.value.has(name)
}

function toggleArea(name: string): void {
  const next = new Set(collapsedAreas.value)
  if (next.has(name)) next.delete(name)
  else next.add(name)
  collapsedAreas.value = next
}

function toggleAllAreas(): void {
  if (allCollapsed.value) {
    collapsedAreas.value = new Set()
  } else {
    collapsedAreas.value = new Set(REINSTALL_AREAS.map((a) => a.name))
  }
}
</script>

<style scoped>
.task-board {
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

.board-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.summary-chip {
  padding: 3px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.summary-chip.total {
  background: #f1f5f9;
  color: #475569;
}

.summary-chip.new-host {
  background: #fffbeb;
  color: #b45309;
}

.summary-chip.reinstalled {
  background: #f0fdf4;
  color: #15803d;
}

.summary-chip.pending {
  background: #fef2f2;
  color: #b91c1c;
}

.progress-bar {
  height: 6px;
  border-radius: 3px;
  background: #f1f5f9;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--accent);
  transition: width 0.3s ease;
}

.board-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--card-border);
}

.search-input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  font-size: 13px;
  color: #1e293b;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
  background: #fff;
}

.toggle-all-btn {
  padding: 6px 14px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #475569;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: 0.15s;
}

.toggle-all-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.area-section {
  border-bottom: 1px solid var(--card-border);
}

.area-section:last-child {
  border-bottom: none;
}

.area-header {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 24px;
  border: none;
  background: #f8fafc;
  cursor: pointer;
  transition: background 0.15s;
  text-align: left;
}

.area-header:hover {
  background: #f1f5f9;
}

.area-arrow {
  display: inline-block;
  font-size: 12px;
  color: #94a3b8;
  transition: transform 0.2s;
}

.area-arrow.collapsed {
  transform: rotate(-90deg);
}

.area-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.area-meta {
  font-size: 12px;
  color: #94a3b8;
}

.table-wrapper {
  overflow-x: auto;
}

.reinstall-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.reinstall-table thead th {
  padding: 10px 16px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  background: #f8fafc;
  border-bottom: 1px solid var(--card-border);
  white-space: nowrap;
}

.col-room {
  width: 100px;
}

.col-status {
  width: 120px;
}

.col-operator {
  width: 160px;
}

.reinstall-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.1s;
}

.reinstall-table tbody tr:hover {
  background: #f8fafc;
}

.reinstall-table tbody tr.filled {
  background: rgba(21, 128, 61, 0.02);
}

.reinstall-table td {
  padding: 8px 16px;
  color: #334155;
}

.room-cell {
  font-weight: 600;
  font-family: 'JuliaMono Medium', sans-serif;
  color: #0f172a;
}

.status-select {
  width: 100%;
  padding: 5px 8px;
  border: 1px solid var(--card-border);
  border-radius: 4px;
  font-size: 13px;
  color: #475569;
  background: #fff;
  cursor: pointer;
  transition: 0.15s;
}

.status-select:focus {
  outline: none;
  border-color: var(--accent);
}

.status-select[data-status='新主机'] {
  background: #fffbeb;
  color: #b45309;
  border-color: #fbbf24;
  font-weight: 600;
}

.status-select[data-status='已重装'] {
  background: #f0fdf4;
  color: #15803d;
  border-color: #4ade80;
  font-weight: 600;
}

.text-input {
  width: 100%;
  padding: 5px 8px;
  border: 1px solid transparent;
  border-radius: 4px;
  font-size: 13px;
  color: #334155;
  background: transparent;
  transition: 0.15s;
}

.text-input:focus {
  outline: none;
  border-color: var(--accent);
  background: #fff;
}

.text-input::placeholder {
  color: #cbd5e1;
}

.no-result {
  padding: 32px;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

@media (max-width: 768px) {
  .board-header {
    padding: 16px 16px 12px;
  }

  .board-toolbar {
    padding: 10px 16px;
    flex-direction: column;
    gap: 8px;
  }

  .search-input {
    width: 100%;
  }

  .area-header {
    padding: 10px 16px;
  }

  .reinstall-table {
    font-size: 12px;
  }

  .reinstall-table thead th,
  .reinstall-table td {
    padding: 6px 10px;
  }

  .col-room {
    width: 80px;
  }

  .col-status {
    width: 100px;
  }
}
</style>
