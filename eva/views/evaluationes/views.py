import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from eva.models import Respuesta, ParametrosGeneral, Ciclo, Comprobacion, Usuario, Categoria, Pregunta, DetalleRespuesta
from psycopg2 import IntegrityError


class AutoEvaluacionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['actions']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    evaluated = Respuesta.objects.filter(teacher=int(question['user'])).first()
                    if evaluated is None:
                        answer = Respuesta()
                        answer.teacher = int(question['user'])
                        answer.cycle = int(question['ciclo'])
                        answer.auto_evaluated = True
                        answer.save()
                        for i in question['preguntas']:
                            resp = DetalleRespuesta()
                            resp.answer = answer.id
                            resp.question = int(i['question'])
                            resp.parameter = int(i['parametro'])
                            resp.save()

                    else:
                        data['message'] = 'El usuario ya realizó la autoevaluación'
        except Exception as e:
            data['error'] = str(e)
        except IntegrityError:
            transaction.rollback()
        return JsonResponse(data)

    def get(self, request):
        contador = Pregunta.objects.count()
        questions = Pregunta.objects.filter(type=1)
        categories = Categoria.objects.all()
        val_prg = ParametrosGeneral.objects.filter(parameter=1)
        cycle = Ciclo.objects.filter(is_active=True)
        comprobations = Respuesta.objects.filter(teacher=self.request.user.id).first()
        flag = False
        if comprobations is None:
            flag = True

        context = {'ciclo': cycle.first(),
                   'contador': contador,
                   'comprobacion': flag,
                   'tipo_evaluacion': 'AUTO EVALUACION DOCENTE',
                   'preguntas': questions,
                   'categorias': categories,
                   'valPreg': val_prg}

        return render(request, 'evaluationes/auto-evaluation.html', context)


class CoEvaluacionView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if self.request.is_ajax():
                evaluation = self.request.POST
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get(self, request):

        valPreg = ParametrosGeneral.objects.filter(parameter_id=2)
        cycle = Ciclo.objects.filter(is_active=True)

        comprobaciones = Comprobacion.objects.filter(co_evaluated=request.user.id).exclude(state__isnull=True)
        comprobacion = False
        for evaluado in comprobaciones:
            if evaluado:
                comprobacion = True

        preguntas = Pregunta.objects.filter(type=1)
        categorias = Categoria.objects.all()

        context = {'ciclo': cycle.first(),
                   'comprobacion': comprobacion,
                   'tipo_evaluacion': 'CO EVALUACION DOCENTE',
                   'preguntas': preguntas,
                   'categorias': categorias,
                   'valPreg': valPreg}

        return render(request, 'evaluationes/co-evaluation.html', context)


class AutoEvaluation(CreateView):
    model = Respuesta
    template_name = 'evaluationes/auto-evaluation.html'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if self.request.is_ajax():
                form = self.form_class(request.POST)

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AutoEvaluation'
        context['preguntas'] = Pregunta.objects.filter(type=1)
        context['categorias'] = Categoria.objects.all()
        context['ciclo'] = Ciclo.objects.filter(is_active=True)
        comprobations = Comprobacion.objects.filter(identify=self.request.user.identify).exclude(identify__isnull=True)
        flag = True
        if comprobations.count() > 0:
            flag = False
        context['comprobacion'] = flag
        context['valPreg'] = ParametrosGeneral.objects.filter(parameter=1)
        context['create_url'] = reverse_lazy('eva:auto-evaluation')
        return context


class Coevaluation(CreateView):
    model = Usuario
    template_name = 'evaluationes/co-evaluation.html'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if self.request.is_ajax():
                form = self.form_class(request.POST)

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Docentes por evaluar'
        context['preguntas'] = Pregunta.objects.filter(type=1)
        context['categorias'] = Categoria.objects.all()
        context['ciclo'] = Ciclo.objects.filter(is_active=True)
        comprobations = Comprobacion.objects.filter(identify=self.request.user.identify).exclude(identify__isnull=True)
        flag = True
        if comprobations.count() > 0:
            flag = False
        context['comprobacion'] = flag
        context['valPreg'] = ParametrosGeneral.objects.filter(parameter=1)
        context['create_url'] = reverse_lazy('eva:co-evaluation')
        return context


