import type { AuthUser, GroupId } from '@/types/auth'

export function hasRole(user: AuthUser | null | undefined, roleName: string): boolean {
  if (!user) return false
  return user.roles.some((assignment) => assignment.role === roleName)
}

export function isRoot(user: AuthUser | null | undefined): boolean {
  return !!user?.isRoot
}

export function isPresidentLike(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  if (user.isRoot) return true
  return user.roles.some(
    (a) =>
      (a.role === 'president' || a.role === 'vice_president') &&
      a.scope.type === 'global',
  )
}

export function canEditOwnProfile(
  user: AuthUser | null | undefined,
  targetUserId: string,
): boolean {
  if (!user) return false
  return user.id === targetUserId || user.isRoot === true
}

export function canManageSophia(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  if (user.isRoot) return true
  return user.roles.some(
    (assignment) =>
      assignment.role === 'sophia_admin' &&
      assignment.scope.type === 'module' &&
      assignment.scope.module === 'woruld_sophia',
  )
}

export function canViewGroup(user: AuthUser | null | undefined, groupId: GroupId): boolean {
  if (!user) return false
  if (user.isRoot) return true
  return user.roles.some((assignment) => {
    if (
      (assignment.role === 'president' || assignment.role === 'vice_president') &&
      assignment.scope.type === 'global'
    ) {
      return true
    }

    if (
      (assignment.role === 'group_leader' ||
        assignment.role === 'vice_group_leader' ||
        assignment.role === 'member') &&
      assignment.scope.type === 'group'
    ) {
      return assignment.scope.groupId === groupId
    }

    if (assignment.role === 'teacher' && assignment.scope.type === 'groups') {
      return assignment.scope.groupIds.includes(groupId)
    }

    return false
  })
}

export function canEditGroup(user: AuthUser | null | undefined, groupId: GroupId): boolean {
  if (!user) return false
  if (user.isRoot) return true
  return user.roles.some((assignment) => {
    if (
      (assignment.role === 'president' || assignment.role === 'vice_president') &&
      assignment.scope.type === 'global'
    ) {
      return true
    }

    if (
      (assignment.role === 'group_leader' || assignment.role === 'vice_group_leader') &&
      assignment.scope.type === 'group'
    ) {
      return assignment.scope.groupId === groupId
    }

    return false
  })
}

export function canEditOwnWorkItem(
  user: AuthUser | null | undefined,
  ownerId: string,
): boolean {
  if (!user) return false
  return user.id === ownerId || user.isRoot === true
}

export function canManageAccounts(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  if (user.isRoot) return true
  return user.roles.some(
    (a) =>
      a.role === 'president' ||
      a.role === 'vice_president' ||
      a.role === 'teacher',
  )
}
