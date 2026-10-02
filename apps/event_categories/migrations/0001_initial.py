from django.db import migrations, models


def seed_event_categories(apps, schema_editor):
    EventCategory = apps.get_model("event_categories", "EventCategory")
    rows = [
        ("saude", "Health", 10),
        ("educacao", "Education", 20),
        ("cultura", "Culture", 30),
        ("assistencia_social", "Social assistance", 40),
        ("comercio", "Commerce", 50),
        ("data_comemorativa", "Commemorative date", 60),
        ("eventos", "Events", 70),
        ("campanhas", "Campaigns", 80),
    ]
    for slug, name, sort_order in rows:
        EventCategory.objects.get_or_create(
            slug=slug,
            defaults={"name": name, "sort_order": sort_order, "is_active": True},
        )


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EventCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=64, unique=True, verbose_name="slug")),
                ("name", models.CharField(max_length=128, verbose_name="name")),
                (
                    "sort_order",
                    models.PositiveSmallIntegerField(default=0, verbose_name="display order"),
                ),
                (
                    "is_active",
                    models.BooleanField(db_index=True, default=True, verbose_name="active"),
                ),
            ],
            options={
                "verbose_name": "event category",
                "verbose_name_plural": "event categories",
                "db_table": "community_eventcategory",
                "ordering": ["sort_order", "slug"],
            },
        ),
        migrations.RunPython(seed_event_categories, migrations.RunPython.noop),
    ]
