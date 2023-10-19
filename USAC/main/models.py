# from email.policy import default
# from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _

# Create your models here.


        
class allusuarios (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False, default='Nombre')
    last_name = models.CharField(max_length=150, null=False, default='Apellidos')
    username = models.CharField(max_length=150, null=False, default=user)
    email = models.EmailField(max_length=150, default="direccion@gmail.com")
    cui = models.CharField(max_length=13, null=False, default="0")
    profile_image = models.ImageField(upload_to='users_pictures', default='users_pictures/default.png')
    login_attempts = models.IntegerField(null=False, default=0)
    active_account = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'RegistrosEstudiantes'
        verbose_name='Registro de Estudiante'
        verbose_name_plural = 'Registro de Estudiantes'
        ordering=['id']      
        
        
class docentes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Una relación 1 a 1 con User
    login_attempts = models.IntegerField(default=0)
    active_account = models.BooleanField(null=False, default=True)
    account_locked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'RegistrosDocentes'
        verbose_name='Registro de Docente'
        verbose_name_plural = 'Registro de Docentes'
        ordering=['id'] 
        
class cursos(models.Model):
    codigo = models.CharField(max_length=4, null=False, unique=True)
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    horario = models.CharField(max_length=150, null=False)
    cupo = models.IntegerField(null=False)
    docente = models.ForeignKey('docentes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='users_pictures', default='users_pictures/default.png')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'RegistroCursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']  
                 
       