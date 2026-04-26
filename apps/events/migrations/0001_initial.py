# Estado inicial dos modelos de eventos (tabelas `community_*` já existentes ou criadas pelo deploy).

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="CommunityEvent",
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
                        ("title", models.CharField(max_length=200, verbose_name="título")),
                        (
                            "description",
                            models.TextField(blank=True, verbose_name="descrição"),
                        ),
                        ("date", models.DateField(verbose_name="data")),
                        (
                            "time",
                            models.CharField(blank=True, max_length=64, verbose_name="horário"),
                        ),
                        (
                            "location",
                            models.CharField(blank=True, max_length=255, verbose_name="local"),
                        ),
                        (
                            "category",
                            models.CharField(
                                choices=[
                                    ("saude", "Saúde"),
                                    ("educacao", "Educação"),
                                    ("cultura", "Cultura"),
                                    ("assistencia_social", "Assistência social"),
                                    ("comercio", "Comércio"),
                                    ("data_comemorativa", "Data comemorativa"),
                                ],
                                default="cultura",
                                max_length=32,
                                verbose_name="categoria",
                            ),
                        ),
                        (
                            "is_highlighted",
                            models.BooleanField(default=False, verbose_name="destaque"),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                    ],
                    options={
                        "verbose_name": "evento comunitário",
                        "verbose_name_plural": "eventos comunitários",
                        "ordering": ["date", "time", "id"],
                        "db_table": "community_communityevent",
                    },
                ),
            ],
        ),
    ]
