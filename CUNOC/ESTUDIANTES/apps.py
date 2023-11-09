from django.apps import AppConfig


class ESTUDIANTESConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ESTUDIANTES'
    verbose_name = 'Registros de Perfiles'
    def ready(self):
        import ESTUDIANTES.signals

    