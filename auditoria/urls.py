from django.contrib.auth.decorators import login_required
from django.urls import path
from auditoria import views
from .views import *

urlpatterns = [
     path(r'auditoria', login_required(views.AuditoriaContentView.as_view()), name='auditoria'),
     path(r'errores', login_required(views.ErrorAuditoriaContentView.as_view()), name='errores'),
]
