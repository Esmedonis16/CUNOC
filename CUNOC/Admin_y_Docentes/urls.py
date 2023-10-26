from django.urls import path 
from . import views
from django.contrib.auth import login, logout, authenticate
from .views import RDocentes
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('registrodocente/', RDocentes.as_view(), name='signup'),
    path('boton/<int:pk>/', views.boton, name='boton'),
    #path('mis_cursos/', views.cursos_del_estudiante, name='cursos_del_estudiante'),
    #path('mis_cursos/', views.pensum, name='llamandocursos'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)