from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Ciclo2
from eva.forms import CicloForm
from eva.forms import CicloFormCN
from django.http import JsonResponse


class CycleListView(ListView):
    model = Ciclo2
    template_name = 'ciclo/list.html'
    success_url = reverse_lazy('eva:list-cycle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Ciclo'
        cycle = Ciclo2.objects.filter(is_active=True).first()
        context['pageview'] = cycle.nombre
        context['create_url'] = reverse_lazy('eva:create-cycle')
        context['url_list'] = reverse_lazy('eva:list-cycle')
        return context


class CycleCreateView(CreateView):
    model = Ciclo2
    form_class = CicloFormCN
    template_name = "ciclo/create.html"
    success_url = reverse_lazy('eva:list-cycle')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    ciclo = Ciclo2.objects.filter(is_active=True).first()
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
        context['title'] = 'Creación de Ciclo'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-cycle')
        return context
    
class CycleUpdateView(UpdateView):
    model = Ciclo2
    form_class = CicloFormCN
    template_name = "ciclo/update.html"
    success_url = reverse_lazy('eva:list-cycle')

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
        context['title'] = 'Actualizar Ciclo'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-cycle')
        return context


class CycleDeleteView(DeleteView):
    model = Ciclo2
    success_url = reverse_lazy('eva:list-cycle')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            cycle = self.get_object()
            cycle.delete()
            # university.save()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-cycle')

#GRUPO REPOSITORIO COE Y EVA
def schange_ciclo(request,cicloId):
    request.session['ciclo_id'] = cicloId
    return JsonResponse({'success':True})

#GRUPO REPOSITORIO COE Y EVA
def gchange_ciclo(request):
    return JsonResponse({'ciclo_id':request.session.get('ciclo_id',0)})
