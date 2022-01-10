from django.db import models



class ConfPreguntas(models.Model):
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(null=True)
    periodo = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.pregunta}'

    class Meta:
        db_table = 'doc_conf_pregunta'

class Evaluacion(models.Model):
    id = models.AutoField(primary_key=True)
    pregunta = models.ForeignKey(ConfPreguntas, on_delete=models.SET_NULL, null=True)
    opcion = models.IntegerField(blank=True, null=True)
    usuario = models.TextField(null=True)
    contestado = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.pregunta.pregunta}'

    class Meta:
        db_table = 'doc_evaluacion'