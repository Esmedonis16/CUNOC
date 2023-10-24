from django.urls import path
from . import views
from .views import VRegistro


urlpatterns = [
    path('logout/', views.salir, name='salir'),
    path('home/', views.home, name='home'),
    path('pensum/', views.Pensum, name='Pensum'), 
    path('registro/', VRegistro.as_view(), name="registro"),
    path('PortalEstudiantes/', views.PE, name='PE'),
    path('LoginEstudiantes/', views.iniciar_sesion_estudiantes, name='InicioE'),
    
]
