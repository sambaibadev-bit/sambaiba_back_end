from django.urls import path

from . import views

urlpatterns = [
    path("", views.CommunityNewsCollectionAPIView.as_view(), name="news-collection"),
    path("<int:pk>/", views.CommunityNewsDetailAPIView.as_view(), name="news-detail"),
]
