from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
# Create your models here.

User = get_user_model()
class allusuarios(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='universitario')
    first_name = models.CharField(max_length=150, null=False, verbose_name='Nombre')
    last_name = models.CharField(max_length=150, null=False, verbose_name='Apellidos')
    username = models.CharField(max_length=150, null=False, default='')
    email = models.EmailField(max_length=150)
    cui = models.CharField(max_length=13, primary_key=True)
    profile_image = models.ImageField(upload_to='Perfiles', default='users_pictures/default.png',verbose_name='Foto de Perfil')
    login_attempts = models.IntegerField(default=0)
    active_account = models.BooleanField(null=False, default=True)
    account_locked = models.BooleanField(default=False)
    #student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'RegistrosEstudiantes'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['cui']
        
    def __str__(self):
        return self.username


@receiver(post_save, sender=allusuarios)
def add_user_to_docentes_group(sender, instance, created, **kwargs):
    if created:
        try:
            est_group, created = Group.objects.get_or_create(name='Estudiantes')
            
            if instance.user:
                instance.user.groups.add(est_group)
        except Exception as e:
            # Aquí puedes manejar el error como quieras, por ejemplo, imprimirlo
            print(f"Error al agregar al usuario al grupo Docentes: {e}")   