# Generated by Django 5.1.1 on 2024-10-25 05:51

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('stock', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Mecanico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('monto_mecanico', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('patente', models.CharField(max_length=200)),
                ('marca', models.CharField(max_length=200)),
                ('modelo', models.CharField(max_length=200)),
                ('fecha_llegada', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fecha_salida', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_vehiculo', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('esperando', 'Esperando'), ('completado', 'Completado'), ('mantenimiento', 'Mantenimiento')], default='esperando', max_length=20)),
                ('reparacion', models.CharField(max_length=100)),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_mecanico', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('mecanico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.mecanico')),
            ],
        ),
    ]
