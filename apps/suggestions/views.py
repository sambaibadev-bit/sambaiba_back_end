from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH

from .models import CommunitySuggestion
from .serializers import (
    CommunitySuggestionCreateSerializer,
    CommunitySuggestionStaffSerializer,
)


class CommunitySuggestionCollectionAPIView(APIView):
    """GET: list (administrator). POST: public submission."""

    serializer_class = CommunitySuggestionStaffSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdministrator()]

    @extend_schema(
        operation_id="suggestions_list",
        summary="List suggestions",
        tags=["Suggestions"],
        responses={200: CommunitySuggestionStaffSerializer(many=True)},
        auth=JWT_AUTH,
    )
    def get(self, request):
        qs = CommunitySuggestion.objects.all().order_by("-created_at", "id")
        data = CommunitySuggestionStaffSerializer(qs, many=True).data
        return Response(data)

    @extend_schema(
        operation_id="suggestions_public_create",
        summary="Submit suggestion (public)",
        description="No authentication required. Types: `evento`, `informacao`, `foto`.",
        tags=["Suggestions"],
        request=CommunitySuggestionCreateSerializer,
        responses={
            201: inline_serializer(
                name="SuggestionCreateResponse",
                fields={
                    "ok": drf_serializers.BooleanField(),
                    "id": drf_serializers.IntegerField(),
                },
            ),
        },
    )
    def post(self, request):
        ser = CommunitySuggestionCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(
            {"ok": True, "id": ser.instance.id},
            status=status.HTTP_201_CREATED,
        )


class CommunitySuggestionDetailAPIView(APIView):
    """GET, PUT, PATCH, DELETE: administrator."""

    serializer_class = CommunitySuggestionStaffSerializer
    permission_classes = [IsAdministrator]

    @extend_schema(
        operation_id="suggestions_retrieve",
        summary="Retrieve suggestion",
        tags=["Suggestions"],
        responses={200: CommunitySuggestionStaffSerializer},
        auth=JWT_AUTH,
    )
    def get(self, request, pk):
        obj = get_object_or_404(CommunitySuggestion, pk=pk)
        return Response(CommunitySuggestionStaffSerializer(obj).data)

    @extend_schema(
        operation_id="suggestions_replace",
        summary="Replace suggestion",
        tags=["Suggestions"],
        request=CommunitySuggestionStaffSerializer,
        responses={200: CommunitySuggestionStaffSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        obj = get_object_or_404(CommunitySuggestion, pk=pk)
        ser = CommunitySuggestionStaffSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="suggestions_partial_update",
        summary="Partially update suggestion",
        tags=["Suggestions"],
        request=CommunitySuggestionStaffSerializer,
        responses={200: CommunitySuggestionStaffSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        obj = get_object_or_404(CommunitySuggestion, pk=pk)
        ser = CommunitySuggestionStaffSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="suggestions_destroy",
        summary="Delete suggestion",
        tags=["Suggestions"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        obj = get_object_or_404(CommunitySuggestion, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
