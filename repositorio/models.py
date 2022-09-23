from enum import auto
from tkinter import image_names
from django.db import models
 

# Create your models here.
#hay que migrar todo dato modificado el mas minimo

#Carpeta
class Carpeta(models.Model): #luego de crear este modelo enla bd, hayq ue migrar, se creara una tabla en la bd, con el nombre libreria_libro
    idcarpeta=models.AutoField(primary_key=True)
    nombre=models.TextField(null=False)
    nombre_anterior=models.TextField(null=True)
    descripcion=models.TextField(null=True)
    fechacreacion=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion", null=True ) #para crear por primera vez
    fechamodificacion=models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion", null=True) #para ver las fechas modificadas
    parent_id = models.IntegerField(default=0)
    ruta=models.TextField(null=True)
    def __str__(self): #esto es para el admin de django
        fila = " " + self.nombre
        return fila

#Archivo
class Archivo(models.Model): #luego de crear este modelo enla bd, hayq ue migrar, se creara una tabla en la bd, con el nombre libreria_libro
    idarchivo=models.AutoField(primary_key=True)
    carpeta=models.ForeignKey(Carpeta, null=False, blank=False, on_delete=models.CASCADE)#clave foranea, relacion entre la carpeta que contiene varios archivos
    nombre=models.TextField(null=False)
    archivo=models.FileField(max_length=7000, upload_to="repositorio_archivos", verbose_name="Archivo", null=False)
    descripcion=models.TextField(null=True)
    fechacreacion=models.DateField(auto_now_add=True, verbose_name="Fecha de creacion", null=True)
    fechamodificacion=models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion", null=True)
    
    def __str__(self):
        fila = "Nombre: " + self.nombre + " - " + "Descripcion: " + self.descripcion
        return fila

    def delete(self, using=None, keep_parents=False):
        self.archivo.storage.delete(self.archivo.name)
        super().delete()
