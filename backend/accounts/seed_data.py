from django.contrib.auth.hashers import make_password


SEED_USERS = [
    {
        'username': 'president',
        'display_name': '会长',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'president', 'scope_type': 'global'},
        ],
    },
    {
        'username': 'teacher',
        'display_name': '指导老师',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'teacher', 'scope_type': 'groups', 'group_ids': ['hardware', 'conference']},
        ],
    },
    {
        'username': 'hardwareLeader',
        'display_name': '硬件组负责人',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'group_leader', 'scope_type': 'group', 'group_id': 'hardware'},
        ],
    },
    {
        'username': 'hardwareMember',
        'display_name': '硬件组成员',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'member', 'scope_type': 'group', 'group_id': 'hardware'},
        ],
    },
    {
        'username': 'conferenceLeader',
        'display_name': '会议组负责人',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'group_leader', 'scope_type': 'group', 'group_id': 'conference'},
        ],
    },
    {
        'username': 'conferenceMember',
        'display_name': '会议组成员',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'member', 'scope_type': 'group', 'group_id': 'conference'},
        ],
    },
    {
        'username': 'softwareLeader',
        'display_name': '软件组负责人',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'group_leader', 'scope_type': 'group', 'group_id': 'software'},
        ],
    },
    {
        'username': 'softwareMember',
        'display_name': '软件组成员',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'member', 'scope_type': 'group', 'group_id': 'software'},
        ],
    },
    {
        'username': 'networkLeader',
        'display_name': '网络组负责人',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'group_leader', 'scope_type': 'group', 'group_id': 'network'},
        ],
    },
    {
        'username': 'networkMember',
        'display_name': '网络组成员',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'member', 'scope_type': 'group', 'group_id': 'network'},
        ],
    },
    {
        'username': 'woruldSophiaAdmin',
        'display_name': '寰宇智域管理员',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'sophia_admin', 'scope_type': 'module', 'module_id': 'woruld_sophia'},
        ],
    },
    {
        'username': 'multiRoleUser',
        'display_name': '多角色用户',
        'password': make_password('123456'),
        'is_root': False,
        'roles': [
            {'role': 'sophia_admin', 'scope_type': 'module', 'module_id': 'woruld_sophia'},
            {'role': 'group_leader', 'scope_type': 'group', 'group_id': 'hardware'},
        ],
    },
]

ROOT_ACCOUNT = {
    'username': 'qiuqiu',
    'display_name': 'root',
    'password': make_password('YnaNz.thKgf.Nub.qq'),
    'is_root': True,
    'roles': [],
}
