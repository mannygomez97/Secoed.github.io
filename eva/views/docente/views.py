from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from eva.forms import DocenteForm
from eva.models import Docente
from django.http import JsonResponse


class TeacherListView(ListView):
    model = Docente
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Listado de Docentes'
        context['object_list'] = Docente.objects.filter(is_evaluator=False)
        context['create_url'] = reverse_lazy('eva:create-teachers')
        return context


class TeacherCoevaluatorListView(ListView):
    model = Docente
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-teachers-co')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Listado de Coevaluadores'
        context['object_list'] = Docente.objects.filter(is_evaluator=True)
        return context


class TeacherCreateView(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = "docente/create.html"
    success_url = reverse_lazy('eva:list-teachers')

    def post(self, request, *args, **kwargs):
        data = {}
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


class TeacherUpdateView(UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = "docente/update.html"
    success_url = reverse_lazy('eva:list-teachers')

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


class TeacherDeleteView(DeleteView):
    model = Docente
    success_url = reverse_lazy('eva:list-teachers')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            teacher = self.get_object()
            teacher.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-teachers')
