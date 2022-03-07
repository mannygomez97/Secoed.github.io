from django.urls import path

from .views import NotificationList,NotificacionView

from django.contrib.auth.decorators import login_required


urlpatterns = [
	path('notify/', NotificationList.as_view(), name='notify'),
	path('readTrue/<int:pk>', login_required(NotificacionView.readTrue), name='readTrue'),
	path('createNotificacion/<int:numActividades>/<int:totalActividades>', login_required(NotificacionView.createNotificacion), name='createNotificacion'),
]