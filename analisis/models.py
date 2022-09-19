from django.db import models
from eva.models import * 
from analisis.models import *

#Modelo para los nivel de kirkpatrick
class Nivel(models.Model):
    ciclo = models.ForeignKey(
            Ciclo,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='ciclo_relacionada'
        )
    nivel = models.CharField(
            max_length=250, 
            unique=True, 
            db_column='nombre'
        )
    date_created = models.DateTimeField(
            auto_now_add=True, 
            db_column='fecha_creacion', 
            help_text='Registra la fecha de creación'
        )
    date_update = models.DateTimeField(
            auto_now=True, 
            db_column='fecha_edicion', 
            help_text='Fecha de edición'
        )

    def __str__(self):
        return self.nivel

    class Meta:
        db_table = "nivel"


#Modelo para las preguntas de Reconocimeinto
class AnalisisPregunta(models.Model):
    nivel = models.ForeignKey(
            Nivel,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='nivel_relacionada'
        )
    pregunta =  models.CharField(
            max_length=250,
            db_column='respuesta'
        )
    ciclo = models.ForeignKey(
            Ciclo,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='ciclo_relacionada_ciclo'
        )
    date_created = models.DateTimeField(
            db_column='fecha_creacion', 
            auto_now_add=True, 
            help_text='Registra la fecha de creación'
        )
    date_update = models.DateTimeField(
            db_column='fecha_edicion', 
            auto_now=True, 
            help_text='Fecha de edición'
        )
                                       
    def __str__(self):
        return self.pregunta

    class Meta:
        db_table = "analisis_pregunta"


#Modelo de las respuestas
class AnalisisRespuestas(models.Model):
    pregunta = models.ForeignKey(
            AnalisisPregunta,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='pregunta_relacionada'
        )
    respuesta = models.CharField(
            max_length=250, 
            db_column='respuesta'
        )
    username = models.IntegerField(
            default=0
        )
    email = models.CharField(
            max_length=250, 
            db_column='email'
        )
    nombres = models.CharField(
            max_length=250, 
            db_column='nombres'
        )
    apellidos = models.CharField(
            max_length=250, 
            db_column='apellidos'
        )
    nivel = models.CharField(
            max_length=250, 
            db_column='nivel'
        )
    ciclo = models.CharField(
            max_length=250, 
            db_column='ciclo'
        )
    date_created = models.DateTimeField(
            db_column='fecha_creacion', 
            auto_now_add=True, 
            help_text='Registra la fecha de creación'
        )
    date_update = models.DateTimeField(
            db_column='fecha_edicion', 
            auto_now=True, 
            help_text='Fecha de edición'
        )
                                       
    def __str__(self):
        return self.analisis_respuestas

    class Meta:
        db_table = "analisis_respuestas"