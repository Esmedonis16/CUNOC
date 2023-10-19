# signals.py
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import docentes
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    try:
        docente = docentes.objects.get(user=user)
        docente.login_attempts = 0  # Reset intentos fallidos
        docente.save()
    except docentes.DoesNotExist:
        pass
