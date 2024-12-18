# Generated by Django 5.1.4 on 2024-12-12 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('descuento', models.IntegerField()),
                ('esta_activa', models.BooleanField(default=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examen.producto')),
                ('usuarios', models.ManyToManyField(to='examen.usuario')),
            ],
        ),
    ]
