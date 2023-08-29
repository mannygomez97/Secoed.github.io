from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Tipo, Ciclo
from eva.forms import TipoForm
from django.http import JsonResponse
from auditoria.apps import GeneradorAuditoria

m_Proceso = "TIPO EVALUACION"
m_NombreTabla = "pt_tipo"
class TypeListView(ListView):
    model = Tipo
    template_name = 'tipo/list.html'
    success_url = reverse_lazy('eva:list-type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Tipos de Evaluaciones'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['create_url'] = reverse_lazy('eva:create-type')
        context['url_list'] = reverse_lazy('eva:list-type')
        return context

class TypeCreateView(CreateView):
    model = Tipo
    form_class = TipoForm
    template_name = "tipo/create.html"
    success_url = reverse_lazy('eva:list-type')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
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
        context['title'] = 'Creación de Tipo'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-type')
        return context

class TypeUpdateView(UpdateView):
    model = Tipo
    form_class = TipoForm
    template_name = "tipo/update.html"
    success_url = reverse_lazy('eva:list-type')

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
        context['title'] = 'Actualizar Tipo'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-type')
        return context


class TypeDeleteView(DeleteView):
    model = Tipo
    success_url = reverse_lazy('eva:list-type')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            type = self.get_object()
            type.state = False
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            type.save()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
            return response
        else:
            return redirect('eva:list-type')
