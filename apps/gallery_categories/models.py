from django.db import models


class GalleryCategory(models.Model):
    """Labels used only for gallery items."""

    slug = models.SlugField("slug", max_length=64, unique=True, db_index=True)
    name = models.CharField("name", max_length=128)
    sort_order = models.PositiveSmallIntegerField("display order", default=0)
    is_active = models.BooleanField("active", default=True, db_index=True)

    class Meta:
        db_table = "community_gallerycategory"
        ordering = ["sort_order", "slug"]
        verbose_name = "gallery category"
        verbose_name_plural = "gallery categories"

    def __str__(self):
        return self.name
