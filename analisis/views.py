from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import get_template
from authentication.models import RolUser, Usuario as User
from analisis.models import *
from django.db import connection
from django.utils import timezone
from django.db.models import Count
from xhtml2pdf import pisa
from auditoria.apps import GeneradorAuditoria

def listar_preguntas_respuestas():
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    sql = """
        SELECT DISTINCT
        n.nombre, COUNT(CAST (A.respuesta AS INTEGER)) AS cantidad, SUM(CAST (A.respuesta AS INTEGER)) as preguntas_respuestas,
        (SUM(CAST (A.respuesta AS INTEGER))/ COUNT(CAST (A.respuesta AS INTEGER))) as promedio
        FROM analisis_respuestas as A
        LEFT JOIN analisis_pregunta as Ap ON Ap.id = A.pregunta_id
        LEFT JOIN nivel as n ON  n.id = Ap.nivel_id
        GROUP BY  n.nombre
        ORDER BY  n.nombre DESC
    """
     # 
    cursor = connection.cursor()
    cursor.execute(sql)
    data = dictfetchall(cursor)
    cursor.close()
    return data

# listar_preguntas_respuestas_usuario_id(int(request.GET.get['usuario']))
def listar_preguntas_respuestas_usuario_id(usuario_id):
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    sql = """
        SELECT DISTINCT
        n.nombre, COUNT(CAST (A.respuesta AS INTEGER)) AS cantidad, SUM(CAST (A.respuesta AS INTEGER)) as preguntas_respuestas,
        (SUM(CAST (A.respuesta AS INTEGER))/ COUNT(CAST (A.respuesta AS INTEGER))) as promedio
        FROM analisis_respuestas as A
        LEFT JOIN analisis_pregunta as Ap ON Ap.id = A.pregunta_id
        LEFT JOIN nivel as n ON  n.id = Ap.nivel_id
        LEFT JOIN conf_user AS U ON U.id = A.username 
        WHERE A.username = {0}
        GROUP BY  n.nombre
        ORDER BY  n.nombre DESC
    """.format(usuario_id)
     # 
    
    
    cursor = connection.cursor()
    cursor.execute(sql)
    data = dictfetchall(cursor)
    cursor.close()
    return data

#Preguntas
def lista(request):
    buscarnivel = request.GET.get("buscarnivel","")
    buscarciclo = request.GET.get("buscarciclo","")
    db_data = AnalisisPregunta.objects.all()
    db_nivel = Nivel.objects.all()
    db_ciclo = Ciclo.objects.all()
    if len(buscarnivel)>0 and len(buscarciclo)>0:
        db_data = AnalisisPregunta.objects.filter(
            nivel__nivel = buscarnivel,
            ciclo__name = buscarciclo
        ).distinct()
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "db_ciclo":db_ciclo
    }
    return render(request, "analisis/list.html", context)

# CONSTANTES
m_NombreTablaAnalisisPregunta = "analisis_pregunta"
m_ProcesoAnalisPregunta = "PREGUNTAS"
def guardar(request):
    add_pregunta = request.POST['pregunta']
    add_nivel = request.POST['nivel']
    add_ciclo = request.POST['ciclo']
    try:
        ciclo_id = Ciclo.objects.get(id=request.POST['ciclo'])
        try:
            nivel = Nivel.objects.get(id=request.POST['nivel'])
            db_data = AnalisisPregunta(pregunta=add_pregunta,nivel=nivel,ciclo=ciclo_id)
            db_data.save()
            newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaAnalisisPregunta)
            GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaAnalisisPregunta, newJson, request.user.id)
        except  Nivel.DoesNotExist:
            pass
    
    except  Ciclo.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("lista"))

def borrar(request,data_id):
    db_data = AnalisisPregunta.objects.filter(id=data_id)
    kwargs = {'pk': data_id}
    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAnalisisPregunta, kwargs)
    db_data.delete()
    GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaAnalisisPregunta, kwargs["pk"], oldJson, request.user.id)
    return HttpResponseRedirect(reverse("lista"))

