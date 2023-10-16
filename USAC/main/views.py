from django.shortcuts import render

from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from axes.utils import reset
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .forms import CustomUserCreationForm  
from django.views.generic import View
from main.models import allusuarios

User = get_user_model()

def home(request):
    return render(request, 'AI-html-1.0.0/home.html')

def catalogo_de_carreras(request):
    return render(request, 'AI-html-1.0.0/carreras.html')




def iniciar_sesion_docentes(request):

    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario = authenticate(request=request, username=username, password=password)
            if usuario is not None and not usuario.is_superuser and Group.objects.get(name='Docentes') in usuario.groups.all():
                login(request, usuario)
                reset(username=username)
                return render(request, "AI-html-1.0.0/home.html", {"form":form})
            else:
                messages.error(request,"Usuario no válido")
        else:
            messages.error(request,"Información no válida")

    #form = AuthenticationForm()
    return render(request, "AI-html-1.0.0/LoginDocentes.html")
   

#def cerrar_sesion(request):
    #logout(request)
    #return redirect('home')


def iniciar_sesion_estudiantes(request):

    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario = authenticate(request=request, username=username, password=password)
            
            if usuario is not None and not usuario.is_superuser and Group.objects.get(name='Estudiantes') in usuario.groups.all():
                login(request, usuario)
                reset(username=username)
                return render(request, "AI-html-1.0.0/home.html", {"form":form})
                
            else:
                messages.error(request,"Usuario no válido")
        else:
            messages.error(request,"Información no válida")

    form = AuthenticationForm()
    return render(request, "AI-html-1.0.0/LoginEstudiantes.html", {"form":form})

def cerrar_sesion(request):
    logout(request)

    return redirect('home')

class VRegistro(View):

    def get(self, request):
        # form = UserCreationForm()
        form = CustomUserCreationForm()
        return render(request, "AI-html-1.0.0/registro.html", {"form":form})

    def post(self, request):
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form)
        # nombre=form2.get_first_name()
        # print(nombre)

        if form.is_valid():
            usuario = form.save()
            # form.email_clean()
            # form.email_clean()
            ncui = form.cleaned_data.get('cui')
            # nimagen = form.cleaned_data.get('profile_imagen')
            img = form.cleaned_data.get("profile_imagen")
            # print(cui)
            # username=request.user.username
            # password=request.user.password1
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            usuario = authenticate(request=request, username=username, password=password)
            login(request, usuario)

            nuevo_usuario = allusuarios(user=request.user, username=request.user.username, first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email, cui=ncui, profile_image = img)
            nuevo_usuario.save()

            messages.success(request,"Registro exitoso")

            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            return render(request, "AI-html-1.0.0/registro.html", {"form":form})
