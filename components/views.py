from email import message
from multiprocessing import context
from traceback import print_tb
from django import conf
from django.http.response import HttpResponse

from asesor.models import ValorationsCourses
from .forms import CourseCicleCarrerForm, CourseAsesorForm, CourseAsesorEditForm
from .models import Evaluation as EvaluationModel, CourseCicleCarrer, CourseAsesor
from components.Evaluation import Evaluation
from components.utils import render_to_pdf
from conf.forms import MenuForm
from conf.models import Menu, Rol
from secoed.settings import EMAIL_HOST_USER
from typing import Any, Dict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.db.models import CharField, Value as V, F, Q
from django.db.models.functions import Concat
from components.models import AprobacionCurso, CursoAsesores
from cursos.models import CoursesMoodle
from authentication.models import Usuario, Rol, RolUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
import io, json
from datetime import datetime, date
from django.core.mail import send_mail
from asesor.services import obtener_datos

from django.contrib.auth.decorators import login_required  # login

from components.forms import CriterioForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Settings
from secoed.settings import TOKEN_MOODLE, API_BASE

# IMPORT
import datetime
from django.forms.models import fields_for_model, model_to_dict
import requests
from auditoria.apps import GeneradorAuditoria

###########################  Recursos para consumir la api###########################

apiBase = API_BASE


def wsfunction(function):
    return {
        "wstoken": TOKEN_MOODLE,
        "wsfunction": function,
        "moodlewsrestformat": "json",
    }


######################################################################################

##### filtrar asesor
def asesor(request, *args, **kwargs):
    data_roles = RolUser.objects.filter(rol=4).values('rol_id', 'user_id')

    asesores = []
    for data in data_roles:
        asesores.append(data['user_id'])

    asesores = Usuario.objects.filter(id__in=asesores)
    ase = Usuario.objects.annotate(names=Concat('nombres', V(' '), 'apellidos'))

    asesor = ase.filter(names__icontains=kwargs["asesor"]).distinct().values('id', nombre=Concat('nombres', V(' '),
                                                                                                 'apellidos'))
    return JsonResponse({'data': list(asesor)})


#############Guardar asesor curso
@csrf_exempt
def guardarAsesorCurso(request, *args, **kwargs):
    if (request.method == "POST"):
        a = json.loads(request.body)
        ase = Usuario.objects.annotate(names=Concat('nombres', V(' '), 'apellidos'))
        for i in ase:
            if (i.names == a['result'][2]):
                palabra = a['result'][2].split()
                # AsesorCursoAsesor.objects.create(relacion = palabra[0]+'_'+a['result'][1],asesor = i, curso = AsesorCursos.objects.get(id_curso = a['result'][0]))
                CursoAsesores.objects.create(id_curso=a['result'][0], id_asesor=i.id)
                return JsonResponse({"estado": "Se le asignó curso correctamente al asesor"}, safe=False)
        return JsonResponse({"estado": "El asesor designado no existe, seleccione bien al asesor que desea asignar"},
                            safe=False)


##################################
def buildEmail(course):
    subject = "Welcome to Skote  Membership"
    email_template_name = "components/email/email-notify.txt"
    email_text = "jorge.penaz@ug.edu.ec"  # "jucacero@hotmail.com"
    context = {
        "courseName": course["fullname"]
    }
    template_email = render_to_string(email_template_name, context)
    # Array de destinatarios
    send_mail(subject, template_email, EMAIL_HOST_USER, [email_text], fail_silently=False)


@csrf_exempt
def getPDF(request):
    eva = Evaluation(request)
    eva.saveEvaluation()
    return render_to_pdf(eva.getLastEvaluationBD(), 'components/templates_pdf/evaluation_final.html')


