#from asyncio.windows_events import NULL
from cProfile import label
from datetime import date
from tkinter import Widget
from tkinter.ttk import LabeledScale
from unicodedata import name
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from tkinter import Widget

from django.forms import *
from conf.models import Rol, RolMoodle
from eva.models import *
from repositorio.models import Carpeta
from repositorio.models import Archivo

#from .models import Archivo

class CarpetaForm(ModelForm):

    class Meta:
        model = Carpeta
        fields= ['nombre','descripcion']

        labels = {
            'nombre': 'NOMBRE',
            'descripcion':'DESCRIPCION'
        }

        widgets = {
        'nombre': TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Ingrese nombre'}),
        'descripcion': TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Ingrese descripcion'}),
        }

class ArchivoForm(ModelForm):
    class Meta:
        model = Archivo
        fields = ['carpeta','nombre','archivo','descripcion']

        labels ={
            'carpeta':'Seleccione la carpeta',
            'nombre': 'Nombre',
            'archivo': 'Archivo',
            'descripcion': 'Descripcion',
        }

        widgets = {
        'carpeta': Select(attrs={'class': 'form-control form-select select2 mb-3'}),
        'nombre': TextInput(attrs={'class': 'form-control mb-3 ', 'placeholder': 'Ingrese nombre'}),
        'archivo': FileInput(attrs={'class': 'form-control mb-3'}),
        'descripcion': TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Ingrese descripcion'}),
        }
        exclude = [
            'carpeta',
        ]