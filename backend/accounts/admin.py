from django.contrib import admin

from .models import (
    Hardware2026Board,
    Hardware2026Month,
    Hardware2026Record,
    RoleAssignment,
    User,
    UserHardware2026Preference,
)

admin.site.register(User)
admin.site.register(RoleAssignment)
admin.site.register(Hardware2026Board)
admin.site.register(Hardware2026Month)
admin.site.register(Hardware2026Record)
admin.site.register(UserHardware2026Preference)
