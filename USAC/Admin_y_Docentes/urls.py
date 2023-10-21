from django.urls import path 
from . import views
from main import views
from django.contrib.auth import login, logout, authenticate
from .views import RDocentes
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/', views.home, name='home'),
    path('registrodocente/', RDocentes.as_view(), name='signup'),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)