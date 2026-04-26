from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventCategoryCollectionAPIView.as_view(), name="event-categories-collection"),
    path("<int:pk>/", views.EventCategoryDetailAPIView.as_view(), name="event-categories-detail"),
]
