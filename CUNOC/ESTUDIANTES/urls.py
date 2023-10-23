from django.urls import path, include
from . import views
from .views import VRegistro

urlpatterns = [

    
    path('productos/', views.products, name='productos'),
    path('logout/', views.exit, name='exit'),
    
    
    path('home/', views.home, name='home'),
    path('pensum/', views.Pensum, name='Pensum'), 
    path('registro/', VRegistro.as_view(), name="registro"),
    path('LoginEstudiantes/', views.iniciar_sesion_estudiantes, name='InicioE'),
    path('PortalEstudiantes/', views.PE, name='PE'),
    path('PortalEstudiantes/', views.PE, name='perfil'),
    path('PortalEstudiantes/', views.PE, name='closed'),

]
