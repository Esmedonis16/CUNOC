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
        db_table = 'registros'
        verbose_name='Cliente'
        verbose_name_plural = 'Clientes'
        ordering=['id']      
        
       