from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Facultad
from eva.forms import FacultadForm
from django.http import JsonResponse


class FacultadListView(ListView):
    model = Facultad
    template_name = 'facultad/list.html'
    success_url = reverse_lazy('eva:list-facultad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Facultades'
        context['create_url'] = reverse_lazy('eva:create-facultad')
        return context


class FacultadCreateView(CreateView):
    model = Facultad
    form_class = FacultadForm
    template_name = "facultad/create.html"
    success_url = reverse_lazy('eva:list-facultad')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                message = f'{self.model.__name__} registrada correctamente'
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


class FacultadUpdateView(UpdateView):
    model = Facultad
    form_class = FacultadForm
    template_name = "facultad/update.html"
    success_url = reverse_lazy('eva:list-facultad')

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


class FacultadDeleteView(DeleteView):
    model = Facultad
    success_url = reverse_lazy('eva:list-facultad')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            school_of = self.get_object()
            school_of.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-facultad')
