import json

from django.db import migrations, models
import django.db.models.deletion


def copy_json_collection_points_to_rows(apps, schema_editor):
    """
    Read legacy JSON from the DB with raw SQL. After CreateModel, the historical
    `DonationCampaign` no longer has a `collection_points` column on the model
    (it is the reverse relation), so ORM iteration would mis-map the DB row.
    """
    DonationCollectionPoint = apps.get_model("donations", "DonationCollectionPoint")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id, collection_points FROM community_donationcampaign")
        rows = cursor.fetchall()
    for camp_id, raw in rows:
        if raw is None:
            continue
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode("utf-8")
        if isinstance(raw, str):
            raw = raw.strip()
            if not raw:
                continue
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                continue
        if not isinstance(raw, list):
            continue
        for idx, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()[:200]
            if not name:
                name = "Collection point"
            address = str(item.get("address") or "").strip()[:500]
            hours = str(item.get("hours") or "").strip()[:255]
            DonationCollectionPoint.objects.create(
                campaign_id=camp_id,
                name=name,
                address=address or "—",
                hours=hours,
                sort_order=min(idx, 32767),
            )


class Migration(migrations.Migration):

    dependencies = [
        ("donations", "0003_goal_numeric_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="DonationCollectionPoint",
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
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "address",
                    models.CharField(max_length=500, verbose_name="address"),
                ),
                (
                    "hours",
                    models.CharField(
                        blank=True,
                        help_text='e.g. "Mon–Fri, 8am–4pm"',
                        max_length=255,
                        verbose_name="opening hours",
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Lower values appear first in listings.",
                        verbose_name="display order",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collection_points",
                        to="donations.donationcampaign",
                        verbose_name="campaign",
                    ),
                ),
            ],
            options={
                "verbose_name": "donation collection point",
                "verbose_name_plural": "donation collection points",
                "db_table": "community_donationcollectionpoint",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.RunPython(copy_json_collection_points_to_rows, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="donationcampaign",
            name="collection_points",
        ),
    ]
