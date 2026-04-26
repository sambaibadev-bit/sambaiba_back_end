from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="DonationCampaign",
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
                        (
                            "donation_type",
                            models.CharField(
                                choices=[
                                    ("roupas", "Roupas"),
                                    ("alimentos", "Alimentos"),
                                    ("brinquedos", "Brinquedos"),
                                    ("moveis", "Móveis"),
                                    ("medicamentos", "Medicamentos"),
                                    ("outros", "Outros"),
                                ],
                                default="outros",
                                max_length=32,
                            ),
                        ),
                        (
                            "is_active",
                            models.BooleanField(db_index=True, default=True, verbose_name="ativa"),
                        ),
                        (
                            "goal",
                            models.CharField(
                                blank=True,
                                max_length=255,
                                verbose_name="meta (texto livre)",
                            ),
                        ),
                        (
                            "collection_points",
                            models.JSONField(
                                default=list,
                                help_text='Lista de objetos: [{"name": "...", "address": "...", "hours": "..."}]',
                                verbose_name="pontos de coleta",
                            ),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                    ],
                    options={
                        "verbose_name": "campanha de doação",
                        "verbose_name_plural": "campanhas de doação",
                        "ordering": ["-created_at", "id"],
                        "db_table": "community_donationcampaign",
                    },
                ),
            ],
        ),
    ]
