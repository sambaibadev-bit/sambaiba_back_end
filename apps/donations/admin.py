from django.contrib import admin

from .models import DonationCampaign, DonationCampaignPointLink


class DonationCampaignPointLinkInline(admin.TabularInline):
    model = DonationCampaignPointLink
    fk_name = "campaign"
    extra = 0
    autocomplete_fields = ("collection_point",)
    ordering = ("sort_order", "id")


@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "donation_type", "goal_target", "goal_unit", "is_active", "created_at")
    list_filter = ("donation_type", "is_active")
    inlines = [DonationCampaignPointLinkInline]


@admin.register(DonationCampaignPointLink)
class DonationCampaignPointLinkAdmin(admin.ModelAdmin):
    list_display = ("campaign", "collection_point", "sort_order")
    list_filter = ("campaign",)
    ordering = ("campaign", "sort_order", "id")
