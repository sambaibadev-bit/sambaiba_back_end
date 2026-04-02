from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    tags=["Health"],
    summary="Health check",
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
class HealthView(APIView):
    """Endpoint simples para verificar se a API está no ar."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "sambaiba_back_end"})
