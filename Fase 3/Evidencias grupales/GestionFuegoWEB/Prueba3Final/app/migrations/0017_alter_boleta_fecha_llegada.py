# Generated by Django 5.1.3 on 2024-12-02 02:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_solicitudbombero_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleta',
            name='fecha_llegada',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
