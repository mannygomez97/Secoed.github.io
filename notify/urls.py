from django.urls import path

from .views import NotificationList,NotificacionView

from notify.views import PostView

from django.contrib.auth.decorators import login_required


urlpatterns = [
	path('notify/', NotificationList.as_view(), name='notify'),
	path('readTrue/<int:pk>', login_required(NotificacionView.readTrue), name='readTrue'),
	path('createNotificacion/<int:numActividades>/<int:totalActividades>/<int:pk>', login_required(NotificacionView.createNotificacion), name='createNotificacion'),
	path(r'publicaciones', login_required(PostView.as_view()), name='publicaciones'),
	path(r'newPost', login_required(PostView.newPost), name='newPost'),
    path(r'editPost/<int:pk>', login_required(PostView.editPost), name='editPost'),
    path(r'deletePost/<int:pk>', login_required(PostView.deletePost), name='deletePost'),
]