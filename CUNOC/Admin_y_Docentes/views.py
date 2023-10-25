from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import inges, Registros, EstudianteCurso
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
#from axes.utils import reset




def boton(request, pk):
    BotonRegistrarD = get_object_or_404(Registros, pk=pk)
    # Aquí puedes hacer algo con BotonRegistrarD
    return redirect('signup')




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


class RDocentes(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            usuario = form.save()     
            ncui = form.cleaned_data.get('cui')           
            img = form.cleaned_data.get("imagen")          
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            usuario = authenticate(request=request, username=username, password=password)
            login(request, usuario)

            nuevo_usuario = inges(user=request.user, username=request.user.username, first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email, cui=ncui, imagen = img)
            nuevo_usuario.save()

            messages.success(request,"Registro exitoso")
            
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            return render(request, "signup.html", {"form":form})
        


def cursos_del_estudiante(request):
    # Filtra los cursos basados en el usuario actual
    cursos_inscritos = EstudianteCurso.objects.filter(estudiante=request.user, asignado=True)
    return render(request, 'CursosAsig.html', {'cursos_inscritos': cursos_inscritos})


