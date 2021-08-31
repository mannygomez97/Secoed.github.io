from django.http.response import HttpResponse
from components.utils import render_to_pdf
from conf.forms import MenuForm
from conf.models import Menu
from secoed.settings import EMAIL_HOST_USER
from typing import Any, Dict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.db.models import CharField, Value as V, F, Q
from django.db.models.functions import Concat
from components.models import AsesorUniversidad, AsesorAsesor, AsesorCursos, AsesorCursoAsesor, AsesorDocentes, AprobacionCurso, CursoAsesores
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,FileResponse,HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
import io,json
from datetime import datetime
from django.core.mail import send_mail
from asesor.services import obtener_datos
import requests
from components.forms import CriterioForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.forms.models import fields_for_model, model_to_dict
###########################  Recursos para consumir la api###########################

apiBase = "http://academyec.com/moodle/webservice/rest/server.php"

def wsfunction(function):
    return {
        "wstoken":"958c77e27c859fac94cfb40ceec68a06",
        "wsfunction":function,
        "moodlewsrestformat":"json",
    }

######################################################################################

#JSON
# @csrf_exempt
def Autocomplete(request):
    curso = AsesorCursos.objects.all()
    return JsonResponse({"curso":curso},safe=False) 

# @csrf_exempt
def obtenerPorcentaje(request):
    return JsonResponse({"porcentajeCompleto":30,"porcentajeNoCompleto":70},safe=False) 

##### filtrar asesor
def asesor(request, *args, **kwargs):                                                                                   
    #asesor = AsesorAsesor.objects.filter(Q(nombres__icontains =  kwargs["asesor"])|Q(apellidos__icontains = kwargs["asesor"])).distinct().values('id_asesor',nombre = Concat('nombres', V(' '),'apellidos'))
    ase = AsesorAsesor.objects.annotate(names = Concat('nombres', V(' ') ,'apellidos'))
    asesor = ase.filter(names__icontains = kwargs["asesor"] ).distinct().values('id_asesor',nombre = Concat('nombres', V(' '),'apellidos'))
         
    return JsonResponse({'data':list(asesor)})

#############Guardar asesor curso
@csrf_exempt
def guardarAsesorCurso(request, *args, **kwargs):
    if(request.method == "POST"): 
        a = json.loads(request.body)
        ase = AsesorAsesor.objects.annotate(names = Concat('nombres', V(' ') ,'apellidos'))

        for i in ase:
            if (i.names == a['result'][2]):
                palabra = a['result'][2].split()
                # AsesorCursoAsesor.objects.create(relacion = palabra[0]+'_'+a['result'][1],asesor = i, curso = AsesorCursos.objects.get(id_curso = a['result'][0]))
                CursoAsesores.objects.create(id_curso = a['result'][0], id_asesor = i.id_asesor)
                return JsonResponse({"estado":"Se le asignó curso correctamente al asesor"},safe=False)
        return JsonResponse({"estado":"El asesor designado no existe, seleccione bien al asesor que desea asignar"},safe=False)

         
##################################
def buildEmail(course):
    subject = "Welcome to Skote  Membership"
    email_template_name = "components/email/email-notify.txt"
    email_text =  "jorge.penaz@ug.edu.ec" #"jucacero@hotmail.com"
    context = {
        "courseName" : course["fullname"]
    }
    template_email = render_to_string(email_template_name, context)
    # Array de destinatarios
    send_mail(subject, template_email, EMAIL_HOST_USER, [email_text], fail_silently=False)

def getChoices(choices = [], answers = []):
    result = choices
    for i in range(len(answers)): 
        result[int(answers[i])] = result[int(answers[i])] + " Correct Answer"
    return result


@csrf_exempt
def getPDF(request):
    context = {
        'course':str(request.POST['course']),
        'questions':request.POST.getlist('question[]'),
        'choices': getChoices(request.POST.getlist('choice[]'), request.POST.getlist('is_correct[]')),
    }
    return render_to_pdf(request, 'components/templates_pdf/evaluation_final.html',context_dict=context)

