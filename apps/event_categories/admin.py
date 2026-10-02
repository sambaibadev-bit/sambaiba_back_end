from django.contrib import admin

from .models import EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("sort_order", "slug")
