from django.urls import path

from . import views

urlpatterns = [
    path("", views.CollectionPointCollectionAPIView.as_view(), name="collection-points-collection"),
    path("<int:pk>/", views.CollectionPointDetailAPIView.as_view(), name="collection-points-detail"),
]
