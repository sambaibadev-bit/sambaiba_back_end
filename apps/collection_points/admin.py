from django.contrib import admin

from .models import CollectionPoint


@admin.register(CollectionPoint)
class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "updated_at")
    search_fields = ("name", "address")
    ordering = ("name", "id")
