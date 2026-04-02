from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions

from .serializers import UserCreateSerializer, UserProfileSerializer

User = get_user_model()


@extend_schema(
    tags=["Usuários"],
    summary="Registrar usuário",
    description=(
        "Cria usuário com perfil **Comunidade**. "
        "Administradores são criados via `createsuperuser` ou painel Django. "
        "Depois obtenha JWT em POST /api/auth/jwt/."
    ),
)
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        tags=["Usuários"],
        summary="Perfil do usuário autenticado",
        description="Requer JWT no header `Authorization: Bearer <access>`.",
    ),
    patch=extend_schema(
        tags=["Usuários"],
        summary="Atualizar perfil",
    ),
    put=extend_schema(exclude=True),
)
class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
