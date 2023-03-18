# Generated by Django 3.2.4 on 2023-03-10 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tabla', models.TextField(max_length=150, null=True, unique=True)),
                ('idregistro', models.IntegerField(null=True)),
                ('comando', models.TextField(max_length=80, null=True)),
                ('registronuevo', models.TextField(null=True)),
                ('registroanterior', models.TextField(null=True)),
                ('fechacreacion', models.DateTimeField(null=True)),
                ('usuario', models.ForeignKey(db_column='idusuariocreacion', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_auditoria',
            },
        ),
    ]