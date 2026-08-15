from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_root_alter_roleassignment_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware2026Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='硬件组2026', max_length=100, verbose_name='表名')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={'verbose_name': '硬件组2026总表', 'verbose_name_plural': '硬件组2026总表'},
        ),
        migrations.CreateModel(
            name='Hardware2026Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20, verbose_name='月份')),
                ('column_labels', models.JSONField(blank=True, default=dict, verbose_name='字段名')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='accounts.hardware2026board')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_hw2026_months', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '硬件组2026月份', 'verbose_name_plural': '硬件组2026月份', 'ordering': ['month'], 'unique_together': {('board', 'month')}},
        ),
        migrations.CreateModel(
            name='Hardware2026Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict, verbose_name='记录数据')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_hw2026_records', to=settings.AUTH_USER_MODEL)),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='accounts.hardware2026month')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_hw2026_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '硬件组2026记录', 'verbose_name_plural': '硬件组2026记录', 'ordering': ['id']},
        ),
        migrations.CreateModel(
            name='UserHardware2026Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('last_month', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.hardware2026month')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hw2026_preference', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '硬件组2026用户偏好', 'verbose_name_plural': '硬件组2026用户偏好'},
        ),
    ]
