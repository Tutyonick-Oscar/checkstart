from django.urls import path

from ..views.index import InvoicesView

urlpatterns = [path("invoices/", InvoicesView.as_view(), name="invoices")]
