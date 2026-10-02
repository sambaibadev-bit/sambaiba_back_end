from django.db import models


class EventCategory(models.Model):
    """Labels used only for community events."""

    slug = models.SlugField("slug", max_length=64, unique=True, db_index=True)
    name = models.CharField("name", max_length=128)
    sort_order = models.PositiveSmallIntegerField("display order", default=0)
    is_active = models.BooleanField("active", default=True, db_index=True)

    class Meta:
        db_table = "community_eventcategory"
        ordering = ["sort_order", "slug"]
        verbose_name = "event category"
        verbose_name_plural = "event categories"

    def __str__(self):
        return self.name
