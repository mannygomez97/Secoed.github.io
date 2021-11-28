from django.contrib.auth.decorators import login_required
from django.urls import path
from docentes import views

urlpatterns = [

    # configuracion de la pregunta de evaluacion
    path(r'conf_preguntas', login_required(views.ConfPreguntasView.as_view()), name='conf_preguntas'),
    path(r'newConfPreguntas', login_required(views.ConfPreguntasView.newConfPreguntas), name='newConfPreguntas'),
    path(r'editConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.editConfPreguntas), name='editConfPreguntas'),
    path(r'viewConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.viewConfPreguntas), name='viewConfPreguntas'),
    path(r'deleteConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.deleteConfPreguntas), name='deleteConfPreguntas'),

]
