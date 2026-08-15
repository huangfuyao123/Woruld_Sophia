from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField('显示名称', max_length=100)
    avatar_url = models.URLField('头像链接', blank=True, default='')
    bio = models.TextField('个人简介', blank=True, default='')
    is_root = models.BooleanField('超级管理员', default=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.display_name or self.username


class RoleAssignment(models.Model):
    ROLE_CHOICES = [
        ('president', '会长'),
        ('vice_president', '副会长'),
        ('group_leader', '组长'),
        ('vice_group_leader', '副组长'),
        ('member', '组员'),
        ('teacher', '指导老师'),
        ('sophia_admin', '寰宇智域管理员'),
    ]

    SCOPE_CHOICES = [
        ('self', '个人'),
        ('global', '全局'),
        ('group', '单组'),
        ('groups', '多组'),
        ('module', '模块'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_assignments')
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES)
    scope_type = models.CharField('作用域类型', max_length=10, choices=SCOPE_CHOICES)
    group_id = models.CharField('分组ID', max_length=20, blank=True, default='')
    group_ids = models.JSONField('多分组ID', blank=True, default=list)
    module_id = models.CharField('模块ID', max_length=30, blank=True, default='')

    class Meta:
        verbose_name = '角色分配'
        verbose_name_plural = '角色分配'

    def __str__(self):
        return f'{self.user.username} - {self.role} ({self.scope_type})'


class Hardware2026Board(models.Model):
    name = models.CharField('表名', max_length=100, default='硬件组2026')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组2026总表'
        verbose_name_plural = '硬件组2026总表'

    def __str__(self):
        return self.name


class Hardware2026Month(models.Model):
    board = models.ForeignKey(Hardware2026Board, on_delete=models.CASCADE, related_name='months')
    month = models.CharField('月份', max_length=20)
    column_labels = models.JSONField('字段名', default=dict, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_hw2026_months')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组2026月份'
        verbose_name_plural = '硬件组2026月份'
        unique_together = [('board', 'month')]
        ordering = ['month']

    def __str__(self):
        return f'{self.board.name} - {self.month}'


class Hardware2026Record(models.Model):
    month = models.ForeignKey(Hardware2026Month, on_delete=models.CASCADE, related_name='records')
    data = models.JSONField('记录数据', default=dict)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_hw2026_records')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_hw2026_records')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组2026记录'
        verbose_name_plural = '硬件组2026记录'
        ordering = ['id']

    def __str__(self):
        return f'{self.month.month} - {self.id}'


class UserHardware2026Preference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hw2026_preference')
    last_month = models.ForeignKey(Hardware2026Month, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组2026用户偏好'
        verbose_name_plural = '硬件组2026用户偏好'

    def __str__(self):
        return f'{self.user.username} preference'


class HardwareRoom(models.Model):
    name = models.CharField('教室', max_length=40, unique=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)

    class Meta:
        verbose_name = '硬件组教室'
        verbose_name_plural = '硬件组教室'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class HardwareMember(models.Model):
    ROLE_CHOICES = [
        ('leader', '组长'),
        ('vice_leader', '副组长'),
        ('member', '成员'),
    ]

    name = models.CharField('姓名', max_length=40)
    grade = models.CharField('年级', max_length=20, blank=True, default='')
    role = models.CharField('组内身份', max_length=20, choices=ROLE_CHOICES, default='member')
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)

    class Meta:
        verbose_name = '硬件组成员'
        verbose_name_plural = '硬件组成员'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class HardwareTableTemplate(models.Model):
    code = models.CharField('模板编码', max_length=40, unique=True)
    name = models.CharField('模板名称', max_length=100)
    layout_type = models.CharField('布局类型', max_length=30, default='reinstall')
    fields_json = models.JSONField('字段定义', default=list)
    use_room_source = models.BooleanField('引用教室数据', default=True)
    use_member_source = models.BooleanField('引用成员数据', default=False)

    class Meta:
        verbose_name = '硬件组表模板'
        verbose_name_plural = '硬件组表模板'

    def __str__(self):
        return self.name


class HardwareDynamicTable(models.Model):
    board = models.ForeignKey(Hardware2026Board, on_delete=models.CASCADE, related_name='dynamic_tables')
    name = models.CharField('表名', max_length=100)
    template = models.ForeignKey(HardwareTableTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    use_room_source = models.BooleanField('引用教室数据', default=False)
    use_member_source = models.BooleanField('引用成员数据', default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_hw_dynamic_tables')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_hw_dynamic_tables')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组动态表'
        verbose_name_plural = '硬件组动态表'

    def __str__(self):
        return self.name


class HardwareDynamicField(models.Model):
    table = models.ForeignKey(HardwareDynamicTable, on_delete=models.CASCADE, related_name='fields')
    key = models.CharField('字段键', max_length=50)
    label = models.CharField('字段名', max_length=100)
    field_type = models.CharField('字段类型', max_length=30)
    options_json = models.JSONField('选项', default=list, blank=True)
    order = models.IntegerField('排序', default=0)
    source_type = models.CharField('来源类型', max_length=20, blank=True, default='')

    class Meta:
        verbose_name = '硬件组动态字段'
        verbose_name_plural = '硬件组动态字段'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.table.name} - {self.label}'


class HardwareDynamicRow(models.Model):
    table = models.ForeignKey(HardwareDynamicTable, on_delete=models.CASCADE, related_name='rows')
    data = models.JSONField('行数据', default=dict)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_hw_dynamic_rows')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_hw_dynamic_rows')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '硬件组动态行'
        verbose_name_plural = '硬件组动态行'
        ordering = ['id']

    def __str__(self):
        return f'{self.table.name} - {self.id}'