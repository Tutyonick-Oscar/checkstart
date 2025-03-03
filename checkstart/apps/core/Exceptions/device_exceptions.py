from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidMacAddressException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("Invalid mac address.")
    default_code = "invalid"
