from dataclasses import field, fields
from email.policy import default
from django.forms import ModelForm, TextInput, Select, ModelChoiceField, DateInput
from authentication.models import Usuario, RolUser
from conf.models import Modulo, Menu, Icono
from eva.models import Ciclo2
from cursos.models import CoursesMoodle
from conf.models import Carrera
from .models import CourseAsesor, CourseCicleCarrer
from django import forms
from asesor.views import getAsesorLogin

ICONOS = Icono.objects.order_by('descripcion')
MODULOS = Modulo.objects.order_by('descripcion')

COURSES = CoursesMoodle.objects.order_by('fullname')
PERIODS = Ciclo2.objects.order_by()
CARRERS = Carrera.objects.order_by('descripcion')
ASESORS = RolUser.objects.filter(rol_id = 4)

class CriterioForm(forms.Form):
    Nivel_CHOICES = (
         ('1','Nivel 1'),
         ('2','Nivel 2'),
         ('3', 'Nivel 3'),
         ('4', 'Nivel 4')
     )

    semaforo_CHOICES = (
        ('1', 'Rojo'),
        ('2', 'Amarillo'),
        ('3', 'Verde'),
        ('4', 'Azul')
    )

    # id = forms.IntegerField(required = False)
    nivel = forms.ChoiceField(choices=Nivel_CHOICES)
    criterio = forms.CharField(label='Criterio', max_length=200)
    semaforo = forms.ChoiceField(choices=semaforo_CHOICES)

class CourseCicleCarrerForm(forms.ModelForm):
    carrer = forms.ModelChoiceField(queryset=Carrera.objects.filter(facultad = 1), label='Carrera', empty_label='Carreras de FCMF')
    cicle = forms.ModelChoiceField(queryset=Ciclo2.objects.filter(is_active = True), label='Ciclo', empty_label='Ciclos disponibles')
    course = forms.ModelChoiceField(queryset=CoursesMoodle.objects.filter(status = False), label='Cursos', empty_label='Cursos disponibles')

    class Meta:
        model = CourseCicleCarrer
        exclude = ['status']
        

class CourseAsesorForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=CourseCicleCarrer.objects.filter(assigned = False), label='Cursos', empty_label='Cursos disponibles')
    asesor = forms.ModelChoiceField(queryset=Usuario.objects.filter(roluser__rol = 4), label='Asesor', empty_label='Asesores disponibles')

    class Meta:
        model = CourseAsesor
        fields = '__all__'

class CourseAsesorEditForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=CourseCicleCarrer.objects.all(), label='Cursos', empty_label='Cursos disponibles')
    asesor = forms.ModelChoiceField(queryset=Usuario.objects.filter(roluser__rol = 4), label='Asesor', empty_label='Asesores disponibles')

    class Meta:
        model = CourseAsesor
        fields = '__all__'