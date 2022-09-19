from notify.models import Notification
from django.contrib.auth.models import AnonymousUser


def notifications(request):
    context = {}

    if isinstance(request.user, AnonymousUser):
        return context
    else:
        allnotifications = request.user.notificaciones.all().order_by('-timestamp')[:100]
        return {'notifyList': allnotifications}
