# Generated by Django 4.2 on 2023-04-24 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_activeproduct_stockitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='UniqueBarcode',
            field=models.TextField(default='1'),
        ),
    ]
