from django.db import models


class CommunityNews(models.Model):
    """Community news and notices."""

    class NewsCategory(models.TextChoices):
        AVISO = "aviso", "Notice"
        COMUNICADO = "comunicado", "Announcement"
        ATUALIZACAO = "atualizacao", "Update"

    title = models.CharField("title", max_length=200)
    content = models.TextField("content")
    category = models.CharField(
        max_length=32,
        choices=NewsCategory.choices,
        default=NewsCategory.COMUNICADO,
    )
    is_pinned = models.BooleanField("pinned", default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "community_communitynews"
        ordering = ["-is_pinned", "-created_at", "id"]
        verbose_name = "news item"
        verbose_name_plural = "news"

    def __str__(self):
        return self.title
