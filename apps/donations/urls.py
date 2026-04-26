from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:campaign_pk>/collection-points/<int:point_pk>/",
        views.DonationCampaignPointLinkDetailAPIView.as_view(),
        name="donation-campaign-collection-point-link",
    ),
    path(
        "<int:campaign_pk>/collection-points/",
        views.DonationCollectionPointByCampaignAPIView.as_view(),
        name="donation-collection-points-by-campaign",
    ),
    path("", views.DonationCampaignCollectionAPIView.as_view(), name="donations-collection"),
    path("<int:pk>/", views.DonationCampaignDetailAPIView.as_view(), name="donations-detail"),
]
