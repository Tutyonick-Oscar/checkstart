import random

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from intergeld.apps.core.Exceptions.device_exceptions import InvalidMacAddressException
from intergeld.apps.core.utils.send_mail import send_mac_access_code
from intergeld.apps.user_app.models import OTP
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)
    mac_address = serializers.CharField(label=_("Mac"), write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        if self.initial_data.get("code"):
            print("verifying code")
            try:
                code = OTP.objects.get(
                    code=self.initial_data.get("code"), user_mail=attrs.get("email")
                )

            except OTP.DoesNotExist:
                raise serializers.ValidationError(
                    "invalid verification code", code="authorization"
                )

            if code.expired:
                raise serializers.ValidationError(
                    "verification code has expired", code="authorization"
                )

            self.initial_data.pop("code")
            attrs["user"] = user
            return attrs

        if user.mac_address != attrs.get("mac_address"):
            code = random.randint(111111, 999999)
            send_mac_access_code(attrs.get("email"), code, user.username)
            otp = OTP(code=code, user_mail=attrs.get("email"))
            otp.save()
            raise InvalidMacAddressException(
                {
                    "detail": {
                        "message": "attempting to log-In with a different device",
                        "verification-info": f"an email with access code was sent to your email : {user.email}",
                    }
                }
            )

        attrs["user"] = user
        return attrs
