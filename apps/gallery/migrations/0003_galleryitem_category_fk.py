import django.db.models.deletion
from django.db import migrations, models


def forwards_fill_gallery_category_tmp(apps, schema_editor):
    GalleryItem = apps.get_model("gallery", "GalleryItem")
    GalleryCategory = apps.get_model("gallery_categories", "GalleryCategory")
    fallback = GalleryCategory.objects.get(slug="cultura")
    for gi in GalleryItem.objects.all():
        raw = (getattr(gi, "category", None) or "").strip().lower()
        slug = raw if raw else "cultura"
        cat = GalleryCategory.objects.filter(slug=slug).first() or fallback
        gi.category_tmp_id = cat.pk
        gi.save(update_fields=["category_tmp_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("gallery_categories", "0001_initial"),
        ("gallery", "0002_alter_galleryitem_options_alter_galleryitem_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryitem",
            name="category_tmp",
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="gallery_items_tmp",
                to="gallery_categories.gallerycategory",
                verbose_name="category",
            ),
        ),
        migrations.RunPython(forwards_fill_gallery_category_tmp, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="galleryitem",
            name="category",
        ),
        migrations.AlterField(
            model_name="galleryitem",
            name="category_tmp",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="gallery_items",
                to="gallery_categories.gallerycategory",
                verbose_name="category",
            ),
        ),
        migrations.RenameField(
            model_name="galleryitem",
            old_name="category_tmp",
            new_name="category",
        ),
    ]
