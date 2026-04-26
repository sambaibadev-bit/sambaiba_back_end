from django.db import models


class GalleryItem(models.Model):
    """Gallery items (photos or videos of community actions)."""

    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    title = models.CharField("title", max_length=200)
    category = models.CharField("category", max_length=64, blank=True)
    media_type = models.CharField(
        max_length=16,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )
    media_url = models.URLField("media URL", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "community_galleryitem"
        ordering = ["-created_at", "id"]
        verbose_name = "gallery item"
        verbose_name_plural = "gallery"

    def __str__(self):
        return self.title
