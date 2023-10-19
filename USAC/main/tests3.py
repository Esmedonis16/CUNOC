import sys
sys.path.append('G:/Mi unidad/8vo Semestre/Proyectos/CUNOC/USAC') 
from Ejemplo.wsgi import *
from main.tests import send_email

def mi_vista(request):
            
            # Pide al usuario que ingrese el destinatario
                destinatario = "h.isaa.3007@gmail.com"

            # Llama a la función send_email con el destinatario proporcionado
                send_email("h.isaa.3007@gmail.com")