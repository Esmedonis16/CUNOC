from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('productos/', views.products, name='productos'),
    path('logout/', views.exit, name='exit'),

]
