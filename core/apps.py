from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    label = "core"

    def ready(self):
        if not getattr(settings, "SQLITE_FALLBACK", False):
            return
        from core.runtime import ensure_sqlite_schema

        ensure_sqlite_schema()
