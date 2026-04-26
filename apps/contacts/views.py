from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdministrator
from core.openapi import JWT_AUTH

from .models import UsefulContact
from .serializers import UsefulContactPublicSerializer, UsefulContactSerializer


class UsefulContactCollectionAPIView(APIView):
    """GET: public sees published only; administrator sees all. POST: administrator."""

    serializer_class = UsefulContactSerializer

    def get_permissions(self):
        return [AllowAny()]

    def _is_admin(self, request):
        return IsAdministrator().has_permission(request, self)

    @extend_schema(
        operation_id="contacts_list",
        summary="List useful contacts",
        description=(
            "Without JWT: only published contacts (`is_published=true`). "
            "With an administrator JWT: all records."
        ),
        tags=["Contacts"],
        responses={200: UsefulContactSerializer(many=True)},
    )
    def get(self, request):
        if self._is_admin(request):
            qs = UsefulContact.objects.all().order_by("sort_order", "name", "id")
            data = UsefulContactSerializer(qs, many=True).data
        else:
            qs = UsefulContact.objects.filter(is_published=True).order_by(
                "sort_order", "name", "id"
            )
            data = UsefulContactPublicSerializer(qs, many=True).data
        return Response(data)

    @extend_schema(
        operation_id="contacts_create",
        summary="Create useful contact",
        tags=["Contacts"],
        request=UsefulContactSerializer,
        responses={201: UsefulContactSerializer},
        auth=JWT_AUTH,
    )
    def post(self, request):
        if not self._is_admin(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        ser = UsefulContactSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(UsefulContactSerializer(ser.instance).data, status=status.HTTP_201_CREATED)


class UsefulContactDetailAPIView(APIView):
    """GET: public only if published. PUT/PATCH/DELETE: administrator."""

    serializer_class = UsefulContactSerializer

    def get_permissions(self):
        return [AllowAny()]

    def _is_admin(self, request):
        return IsAdministrator().has_permission(request, self)

    @extend_schema(
        operation_id="contacts_retrieve",
        summary="Retrieve useful contact",
        description="Public: only if `is_published`. Administrator: any record.",
        tags=["Contacts"],
        responses={200: UsefulContactSerializer},
    )
    def get(self, request, pk):
        obj = get_object_or_404(UsefulContact, pk=pk)
        if not obj.is_published and not self._is_admin(request):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self._is_admin(request):
            return Response(UsefulContactSerializer(obj).data)
        return Response(UsefulContactPublicSerializer(obj).data)

    @extend_schema(
        operation_id="contacts_replace",
        summary="Replace useful contact",
        tags=["Contacts"],
        request=UsefulContactSerializer,
        responses={200: UsefulContactSerializer},
        auth=JWT_AUTH,
    )
    def put(self, request, pk):
        if not self._is_admin(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        obj = get_object_or_404(UsefulContact, pk=pk)
        ser = UsefulContactSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="contacts_partial_update",
        summary="Partially update useful contact",
        tags=["Contacts"],
        request=UsefulContactSerializer,
        responses={200: UsefulContactSerializer},
        auth=JWT_AUTH,
    )
    def patch(self, request, pk):
        if not self._is_admin(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        obj = get_object_or_404(UsefulContact, pk=pk)
        ser = UsefulContactSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @extend_schema(
        operation_id="contacts_destroy",
        summary="Delete useful contact",
        tags=["Contacts"],
        responses={204: OpenApiResponse(description="No content.")},
        auth=JWT_AUTH,
    )
    def delete(self, request, pk):
        if not self._is_admin(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        obj = get_object_or_404(UsefulContact, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
