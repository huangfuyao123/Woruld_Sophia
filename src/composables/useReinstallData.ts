import { computed, reactive, watch } from 'vue'

export interface Area {
  name: string
  classrooms: string[]
}

export interface ClassroomRecord {
  reinstallStatus: string
  operator: string
  remark: string
}

const STORAGE_KEY = 'hw_reinstall_table'

export const REINSTALL_AREAS: Area[] = [
  { name: 'A区', classrooms: ['A101', 'A103', 'A201', 'A203', 'A301', 'A303'] },
  {
    name: 'B区',
    classrooms: ['B101', 'B102', 'B103', 'B104', 'B201', 'B202', 'B203', 'B204', 'B301', 'B302', 'B303', 'B304', 'B401', 'B402'],
  },
  {
    name: 'C区',
    classrooms: ['C101', 'C102', 'C103', 'C104', 'C201', 'C202', 'C203', 'C204', 'C301', 'C302', 'C303', 'C304', 'C401', 'C402', 'C403', 'C404'],
  },
  {
    name: 'D区',
    classrooms: ['D102', 'D104', 'D105', 'D106', 'D108', 'D202', 'D204', 'D206', 'D209', 'D302', 'D303', 'D304', 'D305', 'D306', 'D307', 'D402', 'D403', 'D404', 'D405', 'D406', 'D407', 'D502', 'D503', 'D504', 'D505', 'D506', 'D507'],
  },
  {
    name: '外语楼',
    classrooms: ['外101', '外104', '外105', '外106', '外107', '外108', '外109', '外110', '外111', '外113', '外210', '外211', '外212', '外213', '外214', '外215', '外307', '外409', '外412'],
  },
  { name: 'E区', classrooms: ['E101', 'E102', 'E103', 'E104', 'E105', 'E201', 'E202', 'E203', 'E204', 'E205'] },
  {
    name: 'F区',
    classrooms: ['F104', 'F105', 'F108', 'F109', 'F201', 'F202', 'F203', 'F204', 'F205', 'F208', 'F209', 'F302', 'F304', 'F305', 'F307', 'F309', 'F310', 'F404', 'F405', 'F409', 'F410', 'F504', 'F505', 'F509', 'F510'],
  },
]

function loadRecords(): Record<string, ClassroomRecord> {
  const result: Record<string, ClassroomRecord> = {}
  for (const area of REINSTALL_AREAS) {
    for (const room of area.classrooms) {
      result[room] = { reinstallStatus: '', operator: '', remark: '' }
    }
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const saved = JSON.parse(raw) as Record<string, Partial<ClassroomRecord>>
      for (const [room, data] of Object.entries(saved)) {
        if (result[room]) {
          result[room] = { ...result[room], ...data }
        }
      }
    }
  } catch {
    /* fallthrough */
  }
  return result
}

const records = reactive(loadRecords())

let saveTimer: ReturnType<typeof setTimeout> | null = null
watch(
  records,
  () => {
    if (saveTimer) clearTimeout(saveTimer)
    saveTimer = setTimeout(() => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(records))
    }, 500)
  },
  { deep: true },
)

const allClassrooms = computed(() => REINSTALL_AREAS.flatMap((a) => a.classrooms))

export function useReinstallData() {
  function getRecord(room: string): ClassroomRecord {
    return records[room] ?? { reinstallStatus: '', operator: '', remark: '' }
  }

  const totalCount = computed(() => allClassrooms.value.length)
  const reinstalledCount = computed(
    () => allClassrooms.value.filter((r) => getRecord(r).reinstallStatus === '已重装').length,
  )
  const newHostCount = computed(
    () => allClassrooms.value.filter((r) => getRecord(r).reinstallStatus === '新主机').length,
  )
  const pendingCount = computed(() => totalCount.value - reinstalledCount.value - newHostCount.value)
  const progressPercent = computed(() =>
    Math.round(((reinstalledCount.value + newHostCount.value) / totalCount.value) * 100),
  )

  function areaDoneCount(area: Area): number {
    return area.classrooms.filter((r) => getRecord(r).reinstallStatus).length
  }

  return {
    records,
    getRecord,
    totalCount,
    reinstalledCount,
    newHostCount,
    pendingCount,
    progressPercent,
    areaDoneCount,
  }
}
