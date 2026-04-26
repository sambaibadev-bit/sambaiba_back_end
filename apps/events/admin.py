from django.contrib import admin

from .models import CommunityEvent


@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "category", "is_highlighted")
    list_filter = ("category", "is_highlighted", "date")
    autocomplete_fields = ("category",)
    search_fields = ("title", "description", "location")
