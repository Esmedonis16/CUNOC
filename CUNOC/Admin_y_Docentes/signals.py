from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import inges


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    try:
        allusuarios_instance = inges.objects.get(user=user)
        allusuarios_instance.login_attempts = 0  # Reset intentos fallidos
        allusuarios_instance.save()
    except inges.DoesNotExist:
        pass


    