def sendEmail(request):
    coursesList: Any = obtener_datos({
        "wsfunction": "core_course_get_courses",
    })
    finishCourses = []
    # courseSelected = [course for course in coursesList['courses'] if  course['id'] == courseId ]
    for course in coursesList:
        justNow = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        endDate = datetime.datetime.fromtimestamp(course['enddate'])
        if (justNow == endDate):
            # Send email
            buildEmail(course)
            finishCourses.append(course['fullname'])
    return JsonResponse({
        "finished_courses": finishCourses,
    })


def cursoA(request, *args, **kwargs):
    params = wsfunction("core_course_get_courses")
    response = requests.get(apiBase, params)

    curso = []
    for data in response.json():
        dat = CursoAsesores.objects.filter(id_curso=data['id'])
        if dat:
            print("nada")
        else:
            curso.append(data)

    datos = {"datas": curso}

    if kwargs["curso"] != "null":
        context = {"context": [p for p in datos["datas"] if kwargs['curso'].lower() in p['fullname'].lower()]}
    else:
        context = {"context": datos['datas']}
    return JsonResponse({'data': context})


# todos los cursos

def cursosTodos(request, *args, **kwargs):
    params = wsfunction("core_course_get_courses")
    response = requests.get(apiBase, params)

    curso = []
    for data in response.json():
        dat = CursoAsesores.objects.filter(id_curso=data['id'])
        if dat:
            print("nada")
        else:
            curso.append(data)

    datos = {"datas": curso}
    context = {"context": datos['datas']}
    return JsonResponse({'data': context})


##########################################################################################################################################
##########################################################################################################################################

# Constantes
m_ProcesoRequisito = "REQUISITO-CURSO"
m_NombreTablaAprobacionCurso = "components_aprobacioncurso"


def menu(request):
    menusview = AprobacionCurso.objects.filter(estado=True).order_by('nivel')
    greeting = {'heading': "REQUISITO DEL CURSO", 'pageview': "Gestor", "menusview": menusview}
    return render(request, 'components/proyecto/components-formrequisito.html', greeting)


def requisito(request):
    if request.method == 'POST':
        ##editarField
        request.POST._mutable = True
        criterioForm = CriterioForm(request.POST)
        if criterioForm.is_valid():
            # criterioForm.save()
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.create(nivel=criterio_data.get("nivel"), criterio=criterio_data.get("criterio"),
                                           semaforo=criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se registro correctamente", "success")
            newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaAprobacionCurso)
            GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaAprobacionCurso, newJson, request.user.id)
        else:
            messages.error(request, "No se puedo registrar", "error")
            GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoRequisito, "No se puedo registrar", request.user.id)
        return redirect('requisito')
    else:
        menuFormView = CriterioForm()
        menu = AprobacionCurso()
        view = False
        context = {'menuFormView': menuFormView, 'requisito': menu, 'view': view}
    return render(request, 'components/proyecto/formrequisito.html', context)


# Editar los datos de un modulo por su pk
class UpdateRequisito(View):
    requisito = lambda self, id: get_object_or_404(AprobacionCurso, pk=id)

    def post(self, request, *args, **kwargs):
        criterioForm = CriterioForm(request.POST, model_to_dict(self.requisito(kwargs["pk"])))
        if criterioForm.is_valid():
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAprobacionCurso, kwargs)
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.filter(id=kwargs["pk"]).update(nivel=criterio_data.get("nivel"),
                                                                   criterio=criterio_data.get("criterio"),
                                                                   semaforo=criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se edito correctamente", "success")
            newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAprobacionCurso, kwargs)
            GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaAprobacionCurso, kwargs["pk"], newJson,
                                                            oldJson, request.user.id)
            return redirect('requisito')

    def get(self, request, *args, **kwargs):
        menuFormView = CriterioForm(model_to_dict(self.requisito(kwargs["pk"])))
        view = False
        context = {'menuFormView': menuFormView, 'menu': self.requisito(kwargs["pk"]), 'view': view}
        return render(request, 'components/proyecto/formrequisito.html', context)


