from django.contrib import admin
from django.urls import path
from secoed import views
from django.urls import include

urlpatterns = [
    path(r'jsnCountLogin', views.AjaxEvent.jsnCountLogin, name="jsnCountLogin"),

    path(r'admin/', admin.site.urls),

    # Dashboards View
    path(r'', views.DashboardView.as_view(), name='dashboard'),
    # Accounts
    path('accounts/login/', views.DashboardView.as_view(), name='dashboard'),
    # Layouts
    path(r'layout/', include('layout.urls')),

     #Authencation
    path(r'authentication/', include('authentication.urls')),

    #Configuraciones
    path(r'conf/', include('conf.urls')),

    # Autoevaluacion
    path('eva/', include('eva.urls')),

    # mis url de mi asesor
    path('asesor/', include('asesor.urls')),

    #Components
    path('components/', include('components.urls')),
]

