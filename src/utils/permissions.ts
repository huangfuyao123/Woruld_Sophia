import type { AuthUser, GroupId } from '@/types/auth'

export function hasRole(user: AuthUser | null | undefined, roleName: string): boolean {
  if (!user) return false
  return user.roles.some((assignment) => assignment.role === roleName)
}

export function canEditOwnProfile(
  user: AuthUser | null | undefined,
  targetUserId: string,
): boolean {
  if (!user) return false
  return user.id === targetUserId
}

export function canManageSophia(user: AuthUser | null | undefined): boolean {
  if (!user) return false
  return user.roles.some((assignment) => {
    return (
      assignment.role === 'sophia_admin' &&
      assignment.scope.type === 'module' &&
      assignment.scope.module === 'woruld_sophia'
    )
  })
}

export function canViewGroup(user: AuthUser | null | undefined, groupId: GroupId): boolean {
  if (!user) return false
  return user.roles.some((assignment) => {
    if (assignment.role === 'president' && assignment.scope.type === 'global') {
      return true
    }

    if (
      (assignment.role === 'group_leader' || assignment.role === 'member') &&
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
  return user.roles.some((assignment) => {
    if (assignment.role === 'president' && assignment.scope.type === 'global') {
      return true
    }

    if (assignment.role === 'group_leader' && assignment.scope.type === 'group') {
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
  return user.id === ownerId
}
