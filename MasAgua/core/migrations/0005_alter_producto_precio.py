# Generated by Django 5.2.3 on 2025-06-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_producto_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=0, max_digits=6),
        ),
    ]
