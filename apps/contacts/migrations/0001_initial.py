from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="UsefulContact",
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
                        ("name", models.CharField(max_length=200, verbose_name="nome")),
                        ("phone", models.CharField(max_length=64, verbose_name="telefone")),
                        ("address", models.CharField(max_length=255, verbose_name="endereço")),
                        (
                            "hours",
                            models.CharField(max_length=120, verbose_name="horário de atendimento"),
                        ),
                        (
                            "sort_order",
                            models.PositiveSmallIntegerField(default=0, verbose_name="ordem"),
                        ),
                        (
                            "is_published",
                            models.BooleanField(db_index=True, default=True, verbose_name="publicado"),
                        ),
                    ],
                    options={
                        "verbose_name": "contato útil",
                        "verbose_name_plural": "contatos úteis",
                        "ordering": ["sort_order", "name", "id"],
                        "db_table": "community_usefulcontact",
                    },
                ),
            ],
        ),
    ]
