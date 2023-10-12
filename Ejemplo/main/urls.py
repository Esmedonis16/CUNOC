from django.urls import path 
from . import views

from .views import VRegistro

urlpatterns = [
    path('home/', views.home, name='home'),
    path('nerds/', views.pagina_estudiantes, name='nerds'),
    #path('estudiantes/', portales),
    path('docentes/', views.portales, name='Docentes'),
    path('carreras/', views.catalogo_de_carreras, name='ingenieria'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', VRegistro.as_view(), name="registro"),
    path('base/', views.iniciar_sesion, name="baseestudiantes"),
]
