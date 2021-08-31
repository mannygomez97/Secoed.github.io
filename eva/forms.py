from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import UserManager, AbstractUser
from django.forms import *
from eva.models import *


class DocenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Seleccione un usuario '
        self.fields['user'].widget.attrs['autofocus'] = True

    class Meta:
        model = Docente
        fields = '__all__'

        labels = {
            'user': 'Usuario',
            'name': 'Nombres',
            'identify': 'Cédula de Identidad',
            'address': 'Dirección',
            'image': 'Foto Perfil',
            'is_evaluator': 'Es Evaluador',
        }

        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del docente'}),
            'identify': TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula de ciudadanía'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección domiciliaría'}),
            'image': TextInput(attrs={'class': 'form-control', 'placeholder': 'Foto de perfil'}),
            'is_evaluator': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UniversidadForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Universidad
        fields = ['name']

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre institución académica'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class FacultadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['university'].empty_label = 'Seleccione un institución académica'
        self.fields['university'].widget.attrs['autofocus'] = True

    class Meta:
        model = Facultad
        fields = ['university', 'name']

        widgets = {
            'university': Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la facultad'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CarreraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['schoolOf'].empty_label = 'Seleccione una facultad'
        self.fields['schoolOf'].widget.attrs['autofocus'] = True

    class Meta:
        model = Carrera
        fields = '__all__'

        widgets = {
            'schoolOf': Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la carrera'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class MateriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['career'].empty_label = 'Seleccione una Carrera'
        self.fields['career'].widget.attrs['autofocus'] = True

    class Meta:
        model = Materia
        fields = ['career', 'name']

        widgets = {
            'career': Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la materia'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CicloForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ciclo
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del ciclo ejemplo: C1-2021'
                }
            ),
            'ciclo_activo': CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la categoria'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TipoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tipo
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Defina aquí el tipo'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PreguntaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pregunta
        fields = '__all__'

        widgets = {
            'category': Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Aquí un título para la pregunta'
                }
            ),
            'description': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción de la pregunta'
                }
            ),
            'type': Select(
                attrs={
                    'class': 'form-control select2',
                }
            )
        }


class AreaConocimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['career'].empty_label = 'Seleccione una carrera'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = AreasConocimiento
        fields = '__all__'

        labels = {
            'name': 'Nombre',
            'career': 'Carrera',
            'docente': 'Docente',
            'materia': 'Materia'
        }

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Aquí nombre del área de conocimiento'
                }
            ),
            'career': Select(
                attrs={
                    'class': 'form-select select2'
                }
            ),
            'materia': SelectMultiple(
                attrs={
                    'class': 'form-select select2-templating'
                }
            ),
            'docente': SelectMultiple(
                attrs={
                    'class': 'form-control select2-templating'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ParametroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Parametro
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción del parámetro'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ParametrosGeneralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parameter'].empty_label = 'Seleccione un parámetro'
        self.fields['parameter'].widget.attrs['autofocus'] = True

    class Meta:
        model = ParametrosGeneral
        fields = '__all__'

        labels = {
            'parameter': 'Parámetro',
            'code': 'Código'
        }

        widgets = {
            'parameter': Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'code': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción del parámetro'
                }
            ),
            'value': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RespuestaForm(ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'
