from django.urls import path

from . import views

urlpatterns = [
    path("", views.GalleryItemCollectionAPIView.as_view(), name="gallery-collection"),
    path("<int:pk>/", views.GalleryItemDetailAPIView.as_view(), name="gallery-detail"),
]
