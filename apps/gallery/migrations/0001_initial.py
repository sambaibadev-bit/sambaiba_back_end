from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="GalleryItem",
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
                            "category",
                            models.CharField(blank=True, max_length=64, verbose_name="categoria"),
                        ),
                        (
                            "media_type",
                            models.CharField(
                                choices=[("image", "Imagem"), ("video", "Vídeo")],
                                default="image",
                                max_length=16,
                            ),
                        ),
                        (
                            "media_url",
                            models.URLField(max_length=500, verbose_name="URL da mídia"),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                    ],
                    options={
                        "verbose_name": "item da galeria",
                        "verbose_name_plural": "galeria",
                        "ordering": ["-created_at", "id"],
                        "db_table": "community_galleryitem",
                    },
                ),
            ],
        ),
    ]
