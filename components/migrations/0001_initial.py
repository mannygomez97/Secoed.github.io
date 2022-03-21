# Generated by Django 3.1.13 on 2021-12-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AprobacionCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.IntegerField(choices=[('1', 'Nivel 1'), ('2', 'Nivel 2'), ('3', 'Nivel 3'), ('4', 'Nivel 4')])),
                ('criterio', models.CharField(max_length=200)),
                ('semaforo', models.IntegerField(choices=[('1', 'Rojo'), ('2', 'Amarillo'), ('3', 'Verde'), ('4', 'Azul')])),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CursoAsesores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_curso', models.IntegerField()),
                ('id_asesor', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('question', models.JSONField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]