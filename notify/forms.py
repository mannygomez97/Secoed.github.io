from authentication.models import Post
from django.forms import ModelForm, TextInput, DateInput

import datetime

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        labels = {
            'title': 'Titulo:',
            'image': 'Imagen:',
            'text': 'Descripción:',
            'timestamp': 'Fecha de publicación:',
            'url': 'Link adicional:',
        }
        widgets = {
            'url': TextInput(attrs={'class': 'form-control'}),
            'text': TextInput(attrs={'class': 'form-control'}),
            'timestamp': DateInput(format='%d/%m/%Y %H:%M:%S'),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
