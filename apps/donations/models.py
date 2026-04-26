from django.db import models


class DonationCampaign(models.Model):
    """Donation campaigns; collection points are linked via `DonationCampaignPointLink`."""

    class DonationType(models.TextChoices):
        ROUPAS = "roupas", "Clothing"
        ALIMENTOS = "alimentos", "Food"
        BRINQUEDOS = "brinquedos", "Toys"
        MOVEIS = "moveis", "Furniture"
        MEDICAMENTOS = "medicamentos", "Medicine"
        OUTROS = "outros", "Other"

    title = models.CharField("title", max_length=200)
    description = models.TextField("description", blank=True)
    donation_type = models.CharField(
        "donation type",
        max_length=32,
        choices=DonationType.choices,
        default=DonationType.OUTROS,
    )
    is_active = models.BooleanField("active", default=True, db_index=True)
    goal_target = models.PositiveIntegerField(
        "goal target",
        null=True,
        blank=True,
        help_text="Numeric collection target (e.g. number of pieces, baskets).",
    )
    goal_unit = models.CharField(
        "goal unit",
        max_length=64,
        blank=True,
        help_text='Unit label shown after the number, e.g. "peças", "cestas", "brinquedos".',
    )
    collection_points = models.ManyToManyField(
        "collection_points.CollectionPoint",
        through="DonationCampaignPointLink",
        related_name="donation_campaigns",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "community_donationcampaign"
        ordering = ["-created_at", "id"]
        verbose_name = "donation campaign"
        verbose_name_plural = "donation campaigns"

    def __str__(self):
        return self.title


class DonationCampaignPointLink(models.Model):
    """Associates a catalog collection point with a campaign (order is per campaign)."""

    campaign = models.ForeignKey(
        DonationCampaign,
        on_delete=models.CASCADE,
        related_name="point_links",
        verbose_name="campaign",
    )
    collection_point = models.ForeignKey(
        "collection_points.CollectionPoint",
        on_delete=models.CASCADE,
        related_name="campaign_links",
        verbose_name="collection point",
    )
    sort_order = models.PositiveSmallIntegerField(
        "display order",
        default=0,
        help_text="Lower values appear first for this campaign.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "community_donationcampaignpointlink"
        ordering = ["sort_order", "id"]
        verbose_name = "donation campaign collection link"
        verbose_name_plural = "donation campaign collection links"
        constraints = [
            models.UniqueConstraint(
                fields=("campaign", "collection_point"),
                name="uniq_donation_campaign_collection_point",
            ),
        ]

    def __str__(self):
        return f"{self.campaign_id} → {self.collection_point_id}"
