from django.db import models
from django.forms import model_to_dict

from authentication.models import Usuario
from conf.models import Carrera

class Periodo(models.Model):    
    fecha_inicial = models.DateTimeField(auto_now_add=True, db_column='fecha_inicial',
                                        help_text='Registra la fecha de creación de un valor')
    fecha_final = models.DateTimeField(auto_now=True, db_column='fecha_final',
                                       help_text='Fecha final del registro')
    nombre = models.CharField(max_length=100, unique=True, db_column='nombre')    
    carrera_id = models.IntegerField(db_column='periodo_id', null=False, blank=False)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = "periodo"

# Migración
class Ciclo(models.Model):
    carrera = models.ForeignKey(Carrera, db_column=u'carrera',  on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_column='nombre')
    is_active = models.BooleanField(default=False, db_column='es_activo')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')
    periodo = models.ForeignKey(Periodo, db_column='periodo_id', on_delete=models.CASCADE)    

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "pt_ciclo"



class Ciclo2(models.Model):
    is_active = models.BooleanField(default=True, db_column='activo')
    date_created = models.DateTimeField(auto_now_add=True, db_column='created_at',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='update_at',
                                       help_text='Fecha de edición del registro')
    nombre = models.CharField(max_length=100,  db_column='nombre')
    identificador = models.CharField(max_length=100, default='', db_column='identificador')
    periodo = models.ForeignKey(Ciclo, db_column='periodo_id', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre) + " " + str(self.periodo.name) + " (" + str(self.periodo.carrera.descripcion) + ")"

    class Meta:
        db_table = "ciclo"

# Migración
class AreasConocimiento(models.Model):
    name = models.CharField(max_length=255, db_column='nombre', unique=True)
    career = models.ForeignKey(Carrera, null=False, blank=False, on_delete=models.CASCADE, db_column='carrera')
    docente = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
    id_ciclo = models.ForeignKey(Ciclo2, db_column='id_ciclo', null=False, blank=False, on_delete=models.CASCADE)
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


# Migración
class Materia(models.Model):
    area = models.ForeignKey(AreasConocimiento, db_column='area', null=False, blank=False, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Usuario, db_column='id_docente', null=False, blank=False, on_delete=models.CASCADE)
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

    def esta_asignadaesta_asignada(self):
        return self.materiaciclo_set.exists()


# Migración
class MateriaCiclo(models.Model):
    materia = models.ForeignKey(Materia, db_column='materia_id', null=False, blank=False, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo2, on_delete=models.CASCADE,null=False, blank=False, default=1)
    date_created = models.DateTimeField(auto_now_add=True, db_column='create_at',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='update_at',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        return self.materia.name

    class Meta:
        db_table = "materia_ciclo"


# Migración
class MateriaDocente(models.Model):
    matter = models.ForeignKey(Materia, null=False, blank=False, on_delete=models.CASCADE, db_column='materia_ciclo_id')
    docente = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, db_column='tutor')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        txt = "{0} asignada al docente {1}"
        return txt.format(self.matter.name, self.docente.user.nombres)

    class Meta:
        db_table = 'pt_materia_docente'





# Desarrollo Nuevo FCI-016
class Categoria(models.Model):
    name = models.CharField(max_length=100, unique=True, db_column='nombre')
    state = models.BooleanField(default=True, db_column='estado')
    #ciclo_id = models.IntegerField(db_column='ciclo_id', null=False, blank=False)
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

    def tiene_pregutna(self):
        return self.pregunta_set.exists()


# Desarrollo Nuevo FCI-016
class Tipo(models.Model):
    name = models.CharField(max_length=60, unique=True, db_column='nombre')
    state = models.BooleanField(default=True, db_column='estado')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación del tipo de Evaluación')
    date_update = models.DateTimeField(auto_now=True, db_column='fecha_edicion',
                                       help_text='Fecha de edición del registro')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pt_tipo"


# Desarrollo Nuevo FCI-016
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


# Desarrollo Nuevo FCI-016
class ParametrosGeneral(models.Model):
    parameter = models.ForeignKey(Parametro, null=False, blank=False, on_delete=models.CASCADE,
                                  verbose_name='parametro_id')
    code = models.CharField(max_length=5, null=False, blank=False, unique=True, db_column='codigo')
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='valor')
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
    state = models.BooleanField(default=True, db_column='estado')
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

    def en_uso(self):
        return self.preguntaciclo_set.exists()


class PreguntaCiclo(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo2, on_delete=models.CASCADE)

    def __str__(self):
        txt = "{0} "
        return txt.format(self.pregunta.title)

    def to_json(self):
        item = model_to_dict(self, exclude=['date_created', 'date_update'])
        return item

    class Meta:
        db_table = "pt_preguntaciclo"
        ordering = ['-id']


# Migración
class Respuesta(models.Model):
    teacher = models.IntegerField(db_column='docente', null=False, blank=False)
    cycle = models.IntegerField(db_column='ciclo', null=False, blank=False)
    type_evaluation = models.IntegerField(db_column='typo_evaluacion')
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_respuesta"


# Desarrollo Nuevo FCI-016
class DetalleRespuesta(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    category = models.IntegerField(db_column='categoria', null=False, blank=False)
    question = models.IntegerField(db_column='pregunta', null=False, blank=False)
    parameter = models.IntegerField(db_column='indicador', null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion',
                                        help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_detalle_respuesta"


# Desarrollo Nuevo FCI-016
class ResultadoProceso(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    cycle = models.IntegerField(null=False, blank=False, db_column='ciclo')
    user = models.IntegerField(null=False, blank=False, db_column='docente')
    coevaluator = models.CharField(max_length=10, null=True, blank=True, db_column='coevaluador')
    auto_result_Tic = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    auto_result_Did = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    auto_result_Ped = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso_Auto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Tic = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Did = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Ped = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso_Coe = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date_created = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True,
                                        help_text='Registra la fecha de creación de un valor')
    updated_at = models.DateTimeField(db_column='fecha_edicion', auto_now=True,
                                      help_text='Registra la fecha de creación de un valor')

    class Meta:
        db_table = "pt_resultado_proceso"


class ResultadoProcesoModel():
    def __init__(self, resultadoProceso, cycle):
        self.resultadoProceso = resultadoProceso
        self.cycle = cycle

    def __repr__(self):
        return f'<ResultadoProcesoModel: {self.resultadoProceso}>'


class Courses(models.Model):
    idMoodle = models.IntegerField(db_column='id_moodle')
    sortName = models.CharField(max_length=150, db_column='nombre_corto')
    fullName = models.CharField(max_length=150, db_column='nombre_completo')
    categoryName = models.CharField(max_length=150, db_column='categoria')
    image = models.ImageField(upload_to='images/eva/', max_length=300, db_column='imagen', default='')
    startDate = models.DateTimeField(db_column='fecha_inicio')
    date_created = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True,
                                        help_text='Registra la fecha de creación de un valor')

    def __str__(self):
        return self.sortName

    class Meta:
        db_table = 'pt_curso'
