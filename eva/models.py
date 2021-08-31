from django.contrib.auth.models import PermissionsMixin
from authentication.models import Usuario
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.forms import model_to_dict
from secoed.settings import MEDIA_URL, STATIC_URL


class Docente(models.Model):
    user = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, db_column='id_usuario')
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, db_column='nombre_usuario')
    identify = models.CharField(max_length=13, unique=True, null=True, blank=True, db_column='identificacion')
    address = models.CharField(max_length=255, null=True, blank=True, db_column='direccion')
    image = models.FileField(upload_to='perfil/%Y/%m/%d', max_length=255, blank=True, null=True, db_column='imagen')
    is_evaluator = models.BooleanField(default=False, db_column='es_evaluador')

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def __str__(self):
        txt = '{0} con identificación: {1}'
        return txt.format(self.name, self.identify)

    class Meta:
        db_table = 'pt_usuario'


class Universidad(models.Model):
    name = models.CharField(max_length=100, unique=True, db_column='nombre',
                            help_text='Registra el nombre de la universidad')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_universidad"
        ordering = ['name']
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'


class Facultad(models.Model):
    university = models.ForeignKey(Universidad, db_column='universidad', null=False, blank=False,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_column='nombre', help_text='Registra el nombre de la facultad')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_facultad"
        ordering = ['name']
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'


class Carrera(models.Model):
    schoolOf = models.ForeignKey(Facultad, null=False, blank=False, on_delete=models.CASCADE, db_column='facultad')
    name = models.CharField(max_length=100, db_column='nombre')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_carrera"
        ordering = ['name']
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'


class Materia(models.Model):
    name = models.CharField(max_length=255, db_column='nombre', unique=True)
    career = models.ForeignKey(Carrera, db_column='carrera', null=False, blank=False, on_delete=models.CASCADE)
    docente = models.ManyToManyField(Docente, db_column='materia_usuario')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} "
        return txt.format(self.name)

    class Meta:
        db_table = "pt_materia"
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'


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
        verbose_name = 'Ciclo'
        verbose_name_plural = 'Ciclos'


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
        ordering = ['name']
        verbose_name = 'categoria'
        verbose_name_plural = 'Categorias'


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
        ordering = ['name']
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'


class AreasConocimiento(models.Model):
    name = models.CharField(max_length=255, db_column='nombre', unique=True)
    career = models.ForeignKey(Carrera, null=False, blank=False, on_delete=models.CASCADE, db_column='carrera')
    docente = models.ManyToManyField(Docente, db_column='area_docente')
    materia = models.ManyToManyField(Materia, db_column='area_materia')
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
        verbose_name = 'Areas_Conocimiento'
        verbose_name_plural = 'Areas_Conocimientos'


class Comprobacion(models.Model):
    co_evaluated = models.IntegerField(db_column='evaluador', null=False, blank=False)
    identify = models.CharField(max_length=13, db_column='evaluado', null=True, blank=True)
    state = models.BooleanField(default=False, db_column='estado', null=False)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_comprobacion"
        verbose_name = 'Comprobacion'
        verbose_name_plural = 'Comprobaciones'

    def to_json(self):
        item = model_to_dict(self, exclude=['date_created', 'date_update'])
        return item


class HistAutoevaluation(models.Model):
    User = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
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
        verbose_name = 'Historia Evaluación'
        verbose_name_plural = 'Historias Evaluaciones'


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
        verbose_name = 'Historia Co-Evaluación'
        verbose_name_plural = 'Historias Co-Evaluaciones'


class AuditoriaAuto(models.Model):
    user_id = models.IntegerField(db_column='docente')
    tipo = models.CharField(max_length=10)
    ciclo = models.CharField(max_length=10)
    ip = models.CharField(max_length=20)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pt_pistas_auditaria_auto"
        ordering = ['ciclo']
        verbose_name = 'Auditoria Evaluación'
        verbose_name_plural = 'Auditorias Evaluaciones'


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
        verbose_name = 'Auditoria Co-Evaluación'
        verbose_name_plural = 'Auditorias Co-Evaluaciones'


class ResultadoProceso(models.Model):
    cycle_id = models.ForeignKey(Ciclo, null=False, blank=False, on_delete=models.CASCADE, db_column='ciclo')
    user_id = models.ForeignKey(Docente, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
    coe_id = models.CharField(max_length=10, null=True, blank=True, db_column='coevaluador')
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
        verbose_name = 'Resultado Proceso'
        verbose_name_plural = 'Resultados Procesos'


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
        verbose_name = 'Parametro'
        verbose_name_plural = 'Parametros'


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
        verbose_name = 'Parametro_General'
        verbose_name_plural = 'Parametros_Generales'


class Pregunta(models.Model):
    title = models.CharField(max_length=255, db_column='titulo', help_text='registra el titulo de la pregunta')
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
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'


class Respuesta(models.Model):
    teacher = models.ForeignKey(Docente, db_column='docente', null=False, blank=False, on_delete=models.CASCADE)
    cycle = models.IntegerField(db_column='ciclo', null=False, blank=False)
    auto_evaluated = models.BooleanField(db_column='auto_evaluacion', default=False)
    co_evaluator = models.CharField(max_length=10, db_column='co_evaluador', null=True, blank=True, )
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_respuesta"
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'


class DetalleRespuesta(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    question = models.IntegerField(db_column='pregunta', null=False, blank=False)
    parameter = models.IntegerField(db_column='indicador', null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_detalle_respuesta"
        verbose_name = 'Respuesta Detalle'
