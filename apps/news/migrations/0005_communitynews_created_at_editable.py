import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0004_communitynews_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communitynews",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
