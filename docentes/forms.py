from django.forms import ModelForm, TextInput
from docentes.models import *
from django.shortcuts import get_object_or_404


class ConfPreguntasForm(ModelForm):
    class Meta:
        model = ConfPreguntas
        fields = '__all__'
        labels = {
            'pregunta': 'Pregunta:',
        }
        widgets = {
            'pregunta': TextInput(attrs={'class': 'form-control', 'placeHolder': 'Ingrese una pregunta'}),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
