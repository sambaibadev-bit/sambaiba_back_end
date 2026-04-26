from rest_framework import serializers

from .models import CommunityEvent


class CommunityEventSerializer(serializers.ModelSerializer):
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
            "is_highlighted",
        )
