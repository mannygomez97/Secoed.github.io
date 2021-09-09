from django.http import request, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from conf.models import *


class DashboardView(View):
    def get(self, request):
        greeting = {'heading': "Inicio", 'pageview': "Inicio"}
        if 'username' in request.session:
            return render(request, 'dashboard/dashboard.html', greeting)
        else:
            return redirect('pages-login')


class AjaxEvent(View):
    def jsnCountLogin(request):
        data = {
            'coqueta': '5-0',
            'la': [{"lunes":10,
                    "martes":20,
                    "miercoles":30,
                    "jueves":40,
                    "viernes":50
                    }]
        }
        return JsonResponse(data)
