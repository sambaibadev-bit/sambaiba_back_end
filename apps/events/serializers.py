from rest_framework import serializers

from apps.event_categories.models import EventCategory

from .models import CommunityEvent


class EventCategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ("id", "slug", "name", "sort_order")


class CommunityEventSerializer(serializers.ModelSerializer):
    category = EventCategoryBriefSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.filter(is_active=True),
        source="category",
        write_only=True,
    )

    class Meta:
        model = CommunityEvent
        fields = (
            "id",
            "title",
            "description",
            "date",
            "time",
            "location",
            "category",
            "category_id",
            "is_highlighted",
        )
