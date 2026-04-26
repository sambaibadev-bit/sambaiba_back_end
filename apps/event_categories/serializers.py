from rest_framework import serializers

from .models import EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ("id", "slug", "name", "sort_order", "is_active")
        read_only_fields = ("id",)
