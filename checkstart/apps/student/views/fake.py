import random
from decimal import Decimal

from django.utils import timezone
from faker import Faker
from rest_framework.response import Response
from rest_framework.views import APIView

from checkstart.apps.authentication.models import User
from checkstart.apps.student.models import AcademicFee, Invoice, Student


class CreateFakeUsersView(APIView):
    def post(self, request):
        fake = Faker()
        for i in range(10):
            User.objects.create_user(
                username=fake.name(),
                email=fake.email(domain="hau.bi"),
                password="Hau@2000",
                photo=fake.image_url(),
            )
        return Response(f"{i + 1} fake users created successfully")


class CreateFakeStudentView(APIView):

    def post(self, request):
        fake = Faker()
        departements = Student.DepartementsChoices.choices

        users = User.objects.all()
        for user in users:
            departement = departements[fake.random_int(0, len(departements) - 1)]
            promotion = fake.random_int(timezone.now().year - 3, timezone.now().year)
            if promotion == timezone.now().year:
                level = "BAC1"
            elif promotion == timezone.now().year - 1:
                level = "BAC2"
            elif promotion == timezone.now().year - 2:
                level = "BAC3"
            else:
                level = "GRDT"
            matricule = f"{str(promotion)[2:]}{departement[0]}0{user.pk}"
            Student.objects.create(
                name=user.username,
                lastname=fake.last_name(),
                departement=departement[0],
                promotion=promotion,
                level=level,
                matricule=matricule,
                user=user,
                created_by=user,
            )
        return Response("fake students generated successfully")


class CreateFakeInvoicesView(APIView):

    health_stack = ["500", "600", "120", "220"]
    others_stack = ["100", "200", "300", "400", "350", "450", "550", "650"]
    all_stack = [
        "100",
        "200",
        "300",
        "400",
        "350",
        "450",
        "550",
        "650",
        "500",
        "600",
        "120",
        "220",
    ]

    def post(self, request):
        type = request.data.get("type", None)
        stack = request.data.get("stack", None)
        if not type or not stack:
            return Response(
                {
                    "success": False,
                    "response_code": "001",
                    "response_data": None,
                    "response_message": "Must include academic fee type and stackholders",
                }
            )
        if stack == "health":
            stack = self.health_stack
        elif stack == "others":
            stack = self.others_stack
        elif stack == "all":
            stack = self.all_stack
        else:
            return Response(
                {
                    "success": False,
                    "response_code": "004",
                    "response_data": None,
                    "response_message": "No stack matching the given name",
                }
            )
        fake = Faker()
        levels = ["BAC1", "BAC2", "BAC3"]
        students = Student.objects.filter(departement__in=stack)
        for i in range(10):
            level = levels[fake.random_int(0, 2)]
            try:
                ac_fee = AcademicFee.objects.get(
                    for_level=level, category=type, stakeholders=stack
                )
            except AcademicFee.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "response_code": "004",
                        "response_data": None,
                        "response_message": "no academic fee matching the given query",
                    },
                    status=400,
                )

            student = students[fake.random_int(0, len(students) - 1)]
            student_last_invoice = student.invoices.filter(
                level=level, type=ac_fee
            ).last()

            if student_last_invoice:
                amount = Decimal(
                    random.randint(1000, int(student_last_invoice.due_amount))
                )
                due_amount = student_last_invoice.due_amount - amount
            else:
                amount = Decimal(random.randint(1000, int(ac_fee.amount)))
                due_amount = ac_fee.amount - amount
            # amount = fake.pydecimal(13,3,True,1000,ac_fee.amount)

            Invoice.objects.create(
                amount=amount,
                level=level,
                type=ac_fee,
                student=student,
                due_amount=due_amount,
                created_by=User.objects.first(),  # as it is not very important
            )

        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": None,
                "response_message": f"{i + 1} invoices created randomly",
            }
        )
