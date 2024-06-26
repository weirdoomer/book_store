# Generated by Django 4.2.11 on 2024-06-14 01:25

from django.db import migrations

from ..utils import slugify

def gen_product_slug(apps, schema_editor):
    model = apps.get_model("products", "Product")

    for row in model.objects.all():
        row.slug = slugify(row.name)
        row.save(update_fields=["slug"])

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_slug'),
    ]

    operations = [
        migrations.RunPython(gen_product_slug, 
                             reverse_code=migrations.RunPython.noop),
    ]
