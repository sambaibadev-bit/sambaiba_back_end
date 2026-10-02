from rest_framework import serializers

from .models import CommunitySuggestion


class CommunitySuggestionCreateSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=CommunitySuggestion.SuggestionType.choices,
        source="suggestion_type",
    )

    class Meta:
        model = CommunitySuggestion
        fields = ("name", "email", "type", "message")

    def create(self, validated_data):
        return CommunitySuggestion.objects.create(**validated_data)


class CommunitySuggestionStaffSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=CommunitySuggestion.SuggestionType.choices,
        source="suggestion_type",
        required=False,
    )

    class Meta:
        model = CommunitySuggestion
        fields = (
            "id",
            "name",
            "email",
            "type",
            "message",
            "attachments",
            "reviewed",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "attachments")
