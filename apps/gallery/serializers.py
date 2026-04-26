from rest_framework import serializers

from apps.gallery_categories.models import GalleryCategory

from .models import GalleryItem


class GalleryCategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ("id", "slug", "name", "sort_order")


class GalleryItemSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(source="created_at", read_only=True)
    category = GalleryCategoryBriefSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=GalleryCategory.objects.filter(is_active=True),
        source="category",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = GalleryItem
        fields = (
            "id",
            "title",
            "category",
            "category_id",
            "media_type",
            "media_url",
            "created_date",
        )
