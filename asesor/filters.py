from cProfile import label
from email.policy import default
import django_filters
from .models import *
from cursos.models import CoursesMoodle
from eva.models import Ciclo2
from conf.models import Carrera
from components.models import CourseCicleCarrer
from authentication.models import Usuario


class valorationCourseStudentFilter(django_filters.FilterSet):
    scoreCourse = django_filters.NumberFilter()
    scoreCourse__gt = django_filters.NumberFilter(field_name='scoreCourse', lookup_expr='gt', label='Nota sea mayor a:')
    scoreCourse__lt = django_filters.NumberFilter(field_name='scoreCourse', lookup_expr='lt',label='Nota sea menor que:')

    studentName  = django_filters.CharFilter(lookup_expr='icontains', label='Nombre del docente')  
    course = django_filters.ModelChoiceFilter(queryset=CoursesMoodle.objects.all(), label='Curso', empty_label='Curso')
    cicle = django_filters.ModelChoiceFilter(queryset=Ciclo2.objects.filter(is_active = True), label='Ciclo', empty_label='Ciclo')
    carrer = django_filters.ModelChoiceFilter(queryset=Carrera.objects.filter(facultad = 1), label='Carrera', empty_label='Carrera')
    class Meta:
        model = ValorationsCourses
        fields = [
            'courseCicleCarrer',
            'course',
            'cicle', 
            'carrer', 
            'studentName',
            'scoreCourse__gt',
            'scoreCourse__lt'
        ]

class valorationToAcademicManagerFilter(django_filters.FilterSet):
    scoreCourse__gt = django_filters.NumberFilter(field_name='scoreCourse', lookup_expr='gt', label='Nota sea mayor a:')
    scoreCourse__lt = django_filters.NumberFilter(field_name='scoreCourse', lookup_expr='lt', label='Nota sea menor que:')
    
    studentName  = django_filters.CharFilter(lookup_expr='icontains', label='Nombre del docente')  
    course = django_filters.ModelChoiceFilter(queryset=CoursesMoodle.objects.all(), label='Curso', empty_label='Curso')
    cicle = django_filters.ModelChoiceFilter(queryset=Ciclo2.objects.filter(is_active = True), label='Ciclo', empty_label='Ciclo')
    carrer = django_filters.ModelChoiceFilter(queryset=Carrera.objects.filter(facultad = 1), label='Carrera', empty_label='Carrera')
    asesor = django_filters.ModelChoiceFilter(queryset=Usuario.objects.filter(roluser__rol = 4), label='Asesor', empty_label='Asesores')
    class Meta:
        model = ValorationsCourses
        fields = [
            'courseCicleCarrer',
            'course',
            'cicle', 
            'carrer', 
            'studentName',
            'asesor',
            'scoreCourse__gt',
            'scoreCourse__lt'
        ]
