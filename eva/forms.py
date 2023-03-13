from django.db.models.lookups import In
from django.forms import *
import os
from conf.models import Rol, RolMoodle
from eva.models import *
from django import forms
from eva.models import Ciclo2
class BaseForm(forms.Form):
    # form_s = '450'
    # form_m = '650'
    # form_l = '850'
    # form_xl = '1024'
    formbase = forms.CharField(widget=forms.HiddenInput(), required=False)
    formtype = forms.CharField(widget=forms.HiddenInput(), required=False)
    formwidth = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    screenwidth = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    labelwidth = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        # ajaxformdinamicbs.html / ajaxformbs.html
        formbase = kwargs.pop('formbase', 'ajaxformbs.html')
        formtype = kwargs.pop('formtype', 'horizontal')
        formwidth = kwargs.pop('formwidth', 850)
        screenwidth = kwargs.pop('screenwidth', 1024)
        labelwidth = kwargs.pop('labelwidth', 160)
        super(BaseForm, self).__init__(*args, **kwargs)
        self.fields['formbase'].initial = formbase
        self.fields['formtype'].initial = formtype
        self.fields['formwidth'].initial = formwidth
        self.fields['screenwidth'].initial = screenwidth
        self.fields['labelwidth'].initial = labelwidth
        if self.form_real_width() < 550:
            self.fields['formtype'].initial = 'vertical'

    def form_base(self):
        return self.fields['formbase'].initial

    def form_width(self):
        return self.fields['formwidth'].initial

    def screenwidth_width(self):
        return self.fields['screenwidth'].initial

    def form_real_width(self):
        if self.screenwidth_width() < self.form_width():
            return self.screenwidth_width()
        return self.form_width()


