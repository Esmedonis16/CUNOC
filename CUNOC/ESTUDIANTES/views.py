from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

# Create your views here.


def home(request):
    return render(request, 'home.html')


@login_required
def products(request):
    return render(request, 'productos.html')


def exit(request):
    logout(request)
    return redirect('home')

