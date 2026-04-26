from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """Simple endpoint to verify the API is running."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Health"],
        summary="Health check",
        operation_id="health_check",
        responses={
            200: inline_serializer(
                name="HealthResponse",
                fields={
                    "status": serializers.CharField(),
                    "service": serializers.CharField(),
                },
            )
        },
    )
    def get(self, request):
        return Response({"status": "ok", "service": "sambaiba_back_end"})
