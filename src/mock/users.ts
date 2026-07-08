import type { User } from '@/types/auth'

export const mockUsers: Record<string, User> = {
  president: {
    id: 'u1',
    username: 'president',
    displayName: '会长',
    password: '123456',
    roles: [
      {
        role: 'president',
        scope: { type: 'global' },
      },
    ],
  },

  teacher: {
    id: 'u2',
    username: 'teacher',
    displayName: '指导老师',
    password: '123456',
    roles: [
      {
        role: 'teacher',
        scope: { type: 'groups', groupIds: ['hardware', 'conference'] },
      },
    ],
  },

  hardwareLeader: {
    id: 'u3',
    username: 'hardwareLeader',
    displayName: '硬件组负责人',
    password: '123456',
    roles: [
      {
        role: 'group_leader',
        scope: { type: 'group', groupId: 'hardware' },
      },
    ],
  },

  hardwareMember: {
    id: 'u4',
    username: 'hardwareMember',
    displayName: '硬件组成员',
    password: '123456',
    roles: [
      {
        role: 'member',
        scope: { type: 'group', groupId: 'hardware' },
      },
    ],
  },

  conferenceLeader: {
    id: 'u5',
    username: 'conferenceLeader',
    displayName: '会议组负责人',
    password: '123456',
    roles: [
      {
        role: 'group_leader',
        scope: { type: 'group', groupId: 'conference' },
      },
    ],
  },

  conferenceMember: {
    id: 'u6',
    username: 'conferenceMember',
    displayName: '会议组成员',
    password: '123456',
    roles: [
      {
        role: 'member',
        scope: { type: 'group', groupId: 'conference' },
      },
    ],
  },

  softwareLeader: {
    id: 'u7',
    username: 'softwareLeader',
    displayName: '软件组负责人',
    password: '123456',
    roles: [
      {
        role: 'group_leader',
        scope: { type: 'group', groupId: 'software' },
      },
    ],
  },

  softwareMember: {
    id: 'u8',
    username: 'softwareMember',
    displayName: '软件组成员',
    password: '123456',
    roles: [
      {
        role: 'member',
        scope: { type: 'group', groupId: 'software' },
      },
    ],
  },

  networkLeader: {
    id: 'u9',
    username: 'networkLeader',
    displayName: '网络组负责人',
    password: '123456',
    roles: [
      {
        role: 'group_leader',
        scope: { type: 'group', groupId: 'network' },
      },
    ],
  },

  networkMember: {
    id: 'u10',
    username: 'networkMember',
    displayName: '网络组成员',
    password: '123456',
    roles: [
      {
        role: 'member',
        scope: { type: 'group', groupId: 'network' },
      },
    ],
  },

  multiRoleUser: {
    id: 'u11',
    username: 'multiRoleUser',
    displayName: '多角色用户',
    password: '123456',
    roles: [
      {
        role: 'sophia_admin',
        scope: { type: 'module', module: 'woruld_sophia' },
      },
      {
        role: 'group_leader',
        scope: { type: 'group', groupId: 'hardware' },
      },
    ],
  },
}
