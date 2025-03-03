from django.apps import AppConfig

from checkstart.utils.main import app_path


class UserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = app_path("authentication")

    def ready(self):
        import checkstart.apps.authentication.signals

        # return super().ready()
