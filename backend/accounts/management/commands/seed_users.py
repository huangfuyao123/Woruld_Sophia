from django.core.management.base import BaseCommand

from accounts.models import RoleAssignment, User
from accounts.seed_data import SEED_USERS


class Command(BaseCommand):
    help = '导入初始测试账号（12 个，密码均为 123456）'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in SEED_USERS:
            user, created = User.objects.get_or_create(
                username=item['username'],
                defaults={
                    'display_name': item['display_name'],
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
                f'导入完成：新建 {created_count} 个，更新 {updated_count} 个，共 {len(SEED_USERS)} 个账号'
            )
        )