def deleteRequisito(request, pk):
    requisito = get_object_or_404(AprobacionCurso, pk=pk)
    if requisito:
        dictionary = {'pk': pk}
        oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAprobacionCurso, dictionary)
        requisito.delete()
        messages.success(request, "Se ha eliminado correctamente", "success")
        GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaAprobacionCurso, pk, oldJson, request.user.id)
    return redirect('requisito')


def deleteAsignacion(request, pk):
    deleteA = get_object_or_404(CursoAsesores, pk=pk)
    if deleteA:
        deleteA.delete()
        messages.success(request, "Se ha eliminado correctamente", "success")
    return redirect('forms-asesor')


# AJAX
@login_required
def loadRequisito(request):
    # modulo_id = request.GET.get('modulo_id')
    modulo_id = request.GET.get('id')
    menus = Menu.objects.filter(Q(modulo_id=modulo_id) & Q(href='')).order_by('descripcion')
    return render(request, 'components/proyecto/requisitoList.html', {'menus': menus})


################################################################


class FormEducacion(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Asesores por cursos."
        greeting['pageview'] = "Forms"

        queryset = request.GET.get("buscar")

        if queryset:
            greeting['asesor'] = AsesorAsesor.objects.filter(
                Q(nombres__icontains=queryset) | Q(apellidos__icontains=queryset)).distinct()
            greeting['curso'] = AsesorCursoAsesor.objects.filter

        return render(request, 'components/proyecto/components-formeducation.html', greeting)


####################Vista de asesores que ya se encuentran asignados

class FormAsesor(View):
    def get(self, request):
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase, params)
        datos = []
        #if response.json():
        if response:
            for data in response.json():
            #for data in response:
                curs = CursoAsesores.objects.filter(id_curso=data['id']).values('id', 'id_asesor')
                if curs:
                    a = Usuario.objects.filter(id=curs[0]['id_asesor']).values(
                        names=Concat('nombres', V(' '), 'apellidos'))

                    context = {"id": curs[0]['id'], "curso": data["fullname"], "asesor": a[0]["names"]}
                    datos.append(context)
                    print('entra aaaaaaaa')
                    print(datos)
        greeting = {}
        greeting['heading'] = "Curso Designado a Asesor"
        greeting['pageview'] = "Formulario test"
        if datos:
            greeting['cursos'] = datos

        return render(request, 'components/proyecto/components-formasesor.html', greeting)


class FormEducaciona(View):
    @csrf_exempt
    def get(self, request):
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase, params)
        greeting = {}
        greeting['heading'] = "Avance del curso"
        greeting['pageview'] = "Forms"
        if response:
            greeting['cursos'] = response.json()

        return render(request, 'components/proyecto/components-formeducation1.html', greeting)


class listadoAsesores(View):
    def get(self, request):
        params = wsfunction("core_enrol_get_enrolled_users")
        params.update(courseid=request.GET.get('id'))
        response = requests.get(apiBase, params)

        greeting = {"heading": "Listado de Docentes", "pageview": "Forms", "curso": request.GET.get('id')}
        if response:
            datos = [rol for rol in response.json() if rol.get('roles') and rol['roles'][0]['roleid'] == 5]

            if datos:
                greeting.update(context=datos)
                if greeting.get("context"):
                    for fecha in greeting["context"]:
                        fecha.update(lastaccess=datetime.datetime.fromtimestamp(fecha['lastaccess']))

        return render(request, 'components/proyecto/components-listadoAsesores.html', greeting)


