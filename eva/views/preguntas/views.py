import json
from pprint import pp

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from eva.models import Pregunta, Categoria, Ciclo, PreguntaCiclo
from eva.forms import PreguntaForm, PreguntaAutoForm, PreguntaCoeForm
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from auditoria.apps import GeneradorAuditoria

#Constantes
m_Proceso = "PREGUNTAS"
m_NombreTabla = "pt_pregunta"

class QuestionsListView(ListView):
    model = Pregunta
    template_name = 'preguntas/list.html'
    success_url = reverse_lazy('eva:list-questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['heading'] = 'Mantenimiento Pregunta'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
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
                    newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTabla)
                    GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTabla, newJson, request.user.id)
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                    return response
        except Exception as e:
            data['error'] = str(e)
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
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
                    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                    form.save()
                    newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                    message = f'{self.model.__name__} actualizado correctamente'
                    error = 'No hay error'
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 201
                    GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTabla, kwargs["pk"], newJson, oldJson, request.user.id)
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo actualizar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                    return response
        except Exception as e:
            data['error'] = str(e)
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
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
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            questions = self.get_object()
            questions.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
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
                        #p = PreguntaCiclo(pregunta=form.cleaned_data['pregunta'],
                        #                  ciclo=self.request.POST['cicloID'])
                        #p.save()
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
    model = PreguntaCiclo
    success_url = reverse_lazy('eva:list-questions')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            questions = self.get_object()
            questions.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
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
class PreguntasCoeCreateView(CreateView):
    model = PreguntaCiclo
    form_class = PreguntaCoeForm
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


class PreguntasCoeDeleteView(DeleteView):
    model = PreguntaCiclo
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


@csrf_exempt
def view(request):
    global ex
    data = {}
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'guardar':
            try:
                lista = json.loads(request.POST['lista'])
                for item in lista:
                    preguntacliclo = PreguntaCiclo(pregunta_id=int(item),
                                                   ciclo_id=request.session['cicloId'])
                    preguntacliclo.save()
                return HttpResponse(json.dumps({"result": "ok"}), content_type="application/json")
            except Exception as ex:
                return HttpResponse(json.dumps({"mensaje": "Error al guardar los datos", "result": "bad"}), content_type="application/json")
    else:
        if 'action' in request.GET:
            action = request.GET['action']
        else:
            try:
                list = []
                data['title'] = u'Agregar Preguntas Autoevaluación'
                pc = PreguntaCiclo.objects.filter(pregunta__type=1)
                for p in pc:
                    list.append(p.pregunta_id)
                data['object_list'] = Pregunta.objects.filter(type=1).exclude(id__in=list)
                return render(request, 'preguntas/create_auto.html', data)
            except Exception as ex:
                return HttpResponseRedirect('/')

@csrf_exempt
def coeview(request):
    global ex
    data = {}
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'guardar':
            try:
                lista = json.loads(request.POST['lista'])
                for item in lista:
                    preguntacliclo = PreguntaCiclo(pregunta_id=int(item),
                                                   ciclo_id=request.session['cicloId'])
                    preguntacliclo.save()
                return HttpResponse(json.dumps({"result": "ok"}), content_type="application/json")
            except Exception as ex:
                return HttpResponse(json.dumps({"mensaje": "Error al guardar los datos", "result": "bad"}), content_type="application/json")
    else:
        if 'action' in request.GET:
            action = request.GET['action']
        else:
            try:
                list = []
                data['title'] = u'Agregar Preguntas Coevaluación'
                pc = PreguntaCiclo.objects.filter(pregunta__type=2)
                for p in pc:
                    list.append(p.pregunta_id)
                data['object_list'] = Pregunta.objects.filter(type=2).exclude(id__in=list)
                return render(request, 'preguntas/create_coe.html', data)
            except Exception as ex:
                return HttpResponseRedirect('/')