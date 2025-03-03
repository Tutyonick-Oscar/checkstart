import random

from django.core.exceptions import ValidationError
from intergeld.apps.core.permissions.main import InterUserPermission
from intergeld.apps.core.utils.send_mail import send_email_verification_code
from intergeld.apps.user_app.models import OTP
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ..serializers.model_serializers import InterUser, InterUserSerializer


class DevUsersViewSet(ModelViewSet):
    serializer_class = InterUserSerializer
    queryset = InterUser.objects.prefetch_related("intergeldaccount")
    permission_classes = [InterUserPermission]

    def create(self, request, *args, **kwargs):
        if request.data.get("code"):
            try:
                code = OTP.objects.get(
                    code=request.data.get("code"), user_mail=request.data.get("email")
                )
            except OTP.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "response_code": "001",
                        "response_data": None,
                        "response_message": "invalid verification code ",
                    },
                    status=404,
                )
            if code.expired:
                return Response(
                    {
                        "success": False,
                        "response_code": "001",
                        "response_data": None,
                        "response_message": "Expired verification code",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                request.data.pop("code")

            user = InterUser(**request.data)
            try:
                user.full_clean()
            except ValidationError as e:
                return Response(
                    {
                        "success": False,
                        "response_code": "001",
                        "response_data": e.error_dict,
                        "response_message": "invalid data",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
                        "email": user.email,
                        "Token": token.key,
                    },
                    "response_message": "Inter User created successfully",
                }
            )

        return Response(
            {
                "success": False,
                "response_code": "001",
                "response_data": None,
                "response_message": "email verificarion cridentials incomplets",
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
                    "response_code": "001",
                    "response_data": e.error_dict,
                    "response_message": "email verificarion cridentials incomplets",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = random.randint(111111, 999999)
        otp = OTP(code=code, user_mail=user.email)
        otp.save()
        send_email_verification_code(
            email=user.email, code=code, username=user.username
        )
        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": None,
                "response_message": f"verification code sent to your email {user.email}",
            },
            status=status.HTTP_206_PARTIAL_CONTENT,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print("About to delete ", instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateSuperUserView(APIView):
    permission_classes = []

    def post(self, request):
        print(request)
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        phone = request.data.get("phone", None)
        country = request.data.get("country", None)
        password = request.data.get("password", None)
        mac_address = request.data.get("mac_address", None)
        try:
            super_user = InterUser.objects.create_superuser(
                username=username,
                email=email,
                phone=phone,
                country=country,
                password=password,
                mac_address=mac_address,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "response_code": "001",
                    "response_data": None,
                    "response_message": f"ERROR when creating super user {str(e)}",
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": {
                    "id": super_user.id,
                    "username": super_user.username,
                    "email": super_user.email,
                },
                "response_message": "Super user created successfully",
            },
            status=status.HTTP_201_CREATED,
        )
