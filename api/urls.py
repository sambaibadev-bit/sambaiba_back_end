from django.urls import include, path

from . import views

urlpatterns = [
    path("health/", views.HealthView.as_view(), name="health"),
    path("auth/", include("apps.jwt_auth.urls")),
    path("users/", include("apps.users.urls")),
]
