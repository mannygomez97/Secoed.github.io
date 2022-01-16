from django.contrib.auth.decorators import login_required
from django.urls import path
from docentes import views

urlpatterns = [

    # categoria de las preguntas
    path(r'categoriaPregunta', login_required(views.CategoriaView.as_view()), name='categoriaPregunta'),
    path(r'newCategoria', login_required(views.CategoriaView.newCategoria), name='newCategoria'),
    path(r'editCategoria/<int:pk>', login_required(views.CategoriaView.editCategoria), name='editCategoria'),
    path(r'viewCategoria/<int:pk>', login_required(views.CategoriaView.viewCategoria), name='viewCategoria'),
    path(r'deleteCategoria/<int:pk>', login_required(views.CategoriaView.deleteCategoria), name='deleteCategoria'),


    # configuracion de la pregunta de evaluacion
    path(r'conf_preguntas', login_required(views.ConfPreguntasView.as_view()), name='conf_preguntas'),
    path(r'newConfPreguntas', login_required(views.ConfPreguntasView.newConfPreguntas), name='newConfPreguntas'),
    path(r'editConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.editConfPreguntas), name='editConfPreguntas'),
    path(r'viewConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.viewConfPreguntas), name='viewConfPreguntas'),
    path(r'deleteConfPreguntas/<int:pk>', login_required(views.ConfPreguntasView.deleteConfPreguntas), name='deleteConfPreguntas'),

    # evaluacion de la plataforma por parte de los docentes
    path(r'evaluacion-plataforma', login_required(views.EvaluacionView.as_view()), name='evaluacion-plataforma'),
    path(r'saveEvaluacion', login_required(views.EvaluacionView.saveEvaluacion), name='saveEvaluacion'),
]
