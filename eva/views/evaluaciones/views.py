import json
import requests
from django.core.mail import send_mail

from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from authentication.models import Usuario
from eva.forms import CoevaluacionForm, AutoEvaluacionForm
from eva.models import Respuesta, DetalleRespuesta, ResultadoProceso, ParametrosGeneral, Ciclo, \
    Pregunta, Categoria
from secoed.settings import TOKEN_MOODLE, API_BASE, COURSE_TICS, COURSE_DIDACTIC, COURSE_PEDAGOGY


class TeachersPendingEvaluationList(ListView):
    model = Usuario
    template_name = 'evaluaciones/list.html'
    success_url = reverse_lazy('eva:list-coevaluar')

    def get_pendings_evaluation(self):
        data = []
        resultado = ResultadoProceso.objects.filter(coevaluator__isnull=False)
        docentes = Usuario.objects.filter(usuario_activo=True, rol_moodle__codigo__gte=5)
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
    model = Usuario
    form_class = AutoEvaluacionForm
    template_name = 'evaluaciones/auto-evaluation.html'
    success_url = reverse_lazy('eva:result-evaluation')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        flag_p = False
        flag_d = False
        flag_t = False
        message = ''
        course = ''
        content = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Usuario.objects.filter(rol_moodle__codigo__gte=5, id=self.request.user.id).first()
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

                        details = DetalleRespuesta.objects.filter(answer=answer.id).values('category',
                                                                                           'question',
                                                                                           'parameter') \
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
                        total_auto = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        result = ResultadoProceso.objects.filter(cycle=answer.cycle,
                                                                 user=answer.teacher,
                                                                 coevaluator__isnull=False).first()
                        if result is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.user = answer.teacher
                            result.cycle = answer.cycle

                            result.auto_result_Tic = aux_tic
                            result.auto_result_Ped = aux_ped
                            result.auto_result_Did = aux_did

                            result.Total_Proceso_Auto = total_auto

                            result.save()

                            message = 'Autoevaluación concluida correctamente'
                            error = ''
                            response = JsonResponse({'message': message, 'error': error})
                            response.status_code = 201
                            return response
                        else:
                            result = ResultadoProceso.objects. \
                                filter(cycle=answer.cycle,
                                       user=answer.teacher,
                                       coevaluator__isnull=False).update(auto_result_Tic=aux_tic,
                                                                         auto_result_Ped=aux_ped,
                                                                         auto_result_Did=aux_did,
                                                                         Total_Proceso_Auto=total_auto)
                            if result:
                                obj = ResultadoProceso.objects.filter(cycle=answer.cycle, user=answer.teacher,
                                                                      coevaluator__isnull=False).first()

                                if obj.Total_Proceso_Coe > 0:
                                    subtotal = float(obj.Total_Proceso_Auto) + float(obj.Total_Proceso_Coe)
                                    obj.Total_Proceso = round(subtotal / 2, 2)

                                    obj.save()

                                    result_ped = (float(obj.auto_result_Ped) + float(obj.coe_result_Ped)) / 2
                                    result_did = (float(obj.auto_result_Did) + float(obj.coe_result_Did)) / 2
                                    result_tic = (float(obj.auto_result_Tic) + float(obj.coe_result_Tic)) / 2
                                    message = ''

                                    if result_ped > 85:

                                        data[
                                            'message'] = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                         'èxitosa '
                                    else:
                                        course = switch_course(COURSE_PEDAGOGY)
                                        message = enroll_course_evaluation(self.request.user, COURSE_PEDAGOGY)
                                        response = JsonResponse({'message': message})
                                        flag_p = True
                                    if result_did > 85:
                                        data[
                                            'message'] = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                         'èxitosa '
                                    else:
                                        course = switch_course(COURSE_DIDACTIC)
                                        message = enroll_course_evaluation(self.request.user, COURSE_DIDACTIC)
                                        response = JsonResponse({'message': message})
                                        flag_d = True
                                    if result_tic > 85:
                                        data['message'] = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                         'èxitosa '
                                    else:
                                        course = switch_course(COURSE_TICS)
                                        message = enroll_course_evaluation(self.request.user, COURSE_TICS)
                                        response = JsonResponse({'message': message})
                                        flag_t = True

                                    content = {
                                        'nombres': docente.nombres,
                                        'apellidos': docente.apellidos,
                                        'course': course,
                                    }

                                if flag_d is not None:
                                    send_mail_notification(docente.email, content)
                                if flag_t is not None:
                                    send_mail_notification(docente.email, content)
                                if flag_p is not None:
                                    send_mail_notification(docente.email, content)
                                return response
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
        teacher = Usuario.objects.filter(id=self.request.user.id).first()
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


course_moodle = {
    '10': 'Pedagogía',
    '11': 'Didactica',
    '12': 'TICs',
}


