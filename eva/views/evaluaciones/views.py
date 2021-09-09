import json

from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from authentication.models import Usuario
from eva.forms import CoevaluacionForm, AutoEvaluacionForm
from eva.models import Respuesta, Docente, DetalleRespuesta, ResultadoProceso, ParametrosGeneral, Ciclo, \
    Pregunta, Categoria


class TeachersPendingEvaluationList(ListView):
    model = Docente
    template_name = 'evaluaciones/list.html'
    success_url = reverse_lazy('eva:list-coevaluar')

    def get_pendings_evaluation(self):
        data = []
        resultado = ResultadoProceso.objects.all()
        docentes = Docente.objects.all().filter(user__usuario_activo=True, is_evaluator=False).select_related('user')
        if resultado.count() == 0:
            data = docentes
        else:
            for r in resultado:
                for d in docentes:
                    if r.user is not d.id:
                        data.append(d)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Docentes pendientes de coevaluar'
        docentes = self.get_pendings_evaluation()
        context['object_list'] = docentes
        context['list_url'] = reverse_lazy('eva:list-coevaluar')
        return context


class AutoEvaluacionCreateView(CreateView):
    model = Docente
    form_class = AutoEvaluacionForm
    template_name = 'evaluaciones/auto-evaluation.html'
    success_url = reverse_lazy('eva:result-evaluation')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Docente.objects.filter(user=int(question['user'])).first()
                    if docente is None:
                        usuario = Usuario.objects.filter(id=request.user.id).first()
                        data['message'] = usuario.nombres + ' Usuario no habilitado para el actual proceso'
                        data['error'] = 'No se pudo realizar el proceso!'
                        return JsonResponse(data)
                    else:
                        answer = Respuesta()
                        answer.teacher = docente.id
                        answer.cycle = int(question['cycle'])
                        answer.type_evaluation = int(question['type'])
                        answer.save()

                        for i in question['questions']:
                            resp = DetalleRespuesta()
                            resp.answer_id = answer.id
                            resp.category = int(i['category'])
                            resp.question = int(i['question'])
                            resp.parameter = int(i['parameter'])
                            resp.save()

                        result = ResultadoProceso.objects.filter(cycle=answer.cycle,
                                                                 user=answer.teacher,
                                                                 coevaluator__isnull=False).first()
                        if result is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.user = answer.teacher
                            result.cycle = answer.cycle

                        details = DetalleRespuesta.objects.filter(answer=answer.id).values('category',
                                                                                           'question',
                                                                                           'parameter')\
                            .order_by('category')

                        ac_tics = 0.00
                        ac_ped = 0.00
                        ac_did = 0.00
                        c_tic = 0
                        c_ped = 0
                        c_did = 0

                        for item in details:
                            if item['category'] == 1:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_tics += float(value['value'])
                                c_tic += 1
                            elif item['category'] == 2:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_ped += float(value['value'])
                                c_ped += 1
                            elif item['category'] == 3:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_did += float(value['value'])
                                c_did += 1

                        aux_tic = round((float(ac_tics) / c_tic) * 100, 2)
                        aux_ped = round((float(ac_ped) / c_ped) * 100, 2)
                        aux_did = round((float(ac_did) / c_did) * 100, 2)

                        result.auto_result_Tic = aux_tic
                        result.auto_result_Ped = aux_ped
                        result.auto_result_Did = aux_did

                        result.Total_Proceso_Auto = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        if result.Total_Proceso_Coe > 0:
                            subtotal = float(result.Total_Proceso_Auto) + float(result.Total_Proceso_Coe)
                            result.Total_Proceso = round(subtotal / 2, 2)

                        result.save()
                        data['message'] = 'Evaluación realizada correctamente.'
        except Exception as e:
            data['error'] = str(e)
            transaction.rollback()
        except IntegrityError:
            transaction.rollback()
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'AutoEvaluación'
        context['object_list'] = Pregunta.objects.filter(type=1)
        context['categories'] = Categoria.objects.all()
        context['parameters'] = ParametrosGeneral.objects.filter(parameter=1)
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['cycle'] = cycle
        teacher = Docente.objects.filter(user=self.request.user.id).first()
        flag = False
        if teacher is not None:
            evaluate = Respuesta.objects.filter(teacher=teacher.id,
                                                cycle=cycle.id,
                                                type_evaluation=1).first()
            if evaluate is None:
                flag = True
        context['verification'] = flag
        context['type'] = 1
        context['type_evaluation'] = 'AUTO EVALUACIÓN DOCENTE'
        return context


