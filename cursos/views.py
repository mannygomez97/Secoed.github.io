import argparse
#import json
import simplejson
from datetime import datetime
import logging
import os
import re
import shlex
import subprocess
import sys
import warnings
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    Type,
)
#import sys as json
from builtins import print
import delorean
from django.http import JsonResponse
from django.shortcuts import render, redirect
from eva.models import Ciclo, Ciclo2
from .models import CoursesMoodle
import requests
from datetime import datetime, date, timedelta, time
from conf.models import Carrera, Facultad
from django.core import serializers
from conf.models import Carrera
from authentication.models import Usuario, FacultyUser,RolUser
from django.core.serializers import json
from django.core import serializers
# Create your views here.
from django.views import View
from django.http import HttpResponse
from auditoria.apps import GeneradorAuditoria

from secoed.settings import TOKEN_MOODLE, API_BASE

m_ProcesoCurso = "CURSOS"
m_NombreTablaCurso = "pt_curso"
class CursoView(View):
    def categoria(request):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        try:
            response = requests.post(API_BASE, params)
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCategorias.html', context={"context": "Bad request"})
            if response:
                r = response.json()
                context = {"context": r}
        except Exception as e:
            print(e)
        return render(request, 'cursos/mantenimientoCategorias.html', context)

    def createEditCategoria(request):
        texto = ""
        if (request.POST['id'] == ""):
            wsfunction = "core_course_create_categories"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "categories[0][name]": request.POST["name"],
                      "categories[0][parent]": request.POST["depth"],
                      "categories[0][description]": request.POST['description'],
                      "categories[0][descriptionformat]": 1,
                      "categories[0][idnumber]": texto
                      }
        else:
            wsfunction = "core_course_update_categories"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "categories[0][id]": request.POST['id'],
                      "categories[0][name]": request.POST["name"],
                      "categories[0][parent]": request.POST["depth"],
                      "categories[0][description]": request.POST['description'],
                      "categories[0][descriptionformat]": 1,
                      "categories[0][idnumber]": texto
                      }
        try:
            response = requests.post(API_BASE, params)
            if response:
                r = response.json()
                if response == 400:
                    print(r.message)
                if response == 500:
                    print(r.message)
                if response == 200:
                    print(r.message)
        except Exception as e:
            print(e)
        return redirect('categoria')

    def deleteCategoria(request, idCategoria):
        params = {
            "wstoken": TOKEN_MOODLE,
            "wsfunction": "core_course_delete_categories",
            "moodlewsrestformat": "json",
            "categories[0][id]": idCategoria,
            "categories[0][recursive]": 1
        }
        try:
            respuesta = requests.post(API_BASE, params)
            if respuesta:
                r = respuesta.json()
                if respuesta.status_code == 400:
                    print(r.message)
                else:
                    print("si se borro")
        except Exception as e:
            print(e)
        return redirect('categoria')

    def getPeriod(request):        
        variable = Usuario.objects.filter(username__icontains=request.session['username']).values()[0]['id']              
        listcarrera = []
        carrera_id= FacultyUser.objects.filter(user=variable).values('carrera_id')          
        esadm = Usuario.objects.filter(username__icontains=request.session['username']).values('usuario_administrador')        
        period = list(Ciclo.objects.filter(is_active=True,carrera__in=carrera_id).values())       
        periodoId = period[0]['id']              
        listrol=[]                
        for i in Usuario.objects.filter(id=variable):
            if request.is_ajax():
                esadm=i.usuario_administrador 
                desrol = {}
                desrol['es_administrador']= i.usuario_administrador 
                listrol.append(desrol)                     
            if(esadm ==True):
                return JsonResponse({'data': list(listcarrera),'context':list(period), 'periodoId' : periodoId, 'validation':list(listrol)})                
                #print((listrol))
                #return JsonResponse({'context':period, 'periodoId' : periodoId,'validation':list(listrol)})
            else:
                for i in FacultyUser.objects.filter(user=variable):
                    if request.is_ajax():
                        test = {}
                        test['id']= i.carrera_id
                        test['name']=i.carrera.descripcion
                        listcarrera.append(test)             
                        return JsonResponse({'data':list(listcarrera),'context':list(period), 'periodoId' : periodoId, 'validation':list(listrol)})
                return HttpResponse ('Wrong request')
       

    def getCycle(request,periodoId): 
       
        request.session['periodoId'] = periodoId  
          
        ciclo = list(Ciclo2.objects.filter(periodo=periodoId).values())
         
        ciclo_idSession = request.session.get('cicloId')
         
        return JsonResponse({'context': ciclo, 'cicloId': ciclo_idSession})

    def setSessionCycle(request,cycleId):
       
        request.session['cicloId'] = cycleId
        return JsonResponse({'context': request.session['cicloId']})

    def get(self, request):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_courses_by_field",
                  "moodlewsrestformat": "json",
                  }
        cursos = {}        
        try:
            response = requests.post(API_BASE, params)
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCursos.html', context={"context": "Bad request"})
            if response:                                                                           
                cursos = {"cursos": response.json()}
        except Exception as e:
            print(e)
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)
        return render(request, 'cursos/mantenimientoCursos.html', cursos)
    
    def viewEdithModalCurso(request, pk):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_courses_by_field",
                  "moodlewsrestformat": "json",
                  }
        
        paramsCategoria = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        contextCategoria = []
        cursos = []
        aList=[] 
        heading="Editar Curso"
        TiempoInicio=""   
        TiempoFin=""    
        try:
            response = requests.post(API_BASE, params)
            responseCategoria = requests.post(API_BASE, paramsCategoria)   
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCursos.html', context={"context": "Bad request"})
            if response and responseCategoria:                                           
                variable= response.json()  
                contextCategoria = responseCategoria.json()
                aList = variable['courses']                                            
                for entrada in aList:                         
                 if( entrada["id"]==pk):                    
                    TiempoInicio=datetime.utcfromtimestamp(entrada["startdate"]).strftime('%m/%d/%Y')
                    TiempoFin=datetime.utcfromtimestamp(entrada["enddate"]).strftime('%m/%d/%Y')
                    entrada["startdate"]=TiempoInicio
                    entrada["enddate"]=TiempoFin                    
                    cursos.append(entrada)                  
                    break                                
        except Exception as e:
            print(e)
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)       
        context = {'cursos': cursos,"categoria": contextCategoria,"heading":heading}
        return render(request, 'cursos/MantenimientoEditForm.html', context,)

    def viewModalCurso(request, pk):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_courses_by_field",
                  "moodlewsrestformat": "json",
                  }        
        paramsCategoria = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        contextCategoria = []
        cursos = []
        aList=[] 
        heading="Visualizar Curso"
        TiempoInicio=""   
        TiempoFin=""    
        try:
            response = requests.post(API_BASE, params)
            responseCategoria = requests.post(API_BASE, paramsCategoria)   
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCursos.html', context={"context": "Bad request"})
            if response and responseCategoria:                                           
                variable= response.json()  
                contextCategoria = responseCategoria.json()
                aList = variable['courses']                                            
                for entrada in aList:                            
                 if( entrada["id"]==pk):                    
                    TiempoInicio=datetime.utcfromtimestamp(entrada["startdate"]).strftime('%m/%d/%Y')
                    TiempoFin=datetime.utcfromtimestamp(entrada["enddate"]).strftime('%m/%d/%Y')
                    entrada["startdate"]=TiempoInicio
                    entrada["enddate"]=TiempoFin                    
                    cursos.append(entrada)                  
                    break                                
        except Exception as e:
            print(e)
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)        
        context = {'cursos': cursos,"categoria": contextCategoria,"heading":heading}
        return render(request, 'cursos/MantenimientoViewForm.html', context)    

    def allCategorias(request):
       #print('entro aqui1')
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        try:
            response = requests.post(API_BASE, params)          
            if response.status_code == 400:
                return response.status_code
            if response:               
                r = response.json()               
                context = {"context": r}
        except Exception as e:
            print(e)           
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)
        return JsonResponse(context)

    def crearEditarCurso(request):
        user = Usuario.objects.filter(username__icontains=request.session['username']).values()[0]['id']        
        datei = request.POST['fechaInicio'].replace('/', '-')        
        init_date = datetime.strptime(datei, '%m-%d-%Y').date()        
        datef = request.POST['fechaFin'].replace('/', '-')        
        end_date = datetime.strptime(datef, '%m-%d-%Y').date()                                              
        calificacion = 0
        actividad = 0
        visibilidad = 0
        sesiones = 0
        notificacion = 0
        if ('calificaciones' in request.POST):
            calificacion = 1
        if ('informeActividad' in request.POST):
            actividad = 1
        if ('visibleAlumno' in request.POST):
            visibilidad = 1
        if ('secciones' in request.POST):
            sesiones = 1
        if ('notificacion' in request.POST):
            notificacion = 1
        if (request.POST['id'] == ""):
            fecha_inicio = datetime.strptime(
                request.POST['fechaInicio'], '%m/%d/%Y')
            fecha_fin = datetime.strptime(request.POST['fechaFin'], '%m/%d/%Y')
            tiempo = delorean.Delorean(fecha_inicio, timezone='UTC').epoch * 1
            tiempo2 = delorean.Delorean(fecha_fin, timezone='UTC').epoch * 1
            wsfunction = "core_course_create_courses"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "courses[0][fullname]": request.POST['fullName'],
                      "courses[0][shortname]": request.POST['nameShort'],
                      "courses[0][categoryid]": request.POST['categoria'],
                      "courses[0][summary]": request.POST['resumen'],
                      "courses[0][showgrades]": calificacion,
                      "courses[0][newsitems]": 5,
                      "courses[0][startdate]": int(tiempo),
                      "courses[0][enddate]": int(tiempo2),
                      "courses[0][numsections]": 1,
                      "courses[0][maxbytes]": 0,
                      "courses[0][showreports]": actividad,
                      "courses[0][visible]": visibilidad,
                      "courses[0][hiddensections]": sesiones,
                      "courses[0][groupmode]": 0,
                      "courses[0][groupmodeforce]": 0,
                      "courses[0][defaultgroupingid]": 0,
                      "courses[0][enablecompletion]": 0,
                      "courses[0][completionnotify]": notificacion,
                      "courses[0][lang]": "es",
                      }
        else:
            
            fecha_inicio_edit = datetime.strptime(
                request.POST['fechaInicio'], '%m/%d/%Y')
            fecha_fin_edit = datetime.strptime(
                request.POST['fechaFin'], '%m/%d/%Y')
            tiempo1_edit = delorean.Delorean(
                fecha_inicio_edit, timezone='UTC').epoch * 1
            tiempo2_edit = delorean.Delorean(
                fecha_fin_edit, timezone='UTC').epoch * 1
            wsfunction = "core_course_update_courses"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "courses[0][id]": request.POST['id'],
                      "courses[0][fullname]": request.POST['fullName'],
                      "courses[0][shortname]": request.POST['nameShort'],
                      "courses[0][categoryid]": request.POST['categoria'],
                      "courses[0][summary]": request.POST['resumen'],
                      "courses[0][showgrades]": calificacion,
                      "courses[0][newsitems]": 5,
                      "courses[0][startdate]": int(tiempo1_edit),
                      "courses[0][enddate]": int(tiempo2_edit),
                      "courses[0][numsections]": 1,
                      "courses[0][maxbytes]": 0,
                      "courses[0][showreports]": actividad,
                      "courses[0][visible]": visibilidad,
                      "courses[0][hiddensections]": sesiones,
                      "courses[0][groupmode]": 0,
                      "courses[0][groupmodeforce]": 0,
                      "courses[0][defaultgroupingid]": 0,
                      "courses[0][enablecompletion]": 0,
                      "courses[0][completionnotify]": notificacion,
                      "courses[0][lang]": "es",
                      }
        print('paso por el params')
        try:
            response = requests.post(API_BASE, params)
            print('paso por el response')
            print(response)
            if response:
                r = response.json()
                if response.status_code == 400:
                    print("ENTRA AL IF 400 " + str(response))
                    print("400")
                    GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, "ENTRA AL IF 400 " + str(response), request.user.id)
                if response.status_code == 500:
                    print("ENTRA AL IF 500 " + str(response))
                    print("500")
                    GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, "ENTRA AL IF 500 " + str(response), request.user.id)
                if response.status_code == 200:
                    print('paso por el response positivo')
                    print('r[0]')
                    print(r)
                    print('++++++++++curso++++++++++++++++')
                    curso = r[0]['id']
                    
                    courseSecoed = CoursesMoodle.objects.create(
                        moodleId = curso,
                        fullname = request.POST['fullName'],
                        shortname = request.POST['nameShort'],
                        description = request.POST['resumen'],
                        startdate = init_date,
                        enddate = end_date,
                        status = False,
                        userCreated = Usuario.objects.get(id = user))

                    newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCurso)
                    GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaCurso, newJson, request.user.id)

                    print(courseSecoed)
                    print("ENTRA AL IF 200 " + str(response))
            else:
                print("NO ENTRA al if")
                GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, "NO ENTRA al if", request.user.id)
        except Exception as e:
            print('ento por exception')
            print("error " + str(e))
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)
        return redirect('cursos')

    def deleteCourse(request, idCourse):       
        params = {
            "wstoken": TOKEN_MOODLE,
            "wsfunction": "core_course_delete_courses",
            "moodlewsrestformat": "json",
            "courseids[0]": idCourse,
        }
        try:
            kwargs = {'pk':idCourse}           
            #oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCurso, kwargs)
            respuesta = requests.post(API_BASE, params)
            print(respuesta)
            print(kwargs)
            print(m_NombreTablaCurso)
            if respuesta:
                r = respuesta.json()
            if respuesta.status_code == 400:
                print(r.message)
                #GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCurso, str(r.message), request.user.id)
            else:
                #GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaCurso, kwargs["pk"], oldJson, request.user.id)
                print("si se borro")
        except Exception as e:
            print(e)
            GeneradorAuditoria().CrearAuditoriaError(m_ProcesoCurso, str(e), request.user.id)
        return redirect('cursos')
