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


def fs_cursos_actividades(moodle_user):
    cursos_actividades = []
    params = {"wstoken": TOKEN_MOODLE,
              "wsfunction": "core_enrol_get_users_courses",
              "moodlewsrestformat": "json",
              "userid": moodle_user}
    response = requests.post(API_BASE, params)
    if response:
        r = response.json()
        d1 = json.dumps(r)
        l1 = json.loads(d1)
        for obj in l1:
            aux1 = core_enrol_get_users_courses(**obj)
            aux2 = []
            aux3 = []
            params2 = {"wstoken": TOKEN_MOODLE,
                       "wsfunction": "core_completion_get_activities_completion_status",
                       "moodlewsrestformat": "json",
                       "userid": moodle_user,
                       "courseid": aux1.id}
            response2 = requests.post(API_BASE, params2)
            if response2:
                r2 = response2.json()
                for obj1 in r2['statuses']:
                    aux2.append(Statuses(**obj1))
                for obj2 in r2['warnings']:
                    aux3.append(Warnings(**obj2))
            cursos_actividades.append(CursosActividades(aux1, aux2, aux3))
            params3 = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": "gradereport_user_get_grade_items",
                      "moodlewsrestformat": "json",
                      "courseid": aux1.id,
                      "userid": moodle_user
                      }
            response3 = requests.post(API_BASE, params3)
            if response3.json().get("usergrades"):
                actividad = [actividades for actividades in response3.json()["usergrades"] if actividades["userid"] == int(moodle_user)]
                if actividad:
                    actividades = [dato for dato in actividad[0]["gradeitems"]]
                    if actividades:
                        actividades2 = actividades[0]["itemnumber"]
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
        temp = fs_cursos_actividades(userObj.moodle_user)
        linea = 600
        for item in temp:
            # Cursos
            c.setFont("Times-Roman", 14)
            c.drawString(30, linea, item.cursos.fullname)
            linea = linea - 10
            c.line(30, linea, 565, linea)
            # table head
            linea = linea - 15
            for item1 in item.actividades:
                # Actividad
                c.setFont("Times-Roman", 12)
                c.drawString(30, linea, item1.modname)
                c.setFont("Times-Roman", 12)
                c.drawString(380, linea, getEstado(item1.state))
                c.setFont("Times-Roman", 12)
                c.drawString(490, linea, getTipo(item1.tracking))
                linea = linea - 15
            # table boddy

            linea = linea - 25

        # save
        c.save()
        pdf = buffer.getvalue();
        buffer.close()
        response.write(pdf)
        return response

class Notasiew(View):
    def get(self, request):
        notas_autoevaluacion = fs_cursos_actividades(userObj.moodle_user)
        notas_coevaluacion = fs_cursos_actividades(userObj.moodle_user)
        greeting = {'heading': 'Notas de ls evaluaciones',
                    'pageview': 'Docentes',
                    'notas_autoevaluacion': notas_autoevaluacion,
                    'notas_coevaluacion': notas_coevaluacion}
        return render(request, 'docentes/seguimientoActividades.html', greeting)
