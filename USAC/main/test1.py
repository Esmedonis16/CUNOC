import sys
sys.path.append('G:/Mi unidad/8vo Semestre/Proyectos/CUNOC/USAC') 
from Ejemplo.wsgi import *
from Ejemplo import settings
from main.models import allusuarios

query = allusuarios.objects.all()
print(query)