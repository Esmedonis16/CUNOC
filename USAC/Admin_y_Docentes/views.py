from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import inges, Registros
from django.views.generic import View



def boton(request, pk):
    BotonRegistrarD = get_object_or_404(Registros, pk=pk)
    # Aquí puedes hacer algo con BotonRegistrarD
    return redirect('signup')




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

