from django.core.exceptions import ValidationError
from intergeld.apps.user_app.utils.phone_check import (
    initiate_phone_verification,
    verify_code,
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..serializers.model_serializers import InterUser, InterUserSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = InterUserSerializer
    queryset = InterUser.objects.all()

    def create(self, request, *args, **kwargs):

        if request.data.get("code") and request.data.get("verification_url"):
            try:
                verification_status = verify_code(
                    request.data.get("code"), request.data.get("verification_url")
                )
                if verification_status != "SUCCESSFUL":
                    return Response(
                        {
                            "message": "invalid code provided",
                            "status": verification_status,
                        },
                        status=400,
                    )
                else:
                    request.data.pop("code")
                    request.data.pop("verification_url")

            except Exception as e:
                return Response(e.__dict__, status=500)

            user = InterUser(**request.data)
            try:
                user.full_clean()
            except ValidationError as e:
                return Response(e.error_dict, status=400)

            user.set_password(request.data["password"])
            user.save()
            token = Token.objects.create(user=user)
            return Response(
                {
                    "success": True,
                    "response_code": "00",
                    "response_data": {
                        "id": user.pk,
                        "username": user.username,
                        "phone": user.phone,
                        "Token": token.key,
                    },
                    "response_message": "Inter User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "response_code": "00",
                "response_data": None,
                "response_message": "phone verificarion cridentials incomplet",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["post"])
    def user_creation_request(self, request):
        user = InterUser(**request.data)
        try:
            user.full_clean()
        except ValidationError as e:

            return Response(
                {
                    "success": False,
                    "response_code": "00",
                    "response_data": e.error_dict,
                    "response_message": "Invalid data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        init_verification = initiate_phone_verification(user.phone)
        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": init_verification,
                "response_message": "Verification code sent via sms",
            },
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
