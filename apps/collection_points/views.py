from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH, param_limit, param_ordering
from core.query_params import parse_limit, parse_ordering

from .models import CollectionPoint
from .serializers import CollectionPointSerializer

_ORDERING = frozenset(
    {"id", "-id", "name", "-name", "created_at", "-created_at", "updated_at", "-updated_at"}
)


class CollectionPointCollectionAPIView(APIView):
    serializer_class = CollectionPointSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="collection_points_list",
        summary="List collection points",
        tags=["Collection Points"],
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by name or address (case-insensitive).",
            ),
            param_ordering(
                "Allowed: `id`, `-id`, `name`, `-name`, `created_at`, `-created_at`, "
                "`updated_at`, `-updated_at`."
            ),
            param_limit(20, 200),
        ],
        responses={200: CollectionPointSerializer(many=True)},
    )
    def get(self, request):
        qs = CollectionPoint.objects.all()
        search = (request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(address__icontains=search))
        order = parse_ordering(request, "name", _ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=50, maximum=200)
        return Response(CollectionPointSerializer(qs[:limit], many=True).data)

    @extend_schema(
        operation_id="collection_points_create",
        summary="Create collection point",
        tags=["Collection Points"],
        request=CollectionPointSerializer,
        responses={201: CollectionPointSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = CollectionPointSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class CollectionPointDetailAPIView(APIView):
    serializer_class = CollectionPointSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="collection_points_retrieve",
        summary="Retrieve collection point",
        tags=["Collection Points"],
        responses={200: CollectionPointSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(CollectionPoint, pk=pk)
        return Response(CollectionPointSerializer(obj).data)

    @extend_schema(
        operation_id="collection_points_replace",
        summary="Replace collection point",
        tags=["Collection Points"],
        request=CollectionPointSerializer,
        responses={200: CollectionPointSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(CollectionPoint, pk=pk)
        ser = CollectionPointSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="collection_points_partial_update",
        summary="Partially update collection point",
        tags=["Collection Points"],
        request=CollectionPointSerializer,
        responses={200: CollectionPointSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(CollectionPoint, pk=pk)
        ser = CollectionPointSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="collection_points_destroy",
        summary="Delete collection point",
        description="Removes the point and all donation campaign links (CASCADE).",
        tags=["Collection Points"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(CollectionPoint, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
