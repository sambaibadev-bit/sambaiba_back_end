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

from .models import GalleryCategory
from .serializers import GalleryCategorySerializer

_ORDERING = frozenset(
    {"id", "-id", "slug", "-slug", "name", "-name", "sort_order", "-sort_order"}
)


class GalleryCategoryCollectionAPIView(APIView):
    serializer_class = GalleryCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="gallery_categories_list",
        summary="List gallery categories",
        tags=["Gallery categories"],
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=str,
                location=OpenApiParameter.QUERY,
                description="`true` (default), `false`, or `all`.",
            ),
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by name or slug (case-insensitive).",
            ),
            param_ordering(
                "Allowed: `id`, `-id`, `slug`, `-slug`, `name`, `-name`, `sort_order`, `-sort_order`."
            ),
            param_limit(20, 200),
        ],
        responses={200: GalleryCategorySerializer(many=True)},
    )
    def get(self, request):
        qs = GalleryCategory.objects.all()
        raw = (request.query_params.get("is_active") or "true").lower()
        if raw in ("false", "0", "no"):
            qs = qs.filter(is_active=False)
        elif raw in ("all", "any"):
            pass
        else:
            qs = qs.filter(is_active=True)
        search = (request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
        order = parse_ordering(request, "sort_order", _ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=100, maximum=200)
        return Response(GalleryCategorySerializer(qs[:limit], many=True).data)

    @extend_schema(
        operation_id="gallery_categories_create",
        summary="Create gallery category",
        tags=["Gallery categories"],
        request=GalleryCategorySerializer,
        responses={201: GalleryCategorySerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = GalleryCategorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class GalleryCategoryDetailAPIView(APIView):
    serializer_class = GalleryCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="gallery_categories_retrieve",
        summary="Retrieve gallery category",
        tags=["Gallery categories"],
        responses={200: GalleryCategorySerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(GalleryCategory, pk=pk)
        return Response(GalleryCategorySerializer(obj).data)

    @extend_schema(
        operation_id="gallery_categories_replace",
        summary="Replace gallery category",
        tags=["Gallery categories"],
        request=GalleryCategorySerializer,
        responses={200: GalleryCategorySerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(GalleryCategory, pk=pk)
        ser = GalleryCategorySerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="gallery_categories_partial_update",
        summary="Partially update gallery category",
        tags=["Gallery categories"],
        request=GalleryCategorySerializer,
        responses={200: GalleryCategorySerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(GalleryCategory, pk=pk)
        ser = GalleryCategorySerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="gallery_categories_destroy",
        summary="Delete gallery category",
        description="Fails if gallery items still reference this row (PROTECT).",
        tags=["Gallery categories"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(GalleryCategory, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
