from django.apps import AppConfig

from checkstart.utils.main import app_path


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = app_path("student")
