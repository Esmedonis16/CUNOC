from django.contrib import admin
from .models import inges, cursos, Notas

from django.contrib.auth.models import Group
# Register your models here.


class CursoInline(admin.TabularInline):
    model = cursos
    extra = 1
    
class DocenteAdmin(admin.ModelAdmin):   
    inlines = [CursoInline]
    
    list_display = ['username', 'first_name', 'last_name', 'cui','user_groups','mostrar_cursos']   
    search_fields = ['user__username', 'user__groups__name'] 
    list_filter = ['user__groups']
    ordering = ['username']   
    
    def mostrar_cursos(self, obj):
        return ", ".join([cursos.nombre for cursos in obj.cursos_set.all()])
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('user__groups')
    
    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.user.groups.all().order_by('name')])
    
    user_groups.short_description = 'Groups'
    
admin.site.register(inges, DocenteAdmin)

class CursosAdmin(admin.ModelAdmin):
    fields=('codigo', 'nombre', 'descripcion', 'costo', 'horario', 'cupo', 'docentes', 'imagen')
    list_display = ['codigo', 'nombre', 'descripcion', 'costo', 'horario', 'cupo', 'docentes','imagen']
    ordering = ['nombre']
    search_fields = ['nombre', 'codigo', 'docentes__nombre']  # Corregido el nombre de los campos
    list_per_page = 15  # Cantidad de items por página
    # Otros atributos que puedes agregar para personalizar la vista del panel de administración

admin.site.register(cursos, CursosAdmin)

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'nota', 'descripcion')
    list_filter = ('curso',)
    search_fields = ('estudiante__username', 'curso__nombre')
