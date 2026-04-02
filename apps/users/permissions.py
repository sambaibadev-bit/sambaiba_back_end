from rest_framework.permissions import BasePermission

from .models import User


class IsAdministrator(BasePermission):
    """Acesso apenas para usuários com papel Administrador (ou superusuário)."""

    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        return getattr(u, "role", None) == User.Role.ADMIN
