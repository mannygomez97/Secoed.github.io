# Generated by Django 3.2.4 on 2022-09-18 20:03

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('eva', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('Tabla', models.CharField(db_column='tabla', max_length=150)),
                ('Comando', models.CharField(db_column='comando', max_length=80)),
                ('RegistroNuevo', models.CharField(db_column='registroNuevo')),
                ('RegistroAnterior', models.CharField(db_column='registroAnterior')),
                ('IdUsuarioCreacion', models.CharField(db_column='idUsuarioCreacion')),
                ('FechaCreacion', models.DateTimeField(db_column='fechaCreacion')),
            ],
            options={
                'db_table': 'TB_AUDITORIA',
            },
        ),
    ]