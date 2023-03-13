from django.db import models
from authentication.models import Usuario

class Auditoria(models.Model):
    id = models.AutoField(primary_key=True)
    tabla = models.TextField(max_length=150, null=True, unique=True)
    idregistro = models.IntegerField(null=True)
    comando = models.TextField(max_length=80, null=True)
    registronuevo = models.TextField(null=True)
    registroanterior = models.TextField(null=True)
    usuario = models.ForeignKey(Usuario, db_column="idusuariocreacion", on_delete=models.SET_NULL, null=True)
    fechacreacion = models.DateTimeField(null=True)

    class Meta:
        db_table = "tb_auditoria"
        app_label = 'auditoria'

    def __str__(self):
        return f'{self.tabla}'

class ErrorAuditoria(models.Model):
    id = models.AutoField(primary_key=True)
    proceso = models.TextField(max_length=180, null=True, unique=True)
    tipo = models.TextField(max_length=50, null=True)
    excepcion = models.TextField(null=True)
    detalles = models.TextField(null=True)
    usuario = models.ForeignKey(Usuario, db_column="idusuario", on_delete=models.SET_NULL, null=True)
    fechacreacion = models.DateTimeField(null=True)

    class Meta:
        db_table = "tb_errores"
        app_label = 'errores'

    def __str__(self):
        return f'{self.tabla}'

