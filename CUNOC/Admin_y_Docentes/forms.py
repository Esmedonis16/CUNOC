from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError 
from .models import  cursos
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth import get_user_model
User = get_user_model()

#from user.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields=['username','first_name', 'last_name', 'email']
    
    cui = forms.IntegerField(label='CUI', help_text='Código Único de Identificación CUI')
    imagen = forms.ImageField(label='Foto de perfil')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email = email)  
        if new.exists():  
            raise ValidationError("El email ya esta vinculado con otra cuenta, utiliza uno diferente.")  
        return email 

class CursosForm(forms.ModelForm):
    docentes = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Docentes'), label ='Docentes')
    
    class Meta:
        model = cursos
        fields=('codigo', 'nombre', 'descripcion', 'costo', 'horarioinicio', 'horariofin', 'cupo', 'docentes')
        list_display = ['codigo', 'nombre', 'descripcion', 'costo', 'horarioinicio', 'horariofin',
                    'cupo', 'docentes','imagen', 'num_estudiantes_inscritos']
        ordering = ['nombre']
        search_fields = ['nombre', 'codigo', 'docentes__nombre']  
        list_per_page = 15  # Cantidad de items por página
        
    helper = FormHelper()
    helper.layout = Layout(
        Field('codigo'),
        Field('nombre'),
        Field('descripcion'),
        Field('costo'),
        Field('horarioinicio'),
        Field('horariofin'),
        Field('cupo'),
        Field('docentes'),
        Submit('submit', 'Submit')
    )
    
    imagen = forms.ImageField(label='Foto de perfil')