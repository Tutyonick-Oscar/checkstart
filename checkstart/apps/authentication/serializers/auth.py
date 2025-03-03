from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response

from intergeld.apps.core.Exceptions.device_exceptions import InvalidMacAddressException
from intergeld.apps.user_app.utils.phone_check import (
    initiate_phone_verification,
    verify_code,
)


class AuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(label=_("Phone"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)
    mac_address = serializers.CharField(label=_("Mac"), write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        if phone and password:
            user = authenticate(
                request=self.context.get("request"), phone=phone, password=password
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        if self.initial_data.get("code") and self.initial_data.get("verification_url"):
            print("verifying code")
            try:
                verification_status = verify_code(
                    self.initial_data.get("code"),
                    self.initial_data.get("verification_url"),
                )

            except Exception as e:
                return Response(e.__dict__)

            if verification_status != "SUCCESSFUL":
                print(verification_status)
                raise InvalidMacAddressException(
                    {"message": "invalid code provided", "status": verification_status}
                )

            else:
                self.initial_data.pop("code")
                self.initial_data.pop("verification_url")
                attrs["user"] = user
                return attrs

        if user.mac_address != attrs.get("mac_address"):
            init_verification = initiate_phone_verification(attrs.get("phone"))
            raise InvalidMacAddressException(
                {
                    "message": "attempting to log-In with a different device",
                    "verification_info": init_verification,
                }
            )

        attrs["user"] = user
        return attrs
