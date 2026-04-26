from django.db import models


class CommunityEvent(models.Model):
    """Events shown on the calendar and in the upcoming events list."""

    title = models.CharField("title", max_length=200)
    description = models.TextField("description", blank=True)
    date = models.DateField("date")
    time = models.CharField("time", max_length=64, blank=True)
    location = models.CharField("location", max_length=255, blank=True)
    category = models.ForeignKey(
        "event_categories.EventCategory",
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="category",
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
