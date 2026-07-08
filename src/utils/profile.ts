import type { AuthUser, GroupId, ProfileType } from '@/types/auth'

const PROFILE_ROUTE_MAP: Record<ProfileType, string> = {
  conference: '/profile/conference',
  hardware: '/profile/hardware',
  software: '/profile/software',
  network: '/profile/network',
  teacher: '/profile/teacher',
  president: '/profile/president',
}

export function getUserPrimaryGroup(user: AuthUser | null | undefined): GroupId | null {
  if (!user) return null

  const groupRole = user.roles.find(
    (assignment) =>
      (assignment.role === 'group_leader' || assignment.role === 'member') &&
      assignment.scope.type === 'group',
  )

  if (groupRole?.scope.type === 'group') {
    return groupRole.scope.groupId
  }

  return null
}

export function isTeacher(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  return user.roles.some(
    (assignment) => assignment.role === 'teacher' && assignment.scope.type === 'groups',
  )
}

export function isPresident(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  return user.roles.some(
    (assignment) => assignment.role === 'president' && assignment.scope.type === 'global',
  )
}

export function hasSophiaAdminRole(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  return user.roles.some(
    (assignment) =>
      assignment.role === 'sophia_admin' &&
      assignment.scope.type === 'module' &&
      assignment.scope.module === 'woruld_sophia',
  )
}

export function resolveProfileType(user: AuthUser | null | undefined): ProfileType | null {
  if (!user) return null

  if (isPresident(user)) return 'president'
  if (isTeacher(user)) return 'teacher'

  const groupId = getUserPrimaryGroup(user)
  if (groupId) return groupId

  return null
}

export function resolveProfileRoute(user: AuthUser | null | undefined): string {
  const profileType = resolveProfileType(user)
  if (!profileType) return '/'
  return PROFILE_ROUTE_MAP[profileType]
}

export function canAccessProfileType(
  user: AuthUser | null | undefined,
  profileType: ProfileType,
): boolean {
  return resolveProfileType(user) === profileType
}
