from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH, param_limit, param_ordering
from core.query_params import parse_limit, parse_ordering

from .models import CommunityNews
from .serializers import CommunityNewsSerializer

_NEWS_ORDERING = frozenset(
    {
        "created_at",
        "-created_at",
        "is_pinned",
        "-is_pinned",
        "id",
        "-id",
    }
)


class CommunityNewsCollectionAPIView(APIView):
    serializer_class = CommunityNewsSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="news_list",
        summary="List news and notices",
        tags=["News"],
        parameters=[
            param_ordering(
                "Allowed: `created_at`, `-created_at`, `is_pinned`, `-is_pinned`, `id`, `-id`."
            ),
            param_limit(12, 100),
        ],
        responses={200: CommunityNewsSerializer(many=True)},
    )
    def get(self, request):
        qs = CommunityNews.objects.all()
        order = parse_ordering(request, "-created_at", _NEWS_ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=12, maximum=100)
        data = CommunityNewsSerializer(qs[:limit], many=True).data
        return Response(data)

    @extend_schema(
        operation_id="news_create",
        summary="Create news item",
        tags=["News"],
        request=CommunityNewsSerializer,
        responses={201: CommunityNewsSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        ser = CommunityNewsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class CommunityNewsDetailAPIView(APIView):
    serializer_class = CommunityNewsSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="news_retrieve",
        summary="Retrieve news item",
        tags=["News"],
        responses={200: CommunityNewsSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(CommunityNews, pk=pk)
        return Response(CommunityNewsSerializer(obj).data)

    @extend_schema(
        operation_id="news_replace",
        summary="Replace news item",
        tags=["News"],
        request=CommunityNewsSerializer,
        responses={200: CommunityNewsSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(CommunityNews, pk=pk)
        ser = CommunityNewsSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="news_partial_update",
        summary="Partially update news item",
        tags=["News"],
        request=CommunityNewsSerializer,
        responses={200: CommunityNewsSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(CommunityNews, pk=pk)
        ser = CommunityNewsSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="news_destroy",
        summary="Delete news item",
        tags=["News"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(CommunityNews, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