def switch_course(course):
    return course_moodle.get(course, "NA")


def send_mail_notification(email, content):
    subject = 'Matriculación Automatica'
    email_template_name = "evaluaciones/enroll-email.txt"
    c = content
    email_1 = render_to_string(email_template_name, c)
    send_mail(subject, email_1, 'secoed.web@gmail.com', [email], fail_silently=False)


def enroll_course_evaluation(user: Usuario, course):
    params = {
        "wstoken": TOKEN_MOODLE,
        "wsfunction": "enrol_manual_enrol_users",
        "moodlewsrestformat": "json",
        "enrolments[0][userid]": user.moodle_user,
        "enrolments[0][courseid]": course,
        "enrolments[0][roleid]": user.rol_moodle.codigo
    }
    c = ''
    response = requests.post(API_BASE, params)

    if response.ok:
        c = switch_course(course)
        data = 'Alumno matriculado, ' + user.nombres + ' ' + user.apellidos + 'correctamente.' + c
    else:
        data = 'Hubo un problema al matricular al alumno, ' + user.nombres + ' ' + user.apellidos + 'en el curso ' + c
    return data


class CoevaluacionCreateView(CreateView):
    model = Usuario
    form_class = CoevaluacionForm
    template_name = 'evaluaciones/co-evaluation.html'
    success_url = reverse_lazy('eva:list-coevaluation')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        content = {}
        flag_p = False
        flag_d = False
        flag_t = False
        message = ''
        course = ''
        try:
            action = self.request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Usuario.objects.filter(id=int(request.session['docente'])).first()
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
                        total_coe = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        evaluated = ResultadoProceso.objects.filter(user=docente.id, cycle=answer.cycle).first()
                        if evaluated is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.cycle = answer.cycle
                            result.user = docente.id
                            result.coevaluator = docente.identificacion

                            result.coe_result_Tic = aux_tic
                            result.coe_result_Ped = aux_ped
                            result.coe_result_Did = aux_did

                            result.Total_Proceso_Coe = total_coe

                            result.save()
                            message = 'Coevaluación concluida correctamente'
                            error = ''
                            response = JsonResponse({'message': message, 'error': error})
                            response.status_code = 201
                            return response
                        else:
                            result = ResultadoProceso.objects. \
                                filter(cycle=answer.cycle, user=answer.teacher)\
                                .update(coevaluator=docente.identificacion,
                                        coe_result_Tic=aux_tic,
                                        coe_result_Ped=aux_ped,
                                        coe_result_Did=aux_did,
                                        Total_Proceso_Coe=total_coe)

                            if result:

                                obj = ResultadoProceso.objects.filter(cycle=answer.cycle, user=answer.teacher,
                                                                      coevaluator__isnull=False).first()

                                subtotal = float(obj.Total_Proceso_Auto) + float(obj.Total_Proceso_Coe)
                                obj.Total_Proceso = round(subtotal / 2, 2)
                                obj.save()

                                result_ped = (float(obj.auto_result_Ped) + float(obj.coe_result_Ped)) / 2
                                result_did = (float(obj.auto_result_Did) + float(obj.coe_result_Did)) / 2
                                result_tic = (float(obj.auto_result_Tic) + float(obj.coe_result_Tic)) / 2

                                if result_ped > 85:
                                    message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                              'èxitosa en Pedagogía'
                                else:
                                    course = switch_course(COURSE_PEDAGOGY)
                                    message = enroll_course_evaluation(docente, COURSE_PEDAGOGY)
                                    response = JsonResponse({'message': message})
                                    flag_p = True
                                if result_did > 85:
                                    message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                              'èxitosa en '
                                else:
                                    course = switch_course(COURSE_DIDACTIC)
                                    message = enroll_course_evaluation(docente, COURSE_DIDACTIC)
                                    response = JsonResponse({'message': message})
                                    flag_d = True
                                if result_tic > 85:
                                    message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                              'èxitosa en '
                                else:
                                    course = switch_course(COURSE_TICS)
                                    message = enroll_course_evaluation(docente, COURSE_TICS)
                                    response = JsonResponse({'message': message})
                                    flag_t = True

                                content = {
                                    'nombres': docente.nombres,
                                    'apellidos': docente.apellidos,
                                    'course': course,
                                }

                            del request.session['docente']

            if flag_d is not None:
                send_mail_notification(docente.email, content)
            if flag_t is not None:
                send_mail_notification(docente.email, content)
            if flag_p is not None:
                send_mail_notification(docente.email, content)
            return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['docente'] = self.request.GET.get('docente')
        context['heading'] = 'Coevaluacion'
        url = reverse_lazy('eva:list-coevaluar')
        context['list_url'] = url
        docente = Usuario.objects.filter(id=self.request.user.id).first()
        if docente is not None:
            if docente.rol_moodle.codigo != 4:
                context['retorno'] = url
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
