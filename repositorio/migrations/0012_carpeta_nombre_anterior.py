# Generated by Django 3.2.15 on 2022-09-11 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0011_carpeta_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpeta',
            name='nombre_anterior',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
