# Generated by Django 4.0.4 on 2022-12-27 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_brand_alter_product_diameter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='diameter',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='height',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='width',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
