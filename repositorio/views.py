from multiprocessing import context
from sre_constants import SUCCESS
from unittest import result
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
import os 
import sys
from pathlib import Path
import datetime
import time
import shutil


from hashlib import new
from lib2to3.pgen2 import token
from multiprocessing import context
import json
from ntpath import join
from re import template
from turtle import st
from typing import Sequence
from django.conf import settings
import requests
from django.views import View
from secoed.settings import TOKEN_MOODLE, API_BASE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Usuario
from components.models import CursoAsesores
from django.http import HttpResponse, JsonResponse, Http404
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from notify.views import notificacionRetroalimentacion
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
# Calendario
#from .utils import Calendar
from datetime import datetime, date
import calendar, locale
# locale.setlocale(locale.LC_ALL, 'es-ES')
from django.utils.safestring import mark_safe
from datetime import timedelta
#librerias de django
#from django.views.generic import CreateView, UpdateView, ListView, DeleteView
#from django.urls import reverse_lazy
#from django.shortcuts import render, redirect

#importar formulario

from .models import Carpeta
from .forms import CarpetaForm

from .models import Archivo
from .forms import ArchivoForm
file_path = settings.MEDIA_ROOT+os.sep+ "repositorio_archivos"

def ensure_dir(directory):
    #directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return False
    return os.path.exists(directory)

def ensure_dir_path(mypath,prefix=True):
    dirpath = file_path
    if(len(mypath)>0):
        if(mypath != "/"):
            if prefix == True:
                mypath = mypath[1:]
            dirpath = os.path.join(file_path, mypath )
    return dirpath

def custom_redirect2(url_name, **kwargs):
    from django.urls import reverse
    import urllib
    url = reverse(url_name)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

def custom_redirect(url_name,idcarpeta, **kwargs):
    from django.urls import reverse
    import urllib
    url = reverse(url_name, kwargs ={"idcarpeta":idcarpeta} )
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)
# Create your views here.

def recursive2(parent_id):
    item2 = Carpeta.objects.filter(idcarpeta=parent_id)
    items2 = []
    items3 = []
    for item in item2:
        items2.append(item)
        items3 = recursive2(item.parent_id)
    return  items3 + items2


def recursive(parent_id):
    item2 = Carpeta.objects.filter(idcarpeta=parent_id)
    
    items2 = []
    items3 = []
    for item in item2:
        if item.parent_id == 0:
            items2.append(item)
        else:
            items2.append(item)
            items3 = recursive2(item.parent_id)
            
    return items3 + items2

#class crearLibro(CreateView):
    #model=Libro
    #form_class = LibroForm
    #template_name='libro/crear.html'
    #succes_url = reverse_lazy['index']

#carpetas
def carpetas(request):
    carpetas=Carpeta.objects.filter(parent_id=0).order_by('idcarpeta')
    request.session['id_carpeta'] = "0"
    return render(request, 'repositorio/carpetas/index.html', {'carpetas': carpetas,'archivos':[]})#ojo carpeta libros #mostrar info al index

def crearcar(request):
    formulario = CarpetaForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid(): #recepcionar los datos
        
      

        m = formulario.save(commit=False) #guardarlos
        if "id_carpeta" in request.session:
                
            id_carpeta= request.session['id_carpeta']                 
            breadcrumbs = recursive(int(id_carpeta))
              
            if(id_carpeta!="0"):
                if len(breadcrumbs)<5:
                    archivo=Carpeta.objects.filter(idcarpeta=int(id_carpeta))
                    item = next(iter(archivo), None)
                    if item is not None:     
                        #print(item.ruta)    
                        #print( str(item.ruta) +os.sep+ formulario.cleaned_data['nombre'])              
                        m.ruta = str(item.ruta) +os.sep+ formulario.cleaned_data['nombre']
                 
                        if not os.path.exists( str(item.ruta) +os.sep+ formulario.cleaned_data['nombre']):
                            os.mkdir( str(item.ruta) +os.sep+ formulario.cleaned_data['nombre'])
                    m.parent_id = int(id_carpeta)
                    m.nombre_anterior=formulario.cleaned_data['nombre']
                    messages.add_message(request, messages.SUCCESS, 'Carpeta creada exitosamente')
                    m.save()
                        
                return redirect('ingresaracar',idcarpeta=id_carpeta)
            else: 
                
                m.ruta = str (file_path) +os.sep+ formulario.cleaned_data['nombre']
                m.parent_id = 0
                m.nombre_anterior=formulario.cleaned_data['nombre']
                m.save()
                messages.add_message(request, messages.SUCCESS, 'Carpeta creada exitosamente')
                if not os.path.exists(str (file_path) +os.sep+ formulario.cleaned_data['nombre'] ):
                    os.mkdir( str (file_path) +os.sep+ formulario.cleaned_data['nombre'] )
                return redirect('carpetas')


        else:
            m.ruta = str (file_path) +os.sep+ formulario.cleaned_data['nombre']
            m.parent_id = 0
            m.save()
            messages.add_message(request, messages.SUCCESS, 'Carpeta creada exitosamente')
            if not os.path.exists(m.ruta ):
                os.mkdir(m.ruta )
            return redirect('carpetas')
       
        
    return render(request, 'repositorio/carpetas/crearcar.html', {'formulario': formulario})


