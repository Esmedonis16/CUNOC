from django.test import TestCase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your tests here.
import smtplib

import sys
sys.path.append('G:/Mi unidad/8vo Semestre/Proyectos/CUNOC/USAC') 
from Ejemplo.wsgi import *
from Ejemplo import settings
from main.models import allusuarios

from django.shortcuts import render
from django.template.loader import render_to_string

def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado . . . ')

        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = "h.isaa.3007@gmail.com"
        mensaje['Subject'] = "Tienes un correo"

        # Renderizamos la plantilla
        content = render_to_string('AI-html-1.0.0/send_email.html', {'cliente': allusuarios.objects.get(pk=1)} )

        # Adjuntamos la plantilla renderizada al mensaje de correo electrónico
        mensaje.attach(MIMEText(content, 'html'))

        # Envío del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            "h.isaa.3007@gmail.com",
                            mensaje.as_string())

        print('Correo enviado correctamente')

    except Exception as e:
        print("Error al enviar el correo:", e)

send_email()