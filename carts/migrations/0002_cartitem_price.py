# Generated by Django 4.0.4 on 2023-02-21 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
