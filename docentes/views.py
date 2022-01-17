from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import numpy

from docentes.models import *
from docentes.forms import *

class CategoriaView(View):
    def get(self, request):
        categoriasView = Categoria.objects.order_by('categoria')
        greeting = {'heading': 'Categoria de preguntas', 'pageview': 'Docentes', 'categoriasView': categoriasView, }
        return render(request, 'docentes/categoriaPreguntas.html', greeting)

    # Metodo para guardar una nueva categoria
    def newCategoria(request):
        if request.method == 'POST':
            categoriaForm = CategoriaForm(request.POST)
            if categoriaForm.is_valid():
                categoriaForm.save()
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
            return redirect('categoriaPregunta')
        else:
            categoriaFormView = CategoriaForm()
            categoria = Categoria()
            view = False
            context = {'categoriaFormView': categoriaFormView, 'categoria': categoria, 'view': view}
        return render(request, 'docentes/categoriaForm.html', context)

    # Consulta el registro de una categoria por su pk
    def viewCategoria(request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoriaFormView = CategoriaForm(instance=categoria)
        view = True
        context = {'categoriaFormView': categoriaFormView, 'categoria': categoria, 'view': view}
        return render(request, 'docentes/categoriaForm.html', context)

    # Editar los datos de una categoria por su pk
    def editCategoria(request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        if request.method == 'POST':
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                messages.success(request, "Se edito correctamente", "success")
                return redirect('categoriaPregunta')
        else:
            categoriaFormView = CategoriaForm(instance=categoria)
            view = False
            context = {'categoriaFormView': categoriaFormView, 'categoria': categoria, 'view': view}
        return render(request, 'docentes/categoriaForm.html', context)

    # Elimina una categoria
    def deleteCategoria(request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        if categoria:
            categoria.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('categoriaPregunta')

class ConfPreguntasView(View):

    def get(self, request):
        confPreguntasView = ConfPreguntas.objects.order_by('pregunta').order_by('periodo')
        greeting = {'heading': "Preguntas de evaluación de la plataforma SECOED", 'pageview': "Docentes",
                    'confPreguntasView': confPreguntasView, }
        return render(request, 'docentes/configuracionPreguntas.html', greeting)

    # Metodo para guardar una nueva pregunta
    def newConfPreguntas(request):
        if request.method == 'POST':
            confPreguntasForm = ConfPreguntasForm(request.POST)
            if confPreguntasForm.is_valid():
                confPreguntasForm.save()
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
            return redirect('conf_preguntas')
        else:
            confPreguntasFormView = ConfPreguntasForm()
            confPreguntas = ConfPreguntas()
            view = False
            context = {'confPreguntasFormView': confPreguntasFormView, 'confPreguntas': confPreguntas, 'view': view}
        return render(request, 'docentes/confPreguntasForm.html', context)

    # Consulta el registro de una pregunta por su pk
    def viewConfPreguntas(request, pk):
        confPreguntas = get_object_or_404(ConfPreguntas, pk=pk)
        confPreguntasFormView = ConfPreguntasForm(instance=confPreguntas)
        view = True
        context = {'confPreguntasFormView': confPreguntasFormView, 'confPreguntas': confPreguntas, 'view': view}
        return render(request, 'docentes/confPreguntasForm.html', context)

    # Editar los datos de un menu por su pk
    def editConfPreguntas(request, pk):
        confPreguntas = get_object_or_404(ConfPreguntas, pk=pk)
        if request.method == 'POST':
            ##editarField
            ##request.POST._mutable = True
            ##request.POST['pregunta'] = request.POST['pregunta'].capitalize()
            ##request.POST._mutable = False
            ##endEditarField
            form = ConfPreguntasForm(request.POST, instance=confPreguntas)
            if form.is_valid():
                form.save()
                messages.success(request, "Se edito correctamente", "success")
                return redirect('conf_preguntas')
        else:
            confPreguntasFormView = ConfPreguntasForm(instance=confPreguntas)
            view = False
            context = {'confPreguntasFormView': confPreguntasFormView, 'confPreguntas': confPreguntas, 'view': view}
        return render(request, 'docentes/confPreguntasForm.html', context)

    # Elimina una pregunta
    def deleteConfPreguntas(request, pk):
        confPreguntas = get_object_or_404(ConfPreguntas, pk=pk)
        if confPreguntas:
            confPreguntas.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('conf_preguntas')

class EvaluacionView(View):
    def get(self, request):
        fecha = datetime.now()
        periodo = fecha.year
        username = request.session['username']
        categoria = Categoria.objects.order_by('categoria')
        preguntas = ConfPreguntas.objects.filter(periodo = periodo)
        evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
        comprobacion = True
        value = [1,2,3,4,5]
        val1 = numpy.size(preguntas)
        val2 = numpy.size(evaluacion)
        if not preguntas:
            print('1.')
            comprobacion = False
        else:
            print('2.')
            if not evaluacion:
                print('2.1.')
                _evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = True)
                if not _evaluacion:
                    print('2.1.1.')
                    for i in preguntas:
                        c = Evaluacion(pregunta = i, opcion = 1, usuario = username, contestado = False)
                        c.save()
                    evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
                else:
                    print('2.1.2.')
                    val3 = numpy.size(_evaluacion)
                    if val1 > val3:
                        print('2.1.2.1.')
                        idPregunta = []
                        for i in _evaluacion:
                            idPregunta.append(i.pregunta.id)
                        temp = ConfPreguntas.objects.exclude(id__in = idPregunta)
                        for i in temp:
                            c = Evaluacion(pregunta = i, opcion = 1, usuario = username, contestado = False)
                            c.save()
                        evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
                    else:
                        print('2.1.2.2.')
                        comprobacion = False
            else:
                print('2.2.')
                _evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = True)
                if not _evaluacion:
                    if val1 > val2 :
                        print('2.2.1.')
                        evaluacion.delete()
                        for i in preguntas:
                            c = Evaluacion(pregunta = i, opcion = 1, usuario = username, contestado = False)
                            c.save()
                        evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
                else:
                    val3 = numpy.size(_evaluacion)
                    if val1 > val3:
                        evaluacion.delete()
                        idPregunta = []
                        for i in _evaluacion:
                            idPregunta.append(i.pregunta.id)
                        temp = ConfPreguntas.objects.exclude(id__in = idPregunta)
                        for i in temp:
                            c = Evaluacion(pregunta = i, opcion = 1, usuario = username, contestado = False)
                            c.save()
                        evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
                    else:
                        print('2.2.2.2.')
                        comprobacion = False
        greeting = {'heading': "Evaluación de la plataforma SECOED", 'pageview':"Docentes", 'preguntas':preguntas, 'comprobacion':comprobacion, 'evaluacion':evaluacion, 'value':value, 'periodo':periodo, 'categoria':categoria}
        return render(request, 'docentes/evaluacionPlataforma.html', greeting)

    def saveEvaluacion(request):
        if request.method == 'POST':
            cont = 1
            for key, values in request.POST.lists():
                if cont > 1:
                    print('Key: ', key,' ---> Valor: ',values[0])
                    evaluacion = get_object_or_404(Evaluacion, pk=key)
                    evaluacion.opcion = values[0]
                    evaluacion.contestado = True
                    evaluacion.save()
                cont +=1
        messages.success(request, "Se guardo correctamente sus respuestas", "success")
        return redirect('evaluacion-plataforma')