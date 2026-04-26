from django.urls import include, path

from . import views

urlpatterns = [
    path("health/", views.HealthView.as_view(), name="health"),
    path("auth/", include("apps.jwt_auth.urls")),
    path("users/", include("apps.users.urls")),
    path("community/event-categories/", include("apps.event_categories.urls")),
    path("community/gallery-categories/", include("apps.gallery_categories.urls")),
    path("community/events/", include("apps.events.urls")),
    path("community/gallery/", include("apps.gallery.urls")),
    path("community/collection-points/", include("apps.collection_points.urls")),
    path("community/donation-campaigns/", include("apps.donations.urls")),
    path("community/news/", include("apps.news.urls")),
    path("community/contacts/", include("apps.contacts.urls")),
    path("community/suggestions/", include("apps.suggestions.urls")),
]
