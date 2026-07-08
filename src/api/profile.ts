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
