from django.http import request
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
