from rest_framework import serializers

from .models import CommunityNews


class CommunityNewsSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = CommunityNews
        fields = (
            "id",
            "title",
            "content",
            "category",
            "is_pinned",
            "created_date",
        )
