from email.policy import default
from django.db import models
from authentication.models import RolUser, Usuario
from modelBase.models import ModelBase
from cursos.models import CoursesMoodle
from eva.models import Ciclo2
from conf.models import Carrera

class AprobacionCurso(models.Model):
    Nivel_CHOICES = (
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
        ('4', 'Nivel 4'),
    )

    Notes_CHOICES = (
        ('1', 25),
        ('2', 50),
        ('3', 75),
        ('4', 100),
    )

    semaforo_CHOICES = (
        ('1', 'Rojo'),
        ('2', 'Amarillo'),
        ('3', 'Verde'),
        ('4', 'Azul')
    )

    nivel = models.IntegerField(choices = Nivel_CHOICES)
    criterio = models.CharField(max_length = 200)
    maxRange = models.IntegerField(choices = Notes_CHOICES, default = 1)
    semaforo = models.IntegerField(choices = semaforo_CHOICES)
    estado = models.BooleanField(default = True)
    
class Evaluation(models.Model):
    course = models.CharField(max_length=100)
    question = models.JSONField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
class CursoAsesores(models.Model):
    id_curso = models.IntegerField()
    id_asesor = models.IntegerField()
    estado = models.BooleanField(default = True)

class CourseCicleCarrer(ModelBase):
    course = models.ForeignKey(CoursesMoodle, on_delete=models.CASCADE,null=False, blank=False, db_column = 'course')
    cicle = models.ForeignKey(Ciclo2, on_delete=models.CASCADE,null=False, blank=False, db_column = 'cicle')
    carrer = models.ForeignKey(Carrera, on_delete=models.CASCADE,null=False, blank=False, db_column = 'carrer')
    assigned = models.BooleanField(default = False)
    evaluated = models.BooleanField(default = False)

    def __str__(self):
        return str(self.course.fullname)+ " " + str(self.cicle.periodo.name) + " " + str(self.cicle.identificador)+" " + str(self.carrer.descripcion)

class CourseAsesor(ModelBase):
    course = models.ForeignKey(CourseCicleCarrer, on_delete=models.CASCADE,null=False, blank=False, db_column = 'course')
    asesor = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=False, blank=False, db_column = 'asesor', related_name='asesor_course_set')

    def __str__(self):
        return str(self.course.course.fullname)+ " " + str(self.asesor)