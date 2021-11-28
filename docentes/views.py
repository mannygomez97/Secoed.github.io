from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from docentes.models import *
from docentes.forms import *


# Create your views here.

class ConfPreguntasView(View):

    def get(self, request):
        confPreguntasView = ConfPreguntas.objects.order_by('pregunta')
        greeting = {'heading': "Preguntas de evaluación de la plataforma SECOED", 'pageview': "Configuración",
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
