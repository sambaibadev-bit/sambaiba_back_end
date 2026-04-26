from django.contrib import admin

from .models import CommunityNews


@admin.register(CommunityNews)
class CommunityNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_pinned", "created_at")
    list_filter = ("category", "is_pinned")
