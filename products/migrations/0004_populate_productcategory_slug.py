# Generated by Django 4.2.11 on 2024-06-08 07:44

from django.db import migrations

from ..utils import slugify

def gen_productcategory_slug(apps, schema_editor):
    model = apps.get_model("products", "ProductCategory")

    for row in model.objects.all():
        row.slug = slugify(row.name)
        row.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productcategory_slug'),
    ]

    operations = [
        migrations.RunPython(gen_productcategory_slug, 
                             reverse_code=migrations.RunPython.noop),
    ]