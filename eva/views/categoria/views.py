from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Categoria
from eva.forms import CategoriaForm
from django.http import JsonResponse


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/list.html'
    success_url = reverse_lazy('eva:list-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Categorias'
        context['create_url'] = reverse_lazy('eva:create-category')
        return context


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/create.html"
    success_url = reverse_lazy('eva:list-category')

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


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/update.html"
    success_url = reverse_lazy('eva:list-category')

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


class CategoriaDeleteView(DeleteView):
    model = Categoria
    success_url = reverse_lazy('eva:list-category')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            category = self.get_object()
            category.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-category')
