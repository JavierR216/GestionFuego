# Generated by Django 5.1.1 on 2024-11-20 21:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_inventario_precio_alter_vehiculo_monto_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiculoenespera',
            old_name='fecha_solicitud',
            new_name='fecha_llegada',
        ),
        migrations.RemoveField(
            model_name='vehiculoenespera',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='vehiculoenespera',
            name='fecha_estimacion',
        ),
        migrations.RemoveField(
            model_name='vehiculoenespera',
            name='repuestos',
        ),
        migrations.RemoveField(
            model_name='vehiculoenespera',
            name='vehiculo',
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='Reparación',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='Repuesto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.inventario'),
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='mecanico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.mecanico'),
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='monto_mecanico',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='monto_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='patente',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiculoenespera',
            name='tipo_vehiculo',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
