from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

from axes.utils import reset
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from main.forms import CustomUserCreationForm
from django.views.generic import View
from main.models import allusuarios, docentes
from django.template.loader import render_to_string


User = get_user_model()


def home(request):
    return render(request, 'home.html')


def Pensum(request):
    return render(request, 'pensum.html')


def PE(request):
    return render(request, 'PortalEstudiantes.html')


def iniciar_sesion_estudiantes(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(
                request=request, username=username, password=password)
            if usuario is not None and not usuario.is_superuser and Group.objects.get(name='Estudiantes') in usuario.groups.all():
                login(request, usuario)
                reset(username=username)
                return render(request, "PortalEstudiantes.html", {"form": form, "cliente": allusuarios.objects.get(username=username)})
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
