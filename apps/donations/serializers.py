from rest_framework import serializers

from apps.collection_points.models import CollectionPoint

from .models import DonationCampaign, DonationCampaignPointLink


class DonationCampaignPointLinkWriteSerializer(serializers.ModelSerializer):
    """Attach an existing collection point to a campaign (admin)."""

    collection_point = serializers.PrimaryKeyRelatedField(queryset=CollectionPoint.objects.all())

    class Meta:
        model = DonationCampaignPointLink
        fields = ("collection_point", "sort_order")

    def create(self, validated_data):
        validated_data["campaign_id"] = self.context["campaign_pk"]
        return super().create(validated_data)


class DonationCampaignSerializer(serializers.ModelSerializer):
    """Exposes a read-only `goal` line; `collection_points` lists linked points (ordered)."""

    goal = serializers.SerializerMethodField(read_only=True)
    collection_points = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DonationCampaign
        fields = (
            "id",
            "title",
            "description",
            "donation_type",
            "is_active",
            "goal_target",
            "goal_unit",
            "goal",
            "collection_points",
        )

    def get_goal(self, obj: DonationCampaign) -> str:
        if obj.goal_target is None:
            return ""
        unit = (obj.goal_unit or "").strip()
        if unit:
            return f"Meta: {obj.goal_target} {unit}"
        return f"Meta: {obj.goal_target}"

    def get_collection_points(self, obj: DonationCampaign):
        cache = getattr(obj, "_prefetched_objects_cache", None)
        if cache and "point_links" in cache:
            links = sorted(obj.point_links.all(), key=lambda l: (l.sort_order, l.id))
        else:
            links = list(
                obj.point_links.select_related("collection_point")
                .order_by("sort_order", "id")
                .all()
            )
        out = []
        for link in links:
            pt = link.collection_point
            out.append(
                {
                    "id": pt.pk,
                    "name": pt.name,
                    "address": pt.address,
                    "hours": pt.hours,
                    "sort_order": link.sort_order,
                }
            )
        return out
