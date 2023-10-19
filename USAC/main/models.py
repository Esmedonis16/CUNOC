# from email.policy import default
# from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

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
        verbose_name='Registro de Docente'
        verbose_name_plural = 'Registro de Docentes'
        ordering=['id']      
        
        
class docentes(models.Model):
    Nombre = models.CharField(max_length=150, null=False)
    Apellido = models.CharField(max_length=150, null=False)
    username = models.CharField(max_length=150, null=False, default='Docentes')
    cui = models.CharField(max_length=13, null=False,)
    login_attempts = models.IntegerField(null=False, default=3) #número de intentos de inicio de sesión fallidos de un usuario
    active_account = models.BooleanField(null=False, default=True)#Puede ser útil para implementar sistemas de activación o desactivación de cuentas de usuario.
    #Contraseña = models.CharField(max_length=128, null=False)
    #ConfirmarContraseña = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.username
    
    #def save(self, *args, **kwargs):
        #if self.Contraseña != self.ConfirmarContraseña:
            #raise ValueError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
        #super().save(*args, **kwargs)

    class Meta:
        db_table = 'RegistrosDocentes'
        verbose_name='Registro de Docente'
        verbose_name_plural = 'Registro de Docentes'
        ordering=['id'] 
        
class cursos(models.Model):
    codigo = models.CharField(max_length=4, null=False, unique=True)
    nombre = models.CharField(max_length=50, null=False)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    horario = models.CharField(max_length=150, null=False)
    cupo = models.IntegerField(null=False)
    docente = models.ForeignKey('docentes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'RegistroCursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']  
                 
       