# Generated by Django 5.2.3 on 2025-06-15 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='nombre',
            field=models.CharField(default='Producto sin nombre', max_length=50, verbose_name='Nombre del Producto'),
            preserve_default=False,
        ),
    ]
