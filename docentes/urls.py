from django.contrib.auth.decorators import login_required
from django.urls import path
from docentes import views

urlpatterns = [
    path(r'cursos_usuario', login_required(views.CursosUserView.as_view()), name='cursos_usuario'),
    path(r'reporte_actividades/<int:pk>/<int:id>', login_required(views.CursosUserView.generarReporte), name='reporte_actividades'),
    path(r'reporte_curso_docente', login_required(views.CursosUserView.reporteXcurso), name='reporte_curso_docente'),
    path(r'view_actividades/<int:pk>', login_required(views.CursosUserView.viewActividades), name='view_actividades'),
    path(r'calificaciones_proceso', login_required(views.CalificacionesProceso.as_view()), name='calificaciones_proceso'),
    path(r'calificaciones_cursos', login_required(views.CalificacionesCursos.as_view()), name='calificaciones_cursos'),
]
