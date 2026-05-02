from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommunitySuggestion",
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
                ("name", models.CharField(max_length=120, verbose_name="nome")),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="e-mail"),
                ),
                (
                    "suggestion_type",
                    models.CharField(
                        choices=[
                            ("evento", "Sugerir evento"),
                            ("informacao", "Enviar informação"),
                            ("foto", "Compartilhar foto"),
                        ],
                        max_length=32,
                        verbose_name="tipo",
                    ),
                ),
                ("message", models.TextField(verbose_name="mensagem")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "reviewed",
                    models.BooleanField(db_index=True, default=False, verbose_name="revisado"),
                ),
            ],
            options={
                "verbose_name": "sugestão",
                "verbose_name_plural": "sugestões",
                "ordering": ["-created_at", "id"],
                "db_table": "community_communitysuggestion",
            },
        ),
    ]
