# Generated by Django 3.2.15 on 2022-08-19 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0003_auto_20220818_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpeta',
            name='fechacreacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='carpeta',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
    ]