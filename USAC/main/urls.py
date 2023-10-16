from django.urls import path 
from . import views

from .views import VRegistro

urlpatterns = [
    path('home/', views.home, name='home'),
    path('carreras/', views.catalogo_de_carreras, name='ingenieria'),
    path('registro/', VRegistro.as_view(), name="registro"),
    
    path('LoginEstudiantes/', views.iniciar_sesion_estudiantes, name="InicioDE"), 
    
    path('LoginDocentes/', views.iniciar_sesion_docentes, name='IniciarD'),
    path('LoginEstudiantes/', views.iniciar_sesion_estudiantes, name='IniciarE'),
    

]
