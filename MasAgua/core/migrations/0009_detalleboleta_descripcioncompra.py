# Generated by Django 5.2.3 on 2025-07-14 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_tipoagua_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleboleta',
            name='descripcionCompra',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
