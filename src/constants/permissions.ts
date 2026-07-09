import type { GroupId, ModuleId, RoleName } from '@/types/auth'

export const GROUP_LABELS: Record<GroupId, string> = {
  conference: '会议组',
  hardware: '硬件组',
  software: '软件组',
  network: '网络组',
}

export const ROLE_LABELS: Record<RoleName, string> = {
  member: '组员',
  group_leader: '组长',
  vice_group_leader: '副组长',
  president: '会长',
  vice_president: '副会长',
  teacher: '指导老师',
  sophia_admin: '寰宇智域管理员',
}

export const MODULE_LABELS: Record<ModuleId, string> = {
  woruld_sophia: '寰宇智域',
}
