from django.contrib.auth.decorators import login_required
from django.urls import path
from docentes import views

urlpatterns = [

    # template de seguimiento de actividades
    path(r'seguimiento_actividades', login_required(views.SeguimientoView.as_view()), name='seguimiento_actividades'),
    path(r'reporte_actividades', login_required(views.SeguimientoView.generarReporte), name='reporte_actividades'),
    path(r'notas_docente', login_required(views.Notasiew.as_view()), name='notas_docente'),
]
