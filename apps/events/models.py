from django.db import models


class CommunityEvent(models.Model):
    """Events shown on the calendar and in the upcoming events list."""

    class Category(models.TextChoices):
        SAUDE = "saude", "Health"
        EDUCACAO = "educacao", "Education"
        CULTURA = "cultura", "Culture"
        ASSISTENCIA_SOCIAL = "assistencia_social", "Social assistance"
        COMERCIO = "comercio", "Commerce"
        DATA_COMEMORATIVA = "data_comemorativa", "Commemorative date"

    title = models.CharField("title", max_length=200)
    description = models.TextField("description", blank=True)
    date = models.DateField("date")
    time = models.CharField("time", max_length=64, blank=True)
    location = models.CharField("location", max_length=255, blank=True)
    category = models.CharField(
        "category",
        max_length=32,
        choices=Category.choices,
        default=Category.CULTURA,
    )
    is_highlighted = models.BooleanField("highlighted", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "community_communityevent"
        ordering = ["date", "time", "id"]
        verbose_name = "community event"
        verbose_name_plural = "community events"

    def __str__(self):
        return f"{self.title} ({self.date})"
