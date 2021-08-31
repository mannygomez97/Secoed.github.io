from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Pregunta, Categoria
from eva.forms import PreguntaForm
from django.http import JsonResponse


class QuestionListView(ListView):
    model = Pregunta
    template_name = 'preguntas/auto-preguntas.html'
    success_url = reverse_lazy('eva:list-Pregunta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Pregunta'
        context['titulo'] = 'Pregunta Autoevaluación'
        context['create_url'] = reverse_lazy('eva:create-Pregunta')
        return context


class QuestionCreateView(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'preguntas/create.html'
    success_url = reverse_lazy('eva:list-Pregunta')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    question = Pregunta(
                        category=form.cleaned_data.get('categoria'),
                        title=form.cleaned_data.get('title'),
                        description=form.cleaned_data.get('description'),
                        type=form.cleaned_data.get('type')
                    )
                    question.save()
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
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Creación de Pregunta'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-Pregunta')
        return context
    

class QuestionUpdateView(UpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "preguntas/update.html"
    success_url = reverse_lazy('eva:list-Pregunta')

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
        context['heading'] = 'Actualizar Pregunta'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-Pregunta')
        return context


class QuestionDeleteView(DeleteView):
    model = Pregunta
    success_url = reverse_lazy('eva:list-Pregunta')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            Question = self.get_object()
            Question.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-Pregunta')


class General():
    def getQuestions(self):
        preguntas = Pregunta.objects.all()
        return preguntas

    def getCategories(self):
        categorias = Categoria.objects.all()
        return categorias


@method_decorator(login_required, name='dispatch')
class PreguntasAutoView(ListView):
    model = Pregunta
    template_name = 'preguntas/auto-preguntas.html'

    def get_context_data(self, **kwargs):
        obj = General
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Preguntas de Autoevaluación'
        context['preguntas'] = obj.getQuestions(self).filter(type=1)
        context['categorias'] = obj.getCategories(self)
        return context


@method_decorator(login_required, name='dispatch')
class PreguntasCoeView(ListView):
    model = Pregunta
    template_name = 'preguntas/coe-preguntas.html'

    def get_context_data(self, **kwargs):
        obj = General
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Preguntas de Coevaluación'
        context['preguntas'] = obj.getQuestions(self).filter(type=2)
        context['categorias'] = obj.getCategories(self)
        return context