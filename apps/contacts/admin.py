from django.contrib import admin

from .models import UsefulContact


@admin.register(UsefulContact)
class UsefulContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "address")
