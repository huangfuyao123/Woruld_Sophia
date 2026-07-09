<template>
  <div class="profile-page" :class="`theme-${theme}`">
    <button class="home-fab" type="button" aria-label="返回首页" @click="goHome">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1V9.5z" />
      </svg>
    </button>

    <div class="profile-container">
      <!-- ===== 左侧 sidebar ===== -->
      <aside class="profile-sidebar">
        <div class="avatar-box">
          <img v-if="avatarPreview" class="avatar-img" :src="avatarPreview" alt="avatar" />
          <div v-else class="avatar-fallback">{{ avatarFallback }}</div>
        </div>
        <button class="avatar-edit-btn" type="button" @click="toggleAvatarEditor">
          {{ isEditingAvatar ? '取消编辑' : '编辑头像' }}
        </button>

        <div v-if="isEditingAvatar" class="avatar-editor">
          <input v-model.trim="avatarInput" type="text" placeholder="头像图片链接 https://..." />
          <div class="avatar-editor-actions">
            <button class="mini-btn" type="button" @click="resetAvatarInput">重置</button>
            <button class="mini-btn primary" type="button" @click="saveAvatar">保存</button>
          </div>
        </div>

        <h1 class="sidebar-name">{{ user?.displayName ?? '-' }}</h1>
        <p class="sidebar-username">{{ user?.username ?? '-' }}</p>
        <p class="sidebar-role">{{ roleLabel }}</p>

        <div class="sidebar-actions">
          <button class="find-materials-btn" type="button" @click="goToMaterials">
            查找资料
          </button>
          <button v-if="!user?.isRoot" class="change-pwd-btn" type="button" @click="showPwdDialog = true">
            修改密码
          </button>
        </div>

        <div class="bio-area">
          <button class="bio-toggle" type="button" @click="toggleBioEditor">
            {{ isEditingBio ? '取消简介' : '编辑简介' }}
          </button>
          <div v-if="isEditingBio" class="bio-editor">
            <textarea v-model="bioInput" rows="3" placeholder="添加一段个人简介..."></textarea>
            <button class="mini-btn primary" type="button" @click="saveBio">保存简介</button>
          </div>
          <p v-else-if="user?.bio" class="bio-text">{{ user.bio }}</p>
        </div>

        <ul class="sidebar-meta">
          <li v-if="user?.email">
            <span class="meta-label">邮箱</span>
            <span class="meta-value">{{ user.email }}</span>
          </li>
          <li v-if="primaryGroup">
            <span class="meta-label">分组</span>
            <span class="meta-value">{{ GROUP_LABELS[primaryGroup] }}</span>
          </li>
          <li v-if="showSophiaSection">
            <span class="meta-label">寰宇智域</span>
            <span class="meta-value">管理员</span>
          </li>
        </ul>

        <div class="sidebar-roles">
          <span v-for="item in roleDescriptions" :key="item" class="role-badge">{{ item }}</span>
        </div>
      </aside>

      <!-- ===== 右侧 content ===== -->
      <div class="profile-main">
        <nav class="profile-tabs">
          <span class="tab active">概览</span>
        </nav>

        <!-- 工作台（上移） -->
        <section class="workspace-section">
          <div class="section-header">
            <h2 class="section-title">{{ title }}</h2>
            <p class="section-subtitle">{{ subtitle }}</p>
          </div>
          <div class="workspace-grid">
            <slot />
          </div>
        </section>

        <!-- 寰宇智域数据（指导老师无） -->
        <section v-if="showSophiaStats" class="sophia-section">
          <h2 class="sophia-title">寰宇智域数据</h2>
          <div class="sophia-stats">
            <div v-for="stat in sophiaStats" :key="stat.label" class="stat-card">
              <span class="stat-label">{{ stat.label }}</span>
              <span class="stat-value">{{ stat.value }}</span>
            </div>
          </div>
        </section>
      </div>
    </div>

    <ChangePasswordDialog :show="showPwdDialog" @cancel="showPwdDialog = false" @success="showPwdDialog = false" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { GROUP_LABELS, ROLE_LABELS } from '@/constants/permissions'
import { hasSophiaAdminRole, getUserPrimaryGroup, isPresident } from '@/utils/profile'
import type { GroupId } from '@/types/auth'
import ChangePasswordDialog from '@/components/ChangePasswordDialog.vue'

