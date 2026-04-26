from django.contrib import admin

from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "media_type", "created_at")
    search_fields = ("title",)
