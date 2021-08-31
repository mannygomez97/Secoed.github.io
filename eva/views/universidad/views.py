from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.mixins import ValidatePermissionRequiredMixin
from eva.models import Universidad
from eva.forms import UniversidadForm
from django.http import JsonResponse


class UniversidadListView(LoginRequiredMixin, ListView, ValidatePermissionRequiredMixin):
    permission_required = ('eva.view_university', 'eva.add_university', 'eva.change_university')
    url_redirect = reverse_lazy('eva:list-university')
    model = Universidad
    template_name = 'universidad/list.html'
    success_url = reverse_lazy('eva:list-university')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Universidad'
        context['create_url'] = reverse_lazy('eva:create-university')
        context['url_list'] = reverse_lazy('eva:list-university')
        return context


class UniversidadCreateView(LoginRequiredMixin, CreateView, ValidatePermissionRequiredMixin):
    model = Universidad
    form_class = UniversidadForm
    template_name = "universidad/create.html"
    success_url = reverse_lazy('eva:list-university')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Universidad'
        context['url_list'] = reverse_lazy('eva:list-university')
        return context


class UniversidadUpdateView(UpdateView, ValidatePermissionRequiredMixin):
    model = Universidad
    form_class = UniversidadForm
    template_name = "universidad/update.html"
    success_url = reverse_lazy('eva:list-university')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Universidad'
        context['url_list'] = reverse_lazy('eva:list-university')
        return context


class UniversidadDeleteView(DeleteView, ValidatePermissionRequiredMixin):
    model = Universidad
    success_url = reverse_lazy('eva:list-university')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            university = self.get_object()
            university.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-university')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Universidad'
        return context
