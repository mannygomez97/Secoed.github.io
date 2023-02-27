from pprint import pp
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from eva.models import Pregunta, Categoria, Ciclo, PreguntaCiclo
from eva.forms import PreguntaForm, PreguntaAutoForm
from django.http import JsonResponse


class QuestionsListView(ListView):
    model = Pregunta
    template_name = 'preguntas/list.html'
    success_url = reverse_lazy('eva:list-questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Pregunta'
        #cycle = Ciclo.objects.filter(is_active=True).first()
        #context['pageview'] = cycle.name
        context['create_url'] = reverse_lazy('eva:create-questions')
        context['url_list'] = reverse_lazy('eva:list-questions')
        context['object_list'] = Pregunta.objects.all()
        return context


class QuestionsCreateView(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "preguntas/create.html"
    success_url = reverse_lazy('eva:list-questions')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                updated_request = request.POST.copy()
                updated_request.update({'ciclo': self.request.session.get('cicloId')})
                form = self.form_class(updated_request)
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
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Pregunta'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-questions')
        return context


class QuestionsUpdateView(UpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "preguntas/update.html"
    success_url = reverse_lazy('eva:list-questions')

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
        context['title'] = 'Actualizar Pregunta'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-questions')
        return context


class QuestionsDeleteView(DeleteView):
    model = Pregunta
    success_url = reverse_lazy('eva:list-questions')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            questions = self.get_object()
            questions.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-questions')

@method_decorator(login_required, name='dispatch')
class PreguntasAutoView(ListView):
    try:
        model = PreguntaCiclo
        template_name = 'preguntas/auto-preguntas.html'
        success_url = reverse_lazy('eva:auto-questions')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['heading'] = 'Preguntas de Autoevaluación'
            context['object_list'] = pregunta = PreguntaCiclo.objects.filter(pregunta__type=1, ciclo=int(self.request.session.get('cicloId')))
            context['create_url'] = reverse_lazy('eva:create-questions-auto')
            context['url_list'] = reverse_lazy('eva:auto-questions')
            return context
    except Exception as ex:
        pass

@method_decorator(login_required, name='dispatch')
class PreguntasAutoCreateView(CreateView):
    model = PreguntaCiclo
    form_class = PreguntaAutoForm
    template_name = "preguntas/create_auto.html"
    success_url = reverse_lazy('eva:auto-questions')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                fi = form.is_valid()
                fw = form.errors
                if form.is_valid():
                    pregunta = PreguntaCiclo.objects.filter(pregunta=form.cleaned_data['pregunta'], ciclo=form.cleaned_data['ciclo']).first()
                    if pregunta is not None and request.POST['option'] == 'true':
                        message = f'El periodo {pregunta.pregunta.title} ya se encuentra ingresada'
                        error = {'Error ': 'No puede ingresar la misma pregunta mas de una vez'}
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
        context['title'] = 'Agragar Pregunta Autoevaluación'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:auto-questions')
        return context


class PreguntasAutoDeleteView(DeleteView):
    model = Pregunta
    success_url = reverse_lazy('eva:list-questions')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            questions = self.get_object()
            questions.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-questions')


@method_decorator(login_required, name='dispatch')
class PreguntasCoeView(ListView):
    try:
        model = PreguntaCiclo
        template_name = 'preguntas/coe-preguntas.html'
        success_url = reverse_lazy('eva:ceo-questions')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['heading'] = 'Preguntas de Coevaluación'
            context['object_list'] = pregunta = PreguntaCiclo.objects.filter(pregunta__type=2, ciclo=int(self.request.session.get('cicloId')))
            context['create_url'] = reverse_lazy('eva:create-questions-coe')
            context['url_list'] = reverse_lazy('eva:coe-questions')
            return context
    except Exception as ex:
        pass


@method_decorator(login_required, name='dispatch')
class PreguntasAutoCreateView(CreateView):
    model = PreguntaCiclo
    form_class = PreguntaAutoForm
    template_name = "preguntas/create_coe.html"
    success_url = reverse_lazy('eva:coe-questions')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                fi = form.is_valid()
                fw = form.errors
                if form.is_valid():
                    pregunta = PreguntaCiclo.objects.filter(pregunta=form.cleaned_data['pregunta'], ciclo=form.cleaned_data['ciclo']).first()
                    if pregunta is not None and request.POST['option'] == 'true':
                        message = f'El periodo {pregunta.pregunta.title} ya se encuentra ingresada'
                        error = {'Error ': 'No puede ingresar la misma pregunta mas de una vez'}
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
        context['title'] = 'Agragar Pregunta Coevaluación'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:coe-questions')
        return context