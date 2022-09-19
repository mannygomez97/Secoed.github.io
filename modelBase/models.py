from django.db import models
from authentication.models import Usuario

class ModelBase(models.Model):
    id = models.AutoField(primary_key = True)
    status = models.BooleanField(default = True)
    createdDate = models.DateTimeField('Fecha de creación', auto_now = False, auto_now_add = True)
    userCreated = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank = True, null = True)

    class Meta:
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"