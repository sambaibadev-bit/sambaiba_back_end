from django.contrib import admin

from .models import CommunitySuggestion


@admin.register(CommunitySuggestion)
class CommunitySuggestionAdmin(admin.ModelAdmin):
    list_display = ("name", "suggestion_type", "created_at", "reviewed")
    list_filter = ("suggestion_type", "reviewed")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
