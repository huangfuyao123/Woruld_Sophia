export type GroupId = 'conference' | 'hardware' | 'software' | 'network'
export type ModuleId = 'woruld_sophia'
export type ProfileType = GroupId | 'teacher' | 'president' | 'root'

export type RoleName =
  | 'president'
  | 'vice_president'
  | 'group_leader'
  | 'vice_group_leader'
  | 'member'
  | 'teacher'
  | 'sophia_admin'

export type Scope =
  | { type: 'self' }
  | { type: 'global' }
  | { type: 'group'; groupId: GroupId }
  | { type: 'groups'; groupIds: GroupId[] }
  | { type: 'module'; module: ModuleId }

export interface RoleAssignment {
  role: RoleName
  scope: Scope
}

export interface User {
  id: string
  username: string
  displayName: string
  email?: string
  avatarUrl?: string
  password: string
  roles: RoleAssignment[]
  isRoot?: boolean
}

export interface AuthUser {
  id: string
  username: string
  displayName: string
  email?: string
  avatarUrl?: string
  bio?: string
  token: string
  roles: RoleAssignment[]
  isRoot?: boolean
}
