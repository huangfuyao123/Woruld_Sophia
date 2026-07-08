from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import AuthUserSerializer, LoginSerializer


def _build_auth_user(user: User, token: str) -> dict:
    data = AuthUserSerializer(user).data
    data['token'] = token
    return data


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    try:
        user = User.objects.select_related(None).prefetch_related('role_assignments').get(
            username=username,
        )
    except User.DoesNotExist:
        return Response({'message': '用户名不存在'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'message': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response(_build_auth_user(user, str(refresh.access_token)))


@api_view(['GET'])
def me(request):
    if not request.user.is_authenticated:
        return Response({'message': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(AuthUserSerializer(request.user).data)


@api_view(['POST'])
def logout(request):
    return Response({'message': '已登出'})
