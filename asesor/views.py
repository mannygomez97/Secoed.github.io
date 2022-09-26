from email.policy import HTTP
from importlib.resources import contents
from multiprocessing import context
from turtle import update
from django.conf import settings
import requests
from asesor.utils import render_to_pdf
from secoed.settings import TOKEN_ROOT, API_BASE, TOKEN_ROOT
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  ValorationsCourses
from authentication.models import Usuario
from components.models import CourseCicleCarrer, CursoAsesores, CourseAsesor
from cursos.models import CoursesMoodle
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from notify.views import notificacionRetroalimentacion
from datetime import datetime, date, timedelta, time
import time
from .filters import *
from django.core.paginator import Paginator
import json
from eva.models import Ciclo2

def getAsesorLogin(request):
    user = Usuario.objects.filter(username__icontains=request.session['username']).values('id')
    userId = user[0]['id']
    return userId

def getAsesorInfo(request):
    login = Usuario.objects.filter(username__icontains=request.session['username'])
    nombre = login.values('nombres')[0]['nombres']
    apellido = login.values('apellidos')[0]['apellidos']
    user = nombre +" "+ apellido
    return user

def getCoursesByActuallyCicle(request):
    cicleId = request.session['activeCicle']

    secoedCourses = CourseCicleCarrer.objects.filter(cicle = cicleId).values('course')
    moodleCourses = CoursesMoodle.objects.all().values('id','moodleId')
    
    courses = []

    for secoed in secoedCourses:
        for moodle in moodleCourses:
            if secoed['course'] == moodle['id']:
                    courses.append(moodle)
    return courses

def getCourses(request):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"core_course_get_courses",
            "moodlewsrestformat":"json",                                    
            }
    courses = []
    response = requests.post(API_BASE, params)
    if response.status_code == 400:
        courses = []
    elif response:
        courses = response.json()
        for y in courses:
                timestamp = datetime.fromtimestamp(y["startdate"])                
                y["startdate"]=timestamp.strftime('%Y-%m-%d')
        for v in courses:                
                timestamp = datetime.fromtimestamp(v["enddate"])                
                v["enddate"]=timestamp.strftime('%Y-%m-%d')
    return courses

def getCalendarEvents(request, id):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"core_calendar_get_calendar_events",
            "moodlewsrestformat":"json",
            "events[courseids][0]":id
            }
    response=requests.post(API_BASE, params)
    if response.status_code==400:
            return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
            events=response.json()
            return events

def getAsesorCourses(request, user):
    asesorList = CourseAsesor.objects.filter(asesor=user).values('course')
    secoedCourses = CourseCicleCarrer.objects.all().values('id','course' )
    cursos_asesor = []

    for secoed in secoedCourses:
        for asesor in asesorList:
            if secoed['id'] == asesor['course']:
                    cursos_asesor.append(secoed['course'])

    return cursos_asesor

def getAsesorCoursesMoodle(request, user):
    courses = CourseAsesor.objects.filter(asesor = user).values('id')
    
    courses_asesor = []
    for i in range(len(courses)):
        courses_asesor.append(courses[i]['id'])
    return courses_asesor

def getStudentList(request, id):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"gradereport_user_get_grade_items",
            "moodlewsrestformat":"json",
            "courseid":id                                   
            }
    student_list = []
    response = requests.post(API_BASE, params)
    if response.status_code != 200:
        return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
        student_list = response.json()["usergrades"]
    return student_list

def getCourseMoodleInfo(request, id):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"gradereport_user_get_grade_items",
            "moodlewsrestformat":"json",
            "courseid":id                                   
            }
    courseInfo = []
    response = requests.post(API_BASE, params)
    if response.status_code != 200:
        return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
        courseInfo = response.json()
    return courseInfo

def getUsers(request, id):
    params = {"wstoken":TOKEN_ROOT,
            "wsfunction":"core_user_get_users",
            "moodlewsrestformat":"json",
            "criteria[0][key]": "id",
            "criteria[0][value]": id                               
    }
    response = requests.post(API_BASE, params)
    if response.status_code==400:
            return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
            users = response.json()
            return users

def getActiveCourseList(request):
    actualCoursesList = CoursesMoodle.objects.filter(status = True).values('moodleId')
    actualCourses = []
    for i in range(len(actualCoursesList)):
        actualCourses.append(actualCoursesList[i]['moodleId'])
    return actualCoursesList

