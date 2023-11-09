from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.views.generic import View, TemplateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import allusuarios
from Admin_y_Docentes.models import cursos, EstudianteCurso, Notas
#from Admin_y_Docentes.models import cursos
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.auth.models import User 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Profile



@login_required
def pensum(request):
    pensum = cursos.objects.filter(cupo__gt=0)
    return render(request, 'pensum.html', {'pensum': pensum})

        
@login_required
def cursos_asignados(request):
    usuario_actual = allusuarios.objects.get(user=request.user)  # Obtener el perfil del usuario actual
    asignaciones = EstudianteCurso.objects.filter(estudiante=usuario_actual, asignado=True)  # Obtener todas las asignaciones para ese usuario que están marcadas como 'asignado'
    return render(request, 'cursos_asignados.html', {'asignaciones': asignaciones})



@login_required
def inscribir_curso(request, curso_id):
    curso = get_object_or_404(cursos, id=curso_id)

    print("Grupos del usuario:", request.user.groups.values_list('name', flat=True))

    if request.user.groups.filter(name='Estudiantes').exists():  # Comprobar si el usuario pertenece al grupo 'Estudiantes'
        try:
            allusuario_instance = allusuarios.objects.get(user=request.user)  # Obtener la instancia del usuario

            if curso.cupo > 0:  # Verificar que haya cupo disponible
                asignacion, creado = EstudianteCurso.objects.get_or_create(
                    estudiante=allusuario_instance,  
                    curso=curso
                )
                if creado:
                    curso.cupo -= 1  
                    curso.save()  
                    asignacion.asignado = True  
                    asignacion.save()  
                    

                    # Enviar correo de confirmación
                    subject = 'Confirmación de Inscripción de Curso'
                    message = render_to_string('emails/asignacion.html', {
                        'user': request.user,
                        'curso': curso
                    })

                    email = EmailMessage(
                        subject,
                        message,
                        'academiacunoc@gmail.com',
                        [request.user.email]
                    )
                    email.content_subtype = 'html'
                    email.send()
                else:
                    messages.warning(request, 'Ya estás asignado a este curso.')
            else:
                messages.error(request, 'Lo sentimos, no hay cupo disponible para este curso.')

        except allusuarios.DoesNotExist:
            messages.error(request, 'Tu perfil de estudiante no se encuentra.')
    else:
        messages.error(request, 'No tienes permisos para inscribirte en cursos.')
    messages.success(request, 'Has sido asignado al curso exitosamente.')
    return redirect('allcursos')
    


@login_required
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(cursos, id=curso_id)

    if request.user.groups.filter(name='Estudiantes').exists():  
        allusuario_instance = allusuarios.objects.get(user=request.user)

        # Consulta alternativa
        asignaciones = EstudianteCurso.objects.filter(estudiante=allusuario_instance, curso=curso)
        
        if asignaciones.exists():  # Verificamos si hay registros que coinciden
            for asignacion in asignaciones:
                asignacion.delete()  # Eliminamos cada registro que coincide

            curso.cupo += 1  # Incrementamos el cupo del curso
            curso.save()
        

            # Enviar correo de confirmación de desasignación
            subject = 'Confirmación de Desasignación de Curso'
            message = render_to_string('emails/desasignacion.html', {
                'user': request.user,
                'curso': curso
            })

            email = EmailMessage(
                subject,
                message,
                'academiacunoc@gmail.com',
                [request.user.email]
            )
            email.content_subtype = 'html'
            email.send()
        else:
            messages.warning(request, 'No estás asignado a este curso para poder eliminarlo.')
            
    messages.success(request, 'Has sido desasignado al curso exitosamente.')
    return redirect('cursos_asignados')




def home(request):
    return render(request, 'Home.html')


def PE(request):
    cliente_username = request.session.get('cliente_username', None)
    if cliente_username is not None:
        cliente = allusuarios.objects.get(username=cliente_username)
        return render(request, "PortalEstudiantes.html", {"cliente": cliente})
    else:
        return redirect('InicioE')


def salir(request):
    logout(request)
    return redirect('home')

def InicioS(request):
    return render(request, 'IniciarSesion.html')

