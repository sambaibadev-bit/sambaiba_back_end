from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .serializers import CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["JWT Auth"],
        summary="Obtain token pair (access + refresh)",
        operation_id="auth_jwt_obtain",
        description=(
            "Credentials: `username` and `password`. "
            "Response includes `access`, `refresh`, `user_id`, `username`, and `role`. "
            "Use `access` in Swagger: **Authorize** → **jwtAuth** scheme."
        ),
        request=CustomTokenObtainPairSerializer,
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
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["JWT Auth"],
        summary="Refresh access token",
        operation_id="auth_jwt_refresh",
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
        tags=["JWT Auth"],
        summary="Verify token (access or refresh)",
        operation_id="auth_jwt_verify",
        request=inline_serializer(
            name="JwtVerifyRequest",
            fields={"token": serializers.CharField()},
        ),
        responses={200: OpenApiTypes.OBJECT},
    )
)
class DocumentedTokenVerifyView(TokenVerifyView):
    pass
