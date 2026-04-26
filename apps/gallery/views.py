from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH, param_limit, param_ordering
from core.query_params import parse_limit, parse_ordering

from .models import GalleryItem
from .serializers import GalleryItemSerializer

_GALLERY_ORDERING = frozenset({"created_at", "-created_at", "id", "-id"})


class GalleryItemCollectionAPIView(APIView):
    serializer_class = GalleryItemSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="gallery_list",
        summary="List gallery items",
        tags=["Gallery"],
        parameters=[
            param_ordering("Allowed: `created_at`, `-created_at`, `id`, `-id`."),
            param_limit(50, 100),
        ],
        responses={200: GalleryItemSerializer(many=True)},
    )
    def get(self, request):
        qs = GalleryItem.objects.all()
        order = parse_ordering(request, "-created_at", _GALLERY_ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=50, maximum=100)
        data = GalleryItemSerializer(qs[:limit], many=True).data
        return Response(data)

    @extend_schema(
        operation_id="gallery_create",
        summary="Create gallery item",
        tags=["Gallery"],
        request=GalleryItemSerializer,
        responses={201: GalleryItemSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = GalleryItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class GalleryItemDetailAPIView(APIView):
    serializer_class = GalleryItemSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="gallery_retrieve",
        summary="Retrieve gallery item",
        tags=["Gallery"],
        responses={200: GalleryItemSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(GalleryItem, pk=pk)
        return Response(GalleryItemSerializer(obj).data)

    @extend_schema(
        operation_id="gallery_replace",
        summary="Replace gallery item",
        tags=["Gallery"],
        request=GalleryItemSerializer,
        responses={200: GalleryItemSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(GalleryItem, pk=pk)
        ser = GalleryItemSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="gallery_partial_update",
        summary="Partially update gallery item",
        tags=["Gallery"],
        request=GalleryItemSerializer,
        responses={200: GalleryItemSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(GalleryItem, pk=pk)
        ser = GalleryItemSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="gallery_destroy",
        summary="Delete gallery item",
        tags=["Gallery"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(GalleryItem, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
