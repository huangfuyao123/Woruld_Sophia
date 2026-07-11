import { computed, reactive, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { canEditGroup, canViewGroup } from '@/utils/permissions'
import { generateUuid } from '@/utils/generateUuid'

export interface RepairRecord {
  id: string
  problemDate: string
  classroom: string
  repairPeriod: string
  problemDetail: string
  firstRepairDate: string
  firstRepairStart: string
  firstRepairEnd: string
  firstRepairStatus: string
  firstSolved: string
  firstRepairPerson: string
  remark: string
  faultPhoto: string
  secondRepairDate: string
  secondRepairPerson: string
  secondRepairContent: string
  secondSolved: string
  secondRepairStart: string
  secondRepairEnd: string
}

export interface Hardware2026ColumnLabels {
  problemDate: string
  classroom: string
  repairPeriod: string
  problemDetail: string
  firstRepairDate: string
  firstRepairTimeRange: string
  firstRepairStatus: string
  firstSolved: string
  firstRepairPerson: string
  firstRepairDuration: string
  remark: string
  faultPhoto: string
  secondRepairDate: string
  secondRepairPerson: string
  secondRepairContent: string
  secondSolved: string
  secondRepairTimeRange: string
  secondRepairDuration: string
}

const STORAGE_KEY = 'hw2026_table'
const NAME_KEY = 'hw2026_table_name'
const COLUMN_LABELS_KEY = 'hw2026_column_labels'

const DEFAULT_COLUMN_LABELS: Hardware2026ColumnLabels = {
  problemDate: '问题时间',
  classroom: '教室',
  repairPeriod: '报修节数',
  problemDetail: '具体问题',
  firstRepairDate: '维修日期',
  firstRepairTimeRange: '维修时间段',
  firstRepairStatus: '维修情况',
  firstSolved: '是否解决',
  firstRepairPerson: '维修人员',
  firstRepairDuration: '维修时长',
  remark: '备注',
  faultPhoto: '故障照片',
  secondRepairDate: '二次维修时间',
  secondRepairPerson: '维修人员',
  secondRepairContent: '维修内容',
  secondSolved: '是否解决',
  secondRepairTimeRange: '维修时间段',
  secondRepairDuration: '维修时长',
}

function createColumnLabels(): Hardware2026ColumnLabels {
  return { ...DEFAULT_COLUMN_LABELS }
}

function createEmptyRecord(): RepairRecord {
  return {
    id: generateUuid(),
    problemDate: '',
    classroom: '',
    repairPeriod: '',
    problemDetail: '',
    firstRepairDate: '',
    firstRepairStart: '',
    firstRepairEnd: '',
    firstRepairStatus: '',
    firstSolved: '',
    firstRepairPerson: '',
    remark: '',
    faultPhoto: '',
    secondRepairDate: '',
    secondRepairPerson: '',
    secondRepairContent: '',
    secondSolved: '',
    secondRepairStart: '',
    secondRepairEnd: '',
  }
}

function loadRecords(): RepairRecord[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as RepairRecord[]
      if (Array.isArray(parsed)) return parsed
    }
  } catch {
    /* fallthrough */
  }
  return []
}

function loadTableName(): string {
  return localStorage.getItem(NAME_KEY) || '硬件组2026'
}

function loadColumnLabels(): Hardware2026ColumnLabels {
  try {
    const raw = localStorage.getItem(COLUMN_LABELS_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as Partial<Hardware2026ColumnLabels>
      return { ...DEFAULT_COLUMN_LABELS, ...parsed }
    }
  } catch {
    /* fallthrough */
  }
  return createColumnLabels()
}

const records = reactive<RepairRecord[]>(loadRecords())
const tableName = reactive({ value: loadTableName() })
const columnLabels = reactive<Hardware2026ColumnLabels>(loadColumnLabels())

let saveTimer: ReturnType<typeof setTimeout> | null = null

function persistTableState(): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(records))
  localStorage.setItem(NAME_KEY, tableName.value)
  localStorage.setItem(COLUMN_LABELS_KEY, JSON.stringify(columnLabels))
}

function scheduleSave(): void {
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(() => {
    persistTableState()
  }, 500)
}

function flushSave(): void {
  if (saveTimer) {
    clearTimeout(saveTimer)
    saveTimer = null
  }
  persistTableState()
}

watch(records, scheduleSave, { deep: true })
watch(tableName, scheduleSave, { deep: true })
watch(columnLabels, scheduleSave, { deep: true })

export function calcDuration(start: string, end: string): string {
  if (!start || !end) return ''
  const parts = start.split(':').map((n) => parseInt(n, 10))
  const parts2 = end.split(':').map((n) => parseInt(n, 10))
  if (parts.length < 2 || parts2.length < 2) return ''
  const sh = parts[0] ?? 0
  const sm = parts[1] ?? 0
  const eh = parts2[0] ?? 0
  const em = parts2[1] ?? 0
  if (isNaN(sh) || isNaN(eh)) return ''
  let minutes = eh * 60 + em - (sh * 60 + sm)
  if (minutes < 0) minutes += 24 * 60
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (mins === 0) return `${hours}h`
  return `${hours}h${mins}min`
}

export function useHardware2026Data() {
  const auth = useAuthStore()

  const canManageSchema = computed(() => {
    const user = auth.user
    if (!user) return false
    if (canEditGroup(user, 'hardware')) return true
    return user.roles.some(
      (a) =>
        a.role === 'teacher' &&
        a.scope.type === 'groups' &&
        a.scope.groupIds.includes('hardware'),
    )
  })

  const canEditTableName = computed(() => canManageSchema.value)
  const canEditFieldSchema = computed(() => canManageSchema.value)

  const canEditContent = computed(() => {
    return canViewGroup(auth.user, 'hardware')
  })

  const canAddRow = computed(() => canEditContent.value)

  const totalCount = computed(() => records.length)
  const solvedCount = computed(
    () => records.filter((r) => r.firstSolved === '已解决' || r.secondSolved === '已解决').length,
  )
  const unsolvedCount = computed(
    () => records.filter((r) => r.firstSolved === '未解决' && r.secondSolved !== '已解决').length,
  )
  const hasSecondRepair = computed(() => records.filter((r) => r.secondRepairDate).length)

  function addRow(): void {
    records.push(createEmptyRecord())
  }

  function deleteRow(id: string): void {
    const idx = records.findIndex((r) => r.id === id)
    if (idx >= 0) records.splice(idx, 1)
  }

  return {
    records,
    tableName,
    columnLabels,
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
    flushSave,
  }
}