def getUserActivities(request, id, idest):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"gradereport_user_get_grade_items",
            "moodlewsrestformat":"json",
            "courseid":id,
            "userid":idest
    }
    response=requests.post(API_BASE, params)
    if response.status_code==400:
            return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
            userActivities=response.json()["usergrades"][0]["gradeitems"]
            return userActivities

def getContentsCourse(request, id):
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"core_course_get_contents",
            "moodlewsrestformat":"json",
            "courseid":id
            }
    response=requests.post(API_BASE, params)
    if response.status_code==400:
            return render(request,'utility/utility-404error.html',context={"context":"Bad request"})
    if response:
            contents=response.json()
            return contents

def coursesSecoedView(request):
    t="Cursos" 
    u="Cursos asignados"
    user = getAsesorLogin(request)
    asesorCourses = getAsesorCourses(request, user)

    allCourses = getCourses(request)
    courseList = getCoursesByActuallyCicle(request)

    courses = []

    for course in allCourses:
        for activeCourse in courseList:
            if course["id"] == activeCourse["moodleId"] and activeCourse["id"] in asesorCourses:
                    courses.append(course)
    context = {'context': courses, 'heading': u,'pageview': t, 'status': 'A'}
    return render(request,'asesor/seguimiento_docente/courses_list.html',context)

def inactiveCourses(request):
    t="Detalle cursos inactivos" 
    u=datetime.today().strftime('%Y')
    
    courses = []
    allCourses = getCourses(request)
    asesorLogin = getAsesorCourses(request)
    
    for course in allCourses:
        if datetime.strptime(course["enddate"], '%Y-%m-%d').date() < date.today():
            if course["id"] in asesorLogin:
                courses.append(course)

    context = {'context': courses, 'heading': u,'pageview': t, 'status': 'I'}
    return render(request,'asesor/seguimiento_docente/lista_cursos_old.html',context)

def listadoEstudiante(request, id, fullname):
    t="Seguimiento" 
    u=fullname

    courseMoodle = CoursesMoodle.objects.filter(moodleId = id).values('id')[0]['id']
    infoCourse = CourseCicleCarrer.objects.filter(course = courseMoodle)
    evalStatus = infoCourse.values('evaluated')[0]['evaluated']  
    try:
        context={"context": getStudentList(request, id),'heading': u,'pageview': t,'fullname': fullname, 'course': id, 'evalStatus': evalStatus}
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/lista_Estudiantes.html',context)

def userActivities(request, id, nombre, idest):   
    nombre_Estudiante=nombre         
    try:
        user_activities =  getUserActivities(request, id, idest)                     
        context={"context":user_activities,'nombre':nombre_Estudiante}
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/act_pdf.html',context)

