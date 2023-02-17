from django.db import models
from modelBase.models import ModelBase

# Create your models here.
class Auditoria(models.Model):
    Tabla = models.CharField(db_column='tabla')
    Comando = models.CharField(db_column='comando')
    RegistroNuevo = models.CharField(db_column='registroNuevo')
    RegistroAnterior = models.CharField(db_column='registroAnterior')
    IdUsuarioCreacion = models.IntegerField(db_column='idUsuarioCreacion')
    FechaCreacion = models.DateTimeField(db_column='fechaCreacion')

    class Meta:
        db_table = "TB_AUDITORIA"

#ejemplo
