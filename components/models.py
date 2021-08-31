# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AsesorActividades(models.Model):
    id_actividades = models.AutoField(primary_key=True)
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=10)  # Field name made lowercase.
    calificacion = models.FloatField(db_column='Calificacion')  # Field name made lowercase.
    fecha_de_apertura = models.DateTimeField(db_column='Fecha_de_Apertura')  # Field name made lowercase.
    fecha_fin = models.DateTimeField(db_column='Fecha_fin')  # Field name made lowercase.
    curso_vinculado = models.ForeignKey('AsesorCursos', models.DO_NOTHING,
                                        db_column='Curso_Vinculado_id')  # Field name made lowercase.
    docente_vinculado = models.ForeignKey('AsesorDocentes', models.DO_NOTHING, db_column='Docente_Vinculado_id',
                                          blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_actividades'


class AsesorAsesor(models.Model):
    id_asesor = models.AutoField(primary_key=True)
    nombres = models.CharField(db_column='Nombres', max_length=15)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=16)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=25)  # Field name made lowercase.
    carrera = models.ForeignKey('AsesorCarrera', models.DO_NOTHING,
                                db_column='Carrera_id')  # Field name made lowercase.
    facultad = models.ForeignKey('AsesorFacultad', models.DO_NOTHING,
                                 db_column='Facultad_id')  # Field name made lowercase.
    nivel_académico = models.ForeignKey('AsesorNivelAcadmico', models.DO_NOTHING,
                                        db_column='Nivel_Académico_id')  # Field name made lowercase.
    titulo = models.ForeignKey('AsesorTitulos', models.DO_NOTHING, db_column='Titulo_id')  # Field name made lowercase.
    universidad = models.ForeignKey('AsesorUniversidad', models.DO_NOTHING,
                                    db_column='Universidad_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_asesor'


class AsesorCabeceraCrono(models.Model):
    id_cabecera_crono = models.AutoField(db_column='Id_Cabecera_Crono', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=10)  # Field name made lowercase.
    dia_creación = models.DateTimeField(db_column='Dia_Creación')  # Field name made lowercase.
    periodo = models.ForeignKey('AsesorPeriodo', models.DO_NOTHING,
                                db_column='Periodo_id')  # Field name made lowercase.
    relación = models.ForeignKey('AsesorCursoAsesor', models.DO_NOTHING, db_column='Relación_id', blank=True,
                                 null=True)  # Field name made lowercase.
    tiempo = models.ForeignKey('AsesorRecursos', models.DO_NOTHING, db_column='Tiempo_id')  # Field name made lowercase.
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_cabecera_crono'


class AsesorCarrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    duración = models.IntegerField(db_column='Duraci�n')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    facultad = models.ForeignKey('AsesorFacultad', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asesor_carrera'


class AsesorCursoAsesor(models.Model):
    id_curso_asesor = models.AutoField(primary_key=True)
    relacion = models.CharField(db_column='Relacion', max_length=20)  # Field name made lowercase.
    asesor = models.ForeignKey(AsesorAsesor, models.DO_NOTHING, db_column='Asesor_id')  # Field name made lowercase.
    curso = models.ForeignKey('AsesorCursos', models.DO_NOTHING, db_column='Curso_id')  # Field name made lowercase.

    # estudiante = models.ForeignKey('AsesorDocentes', models.DO_NOTHING, db_column='Estudiante_id')  # Field name made lowercase.
    # asignacion = models.BooleanField(default = True)

    class Meta:
        managed = False
        db_table = 'asesor_curso_asesor'


class AsesorCursos(models.Model):
    id_curso = models.AutoField(db_column='Id_curso', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=15)  # Field name made lowercase.
    fecha_de_apertura = models.DateTimeField(db_column='Fecha_de_Apertura')  # Field name made lowercase.
    fecha_fin = models.DateTimeField(db_column='Fecha_fin')  # Field name made lowercase.
    carrera = models.ForeignKey(AsesorCarrera, models.DO_NOTHING, db_column='Carrera_id')  # Field name made lowercase.
    facultad = models.ForeignKey('AsesorFacultad', models.DO_NOTHING,
                                 db_column='Facultad_id')  # Field name made lowercase.
    universidad = models.ForeignKey('AsesorUniversidad', models.DO_NOTHING,
                                    db_column='Universidad_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_cursos'


class AsesorDocentes(models.Model):
    id_docentes = models.AutoField(primary_key=True)
    nombres = models.CharField(db_column='Nombres', max_length=18)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=18)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=30)  # Field name made lowercase.
    carrera = models.ForeignKey(AsesorCarrera, models.DO_NOTHING, db_column='Carrera_id')  # Field name made lowercase.
    curso = models.ForeignKey(AsesorCursos, models.DO_NOTHING, db_column='Curso_id')  # Field name made lowercase.
    facultad = models.ForeignKey('AsesorFacultad', models.DO_NOTHING,
                                 db_column='Facultad_id')  # Field name made lowercase.
    nivel_académico = models.ForeignKey('AsesorNivelAcadmico', models.DO_NOTHING,
                                        db_column='Nivel_Acad�mico_id')  # Field name made lowercase.
    titulo = models.ForeignKey('AsesorTitulos', models.DO_NOTHING, db_column='Titulo_id')  # Field name made lowercase.
    universidad = models.ForeignKey('AsesorUniversidad', models.DO_NOTHING,
                                    db_column='Universidad_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_docentes'


class AsesorEvent(models.Model):
    title = models.CharField(unique=True, max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField()
    user = models.ForeignKey(AsesorCabeceraCrono, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'asesor_event'


class AsesorFacultad(models.Model):
    id_facultad = models.AutoField(primary_key=True)
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    universidad = models.ForeignKey('AsesorUniversidad', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asesor_facultad'


class AsesorNivelAcadmico(models.Model):
    id_academico = models.AutoField(primary_key=True)
    nivel = models.CharField(db_column='Nivel', max_length=60)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=60)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_nivel_académico'


class AsesorPeriodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    tipo = models.CharField(db_column='Tipo', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_periodo'


class AsesorRecursos(models.Model):
    id_recursos = models.AutoField(primary_key=True)
    tiempo = models.CharField(db_column='Tiempo', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_recursos'


class AsesorTitulos(models.Model):
    id_titulo = models.AutoField(primary_key=True)
    nombramiento = models.CharField(db_column='Nombramiento', max_length=25)  # Field name made lowercase.
    carrera = models.ForeignKey(AsesorCarrera, models.DO_NOTHING, db_column='Carrera_id')  # Field name made lowercase.
    facultad = models.ForeignKey(AsesorFacultad, models.DO_NOTHING,
                                 db_column='Facultad_id')  # Field name made lowercase.
    universidad = models.ForeignKey('AsesorUniversidad', models.DO_NOTHING,
                                    db_column='Universidad_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_titulos'


class AsesorUniversidad(models.Model):
    id_universidad = models.AutoField(primary_key=True)
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    categoria_global = models.CharField(db_column='Categoria_Global', max_length=5)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=7)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asesor_universidad'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ConfMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField()
    orden = models.IntegerField()
    href = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    modulo = models.ForeignKey('ConfModulo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conf_menu'


class ConfModulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField()
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conf_modulo'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PtAreaConocimientos(models.Model):
    id = models.BigAutoField(primary_key=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    universidad = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_area_conocimientos'


class PtAreaHasMaterias(models.Model):
    id = models.BigAutoField(primary_key=True)
    area = models.ForeignKey(PtAreaConocimientos, models.DO_NOTHING, blank=True, null=True)
    materia = models.ForeignKey('PtMaterias', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_area_has_materias'


class PtAreaUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    area_conocimiento = models.ForeignKey(PtAreaConocimientos, models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('PtUsers', models.DO_NOTHING, db_column='usuario', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_area_users'


class PtCarreras(models.Model):
    id = models.BigAutoField(primary_key=True)
    facultad = models.ForeignKey('PtFacultades', models.DO_NOTHING, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_carreras'


class PtCategorias(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_categorias'


class PtCiclos(models.Model):
    id = models.BigAutoField(primary_key=True)
    ciclo = models.CharField(unique=True, max_length=20, blank=True, null=True)
    ciclo_actual = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_ciclos'


class PtComprobaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    ci_coevaluador = models.ForeignKey('PtUsers', models.DO_NOTHING, blank=True, null=True)
    evaluado = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_comprobaciones'


class PtCursos(models.Model):
    id = models.BigAutoField(primary_key=True)
    curso = models.CharField(max_length=250, blank=True, null=True)
    criterio = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_cursos'


class PtFacultades(models.Model):
    id = models.BigAutoField(primary_key=True)
    universidad = models.ForeignKey('PtUniversidades', models.DO_NOTHING, blank=True, null=True)
    facultad = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_facultades'


class PtHistoAutoevaluaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    docente = models.ForeignKey('PtUsers', models.DO_NOTHING, db_column='docente', blank=True, null=True)
    name_docente = models.CharField(max_length=255, blank=True, null=True)
    apellido_docente = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    ciclo = models.CharField(max_length=20, blank=True, null=True)
    universidad = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_histo_autoevaluaciones'


class PtHistoCoevaluadores(models.Model):
    id = models.BigAutoField(primary_key=True)
    ci_coevaluador = models.ForeignKey('PtUsers', models.DO_NOTHING, blank=True, null=True)
    name_coevaluador = models.CharField(max_length=255, blank=True, null=True)
    apellido_coevaluador = models.CharField(max_length=255, blank=True, null=True)
    ci_evaluado = models.CharField(max_length=10, blank=True, null=True)
    name_evaluado = models.CharField(max_length=255, blank=True, null=True)
    apellido_evaluado = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    ciclo = models.CharField(max_length=20, blank=True, null=True)
    universidad = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_histo_coevaluadores'


class PtMateriaUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    materias = models.ForeignKey('PtMaterias', models.DO_NOTHING, blank=True, null=True)
    docente = models.ForeignKey('PtUsers', models.DO_NOTHING, db_column='docente', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_materia_users'


class PtMaterias(models.Model):
    id = models.BigAutoField(primary_key=True)
    materia = models.CharField(max_length=255, blank=True, null=True)
    universidad = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_materias'


class PtMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    migration = models.CharField(max_length=255, blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_migrations'


class PtPasswordResets(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.ForeignKey('PtUsers', models.DO_NOTHING, db_column='email', blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_password_resets'


class PtPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    guard_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_permissions'


class PtPistasAuditoriaAuto(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    ciclo = models.CharField(max_length=20, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_pistas_auditoria_auto'


class PtPistasAuditoriaCoe(models.Model):
    id = models.BigAutoField(primary_key=True)
    coevaluador = models.CharField(max_length=10, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    ciclo = models.CharField(max_length=20, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_pistas_auditoria_coe'


class PtPreguntas(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(PtCategorias, models.DO_NOTHING, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_preguntas'


class PtRespuestas(models.Model):
    id = models.BigAutoField(primary_key=True)
    resultado = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('PtUsers', models.DO_NOTHING, blank=True, null=True)
    pregunta = models.ForeignKey(PtPreguntas, models.DO_NOTHING, blank=True, null=True)
    ciclo = models.CharField(max_length=20, blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    materia = models.CharField(max_length=255, blank=True, null=True)
    area_conocimiento = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    coevaluador = models.CharField(max_length=10, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_respuestas'


class PtRoleHasPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    permission = models.ForeignKey(PtPermissions, models.DO_NOTHING, blank=True, null=True)
    role = models.ForeignKey('PtRoles', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_role_has_permissions'


class PtRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    guard_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_roles'


class PtUniversidades(models.Model):
    id = models.BigAutoField(primary_key=True)
    universidad = models.CharField(unique=True, max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_universidades'


# class HistorialEvaluacion(models.Model):
#     pdf_file = models.FileField(upload_to='customers_id')

class PtUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    cedula = models.CharField(unique=True, max_length=10, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    auto = models.CharField(max_length=1, blank=True, null=True)
    universidad = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    evaluador1 = models.CharField(max_length=10, blank=True, null=True)
    evaluador2 = models.CharField(max_length=10, blank=True, null=True)
    evaluador3 = models.CharField(max_length=10, blank=True, null=True)
    evaluador4 = models.CharField(max_length=10, blank=True, null=True)
    evaluador5 = models.CharField(max_length=10, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_users'

class AprobacionCurso(models.Model):
    Nivel_CHOICES = (
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2')
    )

    semaforo_CHOICES = (
        ('1', 'Rojo'),
        ('2', 'Amarillo'),
        ('3', 'Verde'),
        ('4', 'Azul')
    )

    nivel = models.IntegerField(choices=Nivel_CHOICES)
    criterio = models.CharField(max_length=200)
    semaforo = models.IntegerField(choices=semaforo_CHOICES)
    estado = models.BooleanField(default=True)


class CursoAsesores(models.Model):
    id_curso = models.IntegerField()
    id_asesor = models.IntegerField()
    estado = models.BooleanField(default=True)
