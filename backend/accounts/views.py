from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import RoleAssignment, User
from .serializers import (
    AccountManageSerializer,
    AuthUserSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    generate_password,
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
    if 'president' in roles or 'vice_president' in roles:
        return True
    if 'teacher' in roles:
        return True
    return False


def _sync_roles(user: User, roles_data: list, is_sophia: bool) -> None:
    user.role_assignments.all().delete()
    for entry in roles_data:
        role = entry.get('role', '')
        scope = entry.get('scope', {})
        scope_type = scope.get('type', 'self')
        group_id = ''
        group_ids = []
        module_id = ''
        if scope_type == 'group':
            group_id = scope.get('groupId', '')
        elif scope_type == 'groups':
            group_ids = scope.get('groupIds', [])
        elif scope_type == 'module':
            module_id = scope.get('module', '')
        RoleAssignment.objects.create(
            user=user,
            role=role,
            scope_type=scope_type,
            group_id=group_id,
            group_ids=group_ids,
            module_id=module_id,
        )
    if is_sophia:
        RoleAssignment.objects.create(
            user=user,
            role='sophia_admin',
            scope_type='module',
            module_id='woruld_sophia',
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.prefetch_related('role_assignments').get(username=username)
        except User.DoesNotExist:
            return Response(
                {'message': '用户名不存在'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.is_root:
            if password != ROOT_PASSWORD:
                return Response(
                    {'message': '密码错误'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            if not user.check_password(password):
                return Response(
                    {'message': '密码错误'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        refresh = RefreshToken.for_user(user)
        return Response(
            _build_auth_user(user, str(refresh.access_token), str(refresh))
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(AuthUserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refreshToken', '')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass
        return Response({'message': '已登出'})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_pwd = serializer.validated_data['oldPassword']
        new_pwd = serializer.validated_data['newPassword']

        user = request.user
        if user.is_root:
            return Response(
                {'message': 'root 账号不可修改密码'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not user.check_password(old_pwd):
            return Response(
                {'message': '原密码错误'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_pwd)
        user.save()
        return Response({'message': '密码修改成功'})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if 'displayName' in request.data:
            user.display_name = request.data['displayName']
        if 'avatarUrl' in request.data:
            user.avatar_url = request.data.get('avatarUrl') or ''
        if 'bio' in request.data:
            user.bio = request.data.get('bio') or ''
        if 'email' in request.data:
            user.email = request.data.get('email') or ''
        user.save()
        return Response(AuthUserSerializer(user).data)

    def patch(self, request):
        return self.put(request)


class AccountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_manager(request.user):
            return Response(
                {'message': '无权限'},
                status=status.HTTP_403_FORBIDDEN,
            )
        users = (
            User.objects
            .prefetch_related('role_assignments')
            .exclude(is_root=True)
            .order_by('id')
        )
        result = []
        for u in users:
            roles_data = []
            is_sophia = False
            for ra in u.role_assignments.all():
                if ra.role == 'sophia_admin':
                    is_sophia = True
                    continue
                entry = {'role': ra.role}
                if ra.scope_type == 'global':
                    entry['scope'] = {'type': 'global'}
                elif ra.scope_type == 'group':
                    entry['scope'] = {'type': 'group', 'groupId': ra.group_id}
                elif ra.scope_type == 'groups':
                    entry['scope'] = {'type': 'groups', 'groupIds': ra.group_ids}
                roles_data.append(entry)
            result.append({
                'id': u.id,
                'displayName': u.display_name,
                'username': u.username,
                'password': '',
                'roles': roles_data,
                'isSophiaAdmin': is_sophia,
            })
        return Response(result)


class AccountCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_root:
            return Response(
                {'message': '仅 root 可创建账户'},
                status=status.HTTP_403_FORBIDDEN,
            )
        ser = AccountManageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'message': '用户名已存在'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pwd = data.get('password') or generate_password()
        user = User.objects.create_user(
            username=data['username'],
            password=pwd,
            display_name=data['displayName'],
        )
        _sync_roles(user, data.get('roles', []), data.get('isSophiaAdmin', False))
        return Response({'message': '创建成功', 'password': pwd})


class AccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk: int):
        if not request.user.is_root:
            return Response(
                {'message': '仅 root 可编辑账户'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            user = User.objects.get(pk=pk, is_root=False)
        except User.DoesNotExist:
            return Response(
                {'message': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND,
            )
        ser = AccountManageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        user.display_name = data['displayName']
        if data.get('username') and data['username'] != user.username:
            if User.objects.filter(username=data['username']).exclude(pk=pk).exists():
                return Response(
                    {'message': '用户名已存在'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.username = data['username']
        pwd = data.get('password')
        if pwd:
            user.set_password(pwd)
        user.save()
        _sync_roles(user, data.get('roles', []), data.get('isSophiaAdmin', False))
        return Response({'message': '更新成功'})


class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk: int):
        if not request.user.is_root:
            return Response(
                {'message': '仅 root 可删除账户'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            user = User.objects.get(pk=pk, is_root=False)
        except User.DoesNotExist:
            return Response(
                {'message': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response({'message': '已删除'})


class GeneratePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_root:
            return Response(
                {'message': '无权限'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response({'password': generate_password()})