def editarcarhijo(carpeta,idcarpeta):
    carpetas=Carpeta.objects.filter(parent_id=idcarpeta)
    archivos=Archivo.objects.filter(carpeta__idcarpeta=idcarpeta)
    carpeta22=Carpeta.objects.filter(idcarpeta=idcarpeta)
    item = next(iter(carpeta22), None)
    items = []
    for item2 in recursive(idcarpeta):
        items.append(item2.nombre)
    items
    if(item is not None):
        for archivo2 in archivos:
            save_item = "repositorio_archivos/"+"/".join(items)+"/"            
            Archivo.objects.filter(idarchivo=archivo2.idarchivo).update(
                archivo = save_item+"/"+os.path.basename(archivo2.archivo.name)
            )
                                                
        for carpeta2 in carpetas:

            save_item = file_path+"/"+"/".join(items)+"/"+carpeta2.nombre_anterior  
            Carpeta.objects.filter(idcarpeta=carpeta2.idcarpeta).update(
                ruta=save_item
            )
            editarcarhijo(carpeta2,carpeta2.idcarpeta)



def editarcar(request,idcarpeta):

    try:
        carpeta=Carpeta.objects.get(idcarpeta=idcarpeta)
        formulario = CarpetaForm(request.POST or None, instance=carpeta)
        if formulario.is_valid() and request.POST:
            formulario.save()
            if(carpeta.parent_id>0):
                #cambiar nombre
               
                
                archivo=Carpeta.objects.filter(idcarpeta=idcarpeta)
                carpetas=Carpeta.objects.filter(parent_id=idcarpeta)
                archivos=Archivo.objects.filter(carpeta__idcarpeta=idcarpeta)
                
                item = next(iter(archivo), None)
                item2 = next(iter(carpetas), None)
                if os.path.exists(
                    carpeta.ruta              
                ):
                    print("aqui2")
                    os.rename(
                        carpeta.ruta,
                        
                        carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre']
                        )
                    )
                   
                    Carpeta.objects.filter(idcarpeta=idcarpeta).update(
                        nombre=formulario.cleaned_data['nombre'],
                        nombre_anterior=formulario.cleaned_data['nombre'],
                        ruta=carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre'] 
                        )
                    )
                    editarcarhijo(carpeta,carpeta.idcarpeta)
                        
                
                messages.add_message(request, messages.SUCCESS, 'Carpeta actualizada exitosamente')
                

                return redirect('ingresaracar',idcarpeta=carpeta.parent_id)
            else:
                #cambiar nombre
                print("aqui2")
                carpetas=Carpeta.objects.filter(parent_id=idcarpeta)
                archivos=Archivo.objects.filter(carpeta__idcarpeta=idcarpeta)
                if os.path.exists(
                    carpeta.ruta              
                ):
                    os.rename(
                        carpeta.ruta,
                        
                        carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre']
                        )
                    )

                    Carpeta.objects.filter(idcarpeta=idcarpeta).update(
                        nombre=formulario.cleaned_data['nombre'],
                        nombre_anterior=formulario.cleaned_data['nombre'],
                        ruta=carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre'] 
                        )
                    )
                    editarcarhijo(carpeta,carpeta.idcarpeta)

                messages.add_message(request, messages.SUCCESS, 'Carpeta actualizada exitosamente')
               

                return redirect('carpetas')
    except Carpeta.DoesNotExist:
        return redirect('carpetas')


    return render(request, 'repositorio/carpetas/editarcar.html', {'formulario': formulario})

