from django.apps import AppConfig


class AcademicappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.academicApp'
    def ready(self):
        import apps.academicApp.signals