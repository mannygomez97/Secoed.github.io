from django.contrib import admin

from .models import Carpeta
from .models import Archivo
# Register your models here.

#admin.site.register(Carpeta)#para el admin
@admin.register(Carpeta)
class CarpetaAdmin(admin.ModelAdmin):
    list_display=('idcarpeta','nombre','fechacreacion','fechamodificacion')
    ordering = ('idcarpeta','nombre')
    search_fields = ('idcarpeta','nombre')
    list_display_links =('nombre',)

#admin.site.register(Archivo)#para el admin
@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display=('idarchivo','nombre','carpeta_id','carpeta','fechacreacion','fechamodificacion')
    ordering = ('idarchivo',)
    search_fields = ('nombre','idarchivo')
    list_display_links =('nombre',)
    list_filter = ('carpeta_id',)
    list_per_page = 10
    exclude=()
    autocomplete_fields=['carpeta']