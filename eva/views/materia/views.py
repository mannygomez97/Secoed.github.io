from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Materia, Ciclo, MateriaCiclo
from eva.forms import MateriaForm
from django.http import JsonResponse
from auditoria.apps import GeneradorAuditoria

m_Proceso = "MATERIA"
m_NombreTabla = "pt_materia"
class MatterListView(ListView):
    model = Materia
    template_name = 'materia/list.html'
    success_url = reverse_lazy('eva:list-matter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Materia'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['object_list'] =  Materia.objects.filter( materiaciclo__ciclo_id = self.request.session.get('cicloId'))

        context['create_url'] = reverse_lazy('eva:create-matter')
        context['url_list'] = reverse_lazy('eva:list-matter')
        return context


class MatterCreateView(CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = "materia/create.html"
    success_url = reverse_lazy('eva:list-matter')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()                    
                    MateriaCiclo.objects.create(materia_ids=form.id, ciclo_id=self.request.session.get('cicloId'))
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
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Materia'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-matter')
        return context
    

class MatterUpdateView(UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = "materia/update.html"
    success_url = reverse_lazy('eva:list-matter')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                message = f'{self.model.__name__} actualizada correctamente'
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
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Materia'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-matter')
        return context


class MatterDeleteView(DeleteView):
    model = Materia
    success_url = reverse_lazy('eva:list-matter')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            matter = self.get_object()
            matter.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
            return response
        else:
            return redirect('eva:list-matter')
