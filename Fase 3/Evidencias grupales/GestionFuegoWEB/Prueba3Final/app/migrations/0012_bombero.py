# Generated by Django 5.1.1 on 2024-11-26 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_boleta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bombero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]