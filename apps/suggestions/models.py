from django.db import models


class CommunitySuggestion(models.Model):
    """Suggestions sent by the public (event, information, photo)."""

    class SuggestionType(models.TextChoices):
        EVENTO = "evento", "Suggest event"
        INFORMACAO = "informacao", "Send information"
        FOTO = "foto", "Share photo"

    name = models.CharField("name", max_length=120)
    email = models.EmailField("email", blank=True)
    suggestion_type = models.CharField(
        "type",
        max_length=32,
        choices=SuggestionType.choices,
    )
    message = models.TextField("message")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField("reviewed", default=False, db_index=True)

    class Meta:
        db_table = "community_communitysuggestion"
        ordering = ["-created_at", "id"]
        verbose_name = "suggestion"
        verbose_name_plural = "suggestions"

    def __str__(self):
        return f"{self.name} — {self.get_suggestion_type_display()}"
