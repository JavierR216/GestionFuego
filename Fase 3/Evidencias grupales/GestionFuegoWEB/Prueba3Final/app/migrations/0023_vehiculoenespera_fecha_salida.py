# Generated by Django 5.1.1 on 2024-12-03 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_vehiculoenespera_fecha_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculoenespera',
            name='fecha_salida',
            field=models.DateField(default='2024-12-02'),
            preserve_default=False,
        ),
    ]