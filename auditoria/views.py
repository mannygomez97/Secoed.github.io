from django.views import View
from auditoria.models import *
from django.shortcuts import render

# Create your views here.
class AuditoriaContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        auditoria = Auditoria.objects.order_by('-fechacreacion')
        greeting = {'heading': "Auditorías Generadas", 'pageview': "Auditorías", 'auditoriaview': auditoria}
        return render(request, 'auditoria/listAuditoria.html', greeting)

class ErrorAuditoriaContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        errores = ErrorAuditoria.objects.order_by('-fechacreacion')
        greeting = {'heading': "Errores Generados", 'pageview': "Auditorías", 'erroresview': errores}
        return render(request, 'auditoria/listErrores.html', greeting)