from django.urls import path
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import (
    RoleAssignment,
    User,
    Hardware2026Board,
    Hardware2026Month,
    Hardware2026Record,
    UserHardware2026Preference,
    HardwareRoom,
    HardwareMember,
    HardwareTableTemplate,
    HardwareDynamicTable,
    HardwareDynamicField,
    HardwareDynamicRow,
)
from .serializers import (
    AccountManageSerializer,
    AuthUserSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    Hardware2026BoardSerializer,
    Hardware2026BoardUpdateSerializer,
    Hardware2026MonthCreateSerializer,
    Hardware2026MonthSerializer,
    Hardware2026RecordCreateSerializer,
    Hardware2026RecordSerializer,
    HardwareOverviewSerializer,
    HardwareOverviewUpdateSerializer,
    HardwareRoomSerializer,
    HardwareMemberSerializer,
    HardwareDynamicTableSerializer,
    HardwareDynamicTableCreateSerializer,
    HardwareDynamicRowCreateSerializer,
    generate_password,
    DEFAULT_COLUMN_LABELS,
)

ROOT_PASSWORD = 'YnaNz.thKgf.Nub.qq'


def _build_auth_user(user: User, access_token: str, refresh_token: str = '') -> dict:
    data = AuthUserSerializer(user).data
    data['token'] = access_token
    if refresh_token:
        data['refreshToken'] = refresh_token
    return data


def _is_manager(user: User) -> bool:
    if user.is_root:
        return True
    roles = user.role_assignments.values_list('role', flat=True)
    return 'president' in roles or 'vice_president' in roles or 'teacher' in roles


def _is_hw_manager(user: User) -> bool:
    if user.is_root:
        return True
    for ra in user.role_assignments.all():
        if ra.role == 'teacher' and ra.scope_type == 'groups' and 'hardware' in ra.group_ids:
            return True
        if ra.role in ('president', 'vice_president'):
            return True
        if ra.role in ('group_leader', 'vice_group_leader') and ra.scope_type == 'group' and ra.group_id == 'hardware':
            return True
        if ra.role in ('group_leader', 'vice_group_leader') and ra.scope_type == 'groups' and 'hardware' in ra.group_ids:
            return True
    return False


def _sync_roles(user: User, roles_data: list, is_sophia: bool) -> None:
    user.role_assignments.all().delete()
    for entry in roles_data:
        role = entry.get('role', '')
        scope = entry.get('scope', {})
        scope_type = scope.get('type', 'self')
        RoleAssignment.objects.create(
            user=user,
            role=role,
            scope_type=scope_type,
            group_id=scope.get('groupId', '') if scope_type == 'group' else '',
            group_ids=scope.get('groupIds', []) if scope_type == 'groups' else [],
            module_id=scope.get('module', '') if scope_type == 'module' else '',
        )
    if is_sophia:
        RoleAssignment.objects.create(user=user, role='sophia_admin', scope_type='module', module_id='woruld_sophia')


def _get_board() -> Hardware2026Board:
    board = Hardware2026Board.objects.order_by('id').first()
    if not board:
        board = Hardware2026Board.objects.create(name='硬件组2026')
    return board


def _get_or_create_pref(user: User) -> UserHardware2026Preference:
    pref, _ = UserHardware2026Preference.objects.get_or_create(user=user)
    return pref


def _can_manage_hardware_overview(user: User) -> bool:
    if _is_hw_manager(user):
        return True
    for ra in user.role_assignments.all():
        if ra.role in ('group_leader', 'vice_group_leader') and ra.scope_type == 'group' and ra.group_id == 'hardware':
            return True
        if ra.role in ('group_leader', 'vice_group_leader') and ra.scope_type == 'groups' and 'hardware' in ra.group_ids:
            return True
    return False


