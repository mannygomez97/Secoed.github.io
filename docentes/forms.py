from django.forms import ModelForm, TextInput, NumberInput
from django.shortcuts import get_object_or_404
from docentes.models import *
from datetime import datetime

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        labels = {
            'categoria': 'Categoria:'
        }
        widgets = {
            'categoria': TextInput(attrs={'class': 'form-control', 'placeHolder': 'Ingrese una categoria'}),
        }

class ConfPreguntasForm(ModelForm):
    class Meta:
        model = ConfPreguntas
        fields = '__all__'
        labels = {
            'pregunta': 'Pregunta:',
            'periodo': 'Período:',
            'categoria': 'Categoria:'
        }
        widgets = {
            'pregunta': TextInput(attrs={'class': 'form-control', 'placeHolder': 'Ingrese una pregunta'}),
            'periodo': NumberInput(attrs={'class': 'form-control', 'placeHolder': 'Ingrese un periodo'}),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            ahora = datetime.now()  # Obtiene fecha y hora actual
            self.fields['periodo'].initial = ahora.year

class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)