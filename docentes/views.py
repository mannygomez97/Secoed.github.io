from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from authentication.models import Usuario
from secoed.settings import TOKEN_MOODLE, API_BASE
from docentes.JSONDATA.dataJSON import *
from django.http import HttpResponse
import requests
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from asesor.models import ValorationsCourses
from eva.models import Ciclo2
from eva.models import ResultadoProceso
from decimal import Decimal
from eva.models import Ciclo, ResultadoProcesoModel
import matplotlib.pyplot as plt
import time
from random import randint


def findCategoria(curso):
    params = {"wstoken": TOKEN_MOODLE,
              "wsfunction": "core_course_get_categories",
              "moodlewsrestformat": "json",
              }
    response = requests.post(API_BASE, params)
    if response.status_code == 400:
        return categoria("", "")
    if response:
        r = response.json()
        d = json.dumps(r)
        l = json.loads(d)
        for obj in l:
            if curso.category == obj['id']:
                name = obj['name']
                facultad = obj['description']
                return categoria(name, facultad)


def fs_cursos_actividades(moodle_user, activos):
    cursos_actividades = []
    print(moodle_user)
    params = {"wstoken": TOKEN_MOODLE,
              "wsfunction": "core_enrol_get_users_courses",
              "moodlewsrestformat": "json",
              "userid": moodle_user}
    course_response = requests.post(API_BASE, params)
    print('RESPONSE SEGUIMIENTO')
    print(course_response )
    if course_response:
        r1 = course_response.json()
        d1 = json.dumps(r1)
        l1 = json.loads(d1)
        for obj in l1:
            aux1 = core_enrol_get_users_courses(**obj)
            print('******* aux1 *******')
            print(aux1)
            categoria = findCategoria(aux1)
            params3 = {"wstoken": TOKEN_MOODLE,
                       "wsfunction": "gradereport_user_get_grade_items",
                       "moodlewsrestformat": "json",
                       "courseid": aux1.id,
                       "userid": moodle_user
                       }
            activiti_response = requests.post(API_BASE, params3)
            actividades = []
            if activiti_response:
                r2 = activiti_response.json().get("usergrades")
                d2 = json.dumps(r2)
                l2 = json.loads(d2)
                for obj in l2:
                    aux2 = gradereport_user_get_grade_items(**obj)
                    d3 = json.dumps(aux2.gradeitems)
                    l3 = json.loads(d3)
                    for obj in l3:
                        aux3 = gradeitems(**obj)
                        if aux3.itemname is not None:
                            actividades.append(aux3)
            if actividades:
                temp = course_activities(aux1, actividades, categoria)
                if activos:
                    if aux1.completed == "EN PROCESO":
                        cursos_actividades.append(temp)
                else:
                    if aux1.completed == "COMPLETO":
                        cursos_actividades.append(temp)
    return cursos_actividades


def cursoVScalificaciones(list, identificacion):
    ruta = "static/images/secoed/mtpl1_" + identificacion + ".png"
    label_list = []
    valores = []
    colores = []
    explode_vals = []
    count = 0
    if list:
        for item in list:
            if item.nota > 0.0:
                label_list.append(item.itemname)
                valores.append(item.nota)
                color = '#{:06x}'.format(randint(0, 256 ** 3))
                colores.append(color)
                explode_vals.append(0)
            else:
                count = count + 1
        if count > 0:
            label_list.append("Sin calificar")
            valores.append(count * 10)
            colores.append('#FE6E50')
            explode_vals.append(0.15)
    else:
        label_list.append("Sin actividades")
        valores.append(10)
        colores.append('#F7F724')
        explode_vals.append(0)
    plt.clf()
    plt.pie(x=valores, labels=label_list, colors=colores, autopct='%1.2f%%', shadow=True, explode=explode_vals)
    plt.title('Actividades VS Calificaciones')
    plt.savefig(ruta)
    return ruta


