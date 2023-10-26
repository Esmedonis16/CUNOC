from django.urls import path 
from . import views
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from .views import RDocentes
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('registrodocente/', RDocentes.as_view(), name='signup'),
    path('boton/<int:pk>/', views.boton, name='boton'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_password/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password/password_reset_complete.html"), name="password_reset_complete"),
    

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)