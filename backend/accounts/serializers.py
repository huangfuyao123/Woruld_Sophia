import random
import string

from rest_framework import serializers

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


class RoleAssignmentSerializer(serializers.ModelSerializer):
    scope = serializers.SerializerMethodField()
    role = serializers.CharField()

    class Meta:
        model = RoleAssignment
        fields = ['role', 'scope']

    def get_scope(self, obj):
        if obj.scope_type == 'self': return {'type': 'self'}
        if obj.scope_type == 'global': return {'type': 'global'}
        if obj.scope_type == 'group': return {'type': 'group', 'groupId': obj.group_id}
        if obj.scope_type == 'groups': return {'type': 'groups', 'groupIds': obj.group_ids}
        if obj.scope_type == 'module': return {'type': 'module', 'module': obj.module_id}
        return {'type': 'self'}


class AuthUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    displayName = serializers.CharField(source='display_name')
    avatarUrl = serializers.CharField(source='avatar_url')
    roles = serializers.SerializerMethodField()
    token = serializers.CharField(read_only=True, default='')
    refreshToken = serializers.CharField(read_only=True, default='')
    isRoot = serializers.BooleanField(source='is_root')

    class Meta:
        model = User
        fields = ['id', 'username', 'displayName', 'email', 'avatarUrl', 'bio', 'token', 'refreshToken', 'roles', 'isRoot']

    def get_id(self, obj): return f'u{obj.id}'
    def get_roles(self, obj): return RoleAssignmentSerializer(obj.role_assignments.all(), many=True).data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField()
    newPassword = serializers.CharField()


def generate_password(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class AccountManageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    displayName = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(required=False, allow_blank=True)
    roles = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    isSophiaAdmin = serializers.BooleanField(required=False, default=False)


DEFAULT_COLUMN_LABELS = {
    'problemDate': '问题时间',
    'classroom': '教室',
    'repairPeriod': '报修节数',
    'problemDetail': '具体问题',
    'firstRepairDate': '维修日期',
    'firstRepairTimeRange': '维修时间段',
    'firstRepairStatus': '维修情况',
    'firstSolved': '是否解决',
    'firstRepairPerson': '维修人员',
    'firstRepairDuration': '维修时长',
    'remark': '备注',
    'faultPhoto': '故障照片',
    'secondRepairDate': '二次维修时间',
    'secondRepairPerson': '维修人员',
    'secondRepairContent': '维修内容',
    'secondSolved': '是否解决',
    'secondRepairTimeRange': '维修时间段',
    'secondRepairDuration': '维修时长',
}


class Hardware2026ColumnLabelsSerializer(serializers.Serializer):
    problemDate = serializers.CharField(required=False, default='问题时间')
    classroom = serializers.CharField(required=False, default='教室')
    repairPeriod = serializers.CharField(required=False, default='报修节数')
    problemDetail = serializers.CharField(required=False, default='具体问题')
    firstRepairDate = serializers.CharField(required=False, default='维修日期')
    firstRepairTimeRange = serializers.CharField(required=False, default='维修时间段')
    firstRepairStatus = serializers.CharField(required=False, default='维修情况')
    firstSolved = serializers.CharField(required=False, default='是否解决')
    firstRepairPerson = serializers.CharField(required=False, default='维修人员')
    firstRepairDuration = serializers.CharField(required=False, default='维修时长')
    remark = serializers.CharField(required=False, default='备注')
    faultPhoto = serializers.CharField(required=False, default='故障照片')
    secondRepairDate = serializers.CharField(required=False, default='二次维修时间')
    secondRepairPerson = serializers.CharField(required=False, default='维修人员')
    secondRepairContent = serializers.CharField(required=False, default='维修内容')
    secondSolved = serializers.CharField(required=False, default='是否解决')
    secondRepairTimeRange = serializers.CharField(required=False, default='维修时间段')
    secondRepairDuration = serializers.CharField(required=False, default='维修时长')


class Hardware2026RecordSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    data = serializers.JSONField()

    class Meta:
        model = Hardware2026Record
        fields = ['id', 'data', 'created_at', 'updated_at']

    def get_id(self, obj): return f'r{obj.id}'


class Hardware2026MonthSerializer(serializers.ModelSerializer):
    records = serializers.SerializerMethodField()

    class Meta:
        model = Hardware2026Month
        fields = ['id', 'month', 'column_labels', 'records']

    def get_records(self, obj):
        return Hardware2026RecordSerializer(obj.records.all(), many=True).data


class Hardware2026BoardSerializer(serializers.ModelSerializer):
    months = Hardware2026MonthSerializer(many=True, read_only=True)

    class Meta:
        model = Hardware2026Board
        fields = ['id', 'name', 'months']


class Hardware2026MonthCreateSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=20)
    column_labels = Hardware2026ColumnLabelsSerializer(required=False)


class Hardware2026BoardUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)


class Hardware2026RecordCreateSerializer(serializers.Serializer):
    data = serializers.JSONField()


class HardwareRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareRoom
        fields = ['id', 'name', 'sort_order', 'is_active']


class HardwareMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareMember
        fields = ['id', 'name', 'grade', 'role', 'sort_order', 'is_active']


class HardwareOverviewSerializer(serializers.Serializer):
    rooms = HardwareRoomSerializer(many=True)
    members = HardwareMemberSerializer(many=True)
    inspection_template = serializers.DictField()


class HardwareRoomUpsertSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=40)
    sort_order = serializers.IntegerField(required=False, default=0)
    is_active = serializers.BooleanField(required=False, default=True)


class HardwareMemberUpsertSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=40)
    grade = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    role = serializers.ChoiceField(choices=['leader', 'vice_leader', 'member'])
    sort_order = serializers.IntegerField(required=False, default=0)
    is_active = serializers.BooleanField(required=False, default=True)


class HardwareOverviewUpdateSerializer(serializers.Serializer):
    rooms = HardwareRoomUpsertSerializer(many=True, required=False)
    members = HardwareMemberUpsertSerializer(many=True, required=False)


class HardwareDynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareDynamicField
        fields = ['id', 'key', 'label', 'field_type', 'options_json', 'order', 'source_type']


class HardwareDynamicRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareDynamicRow
        fields = ['id', 'data', 'created_at', 'updated_at']


class HardwareDynamicTableSerializer(serializers.ModelSerializer):
    fields = HardwareDynamicFieldSerializer(many=True, read_only=True)
    rows = HardwareDynamicRowSerializer(many=True, read_only=True)

    class Meta:
        model = HardwareDynamicTable
        fields = [
            'id',
            'name',
            'template_id',
            'use_room_source',
            'use_member_source',
            'fields',
            'rows',
            'created_at',
            'updated_at',
        ]


class HardwareDynamicTableCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    template_code = serializers.CharField(max_length=40, required=False, allow_blank=True, default='')
    use_room_source = serializers.BooleanField(required=False, default=False)
    use_member_source = serializers.BooleanField(required=False, default=False)
    fields = serializers.ListField(child=serializers.DictField(), required=False, default=list)


class HardwareDynamicRowCreateSerializer(serializers.Serializer):
    data = serializers.JSONField()
