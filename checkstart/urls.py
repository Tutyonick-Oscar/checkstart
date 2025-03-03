from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (  # SpectacularSwaggerView,
    SpectacularAPIView,
    SpectacularRedocView,
)

admin.site.site_title = "CHECKSTART"
admin.site.site_header = "CHECKSTART ADMIN"
admin.site.index_title = "CHECKSTART ADMIN"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("checkstart.routes.api")),
]

# specular
urlpatterns += [
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
