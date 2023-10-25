from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ESTUDIANTES.urls')),
    path('', include('Admin_y_Docentes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
