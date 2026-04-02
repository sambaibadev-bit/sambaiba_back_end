from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .serializers import CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Autenticação JWT"],
    summary="Obter par de tokens (access + refresh)",
    description=(
        "Credenciais: `username` e `password`. "
        "Resposta inclui `access`, `refresh`, `user_id`, `username` e `role`."
    ),
    responses={
        200: inline_serializer(
            name="JwtObtainPairResponse",
            fields={
                "access": serializers.CharField(),
                "refresh": serializers.CharField(),
                "user_id": serializers.IntegerField(),
                "username": serializers.CharField(),
                "role": serializers.CharField(),
            },
        )
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Autenticação JWT"],
        summary="Renovar access token",
        request=inline_serializer(
            name="JwtRefreshRequest",
            fields={"refresh": serializers.CharField()},
        ),
        responses={
            200: inline_serializer(
                name="JwtRefreshResponse",
                fields={"access": serializers.CharField()},
            )
        },
    )
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(
    post=extend_schema(
        tags=["Autenticação JWT"],
        summary="Validar token (access ou refresh)",
        request=inline_serializer(
            name="JwtVerifyRequest",
            fields={"token": serializers.CharField()},
        ),
        responses={200: OpenApiTypes.OBJECT},
    )
)
class DocumentedTokenVerifyView(TokenVerifyView):
    pass