withDefaults(
  defineProps<{
    title: string
    subtitle: string
    roleLabel: string
    theme: string
    showSophiaStats?: boolean
  }>(),
  { showSophiaStats: true },
)

const router = useRouter()
const auth = useAuthStore()
const user = computed(() => auth.user)

const isEditingAvatar = ref(false)
const avatarInput = ref('')
const isEditingBio = ref(false)
const bioInput = ref('')
const showPwdDialog = ref(false)

watch(
  user,
  (value) => {
    avatarInput.value = value?.avatarUrl?.trim() ?? ''
    bioInput.value = value?.bio?.trim() ?? ''
  },
  { immediate: true },
)

const avatarPreview = computed(() => avatarInput.value || user.value?.avatarUrl?.trim() || '')
const avatarFallback = computed(() => {
  const source = user.value?.displayName?.trim() || user.value?.username?.trim() || 'U'
  return source.charAt(0).toUpperCase()
})

const primaryGroup = computed<GroupId | null>(() => getUserPrimaryGroup(user.value))
const showSophiaSection = computed(() => hasSophiaAdminRole(user.value))

const roleDescriptions = computed(() => {
  if (!user.value) return []
  return user.value.roles.map((assignment) => {
    const roleName = ROLE_LABELS[assignment.role]
    if (assignment.scope.type === 'global') return roleName
    if (assignment.scope.type === 'group') return `${roleName}·${GROUP_LABELS[assignment.scope.groupId]}`
    if (assignment.scope.type === 'groups') {
      const groups = assignment.scope.groupIds.map((g) => GROUP_LABELS[g]).join('/')
      return `${roleName}·${groups}`
    }
    if (assignment.scope.type === 'module') return `${roleName}·寰宇智域`
    return roleName
  })
})

const sophiaStats = computed(() => {
  if (!user.value) return []
  const groupLabel = primaryGroup.value
    ? GROUP_LABELS[primaryGroup.value]
    : isPresident(user.value)
      ? '全局'
      : user.value?.isRoot
        ? '超级管理员'
        : '—'
  return [
    { label: '账号 ID', value: user.value.id },
    { label: '角色数量', value: String(user.value.roles.length) },
    { label: '主要分组', value: groupLabel },
    { label: '寰宇智域', value: hasSophiaAdminRole(user.value) ? '管理员' : '普通成员' },
  ]
})

function toggleAvatarEditor(): void {
  isEditingAvatar.value = !isEditingAvatar.value
  if (!isEditingAvatar.value) resetAvatarInput()
}

function resetAvatarInput(): void {
  avatarInput.value = user.value?.avatarUrl?.trim() ?? ''
}

function saveAvatar(): void {
  auth.updateProfile({ avatarUrl: avatarInput.value || undefined })
  isEditingAvatar.value = false
}

function toggleBioEditor(): void {
  isEditingBio.value = !isEditingBio.value
  if (!isEditingBio.value) {
    bioInput.value = user.value?.bio?.trim() ?? ''
  }
}

function saveBio(): void {
  auth.updateProfile({ bio: bioInput.value || undefined })
  isEditingBio.value = false
}

function goToMaterials(): void {
  router.push('/materials')
}

function goHome(): void {
  router.push('/')
}
</script>

<style scoped>
/* ===== Base ===== */
.profile-page {
  --accent: #1e40af;
  --accent-soft: #eff6ff;
  --accent-border: rgba(30, 64, 175, 0.18);
  --card-radius: 8px;
  --card-border: #e2e8f0;
  min-height: 100vh;
  padding: 80px 16px 64px;
  background: linear-gradient(180deg, var(--accent-soft) 0%, #f1f5f9 45%, #f8fafc 100%);
  color: #1e293b;
  font-family: '寒蝉正楷体', 'JuliaMono Medium', sans-serif;
  position: relative;
}

.home-fab {
  position: fixed;
  top: 20px;
  right: 24px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 4px 14px var(--accent-border);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 50;
}

.home-fab svg {
  width: 22px;
  height: 22px;
}

.home-fab:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--accent-border);
}

.home-fab:active {
  transform: translateY(0);
}

.profile-container {
  display: grid;
  grid-template-columns: 296px 1fr;
  gap: 24px;
  max-width: 1280px;
  margin: 0 auto;
}

