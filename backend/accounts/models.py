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