def buscarcarp(request):
    buscar_carpeta="repositorio/carpetas/index.html"
    buscar=request.GET.get("buscar","")
    context={
            'carpetas': [],
            'archivos': [],
            'contar_resultado':[]
        }
    if len(buscar)>0:
        carpetas=Carpeta.objects.filter(nombre__icontains=buscar)
        archivos=Archivo.objects.filter(nombre__icontains=buscar)
        if "id_carpeta" in request.session:
            id_carpeta= request.session['id_carpeta']
            carpetas=Carpeta.objects.filter(nombre__icontains=buscar,parent_id=id_carpeta)
            archivos=Archivo.objects.filter(nombre__icontains=buscar,carpeta_id=id_carpeta)
            
        contar_resultado = (len(carpetas) == 0  and len(archivos) == 0) == True
        context['carpetas']=carpetas
        context['archivos']=archivos
        context['contar_resultado']=contar_resultado    
    return render(request, buscar_carpeta, context)

def ingresaracar(request,idcarpeta):
    nombre_carpeta = get_object_or_404(Carpeta, pk=idcarpeta)
    request.session['id_carpeta'] = str(idcarpeta)
    request.session['nombre_carpeta'] = nombre_carpeta.nombre
    carpetas = []
    if "id_carpeta" in request.session:
        carpetas=Carpeta.objects.filter(parent_id=request.session['id_carpeta'] ).order_by('idcarpeta')
    archivos=Archivo.objects.all().filter(carpeta_id=idcarpeta)
    breadcrumbs = recursive(idcarpeta)
    return render(request, 'repositorio/archivos/index.html', {'archivos': archivos,'carpetas':carpetas,'breadcrumbs':breadcrumbs})

def eliminarcar(request, idcarpeta):#PROCESO FALTA
    
    carpeta=Carpeta.objects.filter(idcarpeta=idcarpeta)
    item2 = next(iter(carpeta), None)
    carpeta.delete()
    if item2 is not None:
        dirpath = item2.ruta
        if os.path.exists(dirpath) == True:
            shutil.rmtree(dirpath, ignore_errors=True)
        carpeta=Carpeta.objects.filter(parent_id=idcarpeta)
        parent_id = item2.parent_id    
        messages.add_message(request, messages.SUCCESS, 'Carpeta eliminada exitosamente')
        carpeta.delete()
        if (parent_id > 0):
            return redirect('ingresaracar',idcarpeta=parent_id)
    
    return redirect('carpetas')


def seleccionar_tipo_archivos(request):
    id_carpeta= request.session['id_carpeta']  
    breadcrumbs = []
    if(id_carpeta!="0"):               
        breadcrumbs = recursive(int(id_carpeta))

    return render(request, 'repositorio/carpetas/seleccionar_tipo_archivos.html', {'breadcrumbs':len(breadcrumbs)<5})
    
#archivos
def archivos(request):#listar archivos
    carpetas = []
    if "id_carpeta" in request.session:
        carpetas=Carpeta.objects.filter(parent_id=request.session['id_carpeta'] ).order_by('idcarpeta')
    archivos=Archivo.objects.all().order_by('idarchivo')
    return render(request, 'repositorio/archivos/index.html', {'archivos': archivos,'carpetas':carpetas})#ojo carpeta libros #mostrar info al index