/* ===== Sidebar ===== */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.avatar-box {
  width: 100%;
  display: flex;
  justify-content: center;
}

.avatar-img,
.avatar-fallback {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  border: 3px solid var(--accent);
  box-shadow: 0 0 0 6px var(--accent-soft);
}

.avatar-img {
  display: block;
  object-fit: cover;
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 60%, #fff));
  color: #fff;
  font-size: 72px;
  font-weight: 700;
}

.avatar-edit-btn {
  margin-top: 12px;
  padding: 5px 16px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #475569;
  font-size: 13px;
  cursor: pointer;
  transition: 0.15s;
}

.avatar-edit-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.avatar-editor {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.avatar-editor input {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #1e293b;
  font-size: 13px;
}

.avatar-editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.mini-btn {
  padding: 5px 14px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #475569;
  font-size: 12px;
  cursor: pointer;
  transition: 0.15s;
}

.mini-btn.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.mini-btn:hover {
  border-color: var(--accent);
}

.mini-btn.primary:hover {
  filter: brightness(1.1);
}

.sidebar-name {
  margin: 20px 0 0;
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
}

.sidebar-username {
  margin: 2px 0 0;
  font-size: 18px;
  color: #64748b;
  font-weight: 300;
}

.sidebar-role {
  margin: 6px 0 0;
  font-size: 14px;
  color: var(--accent);
  font-weight: 600;
}

.find-materials-btn {
  width: 100%;
  margin-top: 20px;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.find-materials-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px var(--accent-border);
}

.sidebar-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.sidebar-actions .find-materials-btn {
  margin-top: 0;
}

.change-pwd-btn {
  width: 100%;
  padding: 9px 16px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
  transition: 0.15s;
}

.change-pwd-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.bio-area {
  width: 100%;
  margin-top: 16px;
}

.bio-toggle {
  width: 100%;
  padding: 6px;
  border: 1px dashed var(--card-border);
  border-radius: 6px;
  background: transparent;
  color: #64748b;
  font-size: 12px;
  cursor: pointer;
  transition: 0.15s;
}

.bio-toggle:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.bio-editor {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bio-editor textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid var(--card-border);
  border-radius: 6px;
  background: #fff;
  color: #1e293b;
  font-size: 13px;
  resize: vertical;
}

.bio-editor .mini-btn {
  align-self: flex-end;
}

.bio-text {
  margin-top: 8px;
  padding: 8px 10px;
  border-radius: 6px;
  background: #fff;
  border: 1px solid var(--card-border);
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
  text-align: left;
}

.sidebar-meta {
  list-style: none;
  margin: 20px 0 0;
  padding: 16px 0 0;
  width: 100%;
  border-top: 1px solid var(--card-border);
  text-align: left;
}

.sidebar-meta li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  font-size: 13px;
}

.meta-label {
  color: #94a3b8;
}

.meta-value {
  color: #334155;
  font-weight: 500;
}

.sidebar-roles {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  margin-top: 16px;
}

.role-badge {
  padding: 3px 12px;
  border: 1px solid var(--accent-border);
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 12px;
  white-space: nowrap;
}

/* ===== Main ===== */
.profile-main {
  min-width: 0;
}

.profile-tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--card-border);
  margin-bottom: 24px;
}

.tab {
  padding: 10px 16px;
  border-bottom: 2px solid transparent;
  font-size: 14px;
  color: #64748b;
  cursor: default;
}

.tab.active {
  border-bottom-color: var(--accent);
  font-weight: 600;
  color: var(--accent);
}

.section-header {
  margin-bottom: 16px;
}

.section-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.section-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.workspace-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* slot 内 .detail-card 通用样式 */
.workspace-grid :deep(.detail-card) {
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  background: #fff;
  padding: 18px;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.workspace-grid :deep(.detail-card:hover) {
  border-color: var(--accent);
  box-shadow: 0 4px 16px var(--accent-border);
}

.workspace-grid :deep(.detail-card h2) {
  margin: 0 0 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--accent);
}

.workspace-grid :deep(.detail-card p) {
  margin: 0;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.workspace-grid :deep(.detail-card .gh-placeholder-hint) {
  display: inline-block;
  margin-top: 8px;
  padding: 2px 8px;
  border: 1px solid var(--card-border);
  border-radius: 999px;
  font-size: 11px;
  color: #94a3b8;
}

/* ===== Sophia stats ===== */
.sophia-section {
  margin-top: 32px;
}

.sophia-title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--card-border);
}

