
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Ciclo, Ciclo2
from eva.forms import CicloForm, CicloFormCN
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator


class PeriodListView(ListView):
    model = Ciclo
    template_name = 'periodo/list.html'
    success_url = reverse_lazy('eva:list-periodo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Periodo'
        cycle = Ciclo.objects.filter(is_active=True).first()
        if(cycle is not None):
            context['pageview'] = cycle.name
        else:
            context['pageview'] = ""
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
            return response
        else:
            return redirect('eva:list-periodo')


def periodociclo(request):
    global ex
    data = {}
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'add':
            try:
                ciclo = Ciclo2(nombre=request.POST['nombre'],
                               periodo_id=int(request.POST['periodo']),
                               is_active=True)
                ciclo.save()
            except Exception as ex:
                pass
    else:
        if 'action' in request.GET:
            action = request.GET['action']

        else:
            try:
                data['title'] = u'Criclo'
                data['periodo'] = periodo = Ciclo.objects.get(pk=int(request.GET['id']))
                data['object_list'] = Ciclo2.objects.filter(periodo=periodo)
                return render(request, 'periodo/periodociclo.html', data)
            except Exception as ex:
                return HttpResponseRedirect('/')
