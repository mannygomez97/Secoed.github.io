from django.contrib.auth.decorators import login_required
from django.urls import path
from authentication import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('perfil', login_required(views.UsuarioPerfilView.as_view()), name="perfil"),
    path('pages-login', views.PagesLoginView.as_view(), name="pages-login"),
    path('pages-recoverpw', views.PagesRecoverpwView.as_view(), name="pages-recoverpw"),
    path('pages-lockscreen', views.PagesLockscreenView.as_view(), name="pages-lockscreen"),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='authentication/pages-change-password-view.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='authentication/pages-change-password-done.html'),
         name='password_change_done'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/pages-reset-password-done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/pages-reset-password-view.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/pages-confirmmail.html'),
         name='password_reset_complete'),
    path('pages-logout', views.logout, name='pages-logout'),

    path(r'usuario', login_required(views.UsuarioView.as_view()), name='usuario'),
    path(r'newUsuario', login_required(views.UsuarioView.newUsuario), name='newUsuario'),
    path(r'editUsuario/<int:pk>', login_required(views.UsuarioView.editUsuario), name='editUsuario'),
    path(r'viewUsuario/<int:pk>', login_required(views.UsuarioView.viewUsuario), name='viewUsuario'),
    path(r'deleteUsuario/<int:pk>', login_required(views.UsuarioView.deleteUsuario), name='deleteUsuario'),
]
