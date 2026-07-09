from django.core.management.base import BaseCommand

from accounts.models import RoleAssignment, User
from accounts.seed_data import ROOT_ACCOUNT, SEED_USERS


class Command(BaseCommand):
    help = '导入初始测试账号（含 root，12 个普通账号密码均为 123456）'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        root, created = User.objects.get_or_create(
            username=ROOT_ACCOUNT['username'],
            defaults={
                'display_name': ROOT_ACCOUNT['display_name'],
                'is_root': True,
            },
        )
        if not created:
            root.display_name = ROOT_ACCOUNT['display_name']
            root.is_root = True
            root.save(update_fields=['display_name', 'is_root'])
        root.role_assignments.all().delete()
        if created:
            created_count += 1
        else:
            updated_count += 1
        self.stdout.write(self.style.SUCCESS(f'root 账号: {"新建" if created else "更新"}'))

        for item in SEED_USERS:
            user, created = User.objects.get_or_create(
                username=item['username'],
                defaults={
                    'display_name': item['display_name'],
                    'is_root': False,
                },
            )

            if not created:
                user.display_name = item['display_name']
                user.save(update_fields=['display_name'])

            user.set_password(item['password'])
            user.save(update_fields=['password'])

            if created:
                created_count += 1
            else:
                updated_count += 1

            user.role_assignments.all().delete()
            for role_data in item['roles']:
                RoleAssignment.objects.create(
                    user=user,
                    role=role_data['role'],
                    scope_type=role_data['scope_type'],
                    group_id=role_data.get('group_id', ''),
                    group_ids=role_data.get('group_ids', []),
                    module_id=role_data.get('module_id', ''),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'导入完成：新建 {created_count} 个，更新 {updated_count} 个，'
                f'共 {len(SEED_USERS) + 1} 个账号（含 root）'
            )
        )
