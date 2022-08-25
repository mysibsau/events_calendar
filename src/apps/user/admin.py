from django.contrib import admin

from apps.user import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "get_full_name", "email", "is_staff")


@admin.register(models.Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "user", "role")
