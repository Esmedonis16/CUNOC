from django.apps import AppConfig


class IsaacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Isaac'
    verbose_name = 'Registros de Perfiles'
    def ready(self):
        import Isaac.signals

    