import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collection_points", "0001_initial"),
        ("donations", "0005_campaign_point_m2m"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="DonationCollectionPoint"),
                migrations.AlterField(
                    model_name="donationcampaignpointlink",
                    name="collection_point",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="campaign_links",
                        to="collection_points.collectionpoint",
                        verbose_name="collection point",
                    ),
                ),
                migrations.AlterField(
                    model_name="donationcampaign",
                    name="collection_points",
                    field=models.ManyToManyField(
                        blank=True,
                        related_name="donation_campaigns",
                        through="donations.DonationCampaignPointLink",
                        to="collection_points.collectionpoint",
                    ),
                ),
            ],
        ),
    ]
