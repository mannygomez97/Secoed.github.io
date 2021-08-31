from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Tipo
from eva.forms import TipoForm
from django.http import JsonResponse


class TipoListView(ListView):
    model = Tipo
    template_name = 'tipo/list.html'
    success_url = reverse_lazy('eva:list-type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Tipos'
        context['create_url'] = reverse_lazy('eva:create-type')
        return context


class TipoCreateView(CreateView):
    model = Tipo
    form_class = TipoForm
    template_name = "tipo/create.html"
    success_url = reverse_lazy('eva:list-type')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
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


class TipoUpdateView(UpdateView):
    model = Tipo
    form_class = TipoForm
    template_name = "tipo/update.html"
    success_url = reverse_lazy('eva:list-type')

    def post(self, request, *args, **kwargs):
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


class TipoDeleteView(DeleteView):
    model = Tipo
    success_url = reverse_lazy('eva:list-type')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            type = self.get_object()
            type.delete()
            message = f'{self.model.__name__} eliminado correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-type')
