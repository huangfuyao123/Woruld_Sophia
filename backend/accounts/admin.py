from django.contrib import admin

from .models import RoleAssignment, User

admin.site.register(User)
admin.site.register(RoleAssignment)
