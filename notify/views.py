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
from notify.forms import PostForm
from authentication.models import Post
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

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

    def createNotificacion(request, numActividades, totalActividades, pk):
        maxPorcentaje = 40
        porcentaje = (numActividades * totalActividades) / 100
        if (porcentaje <= maxPorcentaje):
            post = Post()
            post.url = '#'
            post.title = "Retroalimentación"
            post.text = "La cantidad de actividades realizada no completa el porcentaje para aprobar el curso"
            post.user = get_object_or_404(Usuario, pk=pk)
            post.save()
            response = JsonResponse({'code': '1', 'success': 'Notificacion creada correctamente'})
        else:
            response = JsonResponse({'code': '0', 'success': 'No se creo una notificación'})
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


class PostView(View):

    # Carga los datos iniciales del HTML
    def get(self, request):
        postsview = Post.objects.order_by('-timestamp')
        greeting = {'heading': "Publicaciones", 'pageview': "Administración", "postsview": postsview}
        return render(request, 'notificacion/publicaciones.html', greeting)

    # Metodo para guardar un nuevo Post
    def newPost(request):
        if request.method == 'POST':
            postForm = PostForm(request.POST)
            if postForm.is_valid():
                postForm.save()
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
            return redirect('publicaciones')
        else:
            postFormView = PostForm()
            post = Post()
            view = False
            context = {'postFormView': postFormView, 'post': post, 'view': view}
        return render(request, 'notificacion/postForm.html', context)

    # Editar los datos de un menu por su pk
    def editPost(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Se edito correctamente", "success")
                return redirect('publicaciones')
        else:
            postFormView = PostForm(instance=post)
            view = False
            context = {'postFormView': postFormView, 'post': post, 'view': view}
        return render(request, 'notificacion/postForm.html', context)

    # Elimina un registro del Post
    def deletePost(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post:
            post.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('publicaciones')
