from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from eva.forms import DocenteForm
from eva.models import Docente


class TeacherListView(ListView):
    model = Docente
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Docente'
        context['object_list'] = Docente.objects.filter(is_evaluator=False)
        context['create_url'] = reverse_lazy('eva:create-teacher')
        context['url_list'] = reverse_lazy('eva:list-teacher')
        return context


class TeacherCoevaluatorListView(ListView):
    model = Docente
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-coevaluators')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Listado de Coevaluadores'
        context['object_list'] = Docente.objects.filter(is_evaluator=True)
        context['url_list'] = reverse_lazy('eva:list-coevaluators')
        return context


class TeacherCreateView(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = "docente/create.html"
    success_url = reverse_lazy('eva:list-teacher')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()
                    message = f'{self.model.__name__} registrado correctamente'
                    error = 'No han ocurrido errores'
                    data = {'message': message, 'error': error}
                    # response = JsonResponse({'message': message, 'error': error})
                    # response.status_code = 201
                    # return response
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
        context['title'] = 'Creación de Docente'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-teacher')
        return context


class TeacherUpdateView(UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = "docente/update.html"
    success_url = reverse_lazy('eva:list-teacher')

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
        context['title'] = 'Actualizar Docente'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-teacher')
        return context


class TeacherDeleteView(DeleteView):
    model = Docente
    success_url = reverse_lazy('eva:list-teacher')

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
            return redirect('eva:list-teacher')
