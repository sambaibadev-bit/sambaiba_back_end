from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions

from .permissions import IsAdministrator
from .serializers import UserCreateSerializer, UserProfileSerializer

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        tags=["Users"],
        summary="Register user",
        operation_id="users_register",
        description=(
            "**Administrators only** (JWT + role `admin` or superuser). "
            "Creates a **Community** user account on behalf of someone else — "
            "not a public self-registration endpoint. "
            "Obtain a JWT with `POST /api/auth/jwt/` first."
        ),
        auth=[{"jwtAuth": []}],
    ),
)
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]


@extend_schema_view(
    get=extend_schema(
        tags=["Users"],
        summary="Authenticated user profile",
        operation_id="users_me_retrieve",
        description="Requires JWT in the `Authorization: Bearer <access>` header.",
        auth=[{"jwtAuth": []}],
    ),
    patch=extend_schema(
        tags=["Users"],
        summary="Update profile",
        operation_id="users_me_partial_update",
        auth=[{"jwtAuth": []}],
    ),
    put=extend_schema(exclude=True),
)
class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