.sophia-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px;
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  background: #fff;
}

.stat-label {
  font-size: 12px;
  color: #94a3b8;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
}

/* ===== 六种主题色调 ===== */
.theme-software {
  --accent: #1e40af;
  --accent-soft: #eff6ff;
  --accent-border: rgba(30, 64, 175, 0.15);
  --card-radius: 8px;
}

.theme-conference {
  --accent: #b45309;
  --accent-soft: #fffbeb;
  --accent-border: rgba(180, 83, 9, 0.15);
  --card-radius: 12px;
}

.theme-hardware {
  --accent: #b91c1c;
  --accent-soft: #fef2f2;
  --accent-border: rgba(185, 28, 28, 0.15);
  --card-radius: 4px;
}

.theme-network {
  --accent: #0f766e;
  --accent-soft: #f0fdfa;
  --accent-border: rgba(15, 118, 110, 0.15);
  --card-radius: 8px;
}

.theme-president {
  --accent: #6b21a8;
  --accent-soft: #f5f3ff;
  --accent-border: rgba(107, 33, 168, 0.15);
  --card-radius: 16px;
}

.theme-teacher {
  --accent: #15803d;
  --accent-soft: #f0fdf4;
  --accent-border: rgba(21, 128, 61, 0.15);
  --card-radius: 8px;
}

.theme-root {
  --accent: #7c3aed;
  --accent-soft: #f5f3ff;
  --accent-border: rgba(124, 58, 237, 0.15);
  --card-radius: 12px;
}

/* ===== 各主题卡片风格差异 ===== */
.theme-hardware .workspace-grid :deep(.detail-card) {
  border-left: 3px solid var(--accent);
}

.theme-network .workspace-grid :deep(.detail-card) {
  border-top: 3px solid var(--accent);
}

.theme-teacher .workspace-grid :deep(.detail-card) {
  border-top: 2px dashed var(--accent);
}

.theme-president .workspace-grid :deep(.detail-card) {
  padding: 20px;
}

.theme-conference .workspace-grid :deep(.detail-card) {
  box-shadow: 0 4px 14px var(--accent-border);
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .profile-container {
    grid-template-columns: 240px 1fr;
    gap: 20px;
  }

  .avatar-img,
  .avatar-fallback {
    width: 160px;
    height: 160px;
    font-size: 56px;
  }
}

@media (max-width: 768px) {
  .profile-page {
    padding: 24px 12px 48px;
  }

  .home-fab {
    top: 14px;
    right: 14px;
    width: 40px;
    height: 40px;
  }

  .home-fab svg {
    width: 20px;
    height: 20px;
  }

  .profile-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .profile-sidebar {
    align-items: center;
  }

  .avatar-img,
  .avatar-fallback {
    width: 120px;
    height: 120px;
    font-size: 44px;
    border-width: 2px;
  }

  .sidebar-name {
    font-size: 22px;
  }

  .sidebar-username {
    font-size: 16px;
  }

  .find-materials-btn {
    font-size: 14px;
    padding: 9px 14px;
  }

  .workspace-grid {
    grid-template-columns: 1fr;
  }

  .sophia-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-title {
    font-size: 18px;
  }

  .stat-value {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 16px 8px 32px;
  }

  .avatar-img,
  .avatar-fallback {
    width: 96px;
    height: 96px;
    font-size: 36px;
  }

  .sidebar-name {
    font-size: 20px;
  }

  .sidebar-username {
    font-size: 14px;
  }

  .sidebar-role {
    font-size: 13px;
  }

  .sidebar-meta li {
    font-size: 12px;
  }

  .role-badge {
    font-size: 11px;
    padding: 2px 10px;
  }

  .find-materials-btn {
    font-size: 13px;
    padding: 8px 12px;
  }

  .sophia-stats {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 12px;
  }

  .stat-value {
    font-size: 16px;
  }

  .workspace-grid :deep(.detail-card) {
    padding: 14px;
  }

  .profile-tabs {
    margin-bottom: 16px;
  }

  .tab {
    padding: 8px 12px;
    font-size: 13px;
  }
}
</style>
