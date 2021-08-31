from django.conf.urls import url
from eva.views.carrera.views import *
from eva.views.categoria.views import *
from eva.views.ciclo.views import *
from eva.views.evaluationes.views import *
from eva.views.facultad.views import *
from eva.views.materia.views import *
from eva.views.preguntas.views import *
from eva.views.docente.views import *
from eva.views.tipo.views import *
from eva.views.universidad.views import *
from eva.views.areas.views import *
from eva.views.parametro.views import *
from eva.views.parametros_generales.views import *

app_name = 'eva'

urlpatterns = [
    # Questions urls
    url(r'^preguntasauto', PreguntasAutoView.as_view(), name='auto-questions'),
    url(r'^preguntascoe', PreguntasCoeView.as_view(), name='coe-questions'),
    # Evaluations urls
    url(r'^autoevalution/crear/', AutoEvaluacionView.as_view(), name='auto-evaluation'),
    url(r'^coevalution/list/', CoEvaluacionView.as_view(), name='co-evaluation'),
    # Materia urls
    url(r'^materia/list/', MateriaListView.as_view(), name='list-matter'),
    url(r'^materia/crear/', MateriaCreateView.as_view(), name='create-matter'),
    url(r'^materia/edit/(?P<pk>\d+)/$', MateriaUpdateView.as_view(), name='update-matter'),
    url(r'^materia/delete/(?P<pk>\d+)/$', MateriaDeleteView.as_view(), name='delete-matter'),
    # Carrera urls
    url(r'^carrera/list/', CarreraListView.as_view(), name='list-career'),
    url(r'^carrera/crear/', CarreraCreateView.as_view(), name='create-career'),
    url(r'^carrera/edit/(?P<pk>\d+)/$', CarreraUpdateView.as_view(), name='update-career'),
    url(r'^carrera/delete/(?P<pk>\d+)/$', CarreraDeleteView.as_view(), name='delete-career'),
    # School_of urls
    url(r'^facultad/list/', FacultadListView.as_view(), name='list-school-of'),
    url(r'^facultad/crear/', FacultadCreateView.as_view(), name='create-school-of'),
    url(r'^facultad/edit/(?P<pk>\d+)/$', FacultadUpdateView.as_view(), name='update-school-of'),
    url(r'^facultad/delete/(?P<pk>\d+)/$', FacultadDeleteView.as_view(), name='delete-school-of'),
    # Ciclo urls
    url(r'^ciclo/list/', CicloListView.as_view(), name='list-cycle'),
    url(r'^ciclo/crear/', CicloCreateView.as_view(), name='create-cycle'),
    url(r'^ciclo/edit/(?P<pk>\d+)/$', CicloUpdateView.as_view(), name='update-cycle'),
    url(r'^ciclo/delete/(?P<pk>\d+)/$', CicloDeleteView.as_view(), name='delete-cycle'),
    # Categoria urls
    url(r'^categoria/list/', CategoriaListView.as_view(), name='list-category'),
    url(r'^categoria/crear/', CategoriaCreateView.as_view(), name='create-category'),
    url(r'^categoria/edit/(?P<pk>\d+)/$', CategoriaUpdateView.as_view(), name='update-category'),
    url(r'^categoria/delete/(?P<pk>\d+)/$', CategoriaDeleteView.as_view(), name='delete-category'),
    # Tipo urls
    url(r'^tipo/list/', TipoListView.as_view(), name='list-type'),
    url(r'^tipo/crear', TipoCreateView.as_view(), name='create-type'),
    url(r'^tipo/edit/(?P<pk>\d+)/$', TipoUpdateView.as_view(), name='update-type'),
    url(r'^tipo/delete/(?P<pk>\d+)/$', TipoDeleteView.as_view(), name='delete-type'),
    # Universidad urls
    url(r'^universidad/list/', UniversidadListView.as_view(), name='list-university'),
    url(r'^universidad/crear/', UniversidadCreateView.as_view(), name='create-university'),
    url(r'^universidad/edit/(?P<pk>\d+)/$', UniversidadUpdateView.as_view(), name='update-university'),
    url(r'^universidad/delete/(?P<pk>\d+)/$', UniversidadDeleteView.as_view(), name='delete-university'),
    # Area de conocimiento
    url(r'^area/list/', AreaConocimientoListView.as_view(), name='list-area'),
    url(r'^area/crear/', AreaConocimientoCreateView.as_view(), name='create-area'),
    url(r'^area/edit/(?P<pk>\d+)/$', AreaConocimientoUpdateView.as_view(), name='update-area'),
    url(r'^area/delete/(?P<pk>\d+)/$', AreaConocimientoDeleteView.as_view(), name='delete-area'),
    # Parameters
    url(r'^parametro/list/', ParametroListView.as_view(), name='list-parameter'),
    url(r'^parametro/create/', ParametroCreateView.as_view(), name='create-parameter'),
    url(r'^parametro/edit/(?P<pk>\d+)/$', ParametroUpdateView.as_view(), name='update-parameter'),
    url(r'^parametro/delete/(?P<pk>\d+)/$', ParametroDeleteView.as_view(), name='delete-parameter'),
    # Parameters generals
    url(r'^parametro_grl/list/', ParametrosGeneralListView.as_view(), name='list-parameter-grl'),
    url(r'^parametro_grl/create/', ParametrosGeneralCreateView.as_view(), name='create-parameter-grl'),
    url(r'^parametro_grl/edit/(?P<pk>\d+)/$', ParametrosGeneralUpdateView.as_view(), name='update-parameter-grl'),
    url(r'^parametro_grl/delete/(?P<pk>\d+)/$', ParametrosGeneralDeleteView.as_view(), name='delete-parameter-grl'),
    # Teacher
    url(r'^docentes/list/', TeacherListView.as_view(), name='list-teachers'),
    url(r'^docentes/list/', TeacherListView.as_view(), name='list-users'),
    url(r'^docentes/coevaluadores/list/', TeacherCoevaluatorListView.as_view(), name='list-teachers-co'),
    url(r'^docentes/create/', TeacherCreateView.as_view(), name='create-teachers'),
    url(r'^docentes/edit/(?P<pk>\d+)/$', TeacherUpdateView.as_view(), name='update-teachers'),
    url(r'^docentes/delete/(?P<pk>\d+)/$', TeacherDeleteView.as_view(), name='delete-teachers'),
]
