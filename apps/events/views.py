from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH, param_limit, param_ordering
from core.query_params import parse_limit, parse_ordering

from .models import CommunityEvent
from .serializers import CommunityEventSerializer

_EVENT_ORDERING = frozenset(
    {"date", "-date", "created_at", "-created_at", "id", "-id", "time", "-time"}
)


class CommunityEventCollectionAPIView(APIView):
    """GET: public list. POST: create (administrator)."""

    serializer_class = CommunityEventSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="events_list",
        summary="List events",
        description="List events for the calendar and upcoming events. Sort with `ordering` (e.g. `-date`, `date`).",
        tags=["Events"],
        parameters=[
            param_ordering(
                "Allowed fields: `date`, `-date`, `created_at`, `-created_at`, `id`, `-id`, `time`, `-time`."
            ),
            param_limit(300, 500),
        ],
        responses={200: CommunityEventSerializer(many=True)},
    )
    def get(self, request):
        qs = CommunityEvent.objects.select_related("category")
        order = parse_ordering(request, "-date", _EVENT_ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=300, maximum=500)
        data = CommunityEventSerializer(qs[:limit], many=True).data
        return Response(data)

    @extend_schema(
        operation_id="events_create",
        summary="Create event",
        tags=["Events"],
        request=CommunityEventSerializer,
        responses={201: CommunityEventSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = CommunityEventSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class CommunityEventDetailAPIView(APIView):
    """GET: public. PUT/PATCH/DELETE: administrator."""

    serializer_class = CommunityEventSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="events_retrieve",
        summary="Retrieve event",
        tags=["Events"],
        responses={200: CommunityEventSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(CommunityEvent.objects.select_related("category"), pk=pk)
        return Response(CommunityEventSerializer(obj).data)

    @extend_schema(
        operation_id="events_replace",
        summary="Replace event",
        tags=["Events"],
        request=CommunityEventSerializer,
        responses={200: CommunityEventSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(CommunityEvent.objects.select_related("category"), pk=pk)
        ser = CommunityEventSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="events_partial_update",
        summary="Partially update event",
        tags=["Events"],
        request=CommunityEventSerializer,
        responses={200: CommunityEventSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(CommunityEvent.objects.select_related("category"), pk=pk)
        ser = CommunityEventSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="events_destroy",
        summary="Delete event",
        tags=["Events"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(CommunityEvent.objects.select_related("category"), pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