class actividades(View):
    def get(self, request):
        params = wsfunction("gradereport_user_get_grade_items")
        params.update(courseid=request.GET.get('curso'))
        response = requests.get(apiBase, params)

        if response.json().get("usergrades"):
            actividad = [actividades for actividades in response.json()["usergrades"] if
                         actividades["userid"] == int(request.GET.get('id'))]
            print(actividad)
        else:
            actividad = None

        greeting = {"heading": "Listado de Actividades", "pageview": "Forms"}
        if actividad:
            actividades = [dato for dato in actividad[0]["gradeitems"]]
            cont = 0
            suma = 0
            nota = 0
            if actividades:
                greeting.update(context=actividades)
                for i in actividades:
                    if i["graderaw"]:
                        nota = (i["graderaw"] * 100) / i["grademax"]
                        suma = nota + suma
                        cont = cont + 1
                if suma == 0:
                    semaforo = 0
                else:
                    semaforo = suma / cont
                    greeting.update(semaforo=self.semaforo(semaforo))
        return render(request, 'components/proyecto/modalActividades.html', greeting)

    def semaforo(self, semaforo):
        # metodo lambda sirver para obtener los criterios de acuerdo a los niveles
        criterio = lambda level: AprobacionCurso.objects.filter(nivel=level) if AprobacionCurso.objects.filter(
            nivel=level) else None
        # condiciones de acuerdo a los niveles de semàforo
        criterios = criterio(1) if semaforo < 30 else criterio(2) if semaforo < 70 else criterio(
            3) if semaforo < 90 else criterio(4)
        return criterios


class FormRequisito(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Requisito del curso"
        greeting['pageview'] = "Forms"
        coursesList: Any = obtener_datos({
            "wsfunction": "core_course_get_courses",
        })
        return render(request, 'components/proyecto/components-formrequisito.html', greeting)


class FormEvaluation(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Evaluation Docente"
        greeting['pageview'] = "Evaluación"
        coursesList: Any = obtener_datos({
            "wsfunction": "core_course_get_courses",
        })
        # greeting['curso'] = AsesorCursoAsesor.objects.filter(~Q(curso = AsesorCursos.objects.all() )).values('curso__id_curso','curso__tipo')
        listcurso=[]

        return render(request, 'components/proyecto/components-formevaluation.html', {
            "greeting": greeting,
            "courses": [course['fullname'] for course in (coursesList)]
        })


def historialEvaluations(request):
    evaluations = EvaluationModel.objects.all()

    return render(request, 'components/proyecto/components-historial_eva.html', {
        "heading": "HIstorial de Evaluaciones",
        'pageview': "Evaluación",
        'evaluations': evaluations,
    })


def historialEvaluation(request, id):
    evaluation = EvaluationModel.objects.get(pk=id)
    return render_to_pdf({"course": evaluation.course, "questions": evaluation.question},
                         'components/templates_pdf/evaluation_final.html')


@login_required
def course_list(request):
    u = "Lista de cursos"

    asesor_list = CursoAsesores.objects.all().values('id_curso')
    curso_asesor = []
    for i in asesor_list:
        curso_asesor.append(i['id_curso'])

    apiBase = API_BASE
    print('siguiendo listado_estudiantes modulo components')
    params = {"wstoken": TOKEN_MOODLE,
              "wsfunction": "core_course_get_courses",
              "moodlewsrestformat": "json",
              }
    context = {}
    try:
        response = requests.post(apiBase, params)
        if response.status_code == 400:
            return render(request, 'lista_cursos.html', context={"context": "Bad request", 'heading': u})
        if response:
            res_new = []
            res = response.json()
            for x in res:
                if date.fromtimestamp(x['enddate']) >= date.today():
                    if x['id'] not in curso_asesor:
                        res_new.append(x)
            context = {"context": res_new, 'heading': u, 'status': 'A'}
    except Exception as e:
        print(e)
    return render(request, 'components/asesor/course_list.html', context)


@login_required
def asesor_list(request, id, fullname):
    u = fullname
    t = "Lista de asesores"
    asesor_list = RolUser.objects.filter(rol__descripcion='Asesor')
    context = {"context": asesor_list, 'heading': u, 'pageview': t, 'course_id': id}
    return render(request, 'components/asesor/asesor_list.html', context)


@login_required
def asesor_course(request, id, course_id):
    save_asesor_course = CursoAsesores(
        id_curso=int(course_id),
        id_asesor=int(id),
        estado=True
    )
    save_asesor_course.save()
    return redirect('/components/course_list')


# Nueva version de asiganción


m_ProcesoCursoPeriodo = "CURSO-PERIODO"
m_NombreTablaCursoPeriodo = "components_courseciclecarrer"
m_NombreTablaCursoMoodle = "cursos_coursesmoodle"
def courseCicleCarrerList(request):
    t = "Mantenimientos"
    u = "Parametrización curso ciclo "
    courses = CourseCicleCarrer.objects.all()
    context = {'courses': courses, 'heading': u, 'pageview': t}
    return render(request, 'components/proyecto/list-course-period.html', context)


def addCourseCicleCarrer(request):
    if request.method == 'POST':
        form = CourseCicleCarrerForm(request.POST)
        if form.is_valid():
            countParams = CourseCicleCarrer.objects.filter(course=request.POST['course']).count()
            userId = Usuario.objects.filter(username__icontains=request.session['username']).values('id')[0]['id']
            if countParams == 0:
                register = form.save(commit=False)
                register.userCreated = Usuario.objects.get(id=int(userId))
                register.save()
                messages.add_message(request, messages.SUCCESS,
                                     message="Curso asociado a una ciclo y carrera de manera exitosa!")

                newJsonCursoPeriodo = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCursoPeriodo)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaCursoPeriodo, newJsonCursoPeriodo, request.user.id)

                courseSecoed = CoursesMoodle.objects.get(id=request.POST['course'])
                courseSecoed.status = True
                courseSecoed.save()
                newJsonCursoMoodle = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCursoMoodle)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaCursoMoodle, newJsonCursoMoodle,
                                                           request.user.id)

                return redirect('course_cicle_carrer')
            else:
                messages.add_message(request, messages.WARNING,
                                     message="Curso ya se encuentra asociado a un cilo y carrera!")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCursoPeriodo, "Curso ya se encuentra "
                                                                                      "asociado a un cilo y carrera!",
                                                               request.user.id)
                return redirect('course_cicle_carrer')
    else:
        form = CourseCicleCarrerForm()
    return render(request, 'components/proyecto/add-course-cicle.html', {'form': form})


