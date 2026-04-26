from rest_framework import serializers

from .models import GalleryCategory


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ("id", "slug", "name", "sort_order", "is_active")
        read_only_fields = ("id",)
