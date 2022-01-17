from django.shortcuts import render
from asesor.models import Asesor

def lista_asesores(request):
    asesor = Asesor.objects.all()
    return render(request, 'mail.html', {'asesor': asesor})	