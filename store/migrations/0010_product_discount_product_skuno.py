# Generated by Django 4.0.4 on 2023-01-03 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_terrain'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='skuno',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]