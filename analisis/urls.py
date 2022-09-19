from django.contrib.auth.decorators import login_required
from django.urls import path
from analisis import views

urlpatterns = [
     #Preguntas 
     path('', views.lista, name='lista'),
     path('guardado/', views.guardar, name='guardar'),
     path('borrar/<int:data_id>', views.borrar, name='borrar'),
     path('actualiza/<int:data_id>', views.actualiza, name='actualiza'),
     path('guardarActualizar/', views.guardarActualizar, name='guardarActualizar'),
     #nivel
     path('nivel/', views.listanivel, name='listanivel'),
     path('guardadonivel/', views.guardarnivel, name='guardarnivel'),
     path('borrarnivel/<int:data_id>', views.borrarnivel, name='borrarnivel'),
     path('actualizanivel/<int:data_id>', views.actualizanivel, name='actualizanivel'),
     path('guardarActualizarnivel/', views.guardarActualizarnivel, name='guardarActualizarnivel'),
     #Respuestas
     path('respuestas/', views.listarespuestas, name='listarespuestas'),
     path('guardarespuestas/', views.guardarespuestas, name='guardarespuestas'), 
     path('borrarespuestas/<int:data_id>', views.borrarespuestas, name='borrarespuestas'),
     #Reportes
     path('reportes/', views.reportes, name='reportes'),
     path('reportes/usuario/<int:data_id>', views.reportes_por_usuario, name='reportesporusuario'),
     path('reportes/pdf/usuario/<int:data_id>', views.reportes_pdf, name='reportes_pdf'),
     path('reporteusuario/', views.reporteusuario, name='reporteusuario'),

     path('reporteusuario/usuario/preguntas/<int:data_id>', views.reporteusuariopregunta, name='reporteusuariopregunta'),
     
]