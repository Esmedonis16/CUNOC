from django.urls import path
from .views import PH, PP

urlpatterns = [
    path('', PH, name='PH'),
    path('products/', PP, name='PP'),
    # path('logout/', exit, name='exit'),
]
