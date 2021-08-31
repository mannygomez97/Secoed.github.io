from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from eva.models import *


@admin.register(Docente)
class Docente(ImportExportModelAdmin):
    list_display = ('user', 'name', 'identify', 'is_evaluator')


@admin.register(Universidad)
class universidadAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ('university', 'name')


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('schoolOf', 'name',)


@admin.register(Materia)
class MatterAdmin(admin.ModelAdmin):
    list_display = ('career', 'name')


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'cycle', 'auto_evaluated', 'co_evaluator')


@admin.register(Pregunta)
class PreguntaAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'category', 'type')


@admin.register(AreasConocimiento)
class AreasAdmin(admin.ModelAdmin):
    list_display = ('career', 'name')


@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ParametrosGeneral)
class ParametrosGeneralesAdmin(admin.ModelAdmin):
    list_display = ('parameter_id', 'code', 'value')


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
