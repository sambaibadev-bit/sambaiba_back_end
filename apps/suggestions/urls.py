from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.CommunitySuggestionCollectionAPIView.as_view(),
        name="suggestions-collection",
    ),
    path(
        "<int:pk>/",
        views.CommunitySuggestionDetailAPIView.as_view(),
        name="suggestions-detail",
    ),
]
