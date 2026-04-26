from rest_framework import serializers

from .models import UsefulContact


class UsefulContactPublicSerializer(serializers.ModelSerializer):
    """Fields exposed on the public landing list."""

    class Meta:
        model = UsefulContact
        fields = ("id", "name", "phone", "address", "hours")


class UsefulContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UsefulContact
        fields = (
            "id",
            "name",
            "phone",
            "address",
            "hours",
            "sort_order",
            "is_published",
        )
        read_only_fields = ("id",)
