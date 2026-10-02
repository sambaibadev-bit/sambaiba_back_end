from django.db import migrations, models


def fill_summary_from_content(apps, schema_editor):
    CommunityNews = apps.get_model("news", "CommunityNews")
    for item in CommunityNews.objects.all().iterator():
        if (item.summary or "").strip():
            continue
        item.summary = (item.content or "")[:280]
        item.save(update_fields=["summary"])


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_alter_communitynews_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitynews",
            name="summary",
            field=models.CharField(default="", max_length=280, verbose_name="summary"),
            preserve_default=False,
        ),
        migrations.RunPython(fill_summary_from_content, migrations.RunPython.noop),
    ]