def actualiza(request,data_id):
    db_data = AnalisisPregunta.objects.filter(id=data_id)
    db_nivel = Nivel.objects.all()
    db_ciclo = Ciclo.objects.all()
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "db_ciclo":db_ciclo
    }
    return render(request, "analisis/actualizar.html", context)

def guardarActualizar(request):
    add_pregunta = request.POST['pregunta']
    add_ciclo = Ciclo.objects.get(pk=int(request.POST['ciclo']))
    add_nivel = Nivel.objects.get(pk=int(request.POST['nivel']))
    db_data = AnalisisPregunta.objects.filter(pk=request.POST['id'])
    pk = request.POST['id']
    kwargs = {'pk': pk}
    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAnalisisPregunta, kwargs)
    db_data.update(pregunta= add_pregunta, nivel= add_nivel, ciclo= add_ciclo)
    newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAnalisisPregunta, kwargs)
    GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaAnalisisPregunta, kwargs["pk"], newJson,
                                                    oldJson, request.user.id)
    return HttpResponseRedirect(reverse("lista"))


#Nivel
def listanivel(request):
    db_data = AnalisisPregunta.objects.all()
    db_nivel = Nivel.objects.all()
    db_ciclo = Ciclo.objects.all()
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "db_ciclo":db_ciclo
    }
    return render(request, "analisis/listanivel.html", context)

# CONSTANTES
m_NombreTablaNivel = "nivel"
m_ProcesoNivel = "CRITERIOS"

def guardarnivel(request):
    add_nivel = request.POST['nivel']
    try:
        ciclo_id = Ciclo.objects.get(id=request.POST['ciclo'])
        db_data = Nivel(ciclo=ciclo_id, nivel=add_nivel)
        db_data.save()
        newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaNivel)
        GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaNivel, newJson, request.user.id)
    except  Ciclo.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("listanivel"))

def borrarnivel(request,data_id):
    db_data = Nivel.objects.filter(id=data_id)
    kwargs = {'pk': data_id}
    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaNivel, kwargs)
    db_data.delete()
    GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaNivel, kwargs["pk"], oldJson, request.user.id)
    return HttpResponseRedirect(reverse("listanivel"))

def actualizanivel(request,data_id):
    db_nivel = Nivel.objects.filter(id=data_id)
    context = {
        "db_nivel":db_nivel,
    }
    return render(request, "analisis/actualizarnivel.html", context)

def guardarActualizarnivel(request):
    act_id = request.POST['id']
    add_nivel = request.POST['nivel']
    db_data = Nivel.objects.get(pk=act_id)
    db_data.nivel = add_nivel
    kwargs = {'pk': act_id}
    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaNivel, kwargs)
    db_data.save()
    newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaNivel, kwargs)
    GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaNivel, kwargs["pk"], newJson, oldJson, request.user.id)
    return HttpResponseRedirect(reverse("listanivel"))


#Respuestas
def listarespuestas(request):
    db_data = AnalisisPregunta.objects.all()
    db_preguntas =  AnalisisRespuestas.objects.filter(username=request.user.id)
    respuesas_completadas = []
    for respuesta in db_preguntas:
        respuesas_completadas.append(respuesta.pregunta.id)
    context = {
        "db_data":db_data,
        "db_preguntas":db_preguntas,
        "respuesas_completadas":respuesas_completadas
    }
    return render(request, "analisis/evaluacion.html", context)

def guardarespuestas(request):
    try:

        add_pregunta = AnalisisPregunta.objects.get(pk=int(request.POST['pregunta']))
        add_respuesta = request.POST['respuesta']
        add_nombres = request.POST['nombres']
        add_apellidos = request.POST['apellidos']
        add_email = request.POST['email']
        add_nivel = request.POST['nivel']
        add_ciclo = request.POST['ciclo']
        db_data = AnalisisRespuestas(pregunta=add_pregunta,
                                    respuesta=add_respuesta,
                                    username=request.user.id,
                                    nombres=add_nombres,
                                    apellidos=add_apellidos,
                                    email=add_email,
                                    nivel=add_nivel,
                                    ciclo=add_ciclo)           
        db_data.save()
        newJson = GeneradorAuditoria().GenerarJSONNuevo(m_ProcesoAnalisPregunta)
        GeneradorAuditoria().GenerarAuditoriaCrear(m_ProcesoAnalisPregunta, newJson, request.user.id)
    except AnalisisPregunta.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("listarespuestas")) 

