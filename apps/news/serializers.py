from rest_framework import serializers

from .models import CommunityNews

MAX_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


class CommunityNewsSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(source="created_at", read_only=True)
    clear_image = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = CommunityNews
        fields = (
            "id",
            "title",
            "summary",
            "content",
            "category",
            "is_pinned",
            "image",
            "created_date",
            "clear_image",
        )
        extra_kwargs = {
            "image": {"required": False, "allow_null": True},
        }

    def validate_image(self, value):
        if not value:
            return value
        if value.size > MAX_IMAGE_BYTES:
            raise serializers.ValidationError("A imagem deve ter no máximo 5 MB.")
        content_type = getattr(value, "content_type", "") or ""
        if content_type and content_type not in ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError("Use uma imagem JPG, PNG ou WebP.")
        return value

    def create(self, validated_data):
        validated_data.pop("clear_image", None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        clear = validated_data.pop("clear_image", False)
        new_image = validated_data.get("image", serializers.empty)
        replacing = new_image is not serializers.empty and new_image
        if replacing and instance.image:
            instance.image.delete(save=False)
        if clear and not replacing:
            if instance.image:
                instance.image.delete(save=False)
            instance.image = None
        return super().update(instance, validated_data)
