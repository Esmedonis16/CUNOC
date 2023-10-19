from django.contrib import admin
from .models import docentes, cursos

from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.

class CursoInline(admin.TabularInline):
    model = cursos
    extra = 1
    
class DocentesAdmin(admin.ModelAdmin):
    inlines = [CursoInline]
    fields=('username','Nombre', 'Apellido', 'cui', 'login_attempts')
    #readonly_fields=('login_attempts') #Evitar la modificacion en la edicion de registro
    list_display = ['username','Apellido', 'Nombre', 'cui','mostrar_cursos'] #Propiedades visibles del campo
    ordering = ['Nombre']    #Ordena registros por
    search_fields = ['Nombre', 'username', 'cui'] #Permite buscar por
    # list_display_links = [''] #brindar link a campo
    # list_filter=['']  #Añadir buscar por filtro
    list_per_page=15    #Cantidad de items por pagina
    # exclude=['']      #Excluir campos en la edicion de registro
    
    def mostrar_cursos(self, obj):
        return ", ".join([cursos.nombre for cursos in obj.cursos_set.all()])

admin.site.register(docentes, DocentesAdmin)

class CursosAdmin(admin.ModelAdmin):
    fields=('codigo', 'nombre', 'costo', 'horario', 'cupo', 'docente')
    list_display = ['codigo', 'nombre', 'costo', 'horario', 'cupo', 'docente']
    ordering = ['nombre']
    search_fields = ['nombre', 'codigo', 'docente__Nombre']  # Puedes personalizar los campos de búsqueda
    list_per_page = 15  # Cantidad de items por página
    # Otros atributos que puedes agregar para personalizar la vista del panel de administración

admin.site.register(cursos, CursosAdmin)

