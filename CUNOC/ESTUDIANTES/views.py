from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.views.generic import View
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import allusuarios
from django.contrib import messages
# Create your views here.




def home(request):
    return render(request, 'home.html')

def Pensum(request):
    return render(request, 'pensum.html')

def PE(request):
    return render(request, 'PortalEstudiantes.html')


@login_required
def products(request):
    return render(request, 'productos.html')


def exit(request):
    logout(request)
    return redirect('home')


def iniciar_sesion_estudiantes(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(
                request=request, username=username, password=password)
            grupo_estudiantes = Group.objects.get(name='Estudiantes')

            if usuario is not None:
                if not usuario.is_superuser and grupo_estudiantes in usuario.groups.all():
                    login(request, usuario)
                    # Asegúrate de que esta función exista y sea necesaria
                    # reset(username=username)
                    return render(request, "PortalEstudiantes.html", {"form": form, "cliente": allusuarios.objects.get(username=username)})
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
        return render(request, "registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form)

        if form.is_valid():
            usuario = form.save()
            ncui = form.cleaned_data.get('cui')
            img = form.cleaned_data.get("profile_imagen")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(
                request=request, username=username, password=password)
            login(request, usuario)
            nuevo_usuario = allusuarios(user=request.user, username=request.user.username, first_name=request.user.first_name,
                                        last_name=request.user.last_name, email=request.user.email, cui=ncui, profile_image=img)
            nuevo_usuario.save()
            messages.success(request, "Registro exitoso")
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
        return render(request, "registro.html", {"form": form})
