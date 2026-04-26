from django.urls import path

from . import views

urlpatterns = [
    path("", views.GalleryCategoryCollectionAPIView.as_view(), name="gallery-categories-collection"),
    path("<int:pk>/", views.GalleryCategoryDetailAPIView.as_view(), name="gallery-categories-detail"),
]
