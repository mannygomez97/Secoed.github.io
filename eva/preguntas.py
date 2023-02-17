from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from eva.models import Ciclo, Ciclo2
from eva.forms import CicloForm, CicloFormCN
from django.http import JsonResponse, Http404, HttpResponseRedirect
from datetime import datetime


def view(request):
    global ex
    data={}

    if request.method == 'POST':
        action = request.POST['action']

        if action == 'add_periodo':
            try:
                form = CicloForm(request.POST)
                if form.is_valid():
                    if Ciclo.objects.filter(carrera=form.cleaned_data['carrera'], is_active=True).exists():
                        ciclo = Ciclo.objects.filter(carrera=form.cleaned_data['carrera'], is_active=True)[0]
                        message = f'Ya existe un periodo activo para la carrera {ciclo.carrera.descripcion} '
                        error = {
                            'Error ': 'Existe un periodo activo para la carrera ' + ciclo.carrera.descripcion + '.'}
                        response = JsonResponse({'message': message, 'error': error})
                        response.status_code = 409

                    ciclo = Ciclo(carrera=form.cleaned_data['carrera'],
                                  is_active=form.cleaned_data['activo'],
                                  name=form.cleaned_data['name'],
                                  date_created=datetime.now()
                                  )
                    ciclo.save(request)
                    return response
                else:
                    message = f'no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    return response
            except Exception as ex:
                transaction.set_rollback(True)
                data['error'] = str(ex)
                return JsonResponse(data)

    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'add_periodo':
                try:
                    data['title'] = u'Adicionar tipo de evidencia'
                    data['form'] = CicloForm
                    return render(request, "periodo/create.html", data)
                except Exception as ex:
                    pass

            if action == 'ciclo':
                try:
                    data['title'] = u'Ciclo'
                    #ids = None
                    periodo = Ciclo.objects.get(id=int(request.GET['id']))
                    object_list = Ciclo2.objects.filter(periodo=periodo)
                    #if 'id' in request.GET:
                    #    #ids = request.GET['id']
                    #    object_list = object_list.filter(periodo=request.GET['id'])
                    data['object_list'] = object_list
                    data['periodo'] = periodo
                    #data['ids'] = ids if ids else ""
                    return render(request, 'periodo/periodociclo.html', data)
                except Exception as ex:
                    pass
        else:
            try:
                data['title'] = u'Peroguntas por Periodo'
                ids = None
                object_list = Ciclo.objects.all()
                if 'id' in request.GET:
                    ids = request.GET['id']
                    object_list = object_list.filter(id=ids)

                data['object_list'] = object_list
                data['ids'] = ids if ids else ""
                return render(request, 'preguntas/list.html', data)
            except Exception as ex:
                return HttpResponseRedirect('/')