def sendEmail(request):
    coursesList: Any = obtener_datos({
        "wsfunction": "core_course_get_courses",
    })
    finishCourses = []
    # courseSelected = [course for course in coursesList['courses'] if  course['id'] == courseId ]
    for course in coursesList:
        justNow = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
        endDate = datetime.fromtimestamp(course['enddate'])
        if(justNow == endDate):
            # Send email
            buildEmail(course)
            finishCourses.append(course['fullname'])
    return JsonResponse({
        "finished_courses": finishCourses,
    })
    

def cursoA(request, *args, **kwargs):
    params = wsfunction("core_course_get_courses")
    response = requests.get(apiBase,params)
    
    curso = []
    for data in response.json():
        dat = CursoAsesores.objects.filter(id_curso = data['id'])
        if dat :
            print("nada")
        else :
            curso.append(data)

    datos = {"datas":curso}

    if kwargs["curso"] != "null":
        context = {"context":[p for p in datos["datas"] if kwargs['curso'].lower() in p['fullname'].lower()]}
    else:
        context = {"context":datos['datas']}
    return JsonResponse({'data':context})



##########################################################################################################################################
##########################################################################################################################################
def menu(request):
    menusview =  AprobacionCurso.objects.filter(estado =True).order_by('nivel')
    greeting = {'heading': "REQUISITO DEL CURSO", 'pageview': "Gestor", "menusview": menusview}
    return render(request, 'components/proyecto/components-formrequisito.html', greeting)

