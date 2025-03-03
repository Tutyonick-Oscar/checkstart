from django.apps import AppConfig

from intergeld.utils.app_path import app_path


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = app_path("core")
