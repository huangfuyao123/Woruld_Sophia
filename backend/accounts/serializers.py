from rest_framework import serializers

from .models import RoleAssignment, User


class RoleAssignmentSerializer(serializers.ModelSerializer):
    scope = serializers.SerializerMethodField()
    role = serializers.CharField()

    class Meta:
        model = RoleAssignment
        fields = ['role', 'scope']

    def get_scope(self, obj):
        if obj.scope_type == 'self':
            return {'type': 'self'}
        if obj.scope_type == 'global':
            return {'type': 'global'}
        if obj.scope_type == 'group':
            return {'type': 'group', 'groupId': obj.group_id}
        if obj.scope_type == 'groups':
            return {'type': 'groups', 'groupIds': obj.group_ids}
        if obj.scope_type == 'module':
            return {'type': 'module', 'module': obj.module_id}
        return {'type': 'self'}


class AuthUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    displayName = serializers.CharField(source='display_name')
    avatarUrl = serializers.CharField(source='avatar_url')
    roles = serializers.SerializerMethodField()
    token = serializers.CharField(read_only=True, default='')

    class Meta:
        model = User
        fields = ['id', 'username', 'displayName', 'email', 'avatarUrl', 'bio', 'token', 'roles']

    def get_id(self, obj):
        return f'u{obj.id}'

    def get_roles(self, obj):
        return RoleAssignmentSerializer(obj.role_assignments.all(), many=True).data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