def deleteCourseCicle(request, id):
    try:
        courseMood = CourseCicleCarrer.objects.filter(id=id).values('course')[0]['course']
        coursesValCount = ValorationsCourses.objects.filter(courseCicleCarrer=id).count()
        if coursesValCount == 0:
            print('Prodece borrado')
            kwargsCursoPeriodo = {'pk':id}
            oldJsonCursoperiodo= GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCursoPeriodo, kwargsCursoPeriodo)
            course_cicle = CourseCicleCarrer.objects.get(id=id)
            course_cicle.delete()
            messages.add_message(request, messages.SUCCESS,
                                 message="Curso eliminado de manera exitosa!")

            kwargsCursoMoodle = {'pk':courseMood}
            oldJsonCursoMoodle= GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCursoMoodle, kwargsCursoMoodle)
            courseSecoed = CoursesMoodle.objects.get(id=courseMood)
            courseSecoed.status = False
            courseSecoed.save()

            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaCursoPeriodo, kwargsCursoPeriodo["pk"], oldJsonCursoperiodo, request.user.id)
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaCursoMoodle, kwargsCursoMoodle["pk"], oldJsonCursoMoodle, request.user.id)
            return redirect('course_cicle_carrer')
        else:
            messages.add_message(request, messages.WARNING,
                                 message="El curso no se puede desvincular debido a que tiene notas asociadas!")
            GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCursoPeriodo, "El curso no se puede desvincular "
                                                                                  "debido a que tiene notas asociadas!",
                                                           request.user.id)
    except Exception as e:
        print(e)
        GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCursoPeriodo, str(e), request.user.id)
    return redirect('course_cicle_carrer')



# Constantes
m_ProcesoCursoAsesor = "CURSO-ASESOR"
m_NombreTablaCursoAsesor = "components_courseciclecarrer"

