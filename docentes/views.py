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
from asesor.models import valoration_course_student
from eva.models import ResultadoProceso
from decimal import Decimal


def fs_cursos_actividades(moodle_user):
    cursos_actividades = []
    params = {"wstoken": TOKEN_MOODLE,
              "wsfunction": "core_enrol_get_users_courses",
              "moodlewsrestformat": "json",
              "userid": moodle_user}
    course_response = requests.post(API_BASE, params)
    if course_response:
        r1 = course_response.json()
        d1 = json.dumps(r1)
        l1 = json.loads(d1)
        for obj in l1:
            aux1 = core_enrol_get_users_courses(**obj)
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
                        actividades.append(aux3)
            temp = course_activities(aux1, actividades)
            cursos_actividades.append(temp)
    print(cursos_actividades)
    return cursos_actividades


def getEstado(state):
    if state == 1:
        return 'COMPLETO'
    else:
        return 'INCOMPLETO'


def getTipo(tracking):
    if tracking == 0:
        return 'NINGUNO'
    elif tracking == 1:
        return 'MANUAL'
    else:
        return 'AUTOMÁTICO'


class SeguimientoView(View):
    def get(self, request):
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        cursos_actividades = []
        if userObj.moodle_user:
            cursos_actividades = fs_cursos_actividades(userObj.moodle_user)
        greeting = {'heading': 'Seguimiento de actividades',
                    'pageview': 'Docentes',
                    'cursos_actividades': cursos_actividades}
        return render(request, 'docentes/seguimientoActividades.html', greeting)

    def generarReporte(request):
        # Create the HttpResponse hearders with PDF
        print('entro')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'atachment; filename = actividades.pdf'
        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # title
        c.drawImage('static/images/secoed/logo-secoed.png', 30, 730, mask='auto', width=100, height=100)
        c.setFont("Times-Roman", 22)
        c.drawString(200, 760, 'REGISTRO DE ACTIVIDADES')
        userObj = get_object_or_404(Usuario, pk=request.user.id)
        c.setFont("Times-Roman", 15)
        c.drawString(30, 700, 'NOMBRES: ' + userObj.nombres)
        c.drawString(30, 680, 'APELLIDOS: ' + userObj.apellidos)
        c.drawString(30, 660, 'IDENTIFICACIÓN: ' + userObj.identificacion)
        temp = fs_cursos_actividades(userObj.moodle_user)
        linea = 620
        for item in temp:
            # Cursos
            c.setFont("Times-Roman", 14)
            c.drawString(30, linea, item.curso.fullname)
            linea = linea - 10
            c.line(30, linea, 565, linea)
            # table head
            linea = linea - 15
            for item1 in item.actividades:
                if item1.itemname :
                    # Actividad
                    c.setFont("Times-Roman", 12)
                    c.drawString(30, linea, item1.itemname or "")
                    c.setFont("Times-Roman", 12)
                    c.drawString(490, linea, str(item1.nota))
                    linea = linea - 15
            linea = linea - 25
        # save
        c.save()
        pdf = buffer.getvalue();
        buffer.close()
        response.write(pdf)
        return response

class NotasView(View):
    def get(self, request):
        notas_cursos = valoration_course_student.objects.order_by('course_name').filter(student_id=request.user.id)
        notas_evaluacion = ResultadoProceso.objects.order_by('-cycle').filter(user=request.user.id)
        print(notas_evaluacion)
        greeting = {'heading': 'Notas de las evaluaciones',
                    'pageview': 'Docentes',
                    'notas_cursos': notas_cursos,
                    'notas_evaluacion': notas_evaluacion}
        return render(request, 'docentes/notaEvaluacion.html', greeting)
