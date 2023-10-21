from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from axes.utils import reset
from django.contrib import messages
from main.models import allusuarios
from .forms import CustomUserCreationForm  
from django.views.generic import View
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    return render(request, 'AI-html-1.0.0/home.html')

def PE(request):
    return render(request, 'AI-html-1.0.0/PortalEstudiantes.html')

def PD(request):
    return render(request, 'AI-html-1.0.0/PortalDocentes.html')

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

    form = AuthenticationForm()
    return render(request, "AI-html-1.0.0/LoginDocentes.html", {"form":form}) #este es el boton directorio



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
                return render(request, "AI-html-1.0.0/PortalEstudiantes.html", {"form":form, "cliente": allusuarios.objects.get(username=username)})          
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
        form = CustomUserCreationForm()
        return render(request, "AI-html-1.0.0/registro.html", {"form":form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form)


        if form.is_valid():
            usuario = form.save()
        
            ncui = form.cleaned_data.get('cui')
           
            img = form.cleaned_data.get("profile_imagen")
          
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
        
        
        
    def logout_request(request):
        logout(request)
        messages.info(request, "Saliste exitosamente")
        return redirect("main:homepage")
