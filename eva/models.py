from django.db import models
from django.forms import model_to_dict

from authentication.models import Usuario
from conf.models import Carrera
from eva.choices import contract, dedication, position


class Docente(models.Model):
    user = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, db_column='id_usuario')
    title = models.CharField(max_length=100, null=True, blank=True, db_column='titulo')
    type_contract = models.CharField(max_length=100, choices=contract, null=True, blank=True, db_column='tipo_contrato')
    dedication = models.CharField(max_length=100, choices=dedication, null=True, blank=True, db_column='dedicacion')
    position = models.CharField(max_length=100, choices=position, null=True, blank=True, db_column='cargo')
    is_evaluator = models.BooleanField(default=False, db_column='es_evaluador')

    class Meta:
        db_table = 'pt_usuario'


class AreasConocimiento(models.Model):
    name = models.CharField(max_length=255, db_column='nombre', unique=True)
    career = models.ForeignKey(Carrera, null=False, blank=False, on_delete=models.CASCADE, db_column='carrera')
    docente = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_area_conocimiento"
        ordering = ['name']


class Materia(models.Model):
    area = models.ForeignKey(AreasConocimiento, db_column='area', null=False, blank=False, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Docente, db_column='id_docente', null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_column='nombre', unique=True)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_materia"


class MateriaDocente(models.Model):
    matter = models.ForeignKey(Materia, null=False, blank=False, on_delete=models.CASCADE, db_column='materia')
    docente = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE, db_column='tutor')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} asignada al docente {1}"
        return txt.format(self.matter.name, self.docente.user.nombres)

    class Meta:
        db_table = 'pt_materia_docente'


class Ciclo(models.Model):
    name = models.CharField(max_length=100, unique=True, db_column='nombre')
    is_active = models.BooleanField(default=False, db_column='es_activo')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_ciclo"


class Categoria(models.Model):
    name = models.CharField(max_length=100, unique=True, db_column='nombre')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    def to_json(self):
        item = model_to_dict(self, exclude=['date_created', 'date_update'])
        return item

    class Meta:
        db_table = "pt_categoria"


class Tipo(models.Model):
    name = models.CharField(max_length=60, unique=True, db_column='nombre')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación del tipo de Evaluación')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pt_tipo"


class Comprobacion(models.Model):
    co_evaluated = models.IntegerField(db_column='evaluador', null=True, blank=True)
    identify = models.CharField(max_length=13, db_column='evaluado', null=True, blank=True)
    state = models.BooleanField(default=False, db_column='estado', null=False)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_comprobacion"

    def to_json(self):
        item = model_to_dict(self, exclude=['date_created', 'date_update'])
        return item


class HistAutoevaluation(models.Model):
    docente = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
    nombre_docente = models.CharField(max_length=60)
    apellido_docente = models.CharField(max_length=60)
    estado = models.CharField(max_length=20)
    ciclo = models.CharField(max_length=20)
    universidad = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pt_historia_evaluacion"
        ordering = ['ciclo']


class HistCoevaluation(models.Model):
    coevaluador_id = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE)
    nombres_coevaluador = models.CharField(max_length=60)
    apellidos_coevaluador = models.CharField(max_length=60)
    evaluado_id = models.CharField(max_length=10)
    nombres_evaluado = models.CharField(max_length=60)
    apellidos_evaluado = models.CharField(max_length=60)
    estado = models.CharField(max_length=20)
    ciclo = models.CharField(max_length=20)
    universidad = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_historia_coevaluacion"
        ordering = ['ciclo']


class AuditoriaAuto(models.Model):
    user_id = models.IntegerField(db_column='docente')
    tipo = models.CharField(max_length=10)
    ciclo = models.CharField(max_length=10)
    ip = models.CharField(max_length=20)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pt_pistas_auditaria_auto"
        ordering = ['ciclo']


class AuditoriaCoe(models.Model):
    coevaluator = models.CharField(max_length=10, db_column='coevaluador')
    user_id = models.CharField(max_length=10, db_column='identificion')
    type = models.CharField(max_length=10, db_column='tipo')
    cycle = models.CharField(max_length=20, db_column='ciclo')
    date_created = models.DateTimeField(
        'fecha_creacion',
        auto_now_add=True,
        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_pistas_auditaria_coe"


class Parametro(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, unique=True, db_column='nombre')
    description = models.CharField(max_length=100, null=False, blank=False, unique=True, db_column='Descripcion')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_parametro"
        ordering = ['name']


class ParametrosGeneral(models.Model):
    parameter = models.ForeignKey(Parametro, null=False, blank=False, on_delete=models.CASCADE,
                                  verbose_name='parametro_id')
    code = models.CharField(max_length=5, null=False, blank=False, unique=True, db_column='codigo')
    value = models.DecimalField(max_digits=4, decimal_places=2, default=0, db_column='valor')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.code)

    class Meta:
        db_table = "pt_parametro_general"


class Pregunta(models.Model):
    title = models.CharField(max_length=1000, db_column='titulo', help_text='registra el titulo de la pregunta')
    description = models.CharField(db_column='description', max_length=255,
                                   help_text='registra la descripción de la pregunta')
    category = models.ForeignKey(Categoria, db_column='categoria', null=False, blank=False, on_delete=models.CASCADE)
    type = models.ForeignKey(Tipo, db_column='tipo', null=False, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True,
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(db_column='fecha_edicion', auto_now=True,
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.title)

    def to_json(self):
        item = model_to_dict(self, exclude=['date_created', 'date_update'])
        return item

    class Meta:
        db_table = "pt_pregunta"
        ordering = ['title']


class Respuesta(models.Model):
    teacher = models.IntegerField(db_column='docente', null=False, blank=False)
    cycle = models.IntegerField(db_column='ciclo', null=False, blank=False)
    type_evaluation = models.IntegerField(db_column='typo_evaluacion')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_respuesta"


class DetalleRespuesta(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    category = models.IntegerField(db_column='categoria', null=False, blank=False)
    question = models.IntegerField(db_column='pregunta', null=False, blank=False)
    parameter = models.IntegerField(db_column='indicador', null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_detalle_respuesta"


class ResultadoProceso(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    cycle = models.IntegerField(null=False, blank=False, db_column='ciclo')
    user = models.IntegerField(null=False, blank=False, db_column='docente')
    coevaluator = models.CharField(max_length=10, null=True, blank=True, db_column='coevaluador')
    auto_result_Tic = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    auto_result_Did = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    auto_result_Ped = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    Total_Proceso_Auto = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    coe_result_Tic = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    coe_result_Did = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    coe_result_Ped = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    Total_Proceso_Coe = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    Total_Proceso = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    date_created = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True,
                                        help_text='Registra la fecha de creación de un valor')
    updated_at = models.DateTimeField(db_column='fecha_edicion', auto_now=True,
                                      help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_resultado_proceso"
