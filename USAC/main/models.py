from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

        
class allusuarios(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='universitario')
    first_name = models.CharField(max_length=150, null=False, verbose_name='Nombre')
    last_name = models.CharField(max_length=150, null=False, verbose_name='Apellidos')
    username = models.CharField(max_length=150, null=False, default='')
    email = models.EmailField(max_length=150)
    cui = models.CharField(max_length=13, null=False)
    profile_image = models.ImageField(upload_to='Perfiles', default='users_pictures/default.png',verbose_name='Foto de Perfil')
    login_attempts = models.IntegerField(default=0)
    active_account = models.BooleanField(null=False, default=True)
    account_locked = models.BooleanField(default=False)

    class Meta:
        db_table = 'RegistrosEstudiantes'
        verbose_name='Registro de Estudiante'
        verbose_name_plural = 'Registro de Estudiantes'
        ordering=['id']    
        
    def __str__(self):
        return self.username   
          
@receiver(post_save, sender=allusuarios)
def add_user_to_docentes_group(sender, instance, created, **kwargs):
    if created:
        docentes_group, _ = Group.objects.get_or_create(name='Estudiantes')
        instance.user.groups.add(docentes_group)     
                 
       