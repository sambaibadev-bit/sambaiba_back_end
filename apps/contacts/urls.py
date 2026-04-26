from django.urls import path

from . import views

urlpatterns = [
    path("", views.UsefulContactCollectionAPIView.as_view(), name="contacts-collection"),
    path("<int:pk>/", views.UsefulContactDetailAPIView.as_view(), name="contacts-detail"),
]
