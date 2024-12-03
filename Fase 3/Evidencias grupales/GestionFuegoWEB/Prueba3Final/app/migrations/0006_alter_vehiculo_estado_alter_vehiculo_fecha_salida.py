# Generated by Django 5.1.1 on 2024-11-13 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_inventario_precio_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='estado',
            field=models.CharField(choices=[('esperando', 'Esperando'), ('completado', 'Completado'), ('mantenimiento', 'Mantenimiento')], db_index=True, default='esperando', max_length=20),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='fecha_salida',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