def courseNotes(request):
    u="Detalle de notas"
    t="Cursos"
    notes = ValorationsCourses.objects.filter(cicle__is_active = True)
    myFilter = valorationCourseStudentFilter(request.GET, queryset = notes)
    notes = myFilter

    paginated_filtered_notes = Paginator(notes.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered_notes.get_page(page_number)

    asesor = getAsesorInfo(request)
    
    context = {'notes': notes, 'myFilter': myFilter, 'page_obj': page_obj, 'heading': u,'pageview': t, 'asesor': asesor}
    return render(request, 'asesor/valorations/course_notes.html', context)

def activitiesNotes(request):
    u="Detalle de actividades"
    t="Cursos"
    notes = ValorationsActivities.objects.all()
    myFilter = valorationActivitiesFilter(request.GET, queryset = notes)
    notes = myFilter

    paginated_filtered_notes = Paginator(notes.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered_notes.get_page(page_number)
    
    context = {'notes': notes, 'myFilter': myFilter, 'page_obj': page_obj,'heading': u,'pageview': t,}
    return render(request, 'asesor/valorations/course_notes_activities.html', context)

def modulesByCourse(request, id, fullname):
    u="Modulos del curso: " + fullname
    t="Cursos"
    try:    
        context={"context":getContentsCourse(request, id), 'heading': u,'pageview': t, 'course':id, 'fullname':fullname}                        
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/modules_course.html',context)

def detailsModule(request,course, id,fullname, name, section): 
    try:
        res = getContentsCourse(request, course)
        for r in res:
            if r["id"]==int(id):
                context={'context':r["modules"], 'heading': name,'pageview': fullname, 'course':course, 'moduleid': id,'fullname':fullname, 'namemod':name, 'section':section}
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/details_module.html',context)

def formAddScheduleEvent(request,courseid, fullname):
    u="Agregar evento"
    t="Cursos"
    context={}
    try:
        context={"courseid":courseid, 'heading': u,'pageview': t, 'fullname':fullname}
    except Exception as e:
        print(e)
    return render(request,'asesor/events/form_add_schedule_event.html',context)

def saveScheduleEvent(request):
    if request.method == 'POST':
        courseid = request.POST.get('courseid')
        fullname = request.POST.get('fullname')
        name = request.POST.get('name')
        description = request.POST.get('description')
        timestart = request.POST.get('timestart')
        timeend = request.POST.get('timeend')

    dt_timestart = time.mktime(datetime.strptime(timestart, '%Y-%m-%d').timetuple())
    dt_timeend = time.mktime(datetime.strptime(timeend, '%Y-%m-%d').timetuple())

    mod_timestart = int(dt_timestart)
    mod_timeend = int(dt_timeend) + 86400
    mod_duration = mod_timeend - mod_timestart

    try:
        params = {
            "wstoken": TOKEN_ROOT,
            "wsfunction": "core_calendar_create_calendar_events",
            "moodlewsrestformat": "json",
            "events[0][name]":name,
            "events[0][description]":description,
            "events[0][format]":1,
            "events[0][courseid]":courseid,
            "events[0][groupid]":0,
            "events[0][repeats]":0,
            "events[0][eventtype]": "course",
            "events[0][timestart]": mod_timestart,
            "events[0][timeduration]":mod_duration,
            "events[0][visible]":1,
            "events[0][sequence]":1
        }
        response = requests.post(API_BASE, params)
        if response.status_code == 400:
            return render(request, 'asesor/events/form_add_schedule_event.html', context={"context": "Bad request"})
        if response:
            r = response.json()
            return redirect('/asesor/study_schedule_events/'+str(courseid)+'/'+str(fullname)+'/')
        
    except Exception as e:
        print(e)
    return redirect('/asesor/study_schedule_events/'+str(courseid)+'/'+str(fullname)+'/')

def studyScheduleEvents(request,id,fullname):
    u="Curso"
    t=fullname
    try:
        context={"events": getCalendarEvents(request, id)["events"],'heading': u,'pageview': t, 'fullname':fullname, 'courseid':id}
    except Exception as e:
        print(e)
    return render(request,'asesor/events/study_schedule_events.html',context)

def delScheduleEvent(request,courseid, id, repeatid, fullname):
    nrepeat = 0
    if repeatid == 'None':
        nrepeat = 0
    else:
        nrepeat = int(repeatid)
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"core_calendar_delete_calendar_events",
            "moodlewsrestformat":"json",
            "events[0][eventid]":id,
            "events[0][repeat]": nrepeat
            }    
    try:
        response=requests.post(API_BASE, params)
        if response:
            return redirect('/asesor/study_schedule_events/'+str(courseid)+'/'+str(fullname)+'/')
    except Exception as e:
        print(e)
    return redirect('/asesor/study_schedule_events/'+str(courseid)+'/'+str(fullname)+'/')

def calRegister(request):
    u="Creación calendario academico"
    t="Seguiimiento docente"
    context={ 'heading': u, 'pageview': t, }
    return render(request,'asesor/cronograma/cal_register.html',context)

def createModule(request,course, section):
    u="Modulos del curso: "
    t="Cursos"
    apiBase=API_BASE
    params={"wstoken":TOKEN_ROOT,
            "wsfunction":"core_course_get_course_content_items",
            "moodlewsrestformat":"json",
            "courseid":course         
            }
    context={}
    try:
        response=requests.post(apiBase, params)
        if response.status_code==400:
            return render(request,'lista_Estudiantes.html',context={"context":"Bad request"})
        if response:
            r=response.json()["content_items"]  
            context={"context":r, 'heading': u,'pageview': t, 'course':course, 'section':section}                        
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/create_module.html',context)

def usersByModule(request, course):        
    try:
        context={"context": getStudentList(request, course), 'heading': "Modulos del curso: ", 'pageview': "Cursos", 'course':course}                       
    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/users_by_module.html',context)

def valorationCourseByUser(request, courseid, userfullname, userid, fullname):
    course = courseid
    user = userid
    
    courseMoodle = CoursesMoodle.objects.filter(moodleId = course).values('id')[0]['id']
    courseSecoed = CourseCicleCarrer.objects.filter(course = courseMoodle).values('id')[0]['id']
    countNotes = ValorationsCourses.objects.filter(studentId = user, course = courseSecoed).count()
    
    activities = getUserActivities(request, course, user)
    
    asesor = getAsesorLogin(request)
    
    newActivities = []
    notes = []
    for r in activities:
        if r["itemtype"] != "course":
            if r['graderaw'] == None:
                r['graderaw'] = 0
            newActivities.append(r)
            notes.append(r["graderaw"])
            
    
    nf_len = len(newActivities)
    nf = 0
    napproved = 0
                    
    for r2 in newActivities:
        if r2["graderaw"] :
            nf = nf + r2["graderaw"]
            napproved = nf/nf_len
    context={"context":newActivities,'name_user':userfullname, 'napproved':napproved, 'heading': userfullname,
    'pageview': fullname, 'course':courseSecoed, 'courseMoodle':courseMoodle,'userid':userid, 'fullname':fullname, 
    'val_note':countNotes, 'activitynumb':nf_len, 'asesor':asesor, 'notes': notes}
    return render(request,'asesor/valorations/val_course_student.html',context)

def saveValCourse(request, course, fullname, userid, name_user, napproved, activitynumb, asesor, courseMoodle):
    saveValCourse = ValorationsCourses(
        course = CourseCicleCarrer.objects.get(id = course),
        studentId = userid,
        studentName = name_user,
        activitiesCourse = activitynumb,
        scoreCourse = napproved,
        userCreated = Usuario.objects.get(id=asesor)
    )
    saveValCourse.save()
    return redirect('/asesor/valoration_course_by_user/'+str(course)+'/'+str(name_user)+'/'+str(userid)+'/'+str(fullname)+'/')

def valActivitiesModuleUsers(request, course, moduleid, namemod, fullname, id, name ):
    asesor = getAsesorLogin(request)

    try:
        res_new = []
        res_ug = getStudentList(request, course)
        lres_ug = len(res_ug)

        for i in range(lres_ug):
            res_name = res_ug[i]["userfullname"]
            res_id = res_ug[i]["userid"]
            res = getStudentList(request, course)[i]["gradeitems"]
            
            for r in res:
                if  r["itemname"] == name and r["cmid"] == id:
                    dicc = {'teachername' : res_name, 'teacherid' : res_id, 'actividad': r }
                    res_new.append(dicc)

        context={"context":res_new,'heading': name, 'pageview': fullname, 'course':course, 'moduleid':moduleid, 'namecourse': namemod, 'modulename':  fullname, 'actname':name, 'actid':id, 'asesor_id':asesor}
    except Exception as e:
        print(e)
    return render(request,'asesor/valorations/val_activities_module_users.html',context)

def valModuleCourse(request, course, id):
    try:
        res_new = []
        res = getStudentList(request, course)
        for r in res:
            if r["gradeitems"]["itemtype"] != "course":
                res_new.append(r)
                for nf in res_new:
                    if nf["id"] == int(id):
                        context={"context":nf['gradeitems'], 'heading': "Modulos del curso: ", 'pageview': "Cursos", 'course':course, }
        context={"context":res_new}
    except Exception as e:
        print(e)
    return render(request,'asesor/valorations/val_module_course.html', context)

def toMail(request,course_name, student_id, student_name, activities_course, score_course):
    context = {}
    try:
        context = {'context': getUsers(request, student_id), 'res_mail':getUsers(request, student_id) ["users"][0]["email"],'course_name':course_name, 'student_id':student_id, 'student_name':student_name, 'activities_course':activities_course, 'score_course':score_course }
    except Exception as e:
        print(e)
    return render(request,'asesor/mailing/get_dest.html', context)

def sendMail(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        academic_period = request.POST.get('academic_period')
        course = request.POST.get('course')
        score_course = request.POST.get('score_course')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        feedback = request.POST.get('feedback')
        attach = request.POST.get('attach')
        
        template = render_to_string('asesor/mailing/email_template.html', {
            'name': name,
            'email': email,
            'academic_period': academic_period,
            'course': course,
            'score_course': score_course,
            'subject': subject,
            'message': message,
            'feedback': feedback
        })
        try:
            email = EmailMessage(subject, template, settings.EMAIL_HOST_USER, [email])
            email.fail_silently = False
            email.send()
        except Exception as e:
            print(e)
            
        messages.success(request, 'Correo enviado correctamente')
        return redirect ('course_notes')

def reportsAsesor(request):
    t = "Reportes" 
    u = "Reporte de calificaciones"

    asesor = getAsesorInfo(request)

    notes = ValorationsCourses.objects.filter(cicle__is_active = True)
    myFilter = valorationToAcademicManagerFilter(request.GET, queryset = notes)
    notes = myFilter

    paginated_filtered_notes = Paginator(notes.qs, 40)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered_notes.get_page(page_number)
    
    context = {'notes': notes, 'myFilter': myFilter, 'page_obj': page_obj, 'heading': u,'pageview': t, 'asesor': asesor}
    return render(request,'asesor/reports/reports_asesor.html', context)

def valorateCourse(request, course):
    t="Valoración general" 
    u=datetime.today().strftime('%Y')

    courseMoodle = CoursesMoodle.objects.filter(moodleId = course).values('id')[0]['id']
    courseSecoed = CourseCicleCarrer.objects.filter(course = courseMoodle).values('id')[0]['id']
    infoSecoed = CourseCicleCarrer.objects.filter(course = courseMoodle).select_related()

    infoCourse = CourseCicleCarrer.objects.filter(course = courseMoodle)
    courseVal = infoCourse.values('course')[0]['course']
    cicleVal = infoCourse.values('cicle')[0]['cicle']
    carrerVal = infoCourse.values('carrer')[0]['carrer']
    evalStatus = infoCourse.values('evaluated')[0]['evaluated']

    asesor = getAsesorLogin(request)
    docentList = getStudentList(request, course)
    
    courseActivities = []
    toSave = []
    lenDocentList = len(docentList)
    notesChart = []

    for i in range(lenDocentList):
        userfullname = docentList[i]["userfullname"]
        userid = docentList[i]["userid"]
        activities = getStudentList(request, course)[i]["gradeitems"]

        notes = 0
        nnotes = 0
                          
        for r in activities:
            if  r["itemname"] != None:
                itemname = r['itemname']
                graderaw = r['graderaw']
                if r['graderaw'] == None:
                    graderaw = 0
                dicc = {
                    "userfullname" : userfullname,
                    "userid" : userid,
                    "itemname": itemname,
                    "graderaw": graderaw
                }
                courseActivities.append(dicc)
                notes = notes + graderaw
                nnotes = nnotes + 1
        calcNote = notes/nnotes
        realNote = round(calcNote, 2)
        dicc2 = {
            'courseSecoed': courseSecoed,
            'courseVal': courseVal,
            'cicleVal': cicleVal,
            'carrerVal': carrerVal,
            'userid' : userid,
            'userfullname' : userfullname,
            'activitiesCourse': nnotes,
            'scoreCourse': realNote,
            'userCreated': asesor
        }
        toSave.append(dicc2)
        notesChart.append(dicc2["scoreCourse"])
    if (evalStatus == False):
        for save in toSave:
            saveNotesCourse = ValorationsCourses(
                courseCicleCarrer = CourseCicleCarrer.objects.get(id = save['courseSecoed']),
                course = CoursesMoodle.objects.get(id = save['courseVal']),
                cicle = Ciclo2.objects.get(id = save['cicleVal']),
                carrer = Carrera.objects.get(id = save['carrerVal']),
                studentId = save['userid'],
                studentName = save['userfullname'],
                activitiesCourse = save['activitiesCourse'],
                scoreCourse = save['scoreCourse'],
                userCreated = Usuario.objects.get(id = save['userCreated']))
            saveNotesCourse.save()
        
        courseCicleCarrer = CourseCicleCarrer.objects.get(id = courseSecoed)
        courseCicleCarrer.evaluated = True
        courseCicleCarrer.save()
        messages.add_message(request, messages.SUCCESS, message = "Notas registradas de forma exitosa!")
    else:
        messages.add_message(request, messages.WARNING, message = "Curso ya se encuentra evaluado!")
    context = {'infoSecoed': infoSecoed, 'courseActivities': courseActivities, 'toSave':toSave, 'heading': u,'pageview': t,
    'asesor': asesor, 'notesChart': notesChart}
    return render(request,'asesor/valorations/notes.html',context)
