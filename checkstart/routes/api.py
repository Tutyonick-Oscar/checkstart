from django.urls import include, path
from checkstart.utils.main import app_path

urlpatterns = [
    path('',include(f"{app_path('student')}.urls.api"))
]