#Reportes
def reportes(request):
    db_nivel = Nivel.objects.all().order_by('-nivel')
    db_data = listar_preguntas_respuestas()
    item2s = []
    for item2 in  db_data:
        item2s.append(item2['promedio']*20)
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "item2s":item2s
    }
    return render(request, "analisis/reportes.html", context)

#Reportes
def reportes_por_usuario(request, data_id):
    db_username =  Usuario.objects.filter(pk=data_id)
    db_nivel = Nivel.objects.all().order_by('-nivel')
    db_data = listar_preguntas_respuestas_usuario_id(int(data_id))
    item2s = []
    for item2 in  db_data:
        item2s.append(item2['promedio']*20)
    context = {
        "db_username":db_username,
        "db_data":db_data,
        "db_nivel":db_nivel,
        "item2s":item2s
    }
    return render(request, "analisis/reportes2usuario.html", context)

def reportes_pdf(request, data_id):
    db_nivel = Nivel.objects.all().order_by('-nivel')
    db_data = AnalisisRespuestas.objects.filter(username=data_id)
    db_usuario = Usuario.objects.filter(pk=data_id)
    db_grafico = listar_preguntas_respuestas_usuario_id(int(data_id))
    template_path = 'analisis/generate_pdf.html'
    item2s = []
    for item2 in  db_grafico:
        item2s.append(item2['promedio']*20)
    context = {
        "db_data":db_data,
        "db_usuario":db_usuario,
        "db_grafico":db_grafico,
        "item2s":item2s,
        "db_nivel":db_nivel
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #to directly download the pdf we need attachment 
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # to view on browser we can remove attachment 
    # response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response
    )
    return response



def reporteusuario(request):
    #usuario_administrador=False
    db_data =  User.objects.filter()
    db_nivel = Nivel.objects.all()
    db_data2 = []
    for item2 in db_data:
        db_data2 = AnalisisRespuestas.objects.filter(username=item2.id)
        if len(db_data2)==0:
            db_data = db_data.exclude(pk=item2.id)

    context = {
        "db_data2":db_data2,
        "db_data":db_data,
        "db_nivel":db_nivel
    }
    return render(request, "analisis/reportesusuarios.html", context)    


def reporteusuariopregunta(request,data_id):
    db_data =  AnalisisRespuestas.objects.filter(username=data_id)
    db_usuario = Usuario.objects.filter(pk=data_id)
    db_nivel = Nivel.objects.all()
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "db_usuario":db_usuario
    }

    return render(request, "analisis/reportesusuarios_preguntas.html", context)    


def borrarespuestas(request,data_id):
    db_data = AnalisisRespuestas.objects.filter(id=data_id)
    kwargs = {'pk': data_id}
    oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaAnalisisPregunta, kwargs)
    db_data.delete()
    GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaAnalisisPregunta, kwargs["pk"], oldJson, request.user.id)
    return HttpResponseRedirect(reverse("listarespuestas"))

def filtrarespuesta(request):
    buscarnivel = request.GET.get("buscarnivel","")
    buscarciclo = request.GET.get("buscarciclo","")
    db_data = AnalisisPregunta.objects.all()
    db_nivel = Nivel.objects.all()
    db_ciclo = Ciclo.objects.all()
    if len(buscarnivel)>0 and len(buscarciclo)>0:
        db_data = AnalisisPregunta.objects.filter(
            nivel__nivel = buscarnivel,
            ciclo__name = buscarciclo
        ).distinct()
    context = {
        "db_data":db_data,
        "db_nivel":db_nivel,
        "db_ciclo":db_ciclo
    }
    return render(request, "analisis/reportesusurios.html", context)