def crear(request):
    formulario = ArchivoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid(): #recepcionar los datos
        m = formulario.save(commit=False) #guardarlos
        
      
        carpeta_id=request.session['id_carpeta']
        archivo=Carpeta.objects.filter(idcarpeta=carpeta_id)
        item = next(iter(archivo), None)
        
        if item is not None:
            m.carpeta = item
            m.save()
            messages.add_message(request, messages.SUCCESS, 'Archivo creado exitosamente')

        
            if 'archivo' in request.FILES:
                #print( os.path.join( 
                #        file_path,
                #        m.archivo.name.replace('repositorio_archivos/','')
                #    ))
                #print(m.carpeta.ruta+os.sep+os.path.basename(m.archivo.name))
                shutil.move(
                    os.path.join( 
                        file_path,
                        m.archivo.name.replace('repositorio_archivos/','')
                    ),
                    os.path.join( 
                        file_path,
                        m.carpeta.ruta+os.sep+os.path.basename(m.archivo.name)
                    ),
                )
                #print( 'repositorio_archivos'+ m.archivo.name.replace(
                #        
                #        "repositorio_archivos/",item.ruta.replace(file_path,"")+"/"
                #    ))
                m.archivo.name = 'repositorio_archivos/'+ m.archivo.name.replace(
                        
                        "repositorio_archivos/",item.ruta.replace(file_path,"")+"/"
                    )
             
            m.save()
            carpeta_id=request.session['id_carpeta']  
            if  carpeta_id !="0":
                return redirect('ingresaracar',idcarpeta=carpeta_id)
        return redirect('archivos')#carga mi vista de archivos
    return render(request, 'repositorio/archivos/crear.html', {'formulario': formulario})#abrimos el formulario de crear

def editar(request,idarchivo):
    try:
        archivo=Archivo.objects.get(idarchivo=idarchivo)
        formulario = ArchivoForm(request.POST or None, request.FILES or None, instance=archivo)
        if formulario.is_valid() and request.POST:
            m = formulario.save(commit=False) #guardarlos
            carpeta_id=request.session['id_carpeta']
            carpeta=Carpeta.objects.filter(idcarpeta=carpeta_id)
            carpetahijos=Carpeta.objects.filter(parent_id=carpeta_id)
            item = next(iter(carpeta), None)
            
            if item is not None:
                m.carpeta = item
                m.save()

                    
                
                messages.add_message(request, messages.SUCCESS, 'Archivo Editado exitosamente')
                if 'archivo' in request.FILES:
                    
                    if not os.path.exists( os.path.join( (item.ruta),m.archivo.name.replace('repositorio_archivos/',''))):
                        shutil.move(
                            os.path.join( (file_path),m.archivo.name.replace('repositorio_archivos/','')),
                            os.path.join( (item.ruta),m.archivo.name.replace('repositorio_archivos/',""))
                        )
                        
                        m.archivo.name = 'repositorio_archivos/'+ m.archivo.name.replace(
                            "repositorio_archivos/",item.ruta.replace(file_path,"")+"/"
                        )
             
                        
                        m.save() 
            carpeta_id=request.session['id_carpeta']  
            if  carpeta_id !="0":
                return redirect('ingresaracar',idcarpeta=carpeta_id)

            return redirect('archivos')
    except Carpeta.DoesNotExist:
        return redirect('carpetas')

    return render(request, 'repositorio/archivos/editar.html', {'formulario': formulario})

def eliminar(request, idarchivo):
    
    archivo=Archivo.objects.all().filter(idarchivo=idarchivo)
    item = next(iter(archivo), None)
    
    
    if(item is not None):
    
        if os.path.exists(
              item.carpeta.ruta+os.sep+ os.path.basename(  item.archivo.name.replace('repositorio_archivos/',''))
            ):
            messages.add_message(request, messages.SUCCESS, 'Archivo eliminado exitosamente')
            
            os.remove(
                 item.carpeta.ruta+os.sep+ os.path.basename(  item.archivo.name.replace('repositorio_archivos/',''))
            )
    archivo.delete()
    carpeta_id=request.session['id_carpeta']  
    if  carpeta_id !="0":
        return redirect('ingresaracar',idcarpeta=carpeta_id)
    return redirect('archivos')

