from django.contrib import admin
from django.urls import path
from secoed import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from secoed.views import Error404View, Error500View
from secoed.settings import DEBUG
urlpatterns = [
    # Inicio de sesión
    path('jsnCountLogin', views.AjaxEvent.jsnCountLogin, name="jsnCountLogin"),

    path(r'admin/', admin.site.urls),

    # Dashboards View
    path(r'', views.DashboardView.as_view(), name='dashboard'),

    # Accounts
    path('accounts/login/', views.DashboardView.as_view(), name='dashboard'),

    # Layouts
    path(r'layout/', include('layout.urls')),

    # Authencation
    path(r'authentication/', include('authentication.urls')),

    # Configuraciones
    path(r'conf/', include('conf.urls')),

    # Autoevaluacion
    path('eva/', include('eva.urls')),

    # mis url de mi asesor
    path('asesor/', include('asesor.urls')),

    # Components
    path('components/', include('components.urls')),
]
if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404View.as_view()
handler500 = Error500View.as_error_view()
