from django.db import models


class UsefulContact(models.Model):
    """Useful contacts displayed on the landing page."""

    name = models.CharField("name", max_length=200)
    phone = models.CharField("phone", max_length=64)
    address = models.CharField("address", max_length=255)
    hours = models.CharField("opening hours", max_length=120)
    sort_order = models.PositiveSmallIntegerField("sort order", default=0)
    is_published = models.BooleanField("published", default=True, db_index=True)

    class Meta:
        db_table = "community_usefulcontact"
        ordering = ["sort_order", "name", "id"]
        verbose_name = "useful contact"
        verbose_name_plural = "useful contacts"

    def __str__(self):
        return self.name
