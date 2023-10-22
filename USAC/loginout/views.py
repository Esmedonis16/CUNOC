from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.


def PH(request):
    return render(request, 'PH.html')


@login_required
def PP(request):
    return render(request, 'PP.html')


'''
def exit(request):
    logout(request)
    return redirect('home')
'''
