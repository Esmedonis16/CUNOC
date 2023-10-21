# from django.db import models
# from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()
# from django.utils.translation import gettext_lazy as _

# # Perfiles de todos los Usuarios desde el superadmin
# class Perfiles(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='Perfil', verbose_name='Usuarios')
#     image = models.ImageField(upload_to='Perfiles', default='users_pictures/default.png', verbose_name='Imagen de perfil')
#     email = models.EmailField(max_length=150, default="direccion@gmail.com")
#     cui = models.CharField(max_length=13, null=False, default="0")
    
#     login_attempts = models.IntegerField(null=False, default=0)
#     active_account = models.BooleanField(null=False, default=True)

#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = 'RegistrosEstudiantes'
#         verbose_name='Registro de Estudiante'
#         verbose_name_plural = 'Registro de Estudiantes'
#         ordering=['id']      