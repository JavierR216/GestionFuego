# Generated by Django 5.1.1 on 2024-11-13 08:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_inventario_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='precio',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_vehiculo', models.CharField(choices=[('Carro Bomba', 'Carro Bomba'), ('Carro Escala', 'Carro Escala'), ('Carro Aljibe', 'Carro Aljibe'), ('Carro de Rescate', 'Carro de Rescate'), ('Carro Forestal', 'Carro Forestal'), ('Carro HazMat', 'Carro HazMat'), ('Unidad de Rescate', 'Unidad de Rescate'), ('Ambulancia de Bomberos', 'Ambulancia de Bomberos'), ('Carro QR', 'Carro QR')], max_length=50)),
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
