from django.urls import path
from . import views
from django.contrib.auth import login, logout, authenticate
from .views import VRegistro
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/', views.home, name='home'),
    path('pensum/', views.Pensum, name='Pensum'),
    path('registro/', VRegistro.as_view(), name="registro"),
    path('LoginEstudiantes/', views.iniciar_sesion_estudiantes, name='InicioE'),
    path('PortalEstudiantes/', views.PE, name='PE'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
