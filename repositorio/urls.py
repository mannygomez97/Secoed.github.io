from urllib.parse import urlparse
from xml.dom.minidom import Document
from django.urls import path
from . import views

from django.conf.urls import include, url

from .views import * #nuevo



from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.views.static import serve
from repositorio import views

urlpatterns = [

#carpetas
    path('inicio/carpetas',views.carpetas, name='carpetas'),
    path('carpetas/crearcar',views.crearcar, name='crearcar'),
    path('carpetas/editarcar',views.editarcar, name='editarcar'),
    path('carpetas/eliminar/<int:idcarpeta>',views.eliminarcar, name='eliminarcar'),
    path('carpetas/editarcar/<int:idcarpeta>',views.editarcar, name='editarcar'),
    path('carpetas/ingresaracar/<int:idcarpeta>',views.ingresaracar, name='ingresaracar'),
    path('buscar/', views.buscarcarp, name='buscar'),
    path('archivos/seleccionar-tipo-archivos',views.seleccionar_tipo_archivos, name='seleccionar_tipo_archivos'),

#archivos
    path('archivos',views.archivos, name='archivos'),#este es la carpeta libro, pero lleva a index
    path('archivos/crear',views.crear, name='crear'),
    path('archivos/editar',views.editar, name='editar'),
    path('archivos/eliminar/<int:idarchivo>',views.eliminar, name='eliminar'),
    path('archivos/editar/<int:idarchivo>',views.editar, name='editar'),
    path('archivos/buscar/', views.buscarar, name='buscarar'),

#busqueda
    path('inicio/busquedageneral',views.vistabusquedageneral, name='vistabuscargeneral'),
    url(r'^busquedageneral/ingresaracar/(?P<idcarpeta>[0-9]+)/{0,1}$', views.ingresaracarbgeneral,name='ingresarbusquedacarpeta'),
    path('busquedageneral/buscar/', views.buscargeneral, name='buscargeneral'),
    path('busquedageneral/carpetas/eliminar/<int:idcarpeta>',views.eliminarbusquedacarpeta, name='eliminarbusquedacarpeta'),
    path('busquedageneral/carpetas/editarcar/<int:idcarpeta>',views.editarcarbusqueda, name='editarbusquedacarpeta'), 
    path('busquedageneral/archivos/eliminar/<int:idarchivo>',views.eliminarbusquedaarchivo, name='eliminarbusquedaarchivo'),
    path('busquedageneral/archivos/editar/<int:idarchivo>',views.editararchivobusqueda, name='editarbusquedaarchivo'),
]