def courseAsesorList(request):
    t = "Mantenimientos"
    u = "Parametrización curso asesor "

    courseAsesor = CourseAsesor.objects.all()
    context = {'courseAsesor': courseAsesor, 'heading': u, 'pageview': t}
    return render(request, 'components/proyecto/list-course-asesor.html', context)


def addCourseAsesor(request):
    if request.method == 'POST':
        form = CourseAsesorForm(request.POST)
        if form.is_valid():
            countParams = CourseAsesor.objects.filter(course=request.POST['course']).count()
            userId = Usuario.objects.filter(username__icontains=request.session['username']).values('id')[0]['id']

            if countParams == 0:
                register = form.save(commit=False)
                register.userCreated = Usuario.objects.get(id=int(userId))
                register.save()
                messages.add_message(request, messages.SUCCESS,
                                     message="Curso asociado a un asesor de manera exitosa!")

                courseSecoed = CourseCicleCarrer.objects.get(id=request.POST['course'])
                courseSecoed.assigned = True
                courseSecoed.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCursoAsesor)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaCursoAsesor, newJson, request.user.id)
                return redirect('course_asesor')
            else:
                messages.add_message(request, messages.WARNING,
                                     message="Curso ya se encuentra asociado asesor!")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCursoAsesor, "Curso ya se encuentra asociado "
                                                                                      "asesor!",
                                                               request.user.id)
                return redirect('course_asesor')
    else:
        form = CourseAsesorForm()
    return render(request, 'components/proyecto/add-course-asesor.html', {'form': form})


def updateCourseAsesor(request, id):
    courseAsesor = CourseAsesor.objects.get(id=id)
    if request.method == 'POST':
        form = CourseAsesorEditForm(request.POST, instance=courseAsesor)
        if form.is_valid():
            kwargs = {'pk': id}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCursoAsesor, kwargs)
            userId = Usuario.objects.filter(username__icontains=request.session['username']).values('id')[0]['id']
            updated = form.save(commit=False)
            updated.userCreated = Usuario.objects.get(id=int(userId))
            updated.save()
            newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCursoAsesor)
            messages.add_message(request, messages.SUCCESS,
                                 message="Relación editada de manera exitosa!")
            GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaCursoAsesor, kwargs["pk"], newJson, oldJson,
                                                            request.user.id)
            return redirect('course_asesor')
    else:
        form = CourseAsesorEditForm(instance=courseAsesor)
    return render(request, 'components/proyecto/add-course-asesor.html', {'form': form})


def deleteCourseAsesor(request, id):
    try:
        courseCicle = CourseAsesor.objects.filter(id=id).values('course')[0]['course']
        courseAsesor = CourseAsesor.objects.filter(id=id).values('asesor')[0]['asesor']

        coursesValCount = ValorationsCourses.objects.filter(userCreated=courseAsesor,
                                                            courseCicleCarrer=courseCicle).count()
        print(coursesValCount)
        course_asesor = CourseAsesor.objects.get(id=id)

        if coursesValCount == 0:
            print('en cero para ser borrado')
            kwargs = {'pk': id}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCursoAsesor, kwargs)
            course_asesor.delete()
            messages.add_message(request, messages.SUCCESS,
                                 message="Curso desasociado del asesor de manera exitosa!")

            courseSecoed = CourseCicleCarrer.objects.get(id=courseCicle)
            courseSecoed.assigned = False
            courseSecoed.save()

            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaCursoAsesor, kwargs["pk"], oldJson, request.user.id)
            return redirect('course_asesor')
            pass
        else:
            messages.add_message(request, messages.WARNING,
                                 message="El asesor no se puede desvincular debido a que tiene notas asociadas!")
            GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCursoAsesor, "El asesor no se puede desvincular"
                                                                                 " debido a que tiene notas asociadas!",
                                                           request.user.id)
    except Exception as e:
        print(e)
        GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCursoAsesor, str(e), request.user.id)
    return redirect('course_asesor')