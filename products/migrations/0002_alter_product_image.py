# Generated by Django 4.2.11 on 2024-05-21 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=256, null=True, upload_to='products_images'),
        ),
    ]
