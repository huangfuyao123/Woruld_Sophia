import { apiRequest } from './client'
import type { AuthUser } from '@/types/auth'
import { resolveProfileType, hasSophiaAdminRole } from '@/utils/profile'

export interface ProfileSummary {
  profileType: ReturnType<typeof resolveProfileType>
  hasSophiaAdminRole: boolean
  user: AuthUser | null
}

export async function getMyProfileSummary(user: AuthUser | null): Promise<ProfileSummary> {
  return {
    profileType: resolveProfileType(user),
    hasSophiaAdminRole: hasSophiaAdminRole(user),
    user,
  }
}

export async function updateProfileAPI(patch: Partial<AuthUser>): Promise<AuthUser> {
  return apiRequest<AuthUser>('/api/profile', {
    method: 'PUT',
    body: JSON.stringify(patch),
  })
}
