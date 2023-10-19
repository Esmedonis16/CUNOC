import sys
sys.path.append('G:/Mi unidad/8vo Semestre/Proyectos/CUNOC/USAC') 
from Ejemplo.wsgi import *
from Ejemplo import settings
from main.models import allusuarios

usuario = allusuarios.objects.get(username= 'nohe')  # Obtén un objeto de usuario
pk_field = usuario._meta.pk  # Obtiene el campo de clave primaria
# El nombre del campo de clave primaria
nombre_pk = pk_field.name
# El valor de la clave primaria del usuario
valor_pk = usuario.pk
print(f"La clave primaria del usuario es '{nombre_pk}' y su valor es {valor_pk}")
