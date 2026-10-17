from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="user-signup"),
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
]
