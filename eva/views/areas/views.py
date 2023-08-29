from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import AreasConocimiento, Ciclo
from eva.forms import AreasConocimientoForm
from django.http import JsonResponse
from auditoria.apps import GeneradorAuditoria

m_Proceso = "AREAS-CONOCIMIENTO"
m_NombreTabla = "pt_area_conocimiento"

class KnowledgeAreasListView(ListView):
    model = AreasConocimiento
    template_name = 'areas/list.html'
    success_url = reverse_lazy('eva:list-area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = ' Áreas de Conocimiento'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['object_list'] = AreasConocimiento.objects.all()
        context['action'] = 'add'
        context['create_url'] = reverse_lazy('eva:create-area')
        context['url_list'] = reverse_lazy('eva:list-area')
        return context


class KnowledgeAreasCreateView(CreateView):
    model = AreasConocimiento
    form_class = AreasConocimientoForm
    template_name = "areas/create.html"
    success_url = reverse_lazy('eva:list-area')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                updated_request = request.POST.copy()
                updated_request.update({'id_ciclo': self.request.session.get('cicloId')})
                option = request.POST['action']
                form = self.form_class(updated_request)
                if option == 'add':
                    form.save()
                    message = f'{self.model.__name__} registrada correctamente'
                    error = 'No han ocurrido errores'
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 201
                    newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTabla)
                    GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTabla, newJson, request.user.id)
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                    return response
        except Exception as e:
            data['error'] = str(e)
            GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(e), request.user.id)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Área de conocimiento'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-area')
        return context
    

class KnowledgeAreasUpdateView(UpdateView):
    model = AreasConocimiento
    form_class = AreasConocimientoForm
    template_name = "areas/update.html"
    success_url = reverse_lazy('eva:list-area')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                message = f'{self.model.__name__} actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 201
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTabla, kwargs["pk"], newJson, oldJson, request.user.id)
                return response
            else:
                message = f'{self.model.__name__} no se pudo actualizar!'
                error = form.errors
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 400
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                return response
        except Exception as e:
            data['error'] = str(e)
            GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(e), request.user.id)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Área de Conocimiento'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-area')
        return context


class KnowledgeAreasDeleteView(DeleteView):
    model = AreasConocimiento
    success_url = reverse_lazy('eva:list-area')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            knowledge_area = self.get_object()
            knowledge_area.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
            return response
        else:
            return redirect('eva:list-area')