class ExtFileField(forms.FileField):
    """
    * max_upload_size - a number indicating the maximum file size allowed for upload.
            500Kb - 524288
            1MB - 1048576
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    t = ExtFileField(ext_whitelist=(".pdf", ".txt"), max_upload_size=)
    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]
        self.max_upload_size = kwargs.pop("max_upload_size")
        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        upload = super(ExtFileField, self).clean(*args, **kwargs)
        if upload:
            size = upload.size
            filename = upload.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if size == 0 or ext not in self.ext_whitelist or size > self.max_upload_size:
                raise forms.ValidationError("Tipo de fichero o tamaño no permitido!")


class PeriodoForm(BaseForm):
    carrera = forms.ModelChoiceField(label=u"Carrera", queryset=Carrera.objects, required=False, widget=forms.Select())
    name = forms.CharField(label=u"Nombre", max_length=200, required=False, widget=forms.TextInput())
    ciclo_activo = forms.BooleanField(label=u'Activo', required=False)


class DocenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Seleccione un usuario '
        self.fields['user'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'identificacion', 'roles', 'rol_moodle', 'moodle_user']

        labels = {
            'user': 'Usuario',
            'title': 'Titulo',
            'type_contract': 'Tipo de Contrato',
            'dedication': 'Dedicación',
            'position': 'Cargo',
            'is_evaluator': 'Es Evaluador'
        }

        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo Profesional'}),
            'type_contract': Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Contrato'}),
            'dedication': Select(attrs={'class': 'form-control', 'placeholder': 'Tiempo de dedicación'}),
            'position': Select(attrs={'class': 'form-control', 'placeholder': 'Cargo del docente'}),
            'is_evaluator': CheckboxInput(attrs={'class': 'form-check-radio'})
        }


class MateriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rol = Rol.objects.filter(descripcion='Docente').first()
        self.fields['teacher'].empty_label = 'Seleccione un docente'
        self.fields['teacher'].queryset = Usuario.objects.filter(roles=rol.id, rol_moodle__codigo__gte=5)
        self.fields['area'].empty_label = 'Seleccione una área de conocimiento'
        self.fields['area'].widget.attrs['autofocus'] = True

    class Meta:
        model = Materia
        fields = ['area', 'teacher', 'name']

        labels = {
            'area': 'Área',
            'teacher': 'Docente',
            'name': 'Nombre Materia',
        }

        widgets = {
            'area': Select(attrs={'class': 'form-select select2-templating'}),
            'teacher': Select(attrs={'class': 'form-select select2-templating'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'}),
            'ciclo': forms.HiddenInput()
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
            'carrera': Select(attrs={'class': 'form-control select2'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del ciclo ejemplo: C1-2021'}),
            'ciclo_activo': CheckboxInput(attrs={'class': 'form-check-input'})
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


class CicloFormCN(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ciclo2
        fields = '__all__'

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del ciclo ejemplo: C1-2021'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'})
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
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoria'}),
            'ciclo_id': forms.HiddenInput()

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
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Defina aquí el tipo'})
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

        labels = {
            'category': 'Categoria',
            'title': 'Título',
            'description': 'Descripción',
            'type': 'Tipo'
        }

        widgets = {
            'category': Select(attrs={'class': 'form-select'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Aquí un título para la pregunta'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la pregunta'}),
            'type': Select(attrs={'class': 'form-control select2'}),
            'ciclo': forms.HiddenInput()
        }


class PreguntaAutoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['pregunta'] = forms.ModelMultipleChoiceField(queryset=Pregunta.objects.filter(type=1), widget=forms.CheckboxSelectMultiple)
        #self.fields['pregunta'].queryset = Pregunta.objects.filter(type=1)

    class Meta:
        model = PreguntaCiclo
        fields = '__all__'

        #labels = {
        #    'pregunta': 'Preguntas'
        #}

        widgets = {
            'pregunta': forms.CheckboxSelectMultiple(),
            #'pregunta': Select(attrs={'class': 'form-select select2'}),
            'ciclo': forms.HiddenInput()
        }


class PreguntaCoeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['pregunta'] = forms.ModelMultipleChoiceField(queryset=Pregunta.objects.filter(type=2), widget=forms.CheckboxSelectMultiple)
        #self.fields['pregunta'].queryset = Pregunta.objects.filter(type=1)

    class Meta:
        model = PreguntaCiclo
        fields = '__all__'

        #labels = {
        #    'pregunta': 'Preguntas'
        #}

        widgets = {
            'pregunta': forms.CheckboxSelectMultiple(),
            #'pregunta': Select(attrs={'class': 'form-select select2'}),
            'ciclo': forms.HiddenInput()
        }


class AreasConocimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        co_evaluators = []
        super().__init__(*args, **kwargs)
        rol = Rol.objects.filter(descripcion='Coevaluador').first()
        rol_ml = RolMoodle.objects.filter(descripcion='Docentes').first()
        self.fields['docente'].queryset = Usuario.objects.filter(roles=rol.id, rol_moodle__codigo__gte=rol_ml.codigo)
        self.fields['career'].empty_label = 'Seleccione una carrera'
        self.fields['docente'].empty_label = 'Seleccione una docente'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = AreasConocimiento
        fields = '__all__'
        

        labels = {'name': 'Nombre', 'career': 'Carrera', 'docente': 'Docente', 'materia': 'Materia'}

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Aquí nombre del área de conocimiento'}),
            'career': Select(attrs={'class': 'form-select select2'}),
            'docente': Select(attrs={'class': 'form-select select2'}),
            'id_ciclo': forms.HiddenInput()
        }

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class ParametroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Parametro
        fields = '__all__'

        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del parámetro'})
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
            'code': 'Código',
            'value': 'Valor',
        }

        widgets = {
            'parameter': Select(attrs={'class': 'form-select'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del parámetro'}),
            'value': NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
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


class CoevaluacionForm(ModelForm):
    class Meta:
        model = Pregunta #Cambio referencial rquinto
        fields = ['id']


class AutoEvaluacionForm(ModelForm):
    class Meta:
        model = Pregunta#Cambio referencial rquinto
        fields = ['id']


class ResultadoProcesoForm(ModelForm):
    class Meta:
        model = ResultadoProceso
        fields = ['coevaluator', 'coe_result_Tic', 'coe_result_Did', 'coe_result_Ped', 'Total_Proceso_Coe', 'Total_Proceso']