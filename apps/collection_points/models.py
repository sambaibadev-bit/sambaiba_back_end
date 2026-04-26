from django.db import models


class CollectionPoint(models.Model):
    """Community drop-off location (catalog entity; campaigns link via donations app)."""

    name = models.CharField("name", max_length=200)
    address = models.CharField("address", max_length=500)
    hours = models.CharField(
        "opening hours",
        max_length=255,
        blank=True,
        help_text='e.g. "Mon–Fri, 8am–4pm"',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "community_donationcollectionpoint"
        ordering = ["name", "id"]
        verbose_name = "collection point"
        verbose_name_plural = "collection points"

    def __str__(self):
        return self.name
