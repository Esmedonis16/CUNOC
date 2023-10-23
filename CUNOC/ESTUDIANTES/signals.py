# signals.py
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import allusuarios

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    try:
        allusuarios_instance = allusuarios.objects.get(user=user)
        allusuarios_instance.login_attempts = 0  # Reset intentos fallidos
        allusuarios_instance.save()
    except allusuarios.DoesNotExist:
        pass
    