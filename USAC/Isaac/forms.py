from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields=['username', 'first_name', 'last_name', 'email']
    
    cui = forms.IntegerField(label='CUI', help_text='Código Único de Identificación CUI')
    profile_imagen = forms.ImageField(label='Foto de perfil')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email = email)  
        if new.exists():  
            raise ValidationError("El email ya esta vinculado con otra cuenta, utiliza uno diferente.")  
        return email 
