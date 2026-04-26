import django.db.models.deletion
from django.db import migrations, models


def forwards_fill_event_category_tmp(apps, schema_editor):
    CommunityEvent = apps.get_model("events", "CommunityEvent")
    EventCategory = apps.get_model("event_categories", "EventCategory")
    fallback = EventCategory.objects.get(slug="cultura")
    for ev in CommunityEvent.objects.all():
        slug = (getattr(ev, "category", None) or "cultura").strip().lower()
        cat = EventCategory.objects.filter(slug=slug).first() or fallback
        ev.category_tmp_id = cat.pk
        ev.save(update_fields=["category_tmp_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("event_categories", "0001_initial"),
        ("events", "0002_alter_communityevent_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityevent",
            name="category_tmp",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events_tmp",
                to="event_categories.eventcategory",
                verbose_name="category",
            ),
        ),
        migrations.RunPython(forwards_fill_event_category_tmp, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="communityevent",
            name="category",
        ),
        migrations.AlterField(
            model_name="communityevent",
            name="category_tmp",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events",
                to="event_categories.eventcategory",
                verbose_name="category",
            ),
        ),
        migrations.RenameField(
            model_name="communityevent",
            old_name="category_tmp",
            new_name="category",
        ),
    ]
