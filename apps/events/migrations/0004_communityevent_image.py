from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_communityevent_category_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityevent",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="events/", verbose_name="image"),
        ),
    ]
