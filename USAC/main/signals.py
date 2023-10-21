# signals.py
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import allusuarios
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    try:
        allusuarios_instance = allusuarios.objects.get(user=user)
        allusuarios_instance.login_attempts = 0  # Reset intentos fallidos
        allusuarios_instance.save()
    except allusuarios.DoesNotExist:
        pass
    
@receiver(post_save, sender=allusuarios)
def add_user_to_perfil_group(sender, instance, created, **kwargs):
    if created:
        try:
            perfil = Group.objects.get(name='Estudiantes')
        except Group.DoesNotExist:
            perfil = Group.objects.create(name='Docentes')
            perfil = Group.objects.create(name='Administrativo')
        instance.user.groups.add(perfil)    
        pass
