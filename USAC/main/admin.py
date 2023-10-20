from django.contrib import admin
from .models import docentes, cursos, Notas

from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.

class CursoInline(admin.TabularInline):
    model = cursos
    extra = 1
    
class DocentesAdmin(admin.ModelAdmin):
    inlines = [CursoInline]
  
    
    fields = ('user', 'login_attempts')
    list_display = ['user', 'mostrar_cursos']
    ordering = ['user']    
    search_fields = ['user__username', 'user__first_name', 'user__last_name'] 
    
    def mostrar_cursos(self, obj):
        return ", ".join([cursos.nombre for cursos in obj.cursos_set.all()])

admin.site.register(docentes, DocentesAdmin)

class CursosAdmin(admin.ModelAdmin):
    fields=('codigo', 'nombre', 'descripcion', 'costo', 'horario', 'cupo', 'docente', 'imagen')
    list_display = ['codigo', 'nombre', 'descripcion', 'costo', 'horario', 'cupo', 'docente','imagen']
    ordering = ['nombre']
    search_fields = ['nombre', 'codigo', 'docente__Nombre']  # Puedes personalizar los campos de búsqueda
    list_per_page = 15  # Cantidad de items por página
    # Otros atributos que puedes agregar para personalizar la vista del panel de administración

admin.site.register(cursos, CursosAdmin)

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'nota', 'descripcion')
    list_filter = ('curso',)
    search_fields = ('estudiante__username', 'curso__nombre')
