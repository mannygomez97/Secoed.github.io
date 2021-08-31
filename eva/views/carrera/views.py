from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Carrera
from eva.forms import CarreraForm
from django.http import JsonResponse


class CarreraListView(ListView):
    model = Carrera
    template_name = 'carrera/list.html'
    success_url = reverse_lazy('eva:list-career')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Carreras'
        context['create_url'] = reverse_lazy('eva:create-career')
        return context


class CarreraCreateView(CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'carrera/create.html'
    success_url = reverse_lazy('eva:list-career')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                message = f'{self.model.__name__} registrada correctamente'
                error = 'No han ocurrido errores'
                response = JsonResponse({'message': message, 'error': error})
                #response.status_code = 201
                return response
            else:
                message = f'{self.model.__name__} no se pudo registrar!'
                error = form.errors
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 400
                return response


class CarreraUpdateView(UpdateView):
    model = Carrera
    form_class = CarreraForm
    template_name = "carrera/update.html"
    success_url = reverse_lazy('eva:list-career')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                message = f'{self.model.__name__} actualizada correctamente'
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


class CarreraDeleteView(DeleteView):
    model = Carrera
    success_url = reverse_lazy('eva:list-career')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            career = self.get_object()
            career.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-career')