def buscarar(request):
    buscar_archivo="repositorio/archivos/index.html"
    buscarar=request.GET.get("buscarar","")
    context={
        'carpetas': [],
        'archivos': [],
        'contar_resultado':[]
    }
    if len(buscarar)>0:

        carpetas=Carpeta.objects.filter(nombre__icontains=buscarar)
        archivos=Archivo.objects.filter(nombre__icontains=buscarar)
        if "id_carpeta" in request.session:
            id_carpeta= request.session['id_carpeta']
            carpetas=Carpeta.objects.filter(nombre__icontains=buscarar,parent_id=id_carpeta)
            archivos=Archivo.objects.filter(nombre__icontains=buscarar,carpeta_id=id_carpeta)
            

        contar_resultado = (len(carpetas) == 0  and len(archivos) == 0) == True
        context['carpetas']=carpetas
        context['archivos']=archivos
        context['contar_resultado']=contar_resultado   
    return render(request, buscar_archivo, context)

    
def vistabusquedageneral(request):
    carpetas=Carpeta.objects.filter(parent_id=0).order_by('idcarpeta')
    request.session['id_carpeta'] = "0"
    return render(request, 'repositorio/buscar/index.html', {'carpetas': carpetas,'archivos':[]})#ojo carpeta libros #mostrar info al index

def ingresaracarbgeneral(request,idcarpeta):
    nombre_carpeta = get_object_or_404(Carpeta, pk=idcarpeta)
    request.session['id_carpeta'] = str(idcarpeta)
    request.session['nombre_carpeta'] = nombre_carpeta.nombre
    carpetas = []
    if "id_carpeta" in request.session:
        carpetas=Carpeta.objects.filter(parent_id=request.session['id_carpeta'] ).order_by('idcarpeta')
    archivos=Archivo.objects.all().filter(carpeta_id=idcarpeta)
    breadcrumbs = recursive(idcarpeta)
    return render(request, 'repositorio/buscar/ingresarcarpetabusqueda.html', {'archivos': archivos,'carpetas':carpetas,'breadcrumbs':breadcrumbs})

def buscargeneral(request):
    buscar_carpeta="repositorio/buscar/ingresarcarpetabusqueda.html"
    buscar=request.GET.get("buscar","")
    context={
            'carpetas': [],
            'archivos': [],
            'contar_resultado':[]
        }
    if len(buscar)>0:
        carpetas=Carpeta.objects.filter(nombre__icontains=buscar)
        archivos=Archivo.objects.filter(nombre__icontains=buscar)

        contar_resultado = (len(carpetas) == 0  and len(archivos) == 0) == True
        context['carpetas']=carpetas
        context['archivos']=archivos
        context['contar_resultado']=contar_resultado    
    return render(request, buscar_carpeta, context)

def editararchivobusqueda(request,idarchivo):
    try:
        archivo=Archivo.objects.get(idarchivo=idarchivo)
        formulario = ArchivoForm(request.POST or None, request.FILES or None, instance=archivo)
        if formulario.is_valid() and request.POST:
            m = formulario.save(commit=False) #guardarlos
            carpeta_id=request.session['id_carpeta']
            archivo=Carpeta.objects.filter(idcarpeta=carpeta_id)
            item = next(iter(archivo), None)
            
            if item is not None:
                m.carpeta = item
                m.save()
                messages.add_message(request, messages.INFO, 'Archivo Editado exitosamente')
                if 'archivo' in request.FILES:
                    
                    if not os.path.exists( os.path.join( (item.ruta),m.archivo.name.replace('repositorio_archivos/',''))):
                        shutil.move(
                            os.path.join( (file_path),m.archivo.name.replace('repositorio_archivos/','')),
                            os.path.join( (item.ruta),m.archivo.name.replace('repositorio_archivos/',""))
                        )
                        m.archivo.name =  os.path.join(
                            'repositorio_archivos/'+ os.sep+(item.ruta.replace(file_path,"")),
                            m.archivo.name.replace('repositorio_archivos/','')
                        )

                    m.save() 
            carpeta_id=request.session['id_carpeta']  
            if  carpeta_id !="0":
                return redirect('ingresarbusquedacarpeta',idcarpeta=carpeta_id)

            return redirect('vistabuscargeneral')
    except Archivo.DoesNotExist:
        return redirect('vistabuscargeneral')
    return render(request, 'repositorio/archivos/editar.html', {'formulario': formulario})

