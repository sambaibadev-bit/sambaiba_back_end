from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suggestions", "0002_alter_communitysuggestion_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitysuggestion",
            name="attachments",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="URLs públicas dos ficheiros enviados (ex.: partilha de fotos).",
                verbose_name="attachments",
            ),
        ),
    ]
