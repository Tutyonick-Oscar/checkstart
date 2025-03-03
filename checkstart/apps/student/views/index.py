from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..serializers.index import InvoiceSerializer, Student, StudentSerializer


class StudentsView(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Student.objects.all().order_by("-promotion")
    serializer_class = StudentSerializer
    lookup_field = "matricule"

    def get_serializer_class(self):
        if self.action == "invoices":
            return InvoiceSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"])
    def invoices(self, request, matricule):

        invoices = self.get_object().invoices.order_by("-created_at")
        serializer = self.get_serializer(
            invoices, many=True, context={"request": request}
        )

        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": serializer.data,
                "response_message": "Student invoices list",
            }
        )

    @action(detail=True, methods=["get"])
    def check_access(self, request, matricule):
        student = self.get_object()
        if len(student.get_expected_fees()) == 0:
            return Response(
                {
                    "success": True,
                    "response_code": "00",
                    "response_data": None,
                    "response_message": "Currently no check is needed for the student",
                }
            )

        payement_terms = student.get_payment_terms()
        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": payement_terms,
                "response_message": "Student payement terms ",
            }
        )

    @action(detail=True, methods=["get"])
    def required_fees(self, request, matricule):
        student = self.get_object()
        required_fees = student.get_formated_expected_fees()
        return Response(
            {
                "success": True,
                "response_code": "00",
                "response_data": required_fees,
                "response_message": "The actual fees expeted to be paid by the student",
            }
        )
