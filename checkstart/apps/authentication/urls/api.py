from django.urls import include, path
from rest_framework import routers

from ..views.auth import obtain_auth_token

# from ..views.model_views import UsersViewSet
from ..views.dev_authentication import CreateSuperUserView, DevUsersViewSet

app_name = "user_app"
router = routers.DefaultRouter()
router.register(r"accounts", DevUsersViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token, name="api-login"),
    path(
        "create-superuser/", CreateSuperUserView.as_view(), name="create-superuser-api"
    ),
]