def _inspection_template_payload() -> dict:
    return {
        'code': 'inspection_template',
        'name': '巡检表模板',
        'layout_type': 'reinstall',
        'use_room_source': True,
        'use_member_source': False,
        'fields': [
            {'key': 'classroom', 'label': '教室', 'field_type': 'room_ref', 'options_json': [], 'order': 0, 'source_type': 'room'},
            {'key': 'inspectDate', 'label': '日期', 'field_type': 'date', 'options_json': [], 'order': 1, 'source_type': ''},
            {'key': 'autoBoot', 'label': '能否自动开机', 'field_type': 'select', 'options_json': ['能', '不能'], 'order': 2, 'source_type': ''},
            {'key': 'cableCheck', 'label': '线路检查', 'field_type': 'select', 'options_json': ['已加固'], 'order': 3, 'source_type': ''},
            {'key': 'soundStatus', 'label': '声音', 'field_type': 'select', 'options_json': ['正常', '异常', '已修好'], 'order': 4, 'source_type': ''},
            {'key': 'officeActivated', 'label': 'office是否激活', 'field_type': 'select', 'options_json': ['已激活', '未激活'], 'order': 5, 'source_type': ''},
            {'key': 'windowsActivated', 'label': 'windows是否激活', 'field_type': 'select', 'options_json': ['已激活', '未激活'], 'order': 6, 'source_type': ''},
            {'key': 'popup360', 'label': '360弹窗', 'field_type': 'select', 'options_json': ['已设置'], 'order': 7, 'source_type': ''},
            {'key': 'sleepSetting', 'label': '熄屏设置', 'field_type': 'select', 'options_json': ['已设置'], 'order': 8, 'source_type': ''},
            {'key': 'photo', 'label': '照片', 'field_type': 'image', 'options_json': [], 'order': 9, 'source_type': ''},
            {'key': 'remark', 'label': '备注', 'field_type': 'text', 'options_json': [], 'order': 10, 'source_type': ''},
            {'key': 'inspector', 'label': '检查人', 'field_type': 'text', 'options_json': [], 'order': 11, 'source_type': ''},
        ],
    }


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s = LoginSerializer(data=request.data); s.is_valid(raise_exception=True)
        username = s.validated_data['username']; password = s.validated_data['password']
        try: user = User.objects.prefetch_related('role_assignments').get(username=username)
        except User.DoesNotExist: return Response({'message': '用户名不存在'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_root:
            if password != ROOT_PASSWORD: return Response({'message': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not user.check_password(password): return Response({'message': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response(_build_auth_user(user, str(refresh.access_token), str(refresh)))


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): return Response(AuthUserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get('refreshToken', '')
        if refresh_token:
            try: RefreshToken(refresh_token).blacklist()
            except TokenError: pass
        return Response({'message': '已登出'})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        s = ChangePasswordSerializer(data=request.data); s.is_valid(raise_exception=True)
        user = request.user
        if user.is_root: return Response({'message': 'root 账号不可修改密码'}, status=status.HTTP_403_FORBIDDEN)
        if not user.check_password(s.validated_data['oldPassword']): return Response({'message': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(s.validated_data['newPassword']); user.save()
        return Response({'message': '密码修改成功'})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        for f in ['displayName', 'avatarUrl', 'bio', 'email']:
            if f in request.data:
                setattr(user, 'display_name' if f == 'displayName' else ('avatar_url' if f == 'avatarUrl' else f), request.data.get(f) or '')
        user.save(); return Response(AuthUserSerializer(user).data)
    def patch(self, request): return self.put(request)


class AccountListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not _is_manager(request.user): return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.prefetch_related('role_assignments').exclude(is_root=True).order_by('id')
        result = []
        for u in users:
            roles_data = []
            is_sophia = False
            for ra in u.role_assignments.all():
                if ra.role == 'sophia_admin': is_sophia = True; continue
                entry = {'role': ra.role}
                if ra.scope_type == 'global': entry['scope'] = {'type': 'global'}
                elif ra.scope_type == 'group': entry['scope'] = {'type': 'group', 'groupId': ra.group_id}
                elif ra.scope_type == 'groups': entry['scope'] = {'type': 'groups', 'groupIds': ra.group_ids}
                elif ra.scope_type == 'module': entry['scope'] = {'type': 'module', 'module': ra.module_id}
                roles_data.append(entry)
            result.append({'id': u.id, 'displayName': u.display_name, 'username': u.username, 'password': '', 'roles': roles_data, 'isSophiaAdmin': is_sophia})
        return Response(result)


class AccountCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not request.user.is_root: return Response({'message': '仅 root 可创建账户'}, status=status.HTTP_403_FORBIDDEN)
        ser = AccountManageSerializer(data=request.data); ser.is_valid(raise_exception=True); data = ser.validated_data
        if User.objects.filter(username=data['username']).exists(): return Response({'message': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
        pwd = data.get('password') or generate_password()
        user = User.objects.create_user(username=data['username'], password=pwd, display_name=data['displayName'])
        _sync_roles(user, data.get('roles', []), data.get('isSophiaAdmin', False))
        return Response({'message': '创建成功', 'password': pwd})


class AccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk: int):
        if not request.user.is_root: return Response({'message': '仅 root 可编辑账户'}, status=status.HTTP_403_FORBIDDEN)
        try: user = User.objects.get(pk=pk, is_root=False)
        except User.DoesNotExist: return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        ser = AccountManageSerializer(data=request.data); ser.is_valid(raise_exception=True); data = ser.validated_data
        user.display_name = data['displayName']
        if data.get('username') and data['username'] != user.username:
            if User.objects.filter(username=data['username']).exclude(pk=pk).exists(): return Response({'message': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
            user.username = data['username']
        if data.get('password'): user.set_password(data['password'])
        user.save(); _sync_roles(user, data.get('roles', []), data.get('isSophiaAdmin', False))
        return Response({'message': '更新成功'})


class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk: int):
        if not request.user.is_root: return Response({'message': '仅 root 可删除账户'}, status=status.HTTP_403_FORBIDDEN)
        try: user = User.objects.get(pk=pk, is_root=False)
        except User.DoesNotExist: return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        user.delete(); return Response({'message': '已删除'})


class GeneratePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_root: return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'password': generate_password()})


class Hardware2026BoardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        board = _get_board()
        return Response(Hardware2026BoardSerializer(board).data)
    def put(self, request):
        if not _is_hw_manager(request.user): return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        board = _get_board()
        ser = Hardware2026BoardUpdateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        if 'name' in ser.validated_data: board.name = ser.validated_data['name']
        board.save(); return Response(Hardware2026BoardSerializer(board).data)


class Hardware2026MonthListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        board = _get_board()
        return Response(Hardware2026MonthSerializer(board.months.all(), many=True).data)
    def post(self, request):
        if not _is_hw_manager(request.user): return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        board = _get_board()
        ser = Hardware2026MonthCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        month = ser.validated_data['month'].strip()
        col = ser.validated_data.get('column_labels') or DEFAULT_COLUMN_LABELS
        month_obj, created = Hardware2026Month.objects.get_or_create(board=board, month=month, defaults={'column_labels': col, 'created_by': request.user})
        if not created and ser.validated_data.get('column_labels'):
            month_obj.column_labels = ser.validated_data['column_labels']; month_obj.save()
        pref = _get_or_create_pref(request.user); pref.last_month = month_obj; pref.save()
        return Response(Hardware2026MonthSerializer(month_obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class Hardware2026MonthDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, month_id: int):
        if not _is_hw_manager(request.user): return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        try: month_obj = Hardware2026Month.objects.get(pk=month_id)
        except Hardware2026Month.DoesNotExist: return Response({'message': '月份不存在'}, status=status.HTTP_404_NOT_FOUND)
        month = (request.data.get('month', month_obj.month) or '').strip()
        if month != month_obj.month and Hardware2026Month.objects.filter(board=month_obj.board, month=month).exclude(pk=month_id).exists():
            return Response({'message': '月份已存在'}, status=status.HTTP_400_BAD_REQUEST)
        month_obj.month = month
        if 'column_labels' in request.data: month_obj.column_labels = request.data.get('column_labels') or DEFAULT_COLUMN_LABELS
        month_obj.save(); return Response(Hardware2026MonthSerializer(month_obj).data)
    def delete(self, request, month_id: int):
        if not _is_hw_manager(request.user): return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        try: month_obj = Hardware2026Month.objects.get(pk=month_id)
        except Hardware2026Month.DoesNotExist: return Response({'message': '月份不存在'}, status=status.HTTP_404_NOT_FOUND)
        month_obj.delete(); return Response({'message': '已删除'})


class Hardware2026RecordListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, month_id: int):
        try: month_obj = Hardware2026Month.objects.get(pk=month_id)
        except Hardware2026Month.DoesNotExist: return Response({'message': '月份不存在'}, status=status.HTTP_404_NOT_FOUND)
        return Response(Hardware2026RecordSerializer(month_obj.records.all(), many=True).data)
    def post(self, request, month_id: int):
        try: month_obj = Hardware2026Month.objects.get(pk=month_id)
        except Hardware2026Month.DoesNotExist: return Response({'message': '月份不存在'}, status=status.HTTP_404_NOT_FOUND)
        ser = Hardware2026RecordCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        obj = Hardware2026Record.objects.create(month=month_obj, data=ser.validated_data['data'], created_by=request.user, updated_by=request.user)
        pref = _get_or_create_pref(request.user); pref.last_month = month_obj; pref.save()
        return Response(Hardware2026RecordSerializer(obj).data, status=status.HTTP_201_CREATED)


class Hardware2026RecordDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, record_id: int):
        try: obj = Hardware2026Record.objects.get(pk=record_id)
        except Hardware2026Record.DoesNotExist: return Response({'message': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)
        obj.data = request.data.get('data', obj.data)
        obj.updated_by = request.user; obj.save(); return Response(Hardware2026RecordSerializer(obj).data)
    def delete(self, request, record_id: int):
        try: obj = Hardware2026Record.objects.get(pk=record_id)
        except Hardware2026Record.DoesNotExist: return Response({'message': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete(); return Response({'message': '已删除'})


class Hardware2026PreferenceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pref = _get_or_create_pref(request.user)
        last_month = pref.last_month
        return Response({'lastMonthId': last_month.id if last_month else None})
    def put(self, request):
        pref = _get_or_create_pref(request.user)
        month_id = request.data.get('lastMonthId')
        if month_id:
            try: pref.last_month = Hardware2026Month.objects.get(pk=month_id)
            except Hardware2026Month.DoesNotExist: return Response({'message': '月份不存在'}, status=status.HTTP_404_NOT_FOUND)
        else:
            pref.last_month = None
        pref.save(); return Response({'message': '已保存'})


class HardwareOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = HardwareRoom.objects.all()
        members = HardwareMember.objects.all()
        payload = {
            'rooms': HardwareRoomSerializer(rooms, many=True).data,
            'members': HardwareMemberSerializer(members, many=True).data,
            'inspection_template': _inspection_template_payload(),
        }
        return Response(HardwareOverviewSerializer(payload).data)

    def put(self, request):
        if not _can_manage_hardware_overview(request.user):
            return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        ser = HardwareOverviewUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        if 'rooms' in ser.validated_data:
            keep_ids = []
            for item in ser.validated_data['rooms']:
                room_id = item.get('id')
                if room_id:
                    room = HardwareRoom.objects.get(pk=room_id)
                    room.name = item['name']
                    room.sort_order = item.get('sort_order', 0)
                    room.is_active = item.get('is_active', True)
                    room.save()
                    keep_ids.append(room.id)
                else:
                    room = HardwareRoom.objects.create(
                        name=item['name'],
                        sort_order=item.get('sort_order', 0),
                        is_active=item.get('is_active', True),
                    )
                    keep_ids.append(room.id)
            HardwareRoom.objects.exclude(id__in=keep_ids).delete()
        if 'members' in ser.validated_data:
            keep_ids = []
            for item in ser.validated_data['members']:
                member_id = item.get('id')
                if member_id:
                    member = HardwareMember.objects.get(pk=member_id)
                    member.name = item['name']
                    member.grade = item.get('grade', '')
                    member.role = item['role']
                    member.sort_order = item.get('sort_order', 0)
                    member.is_active = item.get('is_active', True)
                    member.save()
                    keep_ids.append(member.id)
                else:
                    member = HardwareMember.objects.create(
                        name=item['name'],
                        grade=item.get('grade', ''),
                        role=item['role'],
                        sort_order=item.get('sort_order', 0),
                        is_active=item.get('is_active', True),
                    )
                    keep_ids.append(member.id)
            HardwareMember.objects.exclude(id__in=keep_ids).delete()
        return self.get(request)


class HardwareDynamicTableListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        board = _get_board()
        tables = board.dynamic_tables.prefetch_related('fields', 'rows').all()
        return Response(HardwareDynamicTableSerializer(tables, many=True).data)

    def post(self, request):
        if not _can_manage_hardware_overview(request.user):
            return Response({'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        ser = HardwareDynamicTableCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        board = _get_board()
        template = None
        fields = ser.validated_data.get('fields', [])
        template_code = ser.validated_data.get('template_code', '').strip()
        if template_code == 'inspection_template':
            payload = _inspection_template_payload()
            fields = payload['fields']
            template, _ = HardwareTableTemplate.objects.get_or_create(
                code='inspection_template',
                defaults={
                    'name': payload['name'],
                    'layout_type': payload['layout_type'],
                    'fields_json': payload['fields'],
                    'use_room_source': True,
                    'use_member_source': False,
                },
            )
        table = HardwareDynamicTable.objects.create(
            board=board,
            name=ser.validated_data['name'],
            template=template,
            use_room_source=ser.validated_data.get('use_room_source', False),
            use_member_source=ser.validated_data.get('use_member_source', False),
            created_by=request.user,
            updated_by=request.user,
        )
        for index, field in enumerate(fields):
            HardwareDynamicField.objects.create(
                table=table,
                key=field.get('key') or f'field_{index + 1}',
                label=field.get('label') or f'字段{index + 1}',
                field_type=field.get('field_type') or 'text',
                options_json=field.get('options_json') or [],
                order=field.get('order', index),
                source_type=field.get('source_type') or '',
            )
        if table.use_room_source:
            room_names = list(HardwareRoom.objects.filter(is_active=True).values_list('name', flat=True))
            field_keys = {field.key for field in table.fields.all()}
            if 'classroom' in field_keys:
                for room_name in room_names:
                    HardwareDynamicRow.objects.create(
                        table=table,
                        data={'classroom': room_name},
                        created_by=request.user,
                        updated_by=request.user,
                    )
        return Response(HardwareDynamicTableSerializer(table).data, status=status.HTTP_201_CREATED)


class HardwareDynamicTableDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, table_id: int):
        try:
            table = HardwareDynamicTable.objects.prefetch_related('fields', 'rows').get(pk=table_id)
        except HardwareDynamicTable.DoesNotExist:
            return Response({'message': '表不存在'}, status=status.HTTP_404_NOT_FOUND)
        return Response(HardwareDynamicTableSerializer(table).data)


class HardwareDynamicRowListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, table_id: int):
        try:
            table = HardwareDynamicTable.objects.get(pk=table_id)
        except HardwareDynamicTable.DoesNotExist:
            return Response({'message': '表不存在'}, status=status.HTTP_404_NOT_FOUND)
        ser = HardwareDynamicRowCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        row = HardwareDynamicRow.objects.create(
            table=table,
            data=ser.validated_data['data'],
            created_by=request.user,
            updated_by=request.user,
        )
        return Response(HardwareDynamicRowSerializer(row).data, status=status.HTTP_201_CREATED)
