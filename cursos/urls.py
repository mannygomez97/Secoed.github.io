from django.contrib.auth.decorators import login_required
from django.urls import path
from cursos import views

urlpatterns = [
    path(r'categoria', login_required(views.CursoView.categoria), name='categoria'),
    path(r'allCategorias', login_required(views.CursoView.allCategorias), name='categoriaAll'),
    path(r'deleteCategoria/<int:idCategoria>', login_required(views.CursoView.deleteCategoria), name='deleteCategoria'),
    path(r'createEditCategoria', login_required(views.CursoView.createEditCategoria), name='createEditCategoria'),
    path(r'', login_required(views.CursoView.as_view()), name='cursos'),
    path(r'crearEditarCurso', login_required(views.CursoView.crearEditarCurso), name='crearEditarCurso'),
    path(r'deleteCourse/<int:idCourse>', login_required(views.CursoView.deleteCourse), name='deleteCourse'),
]
