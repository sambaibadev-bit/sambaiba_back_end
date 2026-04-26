from django.db import IntegrityError
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH, param_is_active_donations, param_limit, param_ordering
from core.query_params import parse_limit, parse_ordering

from .models import DonationCampaign, DonationCampaignPointLink
from .serializers import DonationCampaignPointLinkWriteSerializer, DonationCampaignSerializer

_DONATION_ORDERING = frozenset({"created_at", "-created_at", "id", "-id"})

_LINK_PREFETCH = Prefetch(
    "point_links",
    queryset=DonationCampaignPointLink.objects.select_related("collection_point").order_by(
        "sort_order", "id"
    ),
)


def _campaign_queryset_with_points():
    return DonationCampaign.objects.prefetch_related(_LINK_PREFETCH)


class DonationCampaignCollectionAPIView(APIView):
    serializer_class = DonationCampaignSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    def _filter_queryset(self, request):
        qs = _campaign_queryset_with_points()
        raw = (request.query_params.get("is_active") or "true").lower()
        if raw in ("false", "0", "no"):
            qs = qs.filter(is_active=False)
        elif raw in ("all", "any"):
            pass
        else:
            qs = qs.filter(is_active=True)
        return qs

    @extend_schema(
        operation_id="donations_list",
        summary="List donation campaigns",
        tags=["Donations"],
        parameters=[
            param_is_active_donations(),
            param_ordering("Allowed: `created_at`, `-created_at`, `id`, `-id`."),
            param_limit(20, 100),
        ],
        responses={200: DonationCampaignSerializer(many=True)},
    )
    def get(self, request):
        qs = self._filter_queryset(request)
        order = parse_ordering(request, "-created_at", _DONATION_ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=20, maximum=100)
        data = DonationCampaignSerializer(qs[:limit], many=True).data
        return Response(data)

    @extend_schema(
        operation_id="donations_create",
        summary="Create donation campaign",
        tags=["Donations"],
        request=DonationCampaignSerializer,
        responses={201: DonationCampaignSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = DonationCampaignSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        obj = _campaign_queryset_with_points().get(pk=ser.instance.pk)
        return Response(DonationCampaignSerializer(obj).data, status=status.HTTP_201_CREATED)


class DonationCampaignDetailAPIView(APIView):
    serializer_class = DonationCampaignSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="donations_retrieve",
        summary="Retrieve donation campaign",
        tags=["Donations"],
        responses={200: DonationCampaignSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(_campaign_queryset_with_points(), pk=pk)
        return Response(DonationCampaignSerializer(obj).data)

    @extend_schema(
        operation_id="donations_replace",
        summary="Replace donation campaign",
        tags=["Donations"],
        request=DonationCampaignSerializer,
        responses={200: DonationCampaignSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(DonationCampaign, pk=pk)
        ser = DonationCampaignSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        obj = get_object_or_404(_campaign_queryset_with_points(), pk=ser.instance.pk)
        return Response(DonationCampaignSerializer(obj).data)

    @extend_schema(
        operation_id="donations_partial_update",
        summary="Partially update donation campaign",
        tags=["Donations"],
        request=DonationCampaignSerializer,
        responses={200: DonationCampaignSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(DonationCampaign, pk=pk)
        ser = DonationCampaignSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        obj = get_object_or_404(_campaign_queryset_with_points(), pk=ser.instance.pk)
        return Response(DonationCampaignSerializer(obj).data)

    @extend_schema(
        operation_id="donations_destroy",
        summary="Delete donation campaign",
        tags=["Donations"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(DonationCampaign, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DonationCollectionPointByCampaignAPIView(APIView):
    """List linked points for a campaign, or attach an existing catalog point (POST)."""

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="donation_collection_points_list",
        summary="List collection points linked to a campaign",
        tags=["Donations"],
        responses={200: DonationCampaignSerializer},
    )
    def get(self, request, campaign_pk):
        obj = get_object_or_404(_campaign_queryset_with_points(), pk=campaign_pk)
        return Response(DonationCampaignSerializer(obj).data["collection_points"])

    @extend_schema(
        operation_id="donation_collection_points_attach",
        summary="Link an existing collection point to this campaign",
        description=(
            "Body: `collection_point` (integer id) and optional `sort_order`. "
            "Create catalog points at `/api/community/collection-points/` first."
        ),
        tags=["Donations"],
        request=DonationCampaignPointLinkWriteSerializer,
        responses={201: DonationCampaignPointLinkWriteSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request, campaign_pk):
        get_object_or_404(DonationCampaign, pk=campaign_pk)
        ser = DonationCampaignPointLinkWriteSerializer(
            data=request.data,
            context={"campaign_pk": campaign_pk},
        )
        ser.is_valid(raise_exception=True)
        try:
            ser.save()
        except IntegrityError:
            return Response(
                {"detail": "This collection point is already linked to this campaign."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ser.data, status=status.HTTP_201_CREATED)


class DonationCampaignPointLinkDetailAPIView(APIView):
    """Update link order (PATCH) or remove point from campaign (DELETE)."""

    def get_permissions(self):
        return [IsAdministrator()]

    @extend_schema(
        operation_id="donation_campaign_point_link_partial_update",
        summary="Update sort order of a linked collection point",
        tags=["Donations"],
        request=DonationCampaignPointLinkWriteSerializer,
        responses={200: DonationCampaignPointLinkWriteSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, campaign_pk, point_pk):
        link = get_object_or_404(
            DonationCampaignPointLink,
            campaign_id=campaign_pk,
            collection_point_id=point_pk,
        )
        ser = DonationCampaignPointLinkWriteSerializer(
            link,
            data=request.data,
            partial=True,
            context={"campaign_pk": campaign_pk},
        )
        ser.is_valid(raise_exception=True)
        if "collection_point" in ser.validated_data:
            return Response(
                {"detail": "Use DELETE and POST to change which point is linked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="donation_campaign_point_link_destroy",
        summary="Unlink collection point from this campaign",
        tags=["Donations"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, campaign_pk, point_pk):
        link = get_object_or_404(
            DonationCampaignPointLink,
            campaign_id=campaign_pk,
            collection_point_id=point_pk,
        )
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
