# Generated by Django 5.1.3 on 2024-12-02 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_boleta_fecha_llegada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boleta',
            name='fecha_llegada',
        ),
    ]