def editarcarbusqueda(request,idcarpeta):
    try:
        carpeta=Carpeta.objects.get(idcarpeta=idcarpeta)
        archivo=Carpeta.objects.filter(idcarpeta=carpeta.parent_id)
        carpetas=Carpeta.objects.filter(parent_id=idcarpeta)
        archivos=Archivo.objects.filter(carpeta__idcarpeta=idcarpeta)                

        formulario = CarpetaForm(request.POST or None, instance=carpeta)
        if formulario.is_valid() and request.POST:
            formulario.save()
            if(carpeta.parent_id>0):
                #cambiar nombre
                print("aqui3")
                item = next(iter(archivo), None)
                if os.path.exists(
                    carpeta.ruta              
                ):
                    
                    os.rename(
                        carpeta.ruta,
                        
                        carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre']
                        )
                    )
                    Carpeta.objects.filter(idcarpeta=idcarpeta).update(
                        nombre=formulario.cleaned_data['nombre'],
                        nombre_anterior=formulario.cleaned_data['nombre'],
                        ruta=carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre'] 
                        )
                    )
                    editarcarhijo(carpeta,carpeta.idcarpeta)

                messages.add_message(request, messages.SUCCESS, 'Carpeta actualizada exitosamente')
                

                return redirect('ingresarbusquedacarpeta',idcarpeta=carpeta.parent_id)
            else:
                print("aqui4")
                #cambiar nombre
                if os.path.exists(
                    carpeta.ruta              
                ):
                    
                    os.rename(
                        carpeta.ruta,
                        
                        carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre']
                        )
                    )
                    Carpeta.objects.filter(idcarpeta=idcarpeta).update(
                        nombre=formulario.cleaned_data['nombre'],
                        nombre_anterior=formulario.cleaned_data['nombre'],
                        ruta=carpeta.ruta.replace(
                            carpeta.nombre_anterior,
                            formulario.cleaned_data['nombre'] 
                        )
                    )
                    editarcarhijo(carpeta,carpeta.idcarpeta)

                messages.add_message(request, messages.SUCCESS, 'Carpeta actualizada exitosamente')
                
                return redirect('vistabuscargeneral')
        #return redirect('vistabuscargeneral')
    except Carpeta.DoesNotExist:
        #return redirect('vistabuscargeneral')
        pass
    return render(request, 'repositorio/carpetas/editarcar.html', {'formulario': formulario})


def eliminarbusquedacarpeta(request, idcarpeta):#PROCESO FALTA
    
    carpeta=Carpeta.objects.filter(idcarpeta=idcarpeta)
    item2 = next(iter(carpeta), None)
    carpeta.delete()
    if item2 is not None:
        dirpath = item2.ruta
        if os.path.exists(dirpath) == True:
            shutil.rmtree(dirpath, ignore_errors=True)
        carpeta=Carpeta.objects.filter(parent_id=idcarpeta)
        parent_id = item2.parent_id    
        messages.add_message(request, messages.SUCCESS, 'Carpeta eliminada exitosamente')
        carpeta.delete()
        if (parent_id > 0):
            return custom_redirect('ingresarbusquedacarpeta',idcarpeta=parent_id,buscar=request.GET.get('buscar',''))

    
    return custom_redirect2('vistabuscargeneral',buscar=request.GET.get('buscar',''))

    return render(request, 'repositorio/archivos/editar.html', {'formulario': formulario})

def eliminarbusquedaarchivo(request, idarchivo):
    
    archivo=Archivo.objects.all().filter(idarchivo=idarchivo)
    item = next(iter(archivo), None)
    
    
    
    if(item is not None):
    
        if os.path.exists(
              item.carpeta.ruta+os.sep+ os.path.basename(  item.archivo.name.replace('repositorio_archivos/',''))
            ):
            messages.add_message(request, messages.SUCCESS, 'Archivo eliminado exitosamente')
            
            os.remove(
                 item.carpeta.ruta+os.sep+ os.path.basename(  item.archivo.name.replace('repositorio_archivos/',''))
            )

    archivo.delete()
    carpeta_id=request.session['id_carpeta']  
    if  carpeta_id !="0":
        return custom_redirect('ingresarbusquedacarpeta',idcarpeta=int(carpeta_id),buscar=request.GET.get('buscar',''))

    
    return custom_redirect2('vistabuscargeneral',buscar=request.GET.get('buscar',''))