from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import inges, cursos, Notas, Registros, EstudianteCurso
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group
from ESTUDIANTES.models import allusuarios
from django.shortcuts import get_object_or_404


@admin.register(Registros)
class clickadmin(admin.ModelAdmin):
    list_display = ('Añadir', 'click_boton')
    
    def click_boton(self, obj):
        return format_html('<a class="button" href="{}">Formulario de Registro</a>', reverse('boton', args=[obj.pk]))

    click_boton.short_description = 'Acción'
    click_boton.allow_tags = False
    

class CursoInline(admin.TabularInline):
    model = cursos
    extra = 1
    
@admin.register(inges)    
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
    
    user_groups.short_description = 'Rol'   

class allusuariosAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', ]
    list_filter = ()
    
    def is_active_display(self, obj):
        return obj.is_active
    is_active_display.short_description = 'Activo'

admin.site.register(allusuarios, allusuariosAdmin)


class CursoInline(admin.TabularInline):
    model = EstudianteCurso
    extra = 1
    fk_name = 'curso'

@admin.register(cursos)
class CursosAdmin(admin.ModelAdmin):
    fields=('codigo', 'nombre', 'descripcion', 'costo', 'horarioinicio', 'horariofin', 'cupo', 'docentes', 'imagen')
    list_display = ['codigo', 'nombre', 'descripcion', 'costo', 'horarioinicio', 'horariofin',
                    'cupo', 'docentes','imagen', 'num_estudiantes_inscritos']
    ordering = ['nombre']
    search_fields = ['nombre', 'codigo', 'docentes__nombre','estudiantes_asignados']  
    list_per_page = 15  # Cantidad de items por página
    #filter_horizontal = ('estudiantes_inscritos',)  
    
    def num_estudiantes_inscritos(self, obj):
        return EstudianteCurso.objects.filter(curso=obj, asignado=True).count()

    num_estudiantes_inscritos.short_description = 'Estudiantes Inscritos'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs # El superusuario ve todos los cursos
        elif request.user.groups.filter(name='Docentes').exists():
            return qs.filter(docentes__user=request.user)# Filtra los cursos por el docente conectado
        else:
            usuario_actual = allusuarios.objects.get(user=request.user)
            if request.user.groups.filter(name='Estudiantes').exists():
            # Filtra los cursos a los que el estudiante se ha asignado
                return qs.filter(estudiantecurso__estudiante=usuario_actual)
        return qs
    
    inlines = [CursoInline]


@admin.register(EstudianteCurso)
class EstudianteCursoAdmin(admin.ModelAdmin): 
    
    list_display = ['estudiante', 'curso', 'asignado']   
    search_fields = ['curso__nombre','estudiantes_asignados'] 
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        elif request.user.groups.filter(name='Docentes').exists():
            return qs.filter(curso__docentes__user=request.user)
        elif request.user.groups.filter(name='Estudiantes').exists():
            usuario_actual = allusuarios.objects.get(user=request.user)
            return qs.filter(estudiantecurso__estudiante=usuario_actual)
        return qs 



@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    
    
    list_display = ('estudiante', 'curso', 'nota', 'descripcion',)
    list_filter = ('curso',)
    search_fields = ('estudiante__username', 'curso__nombre')
    actions = ['exportar_notas_a_excel']

    def nota_final(self, obj):
        return obj.nota if obj.nota else None

    nota_final.short_description = 'Nota Final'

    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restringe las opciones de estudiantes y cursos en el formulario de notas basado en la inscripción y asignación del curso. """
        if db_field.name == 'estudiante':
            if request.user.is_superuser:
                kwargs["queryset"] = allusuarios.objects.all()
            else:
                docente = get_object_or_404(inges, user=request.user)
                cursos_del_docente = cursos.objects.filter(docentes=docente)
                kwargs["queryset"] = allusuarios.objects.filter(
                    estudiantecurso__curso__in=cursos_del_docente,
                    estudiantecurso__asignado=True
                ).distinct()
        elif db_field.name == "curso" and not request.user.is_superuser:
            docente = get_object_or_404(inges, user=request.user)
            kwargs["queryset"] = cursos.objects.filter(docentes=docente)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Docentes').exists():
            docente = get_object_or_404(inges, user=request.user)
            cursos_del_docente = cursos.objects.filter(docentes=docente)
            # Asegúrate de referenciar la relación y el campo correcto
            estudiantes_ids = EstudianteCurso.objects.filter(
                curso__in=cursos_del_docente, 
                asignado=True
            ).values_list('estudiante__user__id', flat=True)  # Aquí estudiante es un allusuarios, por lo que se usa user__id
            return qs.filter(curso__in=cursos_del_docente, estudiante__user__id__in=estudiantes_ids)
        return qs.none()

    @admin.action(description='Exportar Notas a Excel')  # Decorador de acción correcto
    def exportar_notas_a_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Notas de los Cursos'

        # Agrega los encabezados de las columnas
        columns = ['Profesor', 'Curso', 'Estudiante', 'Nota', 'Comentario']
        ws.append(columns)

        # Itera sobre el queryset para obtener los cursos del profesor
        for nota in queryset:
            curso = nota.curso
            docente = curso.docentes
            estudiante = nota.estudiante
            row = [
                docente.user.get_full_name(),
                curso.nombre,
                estudiante.user.get_full_name(),
                nota.nota,
                nota.descripcion
            ]
            ws.append(row)

        # Establece el nombre del archivo Excel
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="notas_del_profesor.xlsx"'
        wb.save(response)

        return response

    exportar_notas_a_excel.short_description = "Exportar Notas a Excel"

