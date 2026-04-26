from django.urls import path

from . import views

urlpatterns = [
    path("", views.CommunityEventCollectionAPIView.as_view(), name="events-collection"),
    path("<int:pk>/", views.CommunityEventDetailAPIView.as_view(), name="events-detail"),
]