def Facial(request):
    return render(request, 'Facial.html')


def exit(request):
    logout(request)
    return redirect('home')


def iniciar_sesion_estudiantes(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(request=request, username=username, password=password)
            grupo_estudiantes = Group.objects.get(name='Estudiantes')
            if usuario is not None:
                if not usuario.is_superuser and grupo_estudiantes in usuario.groups.all():
                    login(request, usuario)
                    cliente = allusuarios.objects.get(username=username)
                    request.session['cliente_username'] = cliente.username
                    messages.success(request, "Inicio de sesión exitoso :) ")
                    return render(request, "PortalEstudiantes.html", {"form": form, "cliente": cliente})
                else:
                    messages.error(request, "Credenciales inválidas")
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Información no válida")
    form = AuthenticationForm()
    return render(request, "LoginEstudiantes.html", {"form": form})



class VRegistro(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "Registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            ncui = form.cleaned_data.get('cui')
            img = form.cleaned_data.get("profile_imagen")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(request=request, username=username, password=password)
            login(request, usuario)
            nuevo_usuario = allusuarios(user=request.user, username=request.user.username, first_name=request.user.first_name,
                                        last_name=request.user.last_name, email=request.user.email, cui=ncui, profile_image=img)
            nuevo_usuario.save()

            # Aquí creamos el perfil asociado al usuario
            perfil, creado = Profile.objects.get_or_create(user=request.user)
            perfil.photo = img  # Asignamos la imagen de perfil al objeto Profile
            perfil.save()  # Guardamos los cambios en el objeto Profile
            
            messages.success(request, "Registro exitoso")
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
        return render(request, "Registro.html", {"form": form})
    



def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Huff, Username already exit')
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Come On, Email was already Taken!')
            return redirect("register")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            mydict = {'username': username}
            user.save()
            html_template = 'correos.html'
            html_messenge = render_to_string (html_template, context=mydict)
            subject = 'Welcome to Service-Verse'
            email_from =settings.EMAIL_HOST_USER
            recipient_list = [email]
            messages = EmailMessage(subject, html_messenge, email_from, recipient_list)
            messages.content_subtype = 'html'
            messages.send()
            return redirect("success")
    else:
        return render(request, 'register.html')
    
def success(request):
    return render(request, 'success.html')





def lockout(request, credentials, *args, **kwargs):
    # Obtener el usuario directamente en lugar de iterar
    user = get_object_or_404(User, username=credentials["username"])
    correo_usuario = user.email
    
    try:
        enviar_mail(
            nombreusuario=user.username,
            emailusuario=correo_usuario
        )
    except Exception as e:  # Captura la excepción real
        print(f"No se ha podido enviar el correo debido a: {e}")
    
    return render(request, "lockout.html")

def enviar_mail(nombreusuario, emailusuario):
    if not nombreusuario or not emailusuario:
        raise ValueError("Se requieren el nombre de usuario y el correo electrónico")
    
    asunto = "Restablecimiento de Contraseña"
    dominio = 'http://127.0.0.1:8000/'  # Cambia esto por el dominio real de tu sitio
    mensaje = render_to_string("emails/reset_pass.html", {"nombreusuario": nombreusuario,"dominio": dominio })
    mensaje_texto = strip_tags(mensaje)
    from_email = "academiacunoc@gmail.com"         
    to = emailusuario         

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)
    
    
# Asegúrate de que is_ajax está definida en alguna parte de tu código o usa esta implementación
def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@require_POST
def find_user_view(request):
    try:
        photo = request.POST.get('photo')
        format, str_img = photo.split(';base64,')  # Asegúrate de que el split es correcto
        decoded_file = base64.b64decode(str_img)

        # Guardamos la foto en el modelo Log
        x = Log()
        x.photo.save('foto_cargada.png', ContentFile(decoded_file))
        x.save()

        # Llamada a la función que clasifica la foto
        res = classify_face(x.photo.path)
        
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()
                login(request, user)
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    
    except Exception as e:
        # Manejo de cualquier excepción que ocurra durante el proceso
        return JsonResponse({'error': str(e)}, status=500)