class CoevaluacionCreateView(CreateView):
    model = Docente
    form_class = CoevaluacionForm
    template_name = 'evaluaciones/co-evaluation.html'
    success_url = reverse_lazy('eva:list-coevaluation')

    def enroll_course(self, request):
        course = None

        return course

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = self.request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Docente.objects.filter(id=int(request.session['docente'])).first()
                    if docente is None:
                        data['message'] = 'usuario no habilitado para está evaluación'
                        return JsonResponse(data)
                    else:
                        answer = Respuesta()
                        answer.teacher = docente.id
                        answer.cycle = int(question['cycle'])
                        answer.type_evaluation = int(question['type'])
                        answer.save()
                        for i in question['questions']:
                            resp = DetalleRespuesta()
                            resp.answer_id = answer.id
                            resp.category = int(i['category'])
                            resp.question = int(i['question'])
                            resp.parameter = int(i['parameter'])
                            resp.save()
                        evaluated = ResultadoProceso.objects.filter(user=docente.id).first()
                        if evaluated is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.cycle = answer.cycle
                            result.user = docente.id
                        elif evaluated.coevaluator is not None:
                            usuario = Usuario.objects.filter(id=self.request.user.id).first()
                            result = ResultadoProceso.objects.filter(user=docente.id, cycle=answer.cycle).first()
                            result.coevaluator = usuario.identificacion
                        else:
                            data['message'] = 'Usted ya realizó la co evaluación al docente' + docente.name
                            return JsonResponse(data)
                        detalle = DetalleRespuesta.objects.filter(answer=answer.id) \
                            .values('category', 'question', 'parameter').order_by('category')

                        coe_tics = 0.00
                        coe_peda = 0.00
                        coe_dida = 0.00
                        c_tic = 0
                        c_ped = 0
                        c_did = 0

                        for item in detalle:
                            if item['category'] == 1:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_tics += float(value['value'])
                                c_tic += 1
                            elif item['category'] == 2:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_peda += float(value['value'])
                                c_ped += 1
                            elif item['category'] == 3:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_dida += float(value['value'])
                                c_did += 1

                        aux_tic = round((float(coe_tics) / c_tic) * 100, 2)
                        aux_ped = round((float(coe_peda) / c_ped) * 100, 2)
                        aux_did = round((float(coe_dida) / c_did) * 100, 2)

                        result.coe_result_Tic = aux_tic
                        result.coe_result_Ped = aux_ped
                        result.coe_result_Did = aux_did

                        result.Total_Proceso_Coe = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        if result.Total_Proceso_Auto > 0:
                            subtotal = float(result.Total_Proceso_Auto) + float(result.Total_Proceso_Coe)
                            result.Total_Proceso = round(subtotal / 2, 2)

                        result.save()
                        del request.session['docente']
                        data['message'] = 'Evaluación realizada correctamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['docente'] = self.request.GET.get('docente')
        context['heading'] = 'Coevaluacion'
        url = reverse_lazy('eva:list-coevaluar')
        context['list_url'] = url
        docente = Docente.objects.filter(user=self.request.user.id).first()
        if docente is not None:
            if docente.is_evaluator is False:
                context['retorno'] = url
                return context
            return context
        context['object_list'] = Pregunta.objects.filter(type=2)
        context['categories'] = Categoria.objects.all()
        context['parameters'] = ParametrosGeneral.objects.filter(parameter=2)
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['cycle'] = cycle
        teacher = int(self.request.GET.get('docente'))
        evaluate = Respuesta.objects.filter(teacher=teacher, cycle=cycle.id, type_evaluation=2).first()
        flag = False
        if evaluate is None:
            flag = True
        context['verification'] = flag
        context['type'] = 2
        context['type_evaluation'] = 'COE EVALUACION DOCENTE'
        return context