def cursoVSFinalizados(list, identificacion):
    ruta = "static/images/secoed/mtpl2_" + identificacion + ".png"
    count = 0
    count2 = 0
    for item in list:
        if item.nota > 0.0:
            count = count + 1
        else:
            count2 = count2 + 1
    if (count == 0 and count2 == 0):
        valores = [100]
        label_list = ['Sin actividades']
        colores = ['#F7F724']
        explode_vals = [0]
    else:
        if (count > 0 and count2 > 0):
            valores = [count, count2]
            label_list = ['Calificados', 'Sin calificar']
            colores = ['#5AF724', '#FE6E50']
            explode_vals = [0, 0.15]
        else:
            if (count > 0 and count2 == 0):
                valores = [count]
                label_list = ['Calificados']
                colores = ['#5AF724']
                explode_vals = [0]
            elif (count == 0 and count2 > 0):
                valores = [count2]
                label_list = ['Sin calificar']
                colores = ['#FE6E50']
                explode_vals = [0]
    plt.clf()
    plt.pie(x=valores, labels=label_list, colors=colores, autopct='%1.2f%%', shadow=True, explode=explode_vals)
    plt.title('Actividades calificados VS Actividades sin calificar')
    plt.savefig(ruta)
    return ruta


class CursosUserView(View):
    def get(self, request):
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        print(userObj)
        print(Usuario)
        print(request.user.id)
        print(userObj.moodle_user)
        cursos_actividades = []
        if userObj.moodle_user:
            print('entro por aqui')
            cursos_actividades = fs_cursos_actividades(userObj.moodle_user, True)
        greeting = {'heading': 'LISTADO DE CURSOS CON SUS ACTIVIDADES1 Y CALIFICACIONES',
                    'pageview': 'Docentes',
                    'cursos_actividades': cursos_actividades}
        return render(request, 'docentes/cursos_usuario.html', greeting)

    def viewActividades(request, pk):
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        if userObj.moodle_user:
            cursos_actividades = fs_cursos_actividades(userObj.moodle_user, True)
            for obj in cursos_actividades:
                if pk == obj.curso.id:
                    context = {'resultList': obj}
        return render(request, 'docentes/cursos_actividades.html', context)

    def reporteXcurso(request):
        # Create the HttpResponse hearders with PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'atachment; filename = cursos_por_docente.pdf'
        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # Clase usuario
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        # Buscar los cursos del usuario
        temp = fs_cursos_actividades(userObj.moodle_user, True)
        # Cabecera
        # title
        c.setFont("Times-Roman", 12)
        c.drawString(30, 790, 'FACULTAD: POR DEFINIR')
        c.drawString(30, 770, 'CARRERA: POR DEFINIR')
        c.drawString(30, 750, 'LISTADO DE CURSOS POR DOCENTE')
        c.drawString(30, 730, (userObj.nombres + ' ' + userObj.apellidos))
        c.drawString(30, 710, 'FECHA DE EMISIÓN: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        c.drawString(510, 710, 'Pag.1/1')
        # cabecera detalle
        c.setFont("Times-Roman", 10)
        c.line(30, 695, 565, 695)
        c.drawString(30, 680, 'CICLO')
        c.drawString(90, 680, 'CATEGORÍA')
        c.drawString(200, 680, 'CURSO')
        c.drawString(410, 680, 'NIVEL')
        c.drawString(460, 680, 'ESTADO')
        c.drawString(530, 680, 'NOTA')
        c.line(30, 675, 565, 675)
        linea = 665
        c.setFont("Times-Roman", 8)
        for obj in temp:
            try_startdate = datetime.strptime(obj.curso.startdate, '%Y-%m-%d %H:%M:%S')
            try_enddate = datetime.strptime(obj.curso.enddate, '%Y-%m-%d %H:%M:%S')
            periodo = Ciclo2.objects.filter(fecha_inicio__lte=try_startdate, fecha_fin__gte=try_enddate)
            temp2 = None
            if periodo:
                for item in periodo:
                    temp2 = item
            aux = ValorationsCourses.objects.filter(student_id=userObj.moodle_user, course_id=obj.curso.id)
            temp = None
            if aux:
                for item in aux:
                    temp = item
            nivel = 0
            nota = 0.0
            if temp:
                nota = temp.score_course
            periodoT = ""
            if temp2:
                periodoT = temp2.periodo.Tipo + "-" + temp2.ciclo
            c.drawString(30, linea, periodoT)
            if len(obj.categoria.name):
                c.drawString(90, linea, obj.categoria.name[0:20])
            else:
                c.drawString(90, linea, obj.categoria.name)
            c.drawString(200, linea, obj.curso.fullname)
            c.drawString(420, linea, str(nivel))
            c.drawString(460, linea, obj.curso.completed)
            c.drawString(530, linea, str(nota))
            linea = linea - 15
        # save
        c.save()
        pdf = buffer.getvalue();
        buffer.close()
        response.write(pdf)
        return response

    def generarReporte(request, pk, id):
        # Create the HttpResponse hearders with PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'atachment; filename = actividades.pdf'
        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        if pk == 1:
            temp = fs_cursos_actividades(userObj.moodle_user, True)
        else:
            temp = fs_cursos_actividades(userObj.moodle_user, False)
        aux = None
        for item in temp:
            if id == item.curso.id:
                aux = item
        # title
        c.drawImage('static/images/secoed/logo-secoed.png', 30, 710, mask='auto', width=100, height=100)
        c.setFont("Times-Roman", 12)
        c.drawString(150, 790, 'FACULTAD: POR DEFINIR')
        c.drawString(150, 770, 'CARRERA: POR DEFINIR')
        c.drawString(150, 750, 'REGISTRO DEL CURSO Y SUS ACTIVIDADES')
        c.drawString(150, 730, 'APELLIDOS Y NOMBRES: ' + userObj.apellidos + " " + userObj.nombres)
        c.drawString(150, 710, 'IDENTIFICACIÓN: ' + userObj.identificacion)
        c.drawString(350, 710, 'IMPRESO: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # CABECERA DEL CURSO
        c.setFont("Times-Roman", 11)
        c.line(30, 695, 565, 695)
        c.drawString(30, 680, 'DETALLE DEL CURSO')
        c.line(30, 675, 565, 675)
        c.setFont("Times-Roman", 11)
        c.drawString(30, 660, 'NOMBRE: ' + aux.curso.fullname.upper())
        c.drawString(30, 640, 'ESTADO: ' + aux.curso.completed)
        c.drawString(200, 640, 'INICIO: ' + aux.curso.startdate)
        c.drawString(390, 640, 'FIN: ' + aux.curso.enddate)
        # DIAGRAMA PASTEL
        c.drawImage(cursoVScalificaciones(aux.actividades, userObj.identificacion), 30, 360, 
            mask='auto', width=300, height=280)
        c.drawImage(cursoVSFinalizados(aux.actividades, userObj.identificacion), 300, 360, 
            mask='auto', width=300, height=280)
        c.drawString(30, 380, 'ACTIVIDADES')
        c.line(30, 375, 565, 375)
        c.drawString(30, 360, 'NOMBRE DE LA ACTIVIDAD')
        c.drawString(450, 360, 'CALIFICACIÓN')
        c.line(30, 355, 565, 355)
        linea = 340
        for item1 in aux.actividades:
            if item1.itemname:
                # Actividad
                c.setFont("Times-Roman", 11)
                c.drawString(30, linea, item1.itemname or "")
                c.setFont("Times-Roman", 11)
                c.drawString(450, linea, str(item1.nota))
                linea = linea - 15
        # save
        c.save()
        pdf = buffer.getvalue();
        buffer.close()
        response.write(pdf)
        return response


class CalificacionesProceso(View):
    def get(self, request):
        notas_evaluacion = ResultadoProceso.objects.order_by('-cycle').filter(user=request.user.id)
        result = []
        for obj in notas_evaluacion:
            ciclo = get_object_or_404(Ciclo, pk=obj.cycle)
            temp = ResultadoProcesoModel(obj, ciclo);
            result.append(temp)
        greeting = {'heading': 'PROCESO DE COEVALUACIÓN - AUTOEVALUACIÓN',
                    'pageview': 'Docentes',
                    'notas_evaluacion': result}
        return render(request, 'docentes/calificaciones_proceso.html', greeting)


class CalificacionesCursos(View):
    def get(self, request):
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        notas_cursos = ValorationsCourses.objects.order_by('course').filter(studentId=userObj.moodle_user)
        greeting = {'heading': 'CALIFICACION DE LOS CURSOS',
                    'pageview': 'Docentes',
                    'notas_cursos': notas_cursos}
        return render(request, 'docentes/calificaciones_cursos.html', greeting)
