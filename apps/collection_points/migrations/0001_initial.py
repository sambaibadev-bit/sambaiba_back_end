from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("donations", "0005_campaign_point_m2m"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="CollectionPoint",
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
                        ("name", models.CharField(max_length=200, verbose_name="name")),
                        (
                            "address",
                            models.CharField(max_length=500, verbose_name="address"),
                        ),
                        (
                            "hours",
                            models.CharField(
                                blank=True,
                                help_text='e.g. "Mon–Fri, 8am–4pm"',
                                max_length=255,
                                verbose_name="opening hours",
                            ),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                    ],
                    options={
                        "verbose_name": "collection point",
                        "verbose_name_plural": "collection points",
                        "db_table": "community_donationcollectionpoint",
                        "ordering": ["name", "id"],
                    },
                ),
            ],
        ),
    ]
