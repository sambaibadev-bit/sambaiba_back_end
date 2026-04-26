from django.apps import AppConfig


class EventCategoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.event_categories"
    label = "event_categories"
    verbose_name = "Event categories"
