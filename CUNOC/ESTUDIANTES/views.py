from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.views.generic import View, TemplateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import allusuarios
from Admin_y_Docentes.models import cursos
from django.contrib import messages

def home(request):
    return render(request, 'Home.html')

@login_required
def Pensum(request):
    return render(request, 'Pensum.html')


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
            messages.success(request, "Registro exitoso")
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
        return render(request, "Registro.html", {"form": form})
    
    
    
#MOSTRAR TODOS LOS CURSOS
class allcursos(TemplateView):
    template_name = "pensum.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursoss = cursos.objects.all()
        student = self.request.user if self.request.user.is_authenticated else None
        
        for item in cursoss:
            if student: 
                registroC = allusuarios.objects.filter(cursosall = item, student=student).first()
                item.is_enrolled = registroC is not None 
            else :
                item.is_enrolled = False 
            enrolled_count = allusuarios.objects.filter(cursosall = item).count()
            item.enrolled_count = enrolled_count
                
        context["cursoss"] = cursoss 
        return context
    
