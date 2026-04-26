from rest_framework import serializers

from .models import GalleryItem


class GalleryItemSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = GalleryItem
        fields = (
            "id",
            "title",
            "category",
            "media_type",
            "media_url",
            "created_date",
        )
