from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    DocumentedTokenRefreshView,
    DocumentedTokenVerifyView,
)

urlpatterns = [
    path("jwt/", CustomTokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", DocumentedTokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", DocumentedTokenVerifyView.as_view(), name="jwt_verify"),
]
