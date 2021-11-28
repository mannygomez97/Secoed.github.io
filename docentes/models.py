from django.db import models

# Create your models here.

class ConfPreguntas(models.Model):
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(null=True)

    def __str__(self):
        return f'{self.pregunta}'

    class Meta:
        db_table = 'docentes_conf_pregunta'
