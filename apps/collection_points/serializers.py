from rest_framework import serializers

from .models import CollectionPoint


class CollectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPoint
        fields = ("id", "name", "address", "hours", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
