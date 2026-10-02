from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
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
            OpenApiParameter(
                name="within_days",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="When set (1–30), only items created within that many days are returned.",
            ),
        ],
        responses={200: CommunityNewsSerializer(many=True)},
    )
    def get(self, request):
        qs = CommunityNews.objects.all()
        within_days = _parse_within_days(request)
        if isinstance(within_days, Response):
            return within_days
        if within_days:
            cutoff = timezone.now() - timedelta(days=within_days)
            qs = qs.filter(created_at__gte=cutoff)
        order = parse_ordering(request, "-created_at", _NEWS_ORDERING)
        if order:
            qs = qs.order_by(*order)
        limit = parse_limit(request, default=12, maximum=100)
        data = CommunityNewsSerializer(
            qs[:limit],
            many=True,
            context={"request": request},
        ).data
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
        ser = CommunityNewsSerializer(data=request.data, context={"request": request})
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
        return Response(CommunityNewsSerializer(obj, context={"request": request}).data)

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
        ser = CommunityNewsSerializer(obj, data=request.data, context={"request": request})
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
        ser = CommunityNewsSerializer(obj, data=request.data, partial=True, context={"request": request})
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
        if obj.image:
            obj.image.delete(save=False)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def _parse_within_days(request):
    raw = (request.query_params.get("within_days") or "").strip()
    if not raw:
        return None
    try:
        days = int(raw)
    except ValueError:
        return Response(
            {"within_days": "Informe um número inteiro de dias."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if days < 1 or days > 30:
        return Response(
            {"within_days": "Use um período entre 1 e 30 dias."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return days
