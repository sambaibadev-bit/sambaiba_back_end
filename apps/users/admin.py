from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (*BaseUserAdmin.list_display, "role")
    list_filter = (*BaseUserAdmin.list_filter, "role")
    ordering = ("-date_joined",)

    fieldsets = (
        *BaseUserAdmin.fieldsets,
        ("Tipo de usuário", {"fields": ("role",)}),
    )
    add_fieldsets = (
        *BaseUserAdmin.add_fieldsets,
        ("Tipo de usuário", {"fields": ("role",)}),
    )
