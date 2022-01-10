from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from docentes.models import *
from docentes.forms import *


# Create your views here.

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

def saveLoadPreguntas(preguntas, username):
     for i in preguntas:
        c = Evaluacion(pregunta = i, opcion = 1, usuario = username, contestado = False)
        c.save()

class EvaluacionView(View):
    def get(self, request):
        fecha = datetime.now()
        periodo = fecha.year
        username = request.session['username']
        preguntas = ConfPreguntas.objects.filter(periodo = periodo)
        evaluacion = Evaluacion.objects.filter(usuario = username).filter(contestado = False)
        for i in evaluacion:
            print()
        comprobacion = True
        value = [1,2,3,4,5]
        if not evaluacion:
            condicion = Evaluacion.objects.filter(usuario = username).filter(contestado = True)
            if not condicion:
                saveLoadPreguntas(preguntas, username)
            else:
                comprobacion = False
        greeting = {'heading': "Evaluación de la plataforma SECOED", 'pageview':"Docentes", 'preguntas':preguntas, 'comprobacion':comprobacion, 'evaluacion':evaluacion, 'value':value, 'periodo':periodo}
        return render(request, 'docentes/evaluacionPlataforma.html', greeting)

    def saveEvaluacion(request):
        if request.method == 'POST':
            cont = 1
            for key, values in request.POST.lists():
                if cont > 1:
                    print(key, values)
                    evaluacion = get_object_or_404(Evaluacion, pk=key)
                    evaluacion.opcion = values[0]
                    evaluacion.contestado = True
                    evaluacion.save()
                cont +=1
        messages.success(request, "Se guardo correctamente sus respuestas", "success")
        return redirect('evaluacion-plataforma')