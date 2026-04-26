from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("community", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="CommunityNews",
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
                        ("content", models.TextField(verbose_name="conteúdo")),
                        (
                            "category",
                            models.CharField(
                                choices=[
                                    ("aviso", "Aviso"),
                                    ("comunicado", "Comunicado"),
                                    ("atualizacao", "Atualização"),
                                ],
                                default="comunicado",
                                max_length=32,
                            ),
                        ),
                        (
                            "is_pinned",
                            models.BooleanField(db_index=True, default=False, verbose_name="fixado"),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                    ],
                    options={
                        "verbose_name": "notícia",
                        "verbose_name_plural": "notícias",
                        "ordering": ["-is_pinned", "-created_at", "id"],
                        "db_table": "community_communitynews",
                    },
                ),
            ],
        ),
    ]
