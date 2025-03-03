import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from checkstart.apps.core.models import BaseModel, CustomBaseManager


class Student(BaseModel):

    class DepartementsChoices(models.TextChoices):
        GGT = "100", _("GGT")
        GCV = "200", _("GCV")
        SAE = "300", _("SAE")
        SIF = "400", _("SIF")
        MEDECINE = "500", ("MEDECINE")
        ANR = "600", _("ANR")
        DROIT = "250", _("DROIT")
        ENTREPRENEURIAT = "350", _("ENTREPRENEURIAT ET GESTION DES AFFAIRES")
        SOCIAL = "450", _("SERVICE SOCIAL")
        COMMUNICATION = "550", _("COMMUNICATION")
        INFO = "650", _("SCIENCES INFORMATIQUES")
        OPHTA = "120", _("OPTHAMOLOGIE")
        MIDWIFE = "220", _("SAGE FEMME")

    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    matricule = models.CharField(max_length=8, unique=True)
    departement = models.CharField(max_length=3, choices=DepartementsChoices.choices)
    promotion = models.IntegerField()
    level = models.CharField(max_length=4)
    speciality = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(
        get_user_model(), related_name="student", on_delete=models.CASCADE
    )
    student_check_pass = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.matricule}"

    def get_expected_fees(self):
        expected_fees = []
        _date = timezone.now().date()
        fees = AcademicFee.objects.filter(
            for_level=self.level, stakeholders__contains=[self.departement]
        )
        for fee in fees:
            # we format the payable date(year) to reflet the student's current level(years)
            payable_from = datetime.date(
                _date.year, fee.payable_from.month, fee.payable_from.day
            )
            if _date >= payable_from:
                expected_fees.append({"fee": fee, "deadline": payable_from})

        return expected_fees

    def get_formated_expected_fees(self):
        expected_fees = self.get_expected_fees()
        fees = {}
        for fee in expected_fees:
            fee_category_name = (
                fee.get("fee", None).get_category_display().replace(" ", "")
            )
            fee_obj = fee.get("fee", None)
            fees[fee_category_name] = {
                "id": fee_obj.pk,
                "amount": fee_obj.amount,
                "category": fee_obj.get_category_display(),
                "level": fee_obj.for_level,
                "deadline": fee.get("deadline", None),
            }

        return fees

    def get_payment_terms(self):
        payment_terms = {}
        expected_fees = self.get_expected_fees()

        for fee in expected_fees:

            invoices = self.invoices.filter(
                type=fee.get("fee", None), level=fee.get("fee", None).for_level
            )
            fee_category_name = (
                fee.get("fee", None).get_category_display().replace(" ", "")
            )
            payment_terms[fee_category_name] = {}
            completed = False
            paid = False

            if len(invoices) > 0:
                completed = (
                    invoices.aggregate(Sum("amount"))["amount__sum"]
                    == fee.get("fee", None).amount
                )
                paid = True
                for indx, invoice in enumerate(invoices):
                    payment_terms[fee_category_name][f"invoice_{indx + 1}"] = {
                        "fee-catgory": fee.get("fee", None).get_category_display(),
                        "deadline": fee.get("deadline", None),
                        "paid_amount": invoice.amount,
                        "due_amount": invoice.due_amount,
                        "paid_on": invoice.created_at.date(),
                    }

                payment_terms[fee_category_name]["paid"] = paid
                payment_terms[fee_category_name]["total_paid_amount"] = (
                    invoices.aggregate(Sum("amount"))["amount__sum"]
                )
                payment_terms[fee_category_name]["completed"] = completed

            else:
                payment_terms[fee_category_name] = {
                    "fee-catgory": fee.get("fee", None).get_category_display(),
                    "deadline": fee.get("deadline", None),
                    "paid": False,
                    "completed": False,
                }

        return payment_terms


class AcademicFee(BaseModel):

    class FeeCategoryChoices(models.TextChoices):
        TUITION = "T", _("TUITION FEE")
        CARD = "C", _("STUDENT CARD")
        GRADUATION = "G", _("GRADUATION FEE")
        MATERIALS = "M", _("MATERIALS FEE")
        INTERNSHIP = "I", _("INTERNSHIP REPORT FEE")

    category = models.CharField(max_length=1, choices=FeeCategoryChoices.choices)
    amount = models.DecimalField(max_digits=16, decimal_places=3)
    for_level = models.CharField(max_length=4, blank=True, null=True)
    stakeholders = ArrayField(
        models.CharField(max_length=3, choices=Student.DepartementsChoices.choices)
    )
    payable_from = models.DateField()

    def __str__(self):
        return self.get_category_display()


class Invoice(BaseModel):
    amount = models.DecimalField(max_digits=16, decimal_places=3)
    level = models.CharField(max_length=4)
    type = models.ForeignKey(
        AcademicFee, on_delete=models.CASCADE, related_name="payements"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="invoices"
    )
    due_amount = models.DecimalField(max_digits=16, decimal_places=3)
