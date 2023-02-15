from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Ciclo
from eva.forms import CicloForm
from django.http import JsonResponse
from auditoria.apps import GeneradorAuditoria

#Constantes
m_NombreTabla = "pt_ciclo"
class PeriodListView(ListView):
    model = Ciclo
    template_name = 'periodo/list.html'
    success_url = reverse_lazy('eva:list-periodo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Periodo'
        cycle = Ciclo.objects.filter(is_active=True).first()
        if(cycle is not None): #Nuevo COE Y EVA - GRUPO REPOSITORIO
            context['pageview'] = cycle.name #Nuevo COE Y EVA - GRUPO REPOSITORIO
        else: #Nuevo COE Y EVA - GRUPO REPOSITORIO
            context['pageview'] = "" #Nuevo COE Y EVA - GRUPO REPOSITORIO
        context['create_url'] = reverse_lazy('eva:create-cycle')
        context['url_list'] = reverse_lazy('eva:list-periodo')
        return context


class PeriodCreateView(CreateView):
    model = Ciclo
    form_class = CicloForm
    template_name = "periodo/create.html"
    success_url = reverse_lazy('eva:list-periodo')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    ciclo = Ciclo.objects.filter(is_active=True).first()
                    if ciclo is not None and ciclo.is_active and request.POST['option'] == 'true':
                        message = f'El periodo {ciclo.name} se encuentra altualmente activo '
                        error = {'Error ': 'El periodo ' + ciclo.name + ' se encuentra activo'}
                        response = JsonResponse({'message': message, 'error': error})
                        response.status_code = 409
                    else:
                        form.save()
                        message = f'{self.model.__name__} registrado correctamente'
                        error = 'No han ocurrido errores'
                        response = JsonResponse({'message': message, 'error': error})
                        response.status_code = 201
                        GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTabla, "json create", 1)
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Periodo'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-periodo')
        return context
    

class PeriodUpdateView(UpdateView):
    model = Ciclo
    form_class = CicloForm
    template_name = "periodo/update.html"
    success_url = reverse_lazy('eva:list-periodo')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                message = f'{self.model.__name__} actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 201
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTabla, "json new", "json old", 1)
                return response
            else:
                message = f'{self.model.__name__} no se pudo actualizar!'
                error = form.errors
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 400
                return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Periodo'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-periodo')
        return context


class PeriodDeleteView(DeleteView):
    model = Ciclo
    success_url = reverse_lazy('eva:list-periodo')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            cycle = self.get_object()
            cycle.delete()
            # university.save()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, "json old", 1)
            return response
        else:
            return redirect('eva:list-periodo')