def requisito(request):
    if request.method == 'POST':
        ##editarField
        request.POST._mutable = True
        request.POST['criterio'] = request.POST['criterio'].capitalize()
        request.POST._mutable = False
        criterioForm = CriterioForm(request.POST)
        if criterioForm.is_valid():
            # criterioForm.save()
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.create(nivel = criterio_data.get("nivel"), criterio = criterio_data.get("criterio"), semaforo = criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se registro correctamente", "success")
        else:
            messages.error(request, "No se puedo registrar", "error")
        return redirect('requisito')
    else:
        menuFormView =CriterioForm()
        menu = AprobacionCurso()
        view = False
        context = {'menuFormView': menuFormView, 'requisito': menu, 'view': view}
    return render(request, 'components/proyecto/formrequisito.html', context)



# Editar los datos de un modulo por su pk
class UpdateRequisito(View):

    requisito = lambda self, id : get_object_or_404(AprobacionCurso, pk = id) 
    
    def post(self, request, *args,  **kwargs):
        request.POST._mutable = True
        request.POST['criterio'] = request.POST['criterio'].capitalize()
        criterioForm = CriterioForm(request.POST, model_to_dict(self.requisito(kwargs["pk"])))
        if criterioForm.is_valid():
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.filter(id = kwargs["pk"]).update(nivel = criterio_data.get("nivel"), criterio = criterio_data.get("criterio"), semaforo = criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se edito correctamente", "success")
            return redirect('requisito')

    def get(self, request, *args,  **kwargs):      
        menuFormView = CriterioForm(model_to_dict(self.requisito(kwargs["pk"])))
        view = False
        context = {'menuFormView': menuFormView, 'menu': self.requisito(kwargs["pk"]), 'view': view}
        return render(request, 'components/proyecto/formrequisito.html', context)


def deleteRequisito(request, pk):
    requisito = get_object_or_404(AprobacionCurso, pk=pk)
    if requisito:
        requisito.delete()
        messages.success(request, "Se ha eliminado correctamente", "success")
    return redirect('requisito')


def cursoA(request, *args, **kwargs):
    apiBase = "http://academyec.com/moodle/webservice/rest/server.php"
    params = {
        "wstoken":"958c77e27c859fac94cfb40ceec68a06",
        "wsfunction":"core_course_get_courses",
        "moodlewsrestformat":"json",
        # "field":"id",
        # "value":"3"
    }
    response = requests.get(apiBase,params)

    datos = {"datas":response.json()}
    
    if kwargs["curso"] != "null":
        context = {"context":[p for p in datos["datas"] if kwargs['curso'].lower() in p['fullname'].lower()]}
    else:
        context = {"context":datos['datas']}

     

    # if kwargs["curso"] != "null":
    #     c = AsesorCursos.objects.filter(asesorcursoasesor__isnull=True).values('id_curso','tipo')
    #     curso = c.filter(Q(tipo__icontains  = kwargs["curso"]))
       
    # else:
    #     #left join
    #     #SELECT * 
    #     # FROM public.asesor_cursos B 
    #     # left JOIN public.asesor_curso_asesor AP
    #     # ON ap."Curso_id" = B."Id_curso"
    #     # where id_curso_asesor is  null
    #     curso = AsesorCursos.objects.filter(asesorcursoasesor__isnull=True).values('id_curso','tipo')
    #return JsonResponse({'data':list(curso)})
    return JsonResponse({'data':context})



##########################################################################################################################################
def menu(request):
    menusview =  AprobacionCurso.objects.filter(estado =True).order_by('id')
    # print(menusview.get_criterio_display())
    # modulos = AsesorCursoAsesor.objects.order_by('curso')
    # menusItem = AsesorCursoAsesor.objects.exclude(curso__isnull=False).exclude(id__isnull=True).order_by('curso')
    greeting = {'heading': "REQUISITO DEL CURSO", 'pageview': "Gestor", "menusview": menusview}
    return render(request, 'components/proyecto/components-formrequisito.html', greeting)

def requisito(request):
    if request.method == 'POST':
        ##editarField
        request.POST._mutable = True
        request.POST['criterio'] = request.POST['criterio'].capitalize()
        # request.POST['key'] = request.POST['descripcion'].replace(" ", "_").lower() + "_" + request.POST['orden']
        request.POST._mutable = False
        # endEditarField
        criterioForm = CriterioForm(request.POST)
        if criterioForm.is_valid():
            # criterioForm.save()
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso
            # AprobacionCurso.objects.create(nivel = criterio_data.get("nivel"))
            AprobacionCurso.objects.create(nivel = criterio_data.get("nivel"), criterio = criterio_data.get("criterio"), semaforo = criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se registro correctamente", "success")
        else:
            messages.error(request, "No se puedo registrar", "error")
        return redirect('requisito')
    else:
        menuFormView =CriterioForm()
        menu = AprobacionCurso()
        view = False
        context = {'menuFormView': menuFormView, 'requisito': menu, 'view': view}
    return render(request, 'components/proyecto/formrequisito.html', context)


# Editar los datos de un modulo por su pk
def editRequisito(request, pk):
    menu = get_object_or_404(AsesorCursoAsesor, pk=pk)
    if request.method == 'POST':
        ##editarField
        request.POST._mutable = True
        request.POST['descripcion'] = request.POST['descripcion'].capitalize()
        request.POST['key'] = request.POST['descripcion'].replace(" ", "_").lower() + "_" + request.POST['orden']
        if request.POST['modulo_id'] and request.POST['parent_id']:
            request.POST['modulo_id'] = ''
        request.POST._mutable = False
        # endEditarField
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Se edito correctamente", "success")
            return redirect('menu')
    else:
        menuFormView = MenuForm(instance=menu)
        view = False
        context = {'menuFormView': menuFormView, 'menu': menu, 'view': view}
    return render(request, 'components/proyecto/formrequisito.html', context)


# AJAX
def loadRequisito(request):
    #modulo_id = request.GET.get('modulo_id')
    modulo_id = request.GET.get('id')
    menus = Menu.objects.filter(Q(modulo_id=modulo_id) & Q(href='')).order_by('descripcion')
    return render(request, 'components/proyecto/requisitoList.html', {'menus': menus})


class FormEducacion(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Designar asesor curso"
        greeting['pageview'] = "Forms"

        queryset = request.GET.get("buscar")
        
        if queryset:
            greeting['asesor'] = AsesorAsesor.objects.filter(Q(nombres__icontains = queryset)|Q(apellidos__icontains = queryset)).distinct()
            greeting['curso'] = AsesorCursoAsesor.objects.filter
    
        return render (request,'components/proyecto/components-formeducation.html',greeting)


class FormAsesor(View):
    def get(self, request):
        
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase,params)
        curso = []
        asesor = []
        for data in response.json():
            curs = CursoAsesores.objects.filter(id_curso = data['id']).values('id_asesor')
            if curs:
                curso.append(data)
                a = AsesorAsesor.objects.filter(id_asesor = curs[0]['id_asesor']) .values(names = Concat('nombres', V(' ') ,'apellidos'))
                if a:
                    curso.append(a[0])
                

        greeting = {}
        greeting['heading'] = "Curso Designado a Asesor"
        greeting['pageview'] = "Forms"

        greeting['cursos'] = curso

        return render (request,'components/proyecto/components-formasesor.html',greeting)


class FormEducaciona(View):
    @csrf_exempt
    def get(self, request):        
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase,params)
        greeting = {}
        greeting['heading'] = "Avance del curso"
        greeting['pageview'] = "Forms"
        greeting['cursos'] = response.json()
        
        return render (request,'components/proyecto/components-formeducation1.html',greeting)

  


class listadoAsesores(View):        
    def get(self, request):
        params = wsfunction("core_enrol_get_enrolled_users")
        params.update(courseid = request.GET.get('id'))
        response = requests.get(apiBase,params)

        datos = [rol for rol in response.json() if rol.get('roles') and rol['roles'][0]['roleid'] == 3]

        greeting = {"heading":"Listado de asesores curso", "pageview":"Forms","curso":request.GET.get('id')}

        if datos: 
            greeting.update(context = datos)

        return render (request,'components/proyecto/components-listadoAsesores.html', greeting)




class actividades(View):        
    def get(self, request):
        params = wsfunction("gradereport_user_get_grade_items")
        params.update(courseid = request.GET.get('curso'))
        response = requests.get(apiBase,params)

        if response.json().get("usergrades"):
            actividad = [actividades for actividades in response.json()["usergrades"] if actividades["userid"] == request.GET.get('id')]
        else:
            actividad = None

        greeting = {"heading":"Listado de Actividades", "pageview":"Forms"}
        if actividad:
            actividades = [dato for dato in actividad[0]["gradeitems"]]
            greeting.update(context = actividades)

            cont = 0
            suma = 0
            if actividades:
                for i in actividades:
                    if i["graderaw"]:
                        suma = i["graderaw"] + suma
                        cont = cont + 1                

                if suma == 0:
                    semaforo = 0
                else:
                    semaforo = suma / cont

                if semaforo < 30:
                    criterio = AprobacionCurso.objects.filter(nivel = 1)
                elif semaforo < 70:
                    criterio = AprobacionCurso.objects.filter(nivel = 2)
                elif semaforo < 90:
                    criterio = AprobacionCurso.objects.filter(nivel = 3)
                elif semaforo < 100:
                    criterio = AprobacionCurso.objects.filter(nivel = 4)
                greeting.update(semaforo = criterio)       

        return render (request,'components/proyecto/modalActividades.html', greeting)

class FormRequisito(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Requisito del curso"
        greeting['pageview'] = "Forms"
       
        return render (request,'components/proyecto/components-formrequisito.html',greeting)



class FormEvaluation(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Evaluation Docente"
        greeting['pageview'] = "Forms"

        #greeting['curso'] = AsesorCursoAsesor.objects.filter(~Q(curso = AsesorCursos.objects.all() )).values('curso__id_curso','curso__tipo')
    
        return render (request,'components/proyecto/components-formevaluation.html',greeting)






#UI-ELEMENTS
class AlertsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Alerts"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-alerts.html',greeting)

class ButtonsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Buttons"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-buttons.html',greeting)

class CardsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Cards"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-cards.html',greeting)    

class CarouselView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Carousel"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-carousel.html',greeting)  


class DropDownsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Dropdowns"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-dropdwons.html',greeting)                    

class GridView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Grid"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-grid.html',greeting) 

class ImagesView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Images"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-images.html',greeting)   

class LightBoxView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Lightbox"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-lightbox.html',greeting)    

class ModalsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Modals"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-modals.html',greeting) 

class RangeSlidebarView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Range Slider"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-rangeslidebar.html',greeting) 

class SessionTimeoutView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Session Timeout"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-sessiontimeout.html',greeting)           

class ProgressBarsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Progress Bars"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-progressbars.html',greeting)    

class SweetAlertView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Sweet-Alert"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-sweetalert.html',greeting)     

class TabsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Tabs & Accordions"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-tabs.html',greeting)   

class TypoGraphyView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Typography"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-typography.html',greeting)   

class VideoView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Video"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-video.html',greeting)   


class GeneralView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "General"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-general.html',greeting)                                                                           

class ColorsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Colors"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-colors.html',greeting)  

class RatingView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Rating"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-rating.html',greeting)  


class NotificationsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Notifications"
        greeting['pageview'] = "UI Elements"
        return render (request,'components/ui-elements/components-notifications.html',greeting)

##FORMS
class FormelementsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Elements"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formelements.html',greeting)


class FormLayoutsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Layouts"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formlayouts.html',greeting)

        
class FormValidationView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Validation"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formvalidation.html',greeting)        

        
class FormAdvancedView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Advanced"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formadvanced.html',greeting)           


class FormEditorsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Editors"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formeditors.html',greeting)         

        
class FormFileuploadView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form File Upload"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formfileupload.html',greeting) 

class FormXeditableView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Xeditable"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formxeditable.html',greeting) 
              
class FormRepeaterView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Repeater"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formrepeater.html',greeting) 
           

class FormWizardView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Wizard"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formrwizard.html',greeting)                  
        
class FormMaskView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Form Mask"
        greeting['pageview'] = "Forms"
        return render (request,'components/forms/components-formrmask.html',greeting)         

        
##Tables
class BasicTablesView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Basic Tables"
        greeting['pageview'] = "Tables"
        greeting['universidad'] = AsesorUniversidad.objects.all()
        return render (request,'components/tables/components-basictables.html',greeting)  

class DataTablesView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Data Tables"
        greeting['pageview'] = "Tables"
        return render (request,'components/tables/components-datatables.html',greeting) 


class ResponsiveTablesView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Responsive Table"
        greeting['pageview'] = "Tables"
        return render (request,'components/tables/components-responsivetables.html',greeting) 

class EditableTablesView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Editable Table"
        greeting['pageview'] = "Tables"
        return render (request,'components/tables/components-editabletables.html',greeting) 

#Charts     
class ApexChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Apex Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-apexcharts.html',greeting)  

class EChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "E Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-echarts.html',greeting)  

class ChartJsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Chartjs Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-chartjs.html',greeting)  

class FlotChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Flot Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-flotcharts.html',greeting)    


class ToastUiChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Toast UI Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-toastuicharts.html',greeting)                  
                         

class JqueryKnobChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jquery Knob Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-jqueryknobcharts.html',greeting)   

class SparklineChartsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Sparkline Charts"
        greeting['pageview'] = "Charts"
        return render (request,'components/charts/components-sparklinecharts.html',greeting)                                   

#Icons        
class BoxIconsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Boxicons"
        greeting['pageview'] = "Icons"
        return render (request,'components/icons/components-boxicons.html',greeting)         
        

class MaterialDesignView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Material Design"
        greeting['pageview'] = "Icons"
        return render (request,'components/icons/components-materialdesign.html',greeting)    


class DripIconsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Dripicons"
        greeting['pageview'] = "Icons"
        return render (request,'components/icons/components-dripicons.html',greeting)  

class FontAwesomeView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Font Awesome"
        greeting['pageview'] = "Icons"
        return render (request,'components/icons/components-fontawesome.html',greeting)                     

#Maps
class GoogleMapsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Google Maps"
        greeting['pageview'] = "Maps"
        return render (request,'components/maps/components-googlemaps.html',greeting) 

class VectorMapsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Vector Maps"
        greeting['pageview'] = "Maps"
        return render (request,'components/maps/components-vectormaps.html',greeting)      

class LeafletMapsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Leaflet Maps"
        greeting['pageview'] = "Maps"
        return render (request,'components/maps/components-leafletmaps.html',greeting)            
        