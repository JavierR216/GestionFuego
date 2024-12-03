# Generated by Django 5.1.1 on 2024-11-21 21:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_vehiculo_repuesto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_vehiculo', models.CharField(max_length=50)),
                ('patente', models.CharField(max_length=200)),
                ('fecha_llegada', models.DateTimeField(default=django.utils.timezone.now)),
                ('reparacion', models.CharField(max_length=100)),
                ('precio_repuestos', models.IntegerField(default=0)),
                ('monto_mecanico', models.IntegerField(default=0)),
                ('monto_total', models.IntegerField(default=0)),
                ('mecanico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.mecanico')),
                ('repuesto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.inventario')),
            ],
        ),
    ]