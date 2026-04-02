from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
]
