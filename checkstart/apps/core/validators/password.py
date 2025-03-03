from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def special_characters_checker(value):
    sp_char = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "()",
        "-",
        "+",
        "=",
        "/",
        "?",
        ">",
        "<",
        ",",
        ".",
        "|",
        "~",
        "_",
    ]
    if not any(char in sp_char for char in value):
        raise ValidationError(
            _("password must contain at least one special character !")
        )


def uppercase_checker(value):

    if not any(char.isupper() for char in value):
        raise ValidationError(_("password must contain at least one UperCase letter !"))


def lowercase_checker(value):

    if not any(char.islower() for char in value):
        raise ValidationError(
            _("password must contain at least one lowerCase letter !")
        )


def name_in_password_checker(password, name):
    if str.lower(name) in str.lower(password):
        raise ValidationError(_("password can not include username !"))


def number_checker(value):
    if not any(element.isdigit() for element in value):
        raise ValidationError(_("password must contain at least one digit!"))
