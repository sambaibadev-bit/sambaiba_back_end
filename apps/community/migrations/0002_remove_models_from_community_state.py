"""Remove modelos do estado do app `community` (tabelas permanecem; donos passam a ser os novos apps)."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0001_initial"),
        ("contacts", "0001_initial"),
        ("donations", "0001_initial"),
        ("events", "0001_initial"),
        ("gallery", "0001_initial"),
        ("news", "0001_initial"),
        ("suggestions", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="CommunityEvent"),
                migrations.DeleteModel(name="GalleryItem"),
                migrations.DeleteModel(name="DonationCampaign"),
                migrations.DeleteModel(name="CommunityNews"),
                migrations.DeleteModel(name="CommunitySuggestion"),
                migrations.DeleteModel(name="UsefulContact"),
            ],
        ),
    ]
