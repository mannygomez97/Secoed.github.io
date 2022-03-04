from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView

from django.views import View

from swapper import load_model

from notify.models import Notification

from django.shortcuts import get_object_or_404, redirect

from authentication.models import *

from django.http import JsonResponse

# built-in signals
from django.db.models.signals import post_save

# signals
from notify.signals import notificar

Notificacion = load_model('notify', 'Notification')

class NotificacionView(View):
    def readTrue(request, pk):
        notificacion = get_object_or_404(Notification, pk=pk)
        notificacion.read = True
        notificacion.save()
        if notificacion.url == '#':
            return redirect('notify')
        else:
            return redirect(notificacion.url)

    def createNotificacion(request, numActividades, totalActividades):
        maxPorcentaje = 40
        porcentaje = (numActividades * totalActividades) / 100
        if (porcentaje <= maxPorcentaje):
            print(request.user.id)
            post_save.connect(notificar.send(request.user.id, destiny=request.user.id, verb='Retroalimentacion', level='Aviso', url='#', detalle='Usted debe recibir retrolimentacion porque no cumple con el porcentaje solicitado'), sender=Post)
            response = JsonResponse({'success': 'Notificacion creada correctamente'})
        else:
            response = JsonResponse({'success': 'No se creo una notificación'})
        response.status_code = 200
        return response

class NotificationList(ListView):
    model = Notificacion
    template_name = 'notificacion/notify.html'
    context_object_name = 'notify'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Notificaciones'
        return context

    @method_decorator(login_required)
    def dispatch(self, requets, *args, **kwargs):
        return super(NotificationList, self).dispatch(requets, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.notificaciones.all().order_by('-timestamp')
