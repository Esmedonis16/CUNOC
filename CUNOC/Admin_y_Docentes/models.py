from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from ESTUDIANTES.models import allusuarios
from django.dispatch import receiver


#get_user_model
#User = get_user_model()

class Registros(models.Model):
    Añadir = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Registro de Docente'
        verbose_name_plural = 'Registro de Docentes'
        ordering = ['id']

class inges(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, null=False, default='',verbose_name='Nombre de usuario')
    first_name = models.CharField(max_length=150, null=False, verbose_name='Nombre')
    last_name = models.CharField(max_length=150, null=False, verbose_name='Apellido')
    email = models.EmailField(max_length=150)
    cui = models.CharField(max_length=13, primary_key=True, verbose_name='DPI')
    imagen = models.ImageField(upload_to='PerfilesDocentes', default='users_pictures/default.png', verbose_name='Foto de Perfil')
    login_attempts = models.IntegerField(default=0)
    active_account = models.BooleanField(null=False, default=True)
    account_locked = models.BooleanField(default=False, verbose_name='Bloquear usuario')

    class Meta:
        db_table = 'RegistrosDocentes'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['cui']

    def __str__(self):
        return self.username
    
@receiver(post_save, sender=inges)
def add_user_to_docentes_group(sender, instance, created, **kwargs):
    if created:
        try:
            docentes_group, created = Group.objects.get_or_create(name='Docentes')
            
            if instance.user:
                instance.user.groups.add(docentes_group)
        except Exception as e:
            # Aquí puedes manejar el error como quieras, por ejemplo, imprimirlo
            print(f"Error al agregar al usuario al grupo Docentes: {e}")

        
class cursos(models.Model):
    
    codigo = models.CharField(max_length=4, null=False, unique=True)
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    horarioinicio = models.CharField(max_length=150, null=False, verbose_name='Inicio')
    horariofin = models.CharField(max_length=150, null=False, verbose_name='Fin')
    estudiantes_inscritos = models.ManyToManyField(User, related_name='cursos_inscritos', blank=True)
    cupo = models.IntegerField(null=False)
    docentes = models.ForeignKey('inges', on_delete=models.CASCADE)  
    imagen = models.ImageField(upload_to='PortadasCursos', default='users_pictures/default.png')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'RegistroCursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id'] 
        

class EstudianteCurso(models.Model):
    estudiante = models.ForeignKey(allusuarios, on_delete=models.CASCADE, verbose_name='Estudiante')
    curso = models.ForeignKey(cursos, on_delete=models.CASCADE, 
                            related_name= 'estudiantes_asignados', verbose_name='Curso')

    asignado = models.BooleanField(default=False, verbose_name='Asignado y Pagado')
    
    def __str__(self):
        return f'{self.estudiante.username} - {self.curso.nombre}'


    class Meta:
        db_table = 'Asigaciones_y_Desasignaciones'
        verbose_name = 'Asignaciones y Desasigaciones'
        verbose_name_plural = 'Asignaciones y Desasigaciones'
        ordering = ['id']
        
class Notas(models.Model):
    estudiante = models.ForeignKey(allusuarios, on_delete=models.CASCADE,verbose_name='Estudiante')
    curso = models.ForeignKey(cursos, on_delete=models.CASCADE, verbose_name='Curso')
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Nota Final')
    descripcion = models.CharField(max_length=100, null=False, verbose_name='Comentario')
    

    def __str__(self):
        return f"Nota de {self.estudiante.username} en {self.curso.nombre}"

    class Meta:
        db_table = 'RegistroNotas'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['id']  
