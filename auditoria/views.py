from django.core.paginator import Paginator
from django.views import View
from auditoria.models import *
from django.shortcuts import render

# Create your views here.
class AuditoriaContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        auditoria = Auditoria.objects.order_by('-fechacreacion')

        paginated_filtered= Paginator(auditoria, 20)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        greeting = {'heading': "Auditorías Generadas", 'pageview': "Auditorías",'page_obj': page_obj, 'auditoriaview': auditoria}
        return render(request, 'auditoria/listAuditoria.html', greeting)

class ErrorAuditoriaContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        errores = ErrorAuditoria.objects.order_by('-fechacreacion')

        paginated_filtered= Paginator(errores, 20)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        greeting = {'heading': "Errores Generados", 'pageview': "Auditorías", 'page_obj': page_obj, 'erroresview': errores}
        return render(request, 'auditoria/listErrores.html', greeting)