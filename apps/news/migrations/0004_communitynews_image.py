from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_communitynews_summary"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitynews",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="news/", verbose_name="image"),
        ),
    ]
