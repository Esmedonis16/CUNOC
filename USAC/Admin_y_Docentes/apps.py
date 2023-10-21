# En Admin_y_Docentes/apps.py

from django.apps import AppConfig

class AdminYDocentesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin_y_Docentes'
    verbose_name = 'Registros de Docentes'
    
    def ready(self):
        import Admin_y_Docentes.signals
